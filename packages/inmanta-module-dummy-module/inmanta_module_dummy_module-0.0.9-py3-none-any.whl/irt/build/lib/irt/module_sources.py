"""
    :copyright: 2021 Inmanta
    :contact: code@inmanta.com

    This file contains all functionality related to discovering modules from remote git provides.

"""
import base64
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Tuple, Union

from irt.credentials import CredentialStore

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

import github
import gitlab
import pydantic
import yaml
from github.Repository import Repository
from gitlab.v4.objects import GroupProject

LOGGER = logging.getLogger(__name__)
MODULE_FILE = "module.yml"


class SkipModule(Exception):
    """
    If this exception is raised during module collection, the module is not included.
    """


class ModuleData(TypedDict, total=False):
    """
    Meta data about a module
    """

    public: bool
    repo_name: str
    url: str
    name: str
    license: str
    version: str

    token: str
    username: str


class ModuleSourceFile(TypedDict):
    """A file containing meta data about Modules, used as a cache"""

    time: str
    """ When this file was created """

    modules: Dict[str, ModuleData]


class ModuleSourceConfigBase(pydantic.BaseModel, ABC):
    """
    Config for a specific target, base class
    """

    type: str
    """ type distinguisher field """
    output: str
    """ file to store the output in, relative to module source folder """

    @abstractmethod
    def get_source(self) -> "ModuleSource":
        """Convert the config into an actual module source"""
        raise NotImplementedError()


class GitlabConfig(ModuleSourceConfigBase):

    type: Literal["gitlab"]
    group: str
    """ the group to search in"""

    def get_source(self) -> "ModuleSource":
        return GitlabSource(self)


class GitHubConfig(ModuleSourceConfigBase):
    type: Literal["github"]
    organisation: str
    """ the github organisation to list """

    def get_source(self) -> "ModuleSource":
        return GitHubModuleSource(self)


ModuleSourceConfig = Union[GitlabConfig, GitHubConfig]
""" Union of all config types, intended to be used in pydantic objects """

legacy_config = {
    "github_inmanta": GitHubConfig(
        type="github",
        organisation="inmanta",
        output="github_inmanta.yaml",
    ),
    "gitlab_inmanta": GitlabConfig(
        type="gitlab",
        output="gitlab_inmanta.yml",
        group="BICS",
    ),
    "gitlab_solutions": GitlabConfig(
        type="gitlab",
        output="gitlab_solutions.yml",
        group="solutions/modules",
    ),
}


class ModuleSource(ABC):
    """A class capable of discovering module from a specific source"""

    @abstractmethod
    def list_modules(self, credentials: CredentialStore) -> Dict[str, ModuleData]:
        """Using the credentials, list all modules"""
        raise NotImplementedError()

    def load_into(
        self, credentials: CredentialStore, cached_file: str
    ) -> Dict[str, ModuleData]:
        """load the modules and cache into the given file"""
        data = self.list_modules(credentials)
        LOGGER.info("Saving module list file to %s", cached_file)
        modules: ModuleSourceFile = {
            "time": str(datetime.now()),
            "modules": data,
        }
        with open(cached_file, "w+") as fd:
            yaml.dump(modules, fd, default_flow_style=False)
        return data

    def add_module_info(
        self, name: str, info: ModuleData, module_def: Dict[str, str]
    ) -> str:
        """load module info from a module.yaml file into a ModuleData structure"""

        info["name"] = module_def["name"] if "name" in module_def else None
        info["license"] = module_def["license"] if "license" in module_def else None
        info["version"] = module_def["version"] if "version" in module_def else None

        if info["repo_name"] != info["name"]:
            LOGGER.warning(
                "Module %s has a different repo (%s) and module (%s) name",
                name,
                info["repo_name"],
                info["name"],
            )
        return info["name"]


class GitlabSource(ModuleSource):
    def __init__(self, config: GitlabConfig) -> None:
        self.config = config

    def list_modules(self, credentials: CredentialStore) -> Dict[str, ModuleData]:
        LOGGER.debug("Finding module repositories for %s", self.config.output)

        my_credentials = credentials.get_credentials_for("gitlab")
        assert (
            my_credentials is not None
        ), "Please provide credentials for gitlab (code.inmanta.com)"

        gl = gitlab.Gitlab(
            "https://code.inmanta.com", private_token=my_credentials.password
        )
        gitlab_group = gl.groups.get(self.config.group)
        projects = gitlab_group.projects.list(all=True)

        data: Dict[str, ModuleData] = {}
        for project in projects:
            try:
                module_yaml = gl.projects.get(project.id).files.get(
                    MODULE_FILE, "master"
                )
                content = yaml.safe_load(
                    base64.decodebytes(module_yaml.content.encode())
                )
                name, info = self._repo_info(project, content)
                data[name] = info
                if my_credentials.password is not None:
                    data[name]["token"] = my_credentials.password
                if my_credentials.username is not None:
                    data[name]["username"] = my_credentials.username
            except gitlab.GitlabError:
                LOGGER.debug("%s repo is not a module, ignoring", project.name)

        return data

    def _repo_info(
        self, repo: GroupProject, module_yaml: Dict
    ) -> Tuple[str, ModuleData]:
        info: ModuleData = {
            "public": repo.visibility == "public",
            "repo_name": repo.name,
            "url": repo.http_url_to_repo,
        }
        name = self.add_module_info(repo.name, info, module_yaml)
        return name, info


class GitHubModuleSource(ModuleSource):
    def __init__(self, config: GitHubConfig) -> None:
        self.config = config

    def list_modules(self, credentials: CredentialStore) -> Dict[str, ModuleData]:
        my_credentials = credentials.get_credentials_for("github")
        assert my_credentials is not None, "Please provide credentials for github"

        gh = github.Github(my_credentials.password)
        user = gh.get_organization(self.config.organisation)
        repos = user.get_repos()

        data: Dict[str, ModuleData] = {}
        for repo in repos:
            try:
                module_yaml = repo.get_contents(MODULE_FILE)
                content = yaml.safe_load(
                    base64.decodebytes(module_yaml.content.encode())
                )
                name, info = self._repo_info(repo, content)
                data[name] = info
                if my_credentials.password is not None:
                    data[name]["token"] = my_credentials.password
            except SkipModule:
                LOGGER.debug("Skipping %s", repo.full_name)
            except github.GithubException:
                LOGGER.debug("%s repo is not a module, ignoring", repo.full_name)

        return data

    def _repo_info(self, repo: Repository, module_yaml: Dict) -> Tuple[str, ModuleData]:
        if repo.archived:
            raise SkipModule()

        info: ModuleData = {
            "public": not repo.private,
            "repo_name": repo.name,
            "url": repo.clone_url,
        }
        name = self.add_module_info(repo.name, info, module_yaml)
        return name, info


class ModuleSourceManager:
    """Class to discover models from multiple sources"""

    def __init__(
        self,
        folder: str,
        sources: Dict[str, ModuleSourceConfig],
        credentials: CredentialStore,
    ) -> None:
        self.folder = folder
        self.sources = sources
        self.credentials = credentials

    def for_sources(self, sources: List[str]) -> "ModuleSourceManager":
        """
        Return a new ModuleSourceManager for a selected subset of the available sources
        :param sources: sources to select
        """
        return ModuleSourceManager(
            self.folder,
            {name: self.sources[name] for name in sources},
            self.credentials,
        )

    def get_modules(self) -> Dict[str, ModuleData]:
        """Get all modules, attempt to get from cache"""
        return {
            name: module
            for source_name, source in self.sources.items()
            for name, module in self._get_module_for(source).items()
        }

    def _get_module_for(self, source: ModuleSourceConfigBase) -> Dict[str, ModuleData]:
        cached_file = os.path.join(self.folder, source.output)
        if os.path.exists(cached_file):
            with open(cached_file, "r") as fh:
                file: ModuleSourceFile = yaml.safe_load(fh)
                return file["modules"]
        else:
            os.makedirs(self.folder, exist_ok=True)
            data = source.get_source().load_into(self.credentials, cached_file)
            return data
