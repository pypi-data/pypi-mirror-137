"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com

    This module contains the merge tool as designed in the inmanta-telco repo. It is responsible for merging pull requests on
    managed repos' development branches (master, iso<x>) and it requires exclusive commit access to those branches to prevent
    race conditions.
"""
import logging
import os
import sys
import time
from collections import defaultdict
from itertools import chain
from typing import Dict, Iterator, List, Optional, Set
from urllib.parse import urljoin

import click
import more_itertools

from irt import changelog, git, version
from irt.changelog import CHANGE_ENTRIES_PATH, ChangeEntry
from irt.const import GITKEEP_FILE
from irt.git import GitRepo, MergeFailure
from irt.mergetool import github
from irt.mergetool.config import MergeToolConfig, parse_config
from irt.mergetool.github import MergeToolPullRequest
from irt.project import Project, ProjectConfig
from irt.version import ChangeType

LOGGER = logging.getLogger(__name__)


class InvalidMergeRequest(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message


class MergeRequest:
    """
    A request to merge changes into one or more development branches. The following invariants hold:
        - For any two development branches, either their heads are aligned (point to the same commit),
            or one has a version that can never be reached by the other due to its version constraints
            (the branches have diverged).
        - SemVer: Dev versions may have a lower but never a higher version than appropriate according to
            the semantic versioning version scheme. This guarantee allows strict semantic versioning to
            be followed for all non-dev builds.
    """

    def __init__(
        self,
        config: MergeToolConfig,
        pull_request: MergeToolPullRequest,
        repo: GitRepo,
    ) -> None:
        self.config: MergeToolConfig = config
        self.pull_request: MergeToolPullRequest = pull_request
        self.repo: GitRepo = repo
        # group of all branches aligned with pull request's target branch prior to merge
        self._group: Optional[List[str]] = None
        self._change_entry: Optional[ChangeEntry] = None
        self._processed: bool = False

    @property
    def group(self) -> List[str]:
        if self._group is None:
            raise Exception("Incorrect control flow: group has not been set yet")
        return self._group

    @property
    def target_branches(self) -> Set[str]:
        """
        Returns the target branches for this pull request, these are the change entry's destination branches that are in this
        pull request's group.
        """
        return set(self.group).intersection(set(self.change_entry.destination_branches))

    @property
    def change_entry(self) -> ChangeEntry:
        if self._change_entry is None:
            raise Exception("Incorrect control flow: change entry has not been set yet")
        return self._change_entry

    def _parse_change_entry(self) -> ChangeEntry:
        """
        Parses the change entry.

        :raises InvalidMergeRequest: Failed to uniquely determine the change entry file or failed to parse it.
        """
        with self.repo.checkout_branch(self.pull_request.source) as branch:
            remote_target = f"origin/{self.pull_request.target}"
            new_files: List[str] = branch.get_new_files(remote_target)
            change_entry_files: List[str] = [
                f
                for f in new_files
                if os.path.normpath(os.path.dirname(f)) == CHANGE_ENTRIES_PATH
                and os.path.basename(f) != GITKEEP_FILE
            ]
            if len(change_entry_files) == 1:
                try:
                    return changelog.parse_change_entry(
                        os.path.join(self.repo.directory, change_entry_files[0])
                    )
                except Exception as e:
                    raise InvalidMergeRequest(
                        "Failed to parse change entry file: %s" % e
                    )
            else:
                if len(change_entry_files) == 0:
                    raise InvalidMergeRequest("No change entry file found")
                else:
                    raise InvalidMergeRequest(
                        f"Multiple change entry files found ({','.join(change_entry_files)}). "
                        f"This may happen when a change entry was removed from the remote "
                        f"repository due to a reverted change. In that case, make sure the "
                        f"latest changes from {remote_target} are merged into "
                        f"{self.pull_request.source} before triggering merge bot."
                    )

    def process(self) -> None:
        """
        Processes this pull request end-to-end.
        """

        if self._processed:
            raise Exception(
                "MergeToolPullRequest.process has side effects. It is unsafe to call it twice for the same instance."
            )
        self._processed = True

        LOGGER.info(f"Processing pull request {self.pull_request}")

        try:
            original: MergeToolPullRequest = (
                self.pull_request.get_original_pull_request()
            )
            message: str = (
                "Processing this pull request"
                if self.pull_request is original
                else f"Processing #{self.pull_request.number}."
            )
            # Comment on the original pull request to inform the developer the tool is on it.
            original.comment(message)

            try:
                self._change_entry = self._parse_change_entry()
                self.sanity_check()
            except InvalidMergeRequest as e:
                self.pull_request.reject(
                    f"Pull request rejected by merge tool. {e.message}"
                )
                return

            # group branches by head
            groups: Dict[str, List[str]] = self.group_aligned_branches()
            target_head: str = more_itertools.one(
                head
                for head, group in groups.items()
                if self.pull_request.target in group
            )
            self._group = groups[target_head]

            # Squash and merge the source into the target branch
            squash_commit: str
            try:
                squash_commit = self._squash_merge()
            except MergeFailure:
                # this should never happen: the sanity check should filter out pull requests that aren't mergeable
                self.pull_request.reject(
                    f"Failed to merge changes into {self.pull_request.target}."
                )
                return

            # propagate to other target branches
            original_pr_requires_attention: bool = False
            LOGGER.info(f"Opening second stage pull requests for {self.pull_request}")
            if not self.pull_request.second_stage:
                for head, group in groups.items():
                    target_branches: Set[str] = set(group).intersection(
                        set(self.change_entry.destination_branches)
                    )
                    if len(target_branches) == 0:
                        continue
                    if head == target_head:
                        # for this pull request's group, open sibling pull requests
                        for branch_name in target_branches:
                            if branch_name == self.pull_request.target:
                                continue
                            self.pull_request.open_sibling(target=branch_name)
                    else:
                        # for all other groups, cherry-pick and open pull requests
                        reference_branch: str = next(iter(target_branches))
                        new_source_branch: str = f"{self.pull_request.get_next_stage_branch_prefix()}{reference_branch}"
                        try:
                            with self.repo.checkout_branch(
                                new_source_branch,
                                base_branch=reference_branch,
                            ) as branch:
                                branch.cherry_pick([squash_commit])
                                branch.push()
                        except MergeFailure:
                            self.pull_request.reject(
                                "Failed to merge changes into %s due to merge conflict."
                                "Please open a pull request for these branches separately."
                                % ", ".join(target_branches)
                            )
                            original_pr_requires_attention = True
                            continue

                        for branch_name in target_branches:
                            self.pull_request.open_sibling(
                                target=branch_name,
                                source=new_source_branch,
                            )
                # We need these pull requests later on, give GitHub some time to reach internal consistency
                time.sleep(5)

            # Pull requests have been created for other groups, from here on only the group of this pull request's
            # target branch is considered.
            # The sanity check has passed for this pull request, so we can proceed with merging it and
            # safely fast-forward to aligned branches (it's the exact same change to the exact same head).

            # Fetch equivalent second stage pull requests and verify the remote state matches the local one.
            next_stage: List[
                MergeToolPullRequest
            ] = self._fetch_next_stage_pull_requests()

            # We've verified local state and remote state match, from here on we reason on the local state,
            # then we close the second stage pull requests we've fetched before without re-fetching them.

            # Diverge (version bump) branches if required. Because of the SemVer invariant (verified in the sanity check),
            # either all this group's target branches get the same bump, or none of them do.
            self._diverge()
            # Fast forward changes onto other target branches in this group.
            self._fast_forward()

            LOGGER.info(
                f"Pushing changes and closing {self.pull_request} and fast-forward candidates."
            )
            for pull_request in chain([self.pull_request], next_stage):
                with self.repo.checkout_branch(pull_request.target) as branch:
                    branch.push()

            # close pull requests in a separate loops so the pushes happen as atomically as possible
            for pull_request in next_stage:
                pull_request.close(f"Merged in {squash_commit}")

            # The original pull request can only be closed if there were no issues above.
            original_pr_message: str = "Merged into branches %s in %s" % (
                ", ".join(self.target_branches),
                squash_commit,
            )
            if original_pr_requires_attention:
                self.pull_request.comment(original_pr_message)
                self.pull_request.reject(
                    "Not closing this pull request due to previously commented issues for some of the destination branches."
                    " Please open a separate pull request for those branches. You can safely close this pull request and delete"
                    " the source branch."
                )
            else:
                self.pull_request.close(original_pr_message)
            # Give GitHub some time to reach internal consistency
            time.sleep(5)

            # If there are no more open pull requests for this source branch, delete it
            open_prs_for_source: Iterator[
                MergeToolPullRequest
            ] = github.get_pull_requests_by_source(
                self.pull_request.repository.name,
                self.pull_request.source,
                self.config.bot_responsibles,
                self.pull_request.token,
            )
            try:
                next(open_prs_for_source)
            except StopIteration:
                self.repo.delete_remote_branch(self.pull_request.source)

        except Exception as e:
            LOGGER.exception(
                "An unexpected error occurred while processing this pull request. The request might have been partially"
                " processed."
            )
            rejection_message: str = (
                "An unexpected error occurred while processing this pull request. The request might have been partially"
                f" processed. Caused by: {e}"
            )
            msg_filtered_pr_token: str = rejection_message.replace(
                self.pull_request.token, "*****"
            )
            self.pull_request.reject(
                msg_filtered_pr_token
                if self.repo.token is None
                else msg_filtered_pr_token.replace(self.repo.token, "*****")
            )

    def _fetch_next_stage_pull_requests(self) -> List[MergeToolPullRequest]:
        """
        Fetches the next stage pull requests for this group and verifies local state (the change entry file)
        matches remote state (the next stage pull requests).
        """
        next_stage: List[MergeToolPullRequest] = [
            pr
            for pr in self.pull_request.get_equivalent_pull_requests()
            if pr.target in self.group
        ]
        if {pr.target for pr in next_stage} != self.target_branches.difference(
            {self.pull_request.target}
        ):
            raise Exception(
                "Remote state does not match local state: got pull requests for branches %s but change entry"
                " specifies branches %s."
                # As long as inmanta/irt#650 hasn't been resolved yet, clarify that it is a possible cause for this exception.
                "\n"
                "If this is a first stage pull request (not opened by the merge tool) this is probably caused by a race"
                " condition (inmanta/irt#650). The best way to resolve this is to make sure the merge tool can pick up this"
                " pull request again and start from a clean slate. To do this, take the following steps:"
                "\n- Close all pull requests opened by the merge tool with the same source branch as this one. Be careful not"
                " to close pull requests for source branches that start with `merge-tool/`. All pull requests created by the"
                " merge tool link to this pull request so you should be able to find them mentioned here."
                "\n- Re-add the `merge-tool-ready` label to this pull request."
                % (
                    ", ".join(
                        chain(
                            [self.pull_request.target], (pr.target for pr in next_stage)
                        )
                    ),
                    ", ".join(self.target_branches),
                )
            )
        return next_stage

    def _squash_merge(self) -> str:
        """
        Squashes and merges the pull request's source into its target branch. Does not push changes.

        :return: The squash merge commit.
        """
        LOGGER.info(
            f"Squashing and merging changes into {self.pull_request.target} for {self.pull_request}"
        )
        issue_description: str = (
            f"Issue {self.change_entry.get_issue_reference()}, "
            if self.change_entry.get_issue_reference() is not None
            else ""
        )
        self.repo.squash(
            source=self.pull_request.source,
            target=self.pull_request.target,
            message=(
                f"{self.change_entry.description}"
                f" ({issue_description}PR #{self.pull_request.get_original_pull_request_number()})"
                "\n\n"
                f"{self.pull_request.body}"
            ),
            author=self.pull_request.authors[0],
        )
        head: Optional[str] = self.repo.get_branch_head(self.pull_request.target)
        if head is None:
            raise Exception("Something went wrong, failed to squash and merge commits")
        return head

    def _diverge(self) -> None:
        """
        Performs appropriate version bumps on the pull request's target branch iff merging it will cause divergence between
        branches that are currently aligned. Assumes the SemVer invariant is met. Does not push changes.
        """
        LOGGER.info(f"Applying divergence logic for {self.pull_request}")
        change_type_less: Optional[ChangeType] = self.change_entry.change_type.less()
        if change_type_less is None:
            # this is a patch commit which is allowed on all dev branches
            return
        nearest_invalid_branch: str = self.config.dev_branches[change_type_less]
        if nearest_invalid_branch not in self.group:
            # we have already diverged from the incompatible branches
            return
        LOGGER.info(f"Diverging for {self.pull_request}")
        self._apply_version_bump()

    def _apply_version_bump(self) -> None:
        """
        Applies the appropriate version bump to the pull request's target branch.
        """
        with self.repo.checkout_branch(self.pull_request.target) as branch:
            project_config: ProjectConfig = Project(
                self.repo.directory
            ).get_project_config()
            tool: version.VersionBumpTool = project_config.version_bump.tool.get_tool(
                self.repo.directory
            )
            tool.bump(self.change_entry.change_type)
            branch.commit("Merge tool: bump version due to divergence")

    def _fast_forward(self) -> None:
        """
        Fast-forwards changes on the target branch to all target branches in this group. Does not push changes.
        """
        LOGGER.info(
            "Fast-forwarding changes onto eligible branches for %s", self.pull_request
        )
        ff_candidates: Set[str] = self.target_branches.difference(
            {self.pull_request.target}
        )
        for candidate in ff_candidates:
            self.repo.fast_forward(source=self.pull_request.target, target=candidate)

    def sanity_check(self) -> None:
        """
        Performs a sanity check on the merge request.

        :raises InvalidMergeRequest: The merge request does not meet the requirements to be processed further.
        """

        LOGGER.info(
            f"Performing sanity check for pull request inmanta/{self.pull_request.repository.name}#{self.pull_request.number}"
        )

        with self.repo.checkout_branch(self.pull_request.target):
            project_config: ProjectConfig = Project(
                self.repo.directory
            ).get_project_config()
            required_file: Optional[str] = project_config.version_bump.tool.get_tool(
                self.repo.directory
            ).requires_file()
            if required_file is not None and not os.path.isfile(
                os.path.join(self.repo.directory, required_file)
            ):
                raise InvalidMergeRequest(
                    f"Target branch should contain a {required_file} file that references all relevant files"
                    " except for the changelog, which must not be in there."
                )

        if (
            self.pull_request.author.permission
            not in {
                github.RepositoryPermission.ADMIN,
                github.RepositoryPermission.MAINTAIN,
                github.RepositoryPermission.WRITE,
            }
            and self.pull_request.author.login not in self.config.author_whitelist
        ):
            raise InvalidMergeRequest(
                "Only pull requests opened by authors with write access to this repo or whitelisted authors are supported by"
                " the merge tool."
            )

        if self.pull_request.repository.name not in self.config.repositories:
            raise InvalidMergeRequest(
                "This repository is not managed by the merge tool. Managed repositories are: %s"
                % ", ".join(self.config.repositories)
            )

        if self.pull_request.source in self.config.dev_branches.values():
            raise InvalidMergeRequest(
                f"Source branch {self.pull_request.source} is a dev branch. Merge tool does not support merging from one dev"
                " branch to another"
            )

        if self.pull_request.target not in self.change_entry.destination_branches:
            raise InvalidMergeRequest(
                f"This pull requests's target branch is {self.pull_request.target} but it is not in the change entry's"
                " destination branches '%s'"
                % ", ".join(self.change_entry.destination_branches)
            )

        for branch in self.change_entry.destination_branches:
            change_type: Optional[ChangeType] = self.config.get_change_type(branch)
            if change_type is None:
                raise InvalidMergeRequest(
                    f"Destination branch {branch} is not a dev branch. Merge tool only supports dev branches as destination."
                    " Dev branches are %s"
                    % ", ".join(self.config.dev_branches.values())
                )
            if change_type < self.change_entry.change_type:
                raise InvalidMergeRequest(
                    f"Destination branch {branch} does not allow {self.change_entry.change_type.value} changes."
                )

        # enforce SemVer compatibility by disallowing divergence unless required by branches' version constraints
        groups: Dict[str, List[str]] = self.group_aligned_branches()
        for eligible in self.config.get_eligible_branches(
            self.change_entry.change_type
        ):
            if eligible not in self.change_entry.destination_branches:
                head: str = more_itertools.one(
                    head for head, group in groups.items() if eligible in group
                )
                if any(
                    aligned in self.change_entry.destination_branches
                    for aligned in groups[head]
                ):
                    raise InvalidMergeRequest(
                        f"SemVer violation: branch {eligible} is eligible for this change and has not diverged from one of the"
                        " branches in the destination set. Applying this merge as requested would result in a version bump due"
                        f" to branches diverging. Since {eligible} is eligible for this change, this version bump would not be"
                        f" in line with the SemVer semantics. Please include {eligible} in the destination set."
                    )

        if self.pull_request.mergeable != github.Mergeable.MERGEABLE:
            raise InvalidMergeRequest(
                "Pull request is not mergeable."
                f" Please check for merge conflicts before re-adding the {github.READY_LABEL} label."
            )

        # require pull request approval except for pull requests opened by the merge tool itself
        if (
            self.pull_request.review_decision != github.ReviewDecision.APPROVED
            and self.pull_request.requires_review
        ):
            raise InvalidMergeRequest("This pull request has not been approved yet.")

        awaiting_approval: Set[str] = self.pull_request.reviewers_requested.difference(
            self.pull_request.reviewers_approved
        )
        if awaiting_approval:
            raise InvalidMergeRequest(
                "This pull request has not been approved yet by some of the requested reviewers. Still awaiting approval from"
                " %s" % " ".join(awaiting_approval)
            )

        if (
            self.pull_request.state is not None
            and self.pull_request.state != github.CommitState.SUCCESS
        ):
            raise InvalidMergeRequest("The tests for this branch did not succeed.")

    def group_aligned_branches(self) -> Dict[str, List[str]]:
        """
        Groups all dev branches by their head commit.
        """
        return group_aligned_branches(self.repo, self.config)


def group_aligned_branches(
    repo: GitRepo, config: MergeToolConfig
) -> Dict[str, List[str]]:
    """
    Groups all dev branches by their head commit.
    """
    result: Dict[str, List[str]] = defaultdict(list)
    for branch in config.dev_branches.values():
        head: Optional[str] = repo.get_branch_head(branch)
        if head is not None:
            result[head].append(branch)
    return result


def poll_and_process(config: MergeToolConfig, token: str) -> None:
    """
    Does a single pass to poll for matching pull requests and process them.
    Loops as long as new pull requests are found. Does not wait for pull requests to come in.
    """
    while True:
        pull_request: Optional[MergeToolPullRequest] = github.get_ready_pull_request(
            list(config.repositories), config.bot_responsibles, token
        )
        if pull_request is None:
            return
        with git.git_repo(
            urljoin(github.ORGANIZATION_URL, pull_request.repository.name), token
        ) as repo:
            MergeRequest(config, pull_request, repo).process()
        # Give GitHub some time to reach consistency
        time.sleep(5)


def open_pull_request(
    config: MergeToolConfig,
    repository_name: str,
    source: str,
    change_entry_name: str,
    change_entry: ChangeEntry,
    token: str,
    include_aligned: bool = False,
) -> None:
    """
    Open a pull request that will be handled by the merge tool. Pushes a change entry to the remote source branch.
    If include_aligned is true, it extends the change entry to include all branches aligned with the specified destination
    branches.
    """
    with git.git_repo(urljoin(github.ORGANIZATION_URL, repository_name), token) as repo:
        full_change_entry: ChangeEntry
        if include_aligned:
            head_groups: Dict[str, List[str]] = group_aligned_branches(repo, config)
            destination_branches: Set[str] = set()
            for target in change_entry.destination_branches:
                target_head: Optional[str] = repo.get_branch_head(target)
                if target_head is None:
                    raise Exception(f"There is no {target} branch in this repo")
                destination_branches = destination_branches.union(
                    head_groups[target_head]
                )
            full_change_entry = change_entry.copy()
            full_change_entry.destination_branches = list(destination_branches)
        else:
            full_change_entry = change_entry

        with repo.checkout_branch(source) as branch:
            change_entry_dir: str = os.path.join(repo.directory, CHANGE_ENTRIES_PATH)
            if not os.path.exists(change_entry_dir):
                os.makedirs(change_entry_dir)
            change_entry.write(
                os.path.join(change_entry_dir, f"{change_entry_name}.yml")
            )
            branch.commit("Added change entry")
            branch.push()

    github.open_pull_request(
        repository=repository_name,
        target=change_entry.destination_branches[0],
        source=source,
        title=full_change_entry.description,
        message="",
        token=token,
    )


@click.command()
@click.option(
    "--config",
    "-c",
    help="The configuration file for the merge tool",
    default="merge-tool.yml",
)
@click.option("--verbose", "-v", help="Use verbose debug logging", is_flag=True)
@click.option(
    "--github-token",
    help=(
        "Token for the GitHub user associated with the merge tool."
        " Used to interact with repositories and with the GitHub API."
        " This value can also be set via the IRT_MERGETOOL_GITHUB_TOKEN environment variable."
    ),
    default=lambda: os.environ.get("IRT_MERGETOOL_GITHUB_TOKEN", None),
)
def main(config: str, verbose: bool, github_token: Optional[str]) -> None:
    if github_token is None:
        raise click.ClickException(
            "GitHub token must be set via --github-token or the IRT_MERGETOOL_GITHUB_TOKEN environment variable."
        )

    root_logger: logging.Logger = logging.getLogger()
    stream: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    if verbose:
        root_logger.setLevel(logging.DEBUG)
        stream.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)
        stream.setLevel(logging.INFO)
    root_logger.addHandler(stream)
    logging.captureWarnings(True)

    config_path: str = os.path.abspath(config)
    config_obj: MergeToolConfig = parse_config(config_path)
    poll_and_process(config_obj, github_token)
