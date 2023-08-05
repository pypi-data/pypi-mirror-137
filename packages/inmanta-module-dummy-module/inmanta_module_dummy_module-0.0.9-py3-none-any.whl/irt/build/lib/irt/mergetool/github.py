"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import logging
import re
from enum import Enum
from itertools import groupby
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Match,
    Optional,
    Set,
    Type,
    TypeVar,
)

import pydantic
import requests
from pydantic import BaseModel

LOGGER = logging.getLogger(__name__)

API_URL = "https://api.github.com/graphql"
ORGANIZATION = "inmanta"
ORGANIZATION_URL = f"https://github.com/{ORGANIZATION}/"

READY_LABEL = "merge-tool-ready"
BRANCH_PREFIX = "merge-tool/"


class RepositoryPermission(Enum):
    ADMIN: str = "ADMIN"
    MAINTAIN: str = "MAINTAIN"
    READ: str = "READ"
    TRIAGE: str = "TRIAGE"
    WRITE: str = "WRITE"


class CommitState(Enum):
    """
    The test state of a commit. Maps with GitHub API's StatusState.
    """

    ERROR: str = "ERROR"
    EXPECTED: str = "EXPECTED"
    FAILURE: str = "FAILURE"
    PENDING: str = "PENDING"
    SUCCESS: str = "SUCCESS"


class Mergeable(Enum):
    CONFLICTING: str = "CONFLICTING"
    MERGEABLE: str = "MERGEABLE"
    UNKNOWN: str = "UNKNOWN"


class ReviewDecision(Enum):
    APPROVED: str = "APPROVED"
    CHANGES_REQUESTED: str = "CHANGES_REQUESTED"
    REVIEW_REQUIRED: str = "REVIEW_REQUIRED"


class Repository(BaseModel):
    id: str
    name: str
    ready_label_id: str


class Author(BaseModel):
    id: str
    login: str
    bot: bool = False
    permission: Optional[RepositoryPermission]


T = TypeVar("T", bound="MergeToolPullRequest")


class MergeToolPullRequest(BaseModel):
    id: str
    number: int
    title: str
    body: str
    requires_review: bool
    second_stage: bool
    author: Author
    authors: List[
        str
    ]  # The list of email addresses that contributed commits, in order of importance
    repository: Repository
    source: str
    target: str
    mergeable: Mergeable
    state: Optional[CommitState]
    review_decision: Optional[ReviewDecision]
    reviewers_requested: Set[str]
    reviewers_approved: Set[str]
    token: str

    _bot_responsibles: List[str]

    def __init__(self, bot_responsibles: Iterable[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self._bot_responsibles = list(bot_responsibles)

    class Config:
        underscore_attrs_are_private = True

    def get_next_stage_branch_prefix(self) -> str:
        """
        Returns the prefix that should be applied to second stage branches opened by the merge tool.
        """
        return f"{BRANCH_PREFIX}{self.get_original_pull_request_number()}/"

    def get_original_pull_request_number(self) -> int:
        """
        Returns the number of the original pull request by inspecting the source branch name prefix.
        """
        if not self.second_stage:
            return self.number
        match: Optional[Match] = re.match("merge-tool/([0-9]+)/.*", self.source)
        if match is None:
            raise Exception(
                "Failed to get original pull request: second stage pull request does not match expected naming scheme."
            )
        return int(match.group(1))

    def get_original_pull_request(self) -> "MergeToolPullRequest":
        """
        Returns the original pull request. For a first stage pull request, this is just the pull request itself. For a second
        stage pull request this is the pull request, opened by a developer, that caused merge tool to open this one.
        """
        original_number: int = self.get_original_pull_request_number()
        if original_number == self.number:
            return self
        result: Optional[MergeToolPullRequest] = get_pull_request_by_number(
            self.repository.name, original_number, self._bot_responsibles, self.token
        )
        if result is None:
            raise Exception(
                "Failed to get original pull request: no pull request found with number %s."
                % original_number
            )
        return result

    @classmethod
    def get_subquery(cls) -> str:
        """
        Returns the graphql field selection subquery for a pull request.
        """
        return """
            author {
                __typename
                ... on Bot {
                    id
                    login
                }
                ... on User {
                    id
                    login
                }
            }
            authorAssociation
            baseRefName
            body
            commits(last: 1) {
                nodes {
                    commit {
                        status {
                            state
                        }
                    }
                }
            }
            authors: commits(last: 100) {
                nodes {
                    commit {
                        changedFiles
                        authors(last: 100) {
                            nodes {
                                email
                                name
                            }
                        }
                    }
                }
            }
            id
            headRefName
            mergeable
            number
            repository {
                id
                label(name: "%s") {
                    id
                }
                name
            }
            reviewDecision
            reviewRequests(first: 100) {
                pageInfo {
                    hasNextPage
                }
                nodes {
                    requestedReviewer {
                        ... on User {
                            login
                        }
                    }
                }
            }
            reviews(first: 100, states: [APPROVED]) {
                pageInfo {
                    hasNextPage
                }
                nodes {
                    author {
                        login
                    }
                }
            }
            title
            viewerDidAuthor
        """ % sanitize_string(
            READY_LABEL
        )

    @classmethod
    def from_query_response(
        cls: Type[T],
        pull_request_data: Dict,
        bot_responsibles: Iterable[str],
        token: str,
    ) -> T:
        """
        Parses the pull request object of the response to a query made with this class' subquery for pull requests.
        """
        try:
            if any(
                pull_request_data[review]["pageInfo"]["hasNextPage"]
                for review in ["reviewRequests", "reviews"]
            ):
                raise Exception(
                    "The current implementation for the merge tool does not support nested pagination."
                    " Can not process pull requests with more than 100 reviews."
                )

            def collect_authors(input: Dict[str, Any]) -> List[str]:
                """
                flatten and order by most files changes
                """
                flat = [
                    (
                        f"{author['name']} <{author['email']}>",
                        commit["commit"]["changedFiles"],
                    )
                    for commit in input["nodes"]
                    for author in commit["commit"]["authors"]["nodes"]
                ]
                grouped = groupby(sorted(flat), lambda x: x[0])
                ordered = sorted(
                    [
                        (email, sum([changes for email, changes in y]))
                        for email, y in grouped
                    ],
                    key=lambda x: -x[1],
                )
                return [x for x, y in ordered]

            return cls(
                id=pull_request_data["id"],
                number=pull_request_data["number"],
                title=pull_request_data["title"],
                body=pull_request_data["body"],
                requires_review=not bool(pull_request_data["viewerDidAuthor"]),
                second_stage=(
                    pull_request_data["viewerDidAuthor"]
                    # This condition excludes pull requests created for branches aligned with the original PR's target branch.
                    # This is fine since these pull requests will be handled atomically with the original PR so they don't
                    # really fit the term second stage anyway.
                    and pull_request_data["headRefName"].startswith(BRANCH_PREFIX)
                ),
                author=Author(
                    **pull_request_data["author"],
                    bot=pull_request_data["author"]["__typename"] == "Bot",
                    permission=get_user_permission(
                        pull_request_data["repository"]["name"],
                        pull_request_data["author"]["login"],
                        token,
                    ),
                ),
                authors=collect_authors(pull_request_data["authors"]),
                repository=Repository(
                    id=pull_request_data["repository"]["id"],
                    name=pull_request_data["repository"]["name"],
                    ready_label_id=pull_request_data["repository"]["label"]["id"],
                ),
                source=pull_request_data["headRefName"],
                target=pull_request_data["baseRefName"],
                mergeable=pull_request_data["mergeable"],
                state=(
                    pull_request_data["commits"]["nodes"][0]["commit"]["status"][
                        "state"
                    ]
                    if pull_request_data["commits"]["nodes"][0]["commit"]["status"]
                    is not None
                    else None
                ),
                review_decision=pull_request_data["reviewDecision"],
                reviewers_requested={
                    subnode["requestedReviewer"]["login"]
                    for subnode in pull_request_data["reviewRequests"]["nodes"]
                },
                reviewers_approved={
                    subnode["author"]["login"]
                    for subnode in pull_request_data["reviews"]["nodes"]
                },
                bot_responsibles=bot_responsibles,
                token=token,
            )
        except pydantic.ValidationError as e:
            raise Exception(
                "Error while parsing GitHub API response: data does not match expected schema: %s"
                % e
            )
        except KeyError as e:
            raise Exception(
                "Error while parsing GitHub API response, expected data not present in response: %s"
                % e
            )

    def get_equivalent_pull_requests(self) -> Iterator["MergeToolPullRequest"]:
        """
        Returns an iterator over all pull requests on the same repo with the same source branch.
        """
        return (
            pr
            for pr in get_merge_tool_pull_request(
                [self.repository.name],
                self._bot_responsibles,
                self.token,
                additional_search=f"head:{self.source}",
            )
            # filter out this pull request
            if pr.target != self.target
        )

    def open_sibling(
        self,
        *,
        target: str,
        source: Optional[str] = None,
    ) -> None:
        """
        Opens a second stage pull request for this one and adds the merge-tool-ready label
        """
        open_pull_request(
            repository=self.repository.name,
            target=target,
            source=source if source is not None else self.source,
            title=f"{self.title} (#{self.number})",
            message=f"Pull request opened by the merge tool on behalf of #{self.number}",
            token=self.token,
        )

    def comment(self, message: str) -> None:
        mutation: str = """
            addComment(
                input: {
                    subjectId: "%s"
                    body: "%s"
                }
            ) {
                clientMutationId
            }
        """ % (
            sanitize_string(self.id),
            sanitize_string(message),
        )
        api_mutation(mutation, self.token)

    def close(self, message: str) -> None:
        self.comment(message)
        mutation: str = """
            closePullRequest(
                input: {
                    pullRequestId: "%s"
                }
            ) {
                clientMutationId
            }
        """ % (
            sanitize_string(self.id),
        )
        api_mutation(mutation, self.token)

    def reject(self, message: str) -> None:
        """
        Reject a pull request:
            - reopen it if closed
            - remove the merge-tool-ready label
            - assign it to the author of the original pull request
        """
        LOGGER.debug(f"Pull request {self} rejected with message: {message}")

        def get_user_id(login: str) -> str:
            query: str = 'user(login: "%s") { id }' % sanitize_string(login)
            data: Dict = api_query(query, self.token)
            try:
                return data["user"]["id"]
            except KeyError as e:
                raise Exception(
                    "Failed to fetch user information for %s, expected data not present in response: %s"
                    % (login, e)
                )

        author: Author = self.get_original_pull_request().author
        assignees: List[str] = (
            [author.id]
            if not author.bot
            else [get_user_id(user) for user in self._bot_responsibles]
        )

        mutation: str = """
            reopenPullRequest(
                input: {
                    pullRequestId: "%(pr_id)s"
                }
            ) {
                clientMutationId
            }

            removeLabelsFromLabelable(
                input: {
                    labelIds: ["%(label_id)s"]
                    labelableId: "%(pr_id)s"
                }
            ) {
                clientMutationId
            }

            addAssigneesToAssignable(
                input: {
                    assignableId: "%(pr_id)s"
                    assigneeIds: [%(assignees)s]
                }
            ) {
                clientMutationId
            }
        """ % {
            "pr_id": sanitize_string(self.id),
            "label_id": sanitize_string(self.repository.ready_label_id),
            "assignees": ", ".join(
                f'"{sanitize_string(assignee)}"' for assignee in assignees
            ),
        }
        api_mutation(mutation, self.token)

        self.comment(message)

    def __str__(self) -> str:
        return f"inmanta/{self.repository.name}#{self.number}"


def open_pull_request(
    repository: str,
    target: str,
    source: str,
    title: str,
    message: str,
    token: str,
) -> None:
    """
    Opens pull request with the merge-tool-ready label.
    """
    query: str = """
        repository(
            name: "%s"
            owner: "inmanta"
        ) {
            id
            label(name: "%s") {
                id
            }
        }
    """ % (
        sanitize_string(repository),
        READY_LABEL,
    )
    data = api_query(query, token)
    repository_id: str
    label_id: str
    try:
        repository_id = data["repository"]["id"]
        label_id = data["repository"]["label"]["id"]
    except KeyError as e:
        raise Exception(
            "Error while parsing GitHub API response: expected data not present in response: %s"
            % e
        )
    create_pr_mutation: str = """
        createPullRequest(
            input: {
                baseRefName: "%s"
                body: "%s"
                draft: false
                headRefName: "%s"
                repositoryId: "%s"
                title: "%s"
            }
        ) {
            pullRequest {
                id
            }
        }
    """ % (
        sanitize_string(target),
        sanitize_string(message),
        sanitize_string(source),
        sanitize_string(repository_id),
        sanitize_string(title),
    )
    new_pr_id: str
    try:
        data = api_mutation(create_pr_mutation, token)
        new_pr_id = pydantic.parse_obj_as(
            str, data["createPullRequest"]["pullRequest"]["id"]
        )
    except KeyError as e:
        raise Exception(
            "Error while parsing GitHub API response: expected data not present in response: %s"
            % e
        )
    except pydantic.ValidationError as e:
        raise Exception(
            "Error while parsing GitHub API response: data does not match expected schema: %s"
            % e
        )

    label_mutation: str = """
        addLabelsToLabelable(
            input: {
                labelIds: ["%s"]
                labelableId: "%s"
            }
        ) {
            clientMutationId
        }
    """ % (
        sanitize_string(label_id),
        sanitize_string(new_pr_id),
    )
    api_mutation(label_mutation, token)


def get_pull_request_by_number(
    repository: str, pr_number: int, bot_responsibles: Iterable[str], token: str
) -> MergeToolPullRequest:
    """
    Returns the pull request with the given number on the given repo.
    """
    try:
        query: str = """
            repository(
                name: "%s",
                owner: "%s",
            ) {
                pullRequest(number: %d) { %s }
            }
        """ % (
            sanitize_string(repository),
            sanitize_string(ORGANIZATION),
            pr_number,
            MergeToolPullRequest.get_subquery(),
        )
        data: Dict = api_query(query, token)
        return MergeToolPullRequest.from_query_response(
            data["repository"]["pullRequest"], bot_responsibles, token
        )
    except KeyError as e:
        raise Exception(
            "Failed to fetch pull requests, expected data not present in response: %s"
            % e
        )


def get_pull_requests_by_source(
    repository: str, source: str, bot_responsibles: Iterable[str], token: str
) -> Iterator[MergeToolPullRequest]:
    return search_pull_requests(
        [repository], bot_responsibles, token, search=f"head:{source}"
    )


def get_ready_pull_request(
    repositories: List[str], bot_responsibles: Iterable[str], token: str
) -> Optional[MergeToolPullRequest]:
    """
    Returns a single pull request that's ready to be processed by the merge tool, if such a pull request exists.
    """
    pull_requests: Iterator[MergeToolPullRequest] = get_merge_tool_pull_request(
        repositories, bot_responsibles, token
    )
    for pull_request in pull_requests:
        if pull_request.mergeable == Mergeable.UNKNOWN:
            # The mergeability of the pull request is still being calculated
            continue
        if pull_request.state is None or pull_request.state in {
            CommitState.EXPECTED,
            CommitState.PENDING,
        }:
            # The tests are still running for this pull request
            continue
        return pull_request
    return None


def get_merge_tool_pull_request(
    repositories: List[str],
    bot_responsibles: Iterable[str],
    token: str,
    additional_search: str = "",
) -> Iterator[MergeToolPullRequest]:
    """
    Returns an iterator over all open pull requests with the merge-tool-ready label that have been approved.
    """
    return search_pull_requests(
        repositories,
        bot_responsibles,
        token,
        search=(
            "label:%s %s"
            % (
                READY_LABEL,
                additional_search,
            )
        ),
    )


def search_pull_requests(
    repositories: List[str],
    bot_responsibles: Iterable[str],
    token: str,
    search: str = "",
    end_cursor: Optional[str] = None,
) -> Iterator[MergeToolPullRequest]:
    """
    Returns an iterator over all open pull requests that match the given search.
    """
    if len(repositories) == 0:
        raise ValueError("At least one repository must be supplied")

    LOGGER.debug(f"Fetching pull requests with {READY_LABEL} label via the GitHub API")
    query: str = """
        search(
            query: "%s is:pr state:open %s"
            type: ISSUE
            first: 10%s
        ) {
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                ... on PullRequest { %s }
            }
        }
    """ % (
        sanitize_string(" ".join(f"repo:inmanta/{repo}" for repo in repositories)),
        sanitize_string(search),
        "" if end_cursor is None else f', after: "{sanitize_string(end_cursor)}"',
        MergeToolPullRequest.get_subquery(),
    )
    data: Dict = api_query(query, token)
    try:
        yield from (
            MergeToolPullRequest.from_query_response(node, bot_responsibles, token)
            for node in data["search"]["nodes"]
        )
        if data["search"]["pageInfo"]["hasNextPage"]:
            yield from search_pull_requests(
                repositories, token, data["search"]["pageInfo"]["endCursor"]
            )
    except KeyError as e:
        raise Exception(
            "Failed to fetch pull requests, expected data not present in response: %s"
            % e
        )


def get_user_permission(
    repository: str,
    user_login: str,
    token: str,
) -> Optional[RepositoryPermission]:
    """
    Returns a user's permissions on a repository.
    """

    def search_user(end_cursor: Optional[str] = None) -> Iterator:
        LOGGER.debug(f"Fetching user permission for {user_login} via the GitHub API")
        query: str = """
            repository(
                name: "%s"
                owner: "%s"
            ) {
                collaborators(
                    query: "%s"
                    first: 10%s
                ) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges {
                        permission
                        node {
                            login
                        }
                    }
                }
            }
        """ % (
            sanitize_string(repository),
            sanitize_string(ORGANIZATION),
            sanitize_string(user_login),
            "" if end_cursor is None else f', after: "{sanitize_string(end_cursor)}"',
        )
        data: Dict = api_query(query, token)
        yield from data["repository"]["collaborators"]["edges"]
        if data["repository"]["collaborators"]["pageInfo"]["hasNextPage"]:
            yield from search_user(
                data["repository"]["collaborators"]["pageInfo"]["endCursor"]
            )

    try:
        # search_user returns partial matches on multiple user fields so additional filtering is required
        return next(
            pydantic.parse_obj_as(RepositoryPermission, user["permission"])
            for user in search_user()
            if user["node"]["login"] == user_login
        )
    except StopIteration:
        return None
    except KeyError as e:
        raise Exception(
            "Failed to fetch user permissions, expected data not present in response: %s"
            % e
        )
    except pydantic.ValidationError as e:
        raise Exception(
            "Error while parsing GitHub API response: data does not match expected schema: %s"
            % e
        )


def sanitize_string(string: str) -> str:
    return string.replace('"', '\\"')


class QueryType(Enum):
    QUERY: str = "query"
    MUTATION: str = "mutation"


def api_query(query: str, token: str, query_type: QueryType = QueryType.QUERY) -> Dict:
    """
    Queries the GitHub API and returns the result as a dictionary.
    """
    response: requests.Response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={"query": "%s { %s }" % (query_type.value, query)},
    )
    if response.status_code != 200:
        raise Exception(
            "GitHub API query failed: got response code %s: %s"
            % (response.status_code, response.text)
        )
    data = response.json()
    if "errors" in data:
        raise Exception(
            "GitHub API query failed: got errors in response: %s" % (data["errors"])
        )
    if "data" not in data:
        raise Exception("GitHub API query failed: no response data")
    return data["data"]


def api_mutation(mutation: str, token: str) -> Dict:
    """
    Performs mutation on the GitHub API and returns the result as a dictionary.
    """
    return api_query(mutation, token, query_type=QueryType.MUTATION)
