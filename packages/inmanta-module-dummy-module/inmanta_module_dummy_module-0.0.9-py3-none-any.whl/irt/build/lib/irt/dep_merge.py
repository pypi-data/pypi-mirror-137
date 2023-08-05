"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import logging
import os
import re
import sys
import time
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin

import click
import colorlog
import requests

import irt.mergetool.config
from irt import git, mergetool
from irt.changelog import ChangeEntry
from irt.mergetool import github
from irt.mergetool.config import MergeToolConfig
from irt.version import ChangeType

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s: %(message)s")
)

LOGGER = logging.getLogger()
LOGGER.addHandler(handler)

if not os.getenv("GITHUB_TOKEN"):
    click.echo("GITHUB_TOKEN environment variable should be set", err=True)
    sys.exit(1)

token: str = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"}
MERGE_SLEEP = 20

required_checks = {
    "integration-build",
    "jenkins-core-build",
    "continuous-integration/jenkins/branch",
    "continuous-integration/jenkins/pr-merge",
}

# Currently just a static set of repos that require reviews
review_required = {
    "inmanta-core",
    "inmanta",
}

API_URL = "https://api.github.com"


@lru_cache()
def get_dep_merge_email() -> str:
    try:
        return github.api_query("viewer { email }", token=token)["viewer"]["email"]
    except KeyError as e:
        raise Exception(
            "Failed to fetch user information for dep-merge bot, expected data not present in response: %s"
            % e
        )


def get_repositories(end_cursor: str = None) -> List[Dict]:
    cursor_template = ""
    if end_cursor:
        cursor_template = f', after: "{end_cursor}"'

    query_template = (
        """
    {
      viewer {
        repositories(orderBy: {field: NAME, direction: ASC}, affiliations: [ORGANIZATION_MEMBER],
                     ownerAffiliations: [OWNER, ORGANIZATION_MEMBER, COLLABORATOR], first: 100%s) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            name
            url
            isPrivate
            isArchived
            pullRequests(first: 10, orderBy: {field: CREATED_AT, direction: ASC}, labels: "dependencies", states: OPEN) {
              nodes {
                mergeable
                author {
                  url
                }
                id
                title
                url
                number
                baseRefName
                headRefName
                labels(first: 100) {
                    pageInfo {
                        hasNextPage
                    }
                    nodes {
                        name
                    }
                }
                commits(last: 1) {
                  nodes {
                    commit {
                      id
                      status {
                        state
                        id
                        contexts {
                          state
                          description
                          creator {
                            url
                          }
                          targetUrl
                          context
                          createdAt
                        }
                      }
                      statusCheckRollup {
                        state
                      }
                    }
                  }
                }
              }
            }
            owner {
              url
            }
          }
        }
      }
    }
    """
        % cursor_template
    )

    response = requests.post(
        f"{API_URL}/graphql",
        headers=headers,
        json={"query": query_template},
    )
    if response.status_code != 200:
        return None

    data = response.json()
    repositories = data["data"]["viewer"]["repositories"]["nodes"]

    if any(
        pr["labels"]["pageInfo"]["hasNextPage"]
        for repo in repositories
        for pr in repo["pullRequests"]["nodes"]
    ):
        raise Exception(
            "There are too many labels on this pull request for dep-merge to process"
        )

    if data["data"]["viewer"]["repositories"]["pageInfo"]["hasNextPage"]:
        repositories.extend(
            get_repositories(
                data["data"]["viewer"]["repositories"]["pageInfo"]["endCursor"]
            )
        )

    return repositories


def get_pr_status(pr: Dict) -> Dict[str, str]:
    """Get the latest pull request status"""
    if not pr["commits"]["nodes"]:
        return {}

    commit = pr["commits"]["nodes"][0]["commit"]

    status = {}
    if not commit["status"] or "contexts" not in commit["status"]:
        return {}

    for ctx in commit["status"]["contexts"]:
        status[ctx["context"]] = ctx["state"]

    return status


def sort_pull_requests(repos: List[Dict]) -> Dict[str, Dict[str, Dict]]:
    # Create pull requests per library
    pull_requests = defaultdict(lambda: defaultdict(list))

    for repo in repos:
        repo_name = repo["name"]
        if repo["pullRequests"]["nodes"]:
            for pr in repo["pullRequests"]["nodes"]:
                if github.READY_LABEL in (
                    label["name"] for label in pr["labels"]["nodes"]
                ):
                    LOGGER.info(
                        "Ignoring %s because it has already been delegated to the merge tool.",
                        pr["url"],
                    )
                    continue

                title = pr["title"]
                match = re.search(
                    r"(Bump|Update) (?P<name>[^\s]+) (requirement )?from (?P<from>[^\s]+) to (?P<to>[^\s]+)",
                    title,
                )
                if not match:
                    print("Unable to parse version bump in PR " + pr["url"])

                data = match.groupdict()

                checks = get_pr_status(pr)

                pull_requests[data["name"]][data["to"]].append(
                    {
                        "title": pr["title"],
                        "id": pr["id"],
                        "repo": repo_name,
                        "source_branch": pr["headRefName"],
                        "target_branch": pr["baseRefName"],
                        "to": data["to"],
                        "pr": pr["number"],
                        "url": pr["url"],
                        "status": pr["mergeable"],
                        "checks": checks,
                    }
                )

    return pull_requests


def verify_status(pr: Dict) -> bool:
    """Check if the status check allows to merge this PR"""
    if not len(pr["checks"]):
        return False

    required = False
    for check_name, check_result in pr["checks"].items():
        if check_name in required_checks:
            required = True

        if check_result != "SUCCESS":
            LOGGER.warning(
                "PR %s check %s has a non success result %s",
                pr["url"],
                check_name,
                check_result,
            )
            return False

    if not required:
        LOGGER.warning(
            "PR %s does not have one of the required status checks %s",
            pr["url"],
            ", ".join(required_checks),
        )
        return False

    return True


class MergeFailedException(Exception):
    pass


def merge(pr_id: str) -> None:
    """merge the given PR (squash is not supported)"""
    query = """
    mutation mergePullRequest($input: MergePullRequestInput!) {
        mergePullRequest(input: $input) {
            pullRequest {
                merged
                mergedAt
                state
                url
            }
        }
    }
    """
    response = requests.post(
        f"{API_URL}/graphql",
        json={"query": query, "variables": {"input": {"pullRequestId": pr_id}}},
        headers=headers,
    )

    if response.status_code != 200:
        raise MergeFailedException()

    data = response.json()
    if "errors" in data:
        LOGGER.error("Got error on merge: %s", data["errors"])
        raise MergeFailedException()


def rest_merge(pr: Dict) -> None:
    url = f"{API_URL}/repos/inmanta/{pr['repo']}/pulls/{pr['pr']}/merge"
    response = requests.put(url, headers=headers, json={"merge_method": "squash"})
    data = response.json()

    if response.status_code != 200:
        LOGGER.error("Merge failed, got error: %s", data)
        raise MergeFailedException()

    if "errors" in data:
        LOGGER.error("Got error on merge: %s", data["errors"])
        raise MergeFailedException()


def delegate_to_merge_tool(pr: Dict, merge_tool_config: MergeToolConfig) -> None:
    """
    Delegate the merging of this pull request to the merge tool by adding a change entry and the appropriate label.
    """
    if recreate_on_conflict(pr, merge_tool_config):
        return
    try:
        # get merge-tool-ready label id
        query: str = """
            repository(
                name: "%s"
                owner: "inmanta"
            ) {
                label(name: "%s") {
                    id
                }
            }
        """ % (
            github.sanitize_string(pr["repo"]),
            github.READY_LABEL,
        )
        data: Dict = github.api_query(query, token)
        label_id: str = data["repository"]["label"]["id"]

        # add change entry
        with git.git_repo(urljoin(github.ORGANIZATION_URL, pr["repo"]), token) as repo:
            target_head: Optional[str] = repo.get_branch_head(pr["target_branch"])
            if target_head is None:
                raise Exception(
                    f"There is no {pr['target_branch']} branch in this repo"
                )
            change_entry: ChangeEntry = ChangeEntry(
                description=pr["title"],
                change_type=ChangeType.PATCH,
                destination_branches=[
                    branch
                    for branch in merge_tool_config.dev_branches.values()
                    if repo.get_branch_head(branch) == target_head
                ],
            )
            with repo.checkout_branch(pr["source_branch"]) as branch:
                change_entry_dir: str = os.path.join(
                    repo.directory, mergetool.CHANGE_ENTRIES_PATH
                )
                if not os.path.exists(change_entry_dir):
                    os.makedirs(change_entry_dir)
                change_entry.write(
                    os.path.join(change_entry_dir, f"{pr['pr']}-dependabot.yml")
                )
                branch.commit("Added change entry")
                branch.push()

        # add merge-tool-ready label
        mutation: str = """
            addLabelsToLabelable(
                input: {
                    labelIds: ["%s"]
                    labelableId: "%s"
                }
            ) {
                clientMutationId
            }
        """ % (
            github.sanitize_string(label_id),
            github.sanitize_string(pr["id"]),
        )
        github.api_mutation(mutation, token)
    except Exception as e:
        LOGGER.error("Failed to delegate pull request to merge tool. Got error: %s", e)
        raise MergeFailedException()


def recreate_on_conflict(
    pr: Dict[str, object], merge_tool_config: MergeToolConfig
) -> bool:
    """
    Instruct dependabot to recreate a pull request if a merge conflict exists and all commits were made by dependabot or by
    this bot's git user.

    Returns True iff this pull request was handled and no further action is required in this iteration.

    :raises MergeFailedException: A conflict exists that can not be resolved.
    """
    LOGGER.info(f"Looking for conflicts on PR {pr['url']}")
    merge_tool_pr: github.MergeToolPullRequest = github.get_pull_request_by_number(
        repository=pr["repo"],
        pr_number=pr["pr"],
        bot_responsibles=merge_tool_config.bot_responsibles,
        token=token,
    )
    if merge_tool_pr.mergeable != github.Mergeable.CONFLICTING:
        return False
    authors: Set[str] = set(merge_tool_pr.authors)
    nb_authors: int = len(authors)
    # assuming at least one of the authors is dependabot
    if nb_authors > 2 or (nb_authors == 2 and get_dep_merge_email() not in authors):
        LOGGER.error(
            f"A conflict exists on PR {pr['url']} but it has commits from someone other than dependabot or dep-merge."
        )
        raise MergeFailedException()
    LOGGER.info(
        f"Instructing dependabot to recreate PR {pr['url']} because of merge conflicts"
    )
    merge_tool_pr.comment("@dependabot recreate")
    return True


def process_pull_requests(
    name: str,
    version: str,
    prs: List[Dict],
    dry_run: bool,
    merge_tool_config: MergeToolConfig,
) -> bool:
    """Process the pull requests per library and per version. If there is an error, this will
    be logged and this method will return False so ci jobs fail.
    """
    LOGGER.info("Processing PR to bump %s to %s", name, version)

    LOGGER.debug("\tChecking merge request status")
    status = defaultdict(list)
    for pr in prs:
        status[pr["status"]].append(pr)

    if len(status) != 1 and "MERGEABLE" not in status:
        del status["MERGEABLE"]
        urls = []
        for st, pr_list in status.items():
            for pr in pr_list:
                urls.append(pr["url"])

        LOGGER.error(
            "\tNot all pull requests for %s to %s are in a mergable state. The following have issues: %s",
            name,
            version,
            ", ".join(urls),
        )
        return False

    LOGGER.debug("\tChecking if all required status checks are green")

    checks = {pr["url"]: verify_status(pr) for pr in prs}
    failed = [name for name, status in checks.items() if not status]

    if len(failed):
        LOGGER.error("\tNot all status checks succeeded for PR: %s", ", ".join(failed))
        return False

    LOGGER.info(
        "\tPR for bumping %s to %s can be merged for %d repos", name, version, len(prs)
    )
    for pr in prs:
        merge_tool_managed: bool = (
            pr["repo"] in merge_tool_config.repositories
            and pr["target_branch"] in merge_tool_config.dev_branches.values()
        )
        if merge_tool_managed:
            LOGGER.info(
                "\t\tbranch %s on repo %s is managed by the merge tool: delegating merge",
                pr["target_branch"],
                pr["repo"],
            )
        if pr["repo"] in review_required or merge_tool_managed:
            LOGGER.info("\t\tApproving review first")
            if not dry_run:
                requests.post(
                    f"{API_URL}/repos/inmanta/{pr['repo']}/pulls/{pr['pr']}/reviews",
                    headers=headers,
                    json={"event": "APPROVE"},
                )

        LOGGER.info("\t\tMerging %s", pr["url"])
        try:
            if not dry_run:
                if merge_tool_managed:
                    # This repo is managed by the merge tool: delegate it instead of merging
                    delegate_to_merge_tool(pr, merge_tool_config)
                else:
                    rest_merge(pr)
        except MergeFailedException:
            LOGGER.error("\t\tFailed to merge %s, skipping all remaining", pr["url"])
            return False

        if not dry_run:
            time.sleep(MERGE_SLEEP)

    return True


@click.command()
@click.option(
    "--merge-tool-config",
    help=(
        "The configuration file for the merge tool. Required to know which repos and branches should be delegated to the merge"
        " tool. This is meant to be a temporary measure: dep-merge should be integrated more closely with the merge tool when"
        " dependency management accross ISO development branches is implemented."
    ),
    default="merge-tool.yml",
)
@click.option(
    "--dry-run", "-d", help="Do a dryrun and do not actually merge.", is_flag=True
)
@click.option("--verbose", "-v", help="Use verbose debug logging", is_flag=True)
def main(dry_run: bool, merge_tool_config: str, verbose: bool) -> None:
    if verbose:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    merge_tool_config_obj: MergeToolConfig = irt.mergetool.config.parse_config(
        merge_tool_config
    )

    repos = get_repositories()
    if repos is None:
        sys.exit(1)

    prs = sort_pull_requests(repos)

    result = True
    for name in prs.keys():
        for version, pr_list in prs[name].items():
            result &= process_pull_requests(
                name, version, pr_list, dry_run, merge_tool_config_obj
            )

    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
