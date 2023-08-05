"""
    Copyright 2020 Inmanta

    Contact: code@inmanta.com
"""
import logging
import subprocess
from typing import Iterable, List

LOGGER = logging.getLogger(__name__)


class LabelUpdate:
    def __init__(self, repository: str, type: str, message: str) -> None:
        self.repository = repository
        self.type = type
        self.message = message

    def __str__(self) -> str:
        return f"[{self.repository}] {self.type}: {self.message}"


def __generate_diff(repository: str, output: str) -> Iterable[LabelUpdate]:
    for line in output.split("\n"):
        if ">" in line:
            parts = line.strip().split(" ")
            yield LabelUpdate(repository, parts[1][:-1], " ".join(parts[2:]))


def __github_label_sync(
    labels_path: str,
    repositories: List[str],
    github_access_token: str,
    dry_run=False,
    delete_additionals=True,
) -> Iterable[LabelUpdate]:
    for repository in repositories:
        LOGGER.debug(f"Checking out {repository}")
        args = [
            "npx",
            "--quiet",
            "github-label-sync",
            "--labels",
            labels_path,
            "--access-token",
            github_access_token,
        ]
        if dry_run:
            args.append("--dry-run")
        if not delete_additionals:
            args.append("--allow-added-labels")
        args.append(repository)
        result = subprocess.run(args=args, check=True, stdout=subprocess.PIPE)
        for update in __generate_diff(repository, result.stdout.decode("utf-8")):
            yield update


def dry_run(
    labels_path: str,
    repositories: List[str],
    github_access_token: str,
    delete_additionals=True,
) -> Iterable[LabelUpdate]:
    """Perform a dry run to identify which labels in a list of repositories should be changed

    :param labels_path: The path to the labels file containing the label to sync
    :param repositories: The repositories on which sync the labels
    :param github_access_token: The token to use to interact with Github api
    :param delete_additionals: Whether additional labels in repositories should be considered
    :return: An iterable of updates to apply to the different repositories provided
    """
    for update in __github_label_sync(
        labels_path,
        repositories,
        github_access_token,
        dry_run=True,
        delete_additionals=delete_additionals,
    ):
        yield update


def sync(
    labels_path: str,
    repositories: List[str],
    github_access_token: str,
    delete_additionals=True,
) -> Iterable[LabelUpdate]:
    """Perform a sync on the given repositories, after this operation, all missing labels will
    be present on the repository

    :param labels_path: The path to the labels file containing the label to sync
    :param repositories: The repositories on which sync the labels
    :param github_access_token: The token to use to interact with Github api
    :param delete_additionals: Whether to delete labels not present in the the model
        which are present in the repository. Defaults to True.
    :return: An iterable of updates to apply to the different repositories provided
    """
    for update in __github_label_sync(
        labels_path,
        repositories,
        github_access_token,
        dry_run=False,
        delete_additionals=delete_additionals,
    ):
        yield update
