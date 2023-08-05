"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import datetime
import enum
import logging
import subprocess
from contextlib import contextmanager
from enum import Enum
from tempfile import TemporaryDirectory
from typing import Iterator, List, Optional, Sequence, Set, Tuple, TypeVar

from packaging.version import InvalidVersion, Version

from irt import util

LOGGER = logging.getLogger(__name__)


@contextmanager
def git_repo(url: str, token: Optional[str] = None) -> Iterator["GitRepo"]:
    with TemporaryDirectory() as repo_dir:
        yield GitRepo(url, repo_dir, token)


class GitRepo:
    """
    Represents a cloned git repository.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        clone_dir: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """
        Either clone_dir has to provided (for repos already present on disk)
        or url (to clone a new repo)

        :param clone_dir: folder to clone the repo to or folder where the repo can be found

        :param url: remote to clone from
        :param token: access token to use when cloning
        """
        if url is None and clone_dir is None:
            raise Exception("either url or clone_dir should be set")
        self.url: Optional[str] = url
        self.directory: str
        if clone_dir is None:
            repo_name: str = url.rsplit("/", maxsplit=1)[-1]
            self.directory = (
                repo_name[0:-4] if repo_name.endswith(".git") else repo_name
            )
        else:
            self.directory = clone_dir
        self.token: Optional[str] = token
        self._branch: Optional[Branch] = None
        if url is not None:
            LOGGER.info("Cloning git repository %s into %s", url, self.directory)
            util.clone_repo(self.url, self.directory, token=self.token)

    def get_commit(self) -> str:
        out: str = util.subprocess_log(
            subprocess.check_output,
            ["git", "rev-parse", "HEAD"],
            logger=LOGGER,
            cwd=self.directory,
        ).decode()
        return out

    def get_branch_head(self, branch: str) -> Optional[str]:
        """
        Returns the head commit for a branch, if it exists. If the branch doesn't exist locally but does on the remote,
        the remote branch's head is returned.
        """

        def show_ref(ref: str) -> Optional[str]:
            try:
                out: str = util.subprocess_log(
                    subprocess.check_output,
                    ["git", "show-ref", "--verify", ref],
                    logger=LOGGER,
                    cwd=self.directory,
                ).decode()
                split: List[str] = out.split()
                if len(split) != 2 or split[1] != ref:
                    raise Exception("Unexpected output for git show-ref")
                return split[0]
            except subprocess.CalledProcessError:
                return None

        local_head: Optional[str] = show_ref(f"refs/heads/{branch}")
        return (
            local_head
            if local_head is not None
            else show_ref(f"refs/remotes/origin/{branch}")
        )

    def get_all_branches(self) -> Set[str]:
        """
        Returns a set of local and remote branch names, without the remote prefix.
        """
        local: str = util.subprocess_log(
            subprocess.check_output,
            ["git", "branch"],
            logger=LOGGER,
            cwd=self.directory,
        ).decode()
        remote: str = util.subprocess_log(
            subprocess.check_output,
            ["git", "branch", "--remotes"],
            logger=LOGGER,
            cwd=self.directory,
        ).decode()
        return set.union(
            {line.strip(" *") for line in local.splitlines()},
            {
                line.strip()[7:]
                for line in remote.splitlines()
                if line.strip().startswith("origin/")
            },
        )

    def get_tagged_versions(self) -> List[Tuple["Tag", Version]]:
        """
        Returns a list of released versions based on git tags, sorted from high to low. For each version, returns a tuple of
        the tag and the corresponding version. Assumes version tags follow Inmanta tagging conventions (v<x.y.z>, annotated).
        """
        separator: str = "<irt_separator>"
        date_format: str = "%Y-%m-%d"
        raw: str = (
            util.subprocess_log(
                subprocess.check_output,
                [
                    "git",
                    "tag",
                    "--list",
                    "--format",
                    f"%(refname:strip=2){separator}%(subject){separator}%(taggerdate:format:{date_format})",
                ],
                logger=LOGGER,
                cwd=self.directory,
            )
            .decode()
            .strip()
        )

        def parse(raw_tag: str) -> Optional[Tag]:
            parts: Sequence[str] = raw_tag.split(separator)
            if len(parts) != 3:
                raise Exception(
                    f"Illegal tag format. Tag name or message should not include '{separator}'"
                )
            if not parts[2]:
                # Not an annotated tag. Release tool always creates annotated tags so safe to assume this is not a (recent)
                # version tag. Skipping
                return None
            return Tag(
                repo=self,
                name=parts[0],
                message=parts[1],
                date=datetime.datetime.strptime(parts[2], date_format).date(),
            )

        tags: Iterator[Optional[Tag]] = (parse(raw_tag) for raw_tag in raw.splitlines())

        def from_tag(tag: Tag) -> Optional[Version]:
            if not tag.name.startswith("v"):
                return None
            try:
                return Version(tag.name[1:])
            except InvalidVersion:
                return None

        return sorted(
            [
                (tag, v)
                for tag, v in ((tag, from_tag(tag)) for tag in tags if tag is not None)
                if v is not None
            ],
            key=lambda tup: tup[1],
            reverse=True,
        )

    def delete_remote_branch(self, branch: str) -> None:
        """
        Deletes a branch from the remote.
        """
        LOGGER.info(
            "Deleting remote branch %s of %s",
            branch,
            self.url,
        )
        util.subprocess_log(
            subprocess.check_output,
            ["git", "push", "--delete", "origin", branch],
            logger=LOGGER,
            cwd=self.directory,
        )

    def merge(
        self,
        *,
        target: str,
        source: str,
        strategy_option: Optional["RecursiveStrategyOption"] = None,
        message: Optional[str] = None,
    ) -> None:
        """
        Merges source into target using the recursive strategy.

        :raises MergeFailure: Failed to merge source into target branch.
        """
        with self.checkout_branch(target) as target_branch:
            target_branch.merge(source, strategy_option, message)

    def squash(
        self,
        *,
        target: str,
        source: str,
        message: Optional[str] = None,
        author: Optional[str] = None,
    ) -> None:
        """
        Squashes and merges source into target.

        :raises MergeFailure: Failed to squash and merge source into target branch.
        """
        with self.checkout_branch(target) as target_branch:
            target_branch.squash(source, message, author)

    def fast_forward(self, *, target: str, source: str) -> None:
        """
        Fast forwards source onto target.

        :raises MergeFailure: Failed to fast-forward source onto target branch.
        """
        with self.checkout_branch(target) as target_branch:
            target_branch.fast_forward(source)

    def cherry_pick(self, target: str, commits: List[str]) -> None:
        """
        Cherry-pick the given commits on the target branch.

        :raises MergeFailure: Failed to cherry-pick commits on target branch.
        """
        with self.checkout_branch(target) as target_branch:
            target_branch.cherry_pick(commits)

    def checkout_branch(
        self, branch: str, *, base_branch: Optional[str] = None
    ) -> "Branch":
        """
        Checks out a branch for use in a `with` block. Can also be used to check out other refs in detached head state.
        """
        return (
            Branch(self, branch)
            if base_branch is None
            else NewBranch(self, branch, base_branch)
        )


class MergeFailure(Exception):
    pass


class InvalidBranch(Exception):
    pass


@enum.unique
class RecursiveStrategyOption(Enum):
    OURS: str = "ours"
    THEIRS: str = "theirs"


T = TypeVar("T", bound="Branch")


class Branch:
    """
    Context manager that represents a checked out branch in a git repository.
    """

    def __init__(self, repo: GitRepo, branch: str) -> None:
        self.repo: GitRepo = repo
        self.branch: str = branch

    def get_new_files(self, reference_branch: str) -> List[str]:
        """
        Returns a list of files that are present in this branch but not in the reference branch.
        """
        output: str = util.subprocess_log(
            subprocess.check_output,
            [
                "git",
                "diff",
                "--no-renames",
                "--name-only",
                "--diff-filter=A",
                reference_branch,
            ],
            logger=LOGGER,
            cwd=self.repo.directory,
        ).decode()
        return output.strip().split()

    def commit(self, message: str, ignore_empty: bool = False) -> None:
        """
        Stages and commits all changes.
        """
        LOGGER.info(
            "Committing changes on branch %s of %s with message '%s'",
            self.branch,
            self.repo.url,
            message,
        )
        util.subprocess_log(
            subprocess.check_output,
            ["git", "add", "--all"],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        diff_exit_code: int = util.subprocess_log(
            subprocess.call,
            ["git", "diff-index", "--quiet", "HEAD"],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        if diff_exit_code == 0:
            if ignore_empty:
                return
            else:
                raise Exception("Attempting commit without changes.")
        util.subprocess_log(
            subprocess.check_output,
            ["git", "commit", "-m", message],
            logger=LOGGER,
            cwd=self.repo.directory,
        )

    def tag(
        self,
        tag: str,
        message: str,
    ) -> "Tag":
        """
        Adds an annotated tag to the current branch head.
        """
        util.subprocess_log(
            subprocess.check_output,
            ["git", "tag", "-a", "-m", message, tag],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        return Tag(self.repo, tag, message, datetime.datetime.now().astimezone())

    def merge(
        self,
        source: str,
        strategy_option: Optional[RecursiveStrategyOption] = None,
        message: Optional[str] = None,
    ) -> None:
        """
        Merges the source branch into this one using the recursive strategy.

        :raises MergeFailure: Failed to merge source into this branch.
        """
        LOGGER.info(
            "Merging branch %s into %s with the recursive strategy", source, self.branch
        )
        try:
            util.subprocess_log(
                subprocess.check_output,
                [
                    "git",
                    "merge",
                    "-s",
                    "recursive",
                    *(
                        ["-X", strategy_option.value]
                        if strategy_option is not None
                        else []
                    ),
                    source,
                ],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        except subprocess.CalledProcessError:
            LOGGER.exception("Failed to merge %s into %s", source, self.branch)
            raise MergeFailure(f"Failed to merge {source} into {self.branch}")

    def squash(
        self, source: str, message: Optional[str] = None, author: Optional[str] = None
    ) -> None:
        """
        Squashes and merges the source branch into this one.

        :raises MergeFailure: Failed to squash and merge source into this branch.
        """
        LOGGER.info(
            "Squashing and merging branch %s into %s on for %s",
            source,
            self.branch,
            author,
        )
        try:
            util.subprocess_log(
                subprocess.check_output,
                ["git", "merge", "--squash", source],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
            util.subprocess_log(
                subprocess.check_output,
                [
                    "git",
                    "commit",
                    *(["-m", message] if message is not None else []),
                    *(["--author", author] if author else []),
                    "--no-edit",
                ],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        except subprocess.CalledProcessError:
            LOGGER.error("Failed to squash and merge %s into %s", source, self.branch)
            raise MergeFailure(
                f"Failed to squash and merge {source} into {self.branch}"
            )

    def fast_forward(self, source: str) -> None:
        """
        Fast forwards the source branch onto this one.

        :raises MergeFailure: Failed to fast-forward source onto this branch.
        """
        LOGGER.info("Fast-forwarding branch %s onto %s", source, self.branch)
        try:
            util.subprocess_log(
                subprocess.check_output,
                ["git", "merge", "--ff-only", source],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        except subprocess.CalledProcessError:
            LOGGER.error("Failed to fast-forward %s onto %s", source, self.branch)
            raise MergeFailure(f"Failed to fast-forward {source} onto {self.branch}")

    def cherry_pick(self, commits: List[str]) -> None:
        """
        Cherry-pick the given commits on this branch.

        :raises MergeFailure: Failed to cherry-pick commits on this branch.
        """
        if not commits:
            return
        LOGGER.info("Cherry-picking commits %s on %s", ", ".join(commits), self.branch)
        try:
            util.subprocess_log(
                subprocess.check_output,
                ["git", "cherry-pick", *commits],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        except subprocess.CalledProcessError:
            LOGGER.error(
                "Failed to cherry-pick %s on %s", ", ".join(commits), self.branch
            )
            raise MergeFailure(
                f"Failed to cherry-pick {', '.join(commits)} on {self.branch}"
            )

    def checkout_path(self, *, branch: str, path: str) -> None:
        """
        Overwrite the contents of the files in the given path with those on the other branch.
        """
        LOGGER.info(
            "Checking out path %s from branch %s onto %s", path, branch, self.branch
        )
        util.subprocess_log(
            subprocess.check_output,
            ["git", "checkout", branch, path],
            logger=LOGGER,
            cwd=self.repo.directory,
        )

    def push(self) -> None:
        """
        Pushes all committed changes to the remote.
        """
        LOGGER.info("Pushing branch %s to %s", self.branch, self.repo.url)
        util.subprocess_log(
            subprocess.check_output,
            ["git", "push", "origin", self.branch],
            logger=LOGGER,
            cwd=self.repo.directory,
        )

    def add_annotated_tag(
        self, tag_name: str, message: str, push: bool = False
    ) -> None:
        LOGGER.info("Adding annotated tag %s on %s", tag_name, self.branch)
        util.subprocess_log(
            subprocess.check_output,
            ["git", "tag", "-a", tag_name, "-m", message],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        if push:
            self.push_tag(tag_name)

    def push_tag(self, tag_name: str) -> None:
        LOGGER.info("Pushing tag %s to %s", tag_name, self.repo.url)
        util.subprocess_log(
            subprocess.check_output,
            ["git", "push", "origin", tag_name],
            logger=LOGGER,
            cwd=self.repo.directory,
        )

    def __enter__(self: T) -> T:
        if self.repo._branch is not None:
            raise Exception("Can not enter context: already in a `with` block")
        status: str = util.subprocess_log(
            subprocess.check_output,
            ["git", "status", "--porcelain=v1"],
            logger=LOGGER,
            cwd=self.repo.directory,
        ).decode()
        if status.strip() != "":
            raise Exception(
                f"Can not checkout {self.branch}: there are uncommitted changes"
            )
        LOGGER.info("Checking out %s of %s", self.branch, self.repo.url)
        try:
            util.subprocess_log(
                subprocess.check_output,
                ["git", "checkout", self.branch],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        except subprocess.CalledProcessError:
            raise InvalidBranch(
                "Can't checkout branch %s: it does not exist." % self.branch
            )
        self.repo._branch = self
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> Optional[bool]:
        util.subprocess_log(
            subprocess.check_output,
            ["git", "reset", "--hard", self.branch],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        util.subprocess_log(
            subprocess.check_output,
            ["git", "clean", "--force", "-d"],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
        self.repo._branch = None
        return None


U = TypeVar("U", bound="NewBranch")


class NewBranch(Branch):
    """
    Represents a checked out branch that does not exist yet at the point of context manager entry.
    Branches off the base branch when entered.
    """

    def __init__(self, repo: GitRepo, branch: str, base_branch: str) -> None:
        super().__init__(repo, branch)
        self.base_branch: str = base_branch

    def __enter__(self: U) -> U:
        LOGGER.info(
            "Branching off %s from %s in %s",
            self.branch,
            self.base_branch,
            self.repo.url,
        )
        with self.repo.checkout_branch(self.base_branch):
            util.subprocess_log(
                subprocess.check_output,
                ["git", "checkout", "-b", self.branch],
                logger=LOGGER,
                cwd=self.repo.directory,
            )
        return super().__enter__()


class Tag:
    """
    Represents an annotated tag.
    """

    def __init__(
        self, repo: GitRepo, name: str, message: str, date: datetime.date
    ) -> None:
        self.repo: GitRepo = repo
        self.name: str = name
        self.message: str = message
        self.date: datetime.date = date

    def push(self) -> None:
        """
        Push this tag to the remote.
        """
        LOGGER.info("Pushing tag %s to %s", self.name, self.repo.url)
        util.subprocess_log(
            subprocess.check_output,
            ["git", "push", "origin", self.name],
            logger=LOGGER,
            cwd=self.repo.directory,
        )
