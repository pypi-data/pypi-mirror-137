"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import json
import logging
import os
import shutil
import subprocess
import sys
import urllib.parse
from typing import Callable, Dict, List, Mapping, Optional, TypeVar, Union

LOGGER = logging.getLogger(__name__)


class Pip:
    """
    A pip instance in a specific venv

    Used to enforce a uniform configuration
    """

    def __init__(self, python_path: str, index_url: str = None, pre: bool = False):
        self.python_path = python_path
        self.index_url = index_url
        self.pre = pre

    def set_env_vars(self, into: Mapping[str, str] = None):
        if into is None:
            into = os.environ
        if self.index_url:
            into["PIP_INDEX_URL"] = self.index_url
        if self.pre:
            into["PIP_PRE"] = "true"
        else:
            if "PIP_PRE" in into:
                del into["PIP_PRE"]

    def install(
        self,
        pkg: Union[str, List[str]] = [],
        requires_files: Union[str, List[str]] = [],
        update: bool = False,
        develop: bool = False,
        constraint_files: Union[str, List[str]] = [],
    ):
        if not isinstance(pkg, List):
            pkg = [pkg]
        if not isinstance(requires_files, List):
            requires_files = [requires_files]
        if not isinstance(constraint_files, List):
            constraint_files = [constraint_files]

        arguments = pkg + [item for r_file in requires_files for item in ("-r", r_file)]

        if not arguments:
            # nothing to install
            return

        pip_install(
            self.python_path,
            arguments,
            update,
            develop,
            self.pre,
            constraint_files,
            self.index_url,
        )

    def list(self) -> List[Dict[str, str]]:
        """
        perform pip list, return as list of dicts (as per pip list --format=json)

        expected keys are "name" and "version"
        """
        output = subprocess_log(
            subprocess.check_output,
            [self.python_path, "-m", "pip", "list", "--format=json"],
        )
        lines = output.decode()
        return json.loads(lines)


def pip_install(
    python_path: str,
    pkg: Union[str, List[str]],
    update: bool = False,
    develop: bool = False,
    pre: bool = False,
    constraint_files: List[str] = [],
    index_url: str = None,
):
    LOGGER.info(
        "pip install %s update=%s, develop=%s, constraints=%s",
        pkg,
        update,
        develop,
        constraint_files,
    )
    cmd = [python_path, "-m", "pip", "install"]
    for f in constraint_files:
        cmd.extend(["-c", f])
    if update:
        cmd.append("-U")
    if develop:
        cmd.append("-e")
    if pre:
        cmd.append("--pre")
    if index_url:
        cmd.extend(["-i", index_url])

    if isinstance(pkg, list):
        cmd.extend(pkg)
    else:
        cmd.append(pkg)

    subprocess_log(
        subprocess.check_call,
        cmd,
        logger=LOGGER,
    )


def ensure_tmp_env(temp_dir: str, python_binary: str = sys.executable) -> str:
    env_dir = os.path.join(temp_dir, "env")
    LOGGER.info("Init venv in %s", env_dir)
    subprocess.check_output([python_binary, "-m", "venv", env_dir])
    python_path = os.path.join(env_dir, "bin", os.path.basename(python_binary))
    subprocess.check_output([python_path, "-m", "pip", "install", "-U", "pip"])
    return python_path


def get_version_python_project(path_python_project: str) -> str:
    cmd = [sys.executable, "setup.py", "-V"]
    return subprocess.check_output(cmd, cwd=path_python_project).decode("utf-8").strip()


def get_name_python_project(path_python_project: str) -> str:
    cmd = [sys.executable, "setup.py", "--name"]
    return subprocess.check_output(cmd, cwd=path_python_project).decode("utf-8").strip()


def get_git_repo_name_for_url(git_url: str) -> str:
    repo_name = git_url.strip().rsplit("/", maxsplit=1)[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[0:-4]
    return repo_name


def get_branch(project_dir: str) -> str:
    cmd = ["git", "branch", "--show-current"]
    result = subprocess_log(
        subprocess.check_output, cmd, logger=LOGGER, cwd=project_dir, encoding="utf-8"
    )
    return result.strip()


def clone_repo(
    url: str, directory: str, branch: str = "master", token: Optional[str] = None
):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    url = add_userinfo_to_url(url, password=token) if "@" not in url else url
    result = subprocess_log(
        subprocess.check_output,
        ["git", "clone", "--branch", branch, url, directory],
        logger=LOGGER,
    )
    return result


def clone_multiple_repos(
    repos: Dict[str, str], output_dir: str, token: Optional[str] = None, branch="master"
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    result = {}
    for repo_name, url in repos.items():
        repo_dir = os.path.join(output_dir, repo_name)
        clone_repo(url, repo_dir, branch, token=token)
        result[repo_name] = repo_dir
    return result


def add_userinfo_to_url(
    url: str, username: Optional[str] = None, password: Optional[str] = None
) -> str:
    if "@" in url:
        return url
    if username is None and password is None:
        return url
    parts = list(urllib.parse.urlsplit(url))
    if username and password:
        user_info = f"{username}:{password}"
    elif username:
        user_info = username
    else:
        user_info = password
    parts[1] = f"{user_info}@{parts[1]}"
    return urllib.parse.urlunsplit(parts)


def ensure_empty_dir(path_to_dir: str) -> None:
    if os.path.exists(path_to_dir):
        shutil.rmtree(path_to_dir)
    os.mkdir(path_to_dir)


def ensure_dir(dir_path: str):
    """
    Make sure the directory exists
    """
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


T = TypeVar("T")


def subprocess_log(
    subprocess_f: Callable[..., T],
    cmd: Union[str, List[str]],
    logger: Optional[logging.Logger] = None,
    **kwargs: object,
) -> T:
    if logger is None:
        logger = LOGGER
    command_log: str
    if isinstance(cmd, str):
        command_log = f"Running command: {cmd}"
    else:
        command_log = f"Running command: {' '.join(cmd)}"
    env_log: str = "" if "env" not in kwargs else f" (with env vars: {kwargs['env']} )"
    logger.debug(f"{command_log}{env_log}")
    return subprocess_f(cmd, **kwargs)


def install_requirements_for_dir(
    python_path: str, directory: str, index_url: Optional[str] = None
) -> None:
    """
    Install the dependencies in the requirements.txt and the requirements.dev.txt if these files exist in `directory`.
    """
    requirements_txt = os.path.join(directory, "requirements.txt")
    requirements_dev_txt = os.path.join(directory, "requirements.dev.txt")
    constraint_files = [
        f for f in [requirements_txt, requirements_dev_txt] if os.path.isfile(f)
    ]
    if constraint_files:
        LOGGER.info("Installing requirements: %s", constraint_files)
        cmd_install_reqs = [python_path, "-m", "pip", "install", "--pre"]
        if index_url:
            cmd_install_reqs.extend(["-i", index_url])
        for f in constraint_files:
            cmd_install_reqs.extend(["-r", f])
        subprocess_log(subprocess.check_call, cmd_install_reqs, logger=LOGGER)


def get_requirements_files(directory: str) -> List[str]:
    result = []
    for file_name in ["requirements.txt", "requirements.dev.txt"]:
        path_req_file = os.path.join(directory, file_name)
        if os.path.exists(path_req_file):
            result.append(path_req_file)
    return result
