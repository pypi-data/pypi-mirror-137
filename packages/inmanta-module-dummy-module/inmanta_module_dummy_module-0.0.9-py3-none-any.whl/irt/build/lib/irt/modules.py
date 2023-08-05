"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import enum
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict
from typing import Dict, List, Optional, Set, Tuple

import yaml
from pydantic import BaseModel, constr

import irt.module_sources
from irt import util
from irt.git import GitRepo
from irt.project import ProductConfig, ProductProject, PythonVersion
from irt.release import BuildType
from irt.util import Pip

LOGGER = logging.getLogger(__name__)

MODULE_FILE = "module.yml"


@enum.unique
class InstallMode(enum.Enum):
    release = "release"
    prerelease = "prerelease"
    master = "master"


class ModuleSetDefinition(BaseModel):
    class Config:
        underscore_attrs_are_private = True

    name: str
    modules: List[
        constr(
            regex=r"^(?P<name>[a-z0-9_\-]+)(?P<version_constraint>(\s*~=\s*[0-9]+\.[0-9]+(\.[0-9]+)?)?)$"
        )
    ]
    modules_filter: Dict[str, bool] = {}
    exclude: List[str] = []
    module_sources: List[str] = []
    extra_modules: Dict[str, List[str]] = {}

    # This field is not part of the model. Only used internally.
    _module_names: List[str]

    def __init__(self, **kwargs):
        super(ModuleSetDefinition, self).__init__(**kwargs)
        self.__set_module_names()

    def __set_module_names(self) -> None:
        """
        Initialize the _module_names variable
        """
        self._module_names = []
        for current_module in self.modules:
            if "~=" in current_module:
                module_name = current_module.split("~=")[0]
                self._module_names.append(module_name)
            else:
                self._module_names.append(current_module)

    def get_module_set(
        self, sources: Dict[str, "irt.module_sources.ModuleData"]
    ) -> Dict[str, "irt.module_sources.ModuleData"]:
        module_set = {}
        excludes_set = set(self.exclude)

        # First find listed modules
        for name in self._module_names:
            mod = sources.get(name, None)

            if mod is None:
                LOGGER.error("Unable to find module %s in module sources.", name)
                sys.exit(1)

            if name not in excludes_set:
                module_set[name] = mod

        # helper methods
        def filter_modules(
            sources: Dict[str, "irt.module_sources.ModuleData"],
            filters: Dict[str, bool],
        ) -> Dict[str, "irt.module_sources.ModuleData"]:
            matched = {}
            for module in sources.values():
                if module["name"] not in matched and match(module, filters):
                    matched[module["name"]] = module

            return matched

        def match(
            module: "irt.module_sources.ModuleData", filters: Dict[str, bool]
        ) -> bool:
            for key, value in filters.items():
                if key not in module:
                    return False

                if module[key] != value:
                    return False
            return True

        # Apply filters
        if self.modules_filter:
            mods = filter_modules(sources, self.modules_filter)
            for name, the_mod in mods.items():
                if name not in module_set and name not in excludes_set:
                    module_set[name] = the_mod
        return module_set

    @classmethod
    def from_file(cls, module_set_file: str) -> "ModuleSetDefinition":
        with open(module_set_file) as fd:
            set_def_dct = yaml.safe_load(fd)
            return ModuleSetDefinition(**set_def_dct)


def download_set(
    python_path: str,
    set_def: ModuleSetDefinition,
    sources: irt.module_sources.ModuleSourceManager,
    set_dir: str,
    install_mode: InstallMode = InstallMode.release,
    pip_index_url: Optional[str] = None,
    remote: Optional[str] = None,
) -> Dict[str, irt.module_sources.ModuleData]:
    """
    :param python_path: The python path for an environment where the appropriate inmanta product has been installed.
    :param set_def: modules set definition
    :param sources: sources to use to find modules
    :param set_dir: destination folder
    :param pip_index_url: The pip index to use for downloading module's dependencies.
    :param remote: override url for all downloads
    """
    LOGGER.info("Downloading modules in module set %s to %s", set_def.name, set_dir)

    # reduce sources to those in the set definition
    sources = sources.for_sources(set_def.module_sources)
    # list all available modules, from cache or discover
    modules = sources.get_modules()
    # apply the module set to the list of available modules
    modules = set_def.get_module_set(modules)

    LOGGER.info("Attempting to get modules [%s]", ",".join(modules.keys()))

    # remove all existing modules from target directory
    set_dir = os.path.abspath(set_dir)
    if os.path.exists(set_dir):
        shutil.rmtree(set_dir)
    os.makedirs(set_dir)

    tmp_dir: str = tempfile.mkdtemp()
    compiler_venv_dir = os.path.join(tmp_dir, ".env")

    if not remote:
        # Construct a list of remote location based on all known urls, add tokens
        def project_url(
            module_name: str,
            module_url: str,
            token: Optional[str],
            username: Optional[str],
        ) -> str:
            result: str = module_url.replace(f"{module_name}.git", "{}.git")
            return util.add_userinfo_to_url(result, username, token)

        repo_list = list(
            {
                project_url(
                    module["name"],
                    module["url"],
                    module.get("token", None),
                    module.get("username", None),
                )
                for module in modules.values()
            }
        )
    else:
        # override the remote
        if "{}" not in remote and "{0}" not in remote and not remote.endswith("/"):
            # Make sure that remote and with a slash. The module name will be appended
            # at the end by the compiler.
            remote = f"{remote}/"
        repo_list = [remote]

    LOGGER.info("Pulling from sources [%s]", ",".join(repo_list))

    with open(os.path.join(tmp_dir, "project.yml"), "w") as fd:
        project_yaml: Dict[str, object] = {
            "name": "temp-project",
            "modulepath": set_dir,
            "downloadpath": set_dir,
            "repo": repo_list,
            "install_mode": install_mode.value,
            "requires": [constraint for constraint in set_def.modules],
        }
        yaml.dump(project_yaml, fd)
    with open(os.path.join(tmp_dir, "main.cf"), "w") as fd:
        fd.write("\n".join(f"import {name}" for name in modules.keys()))

    # load project from a separate process with the appropriate venv to make sure no version conflicts can arise between the
    # modules' requirements and this project's internal dependencies
    script_path: str = os.path.join(tmp_dir, "load_inmanta_project.py")
    with open(script_path, "w") as fd:
        fd.write(
            f"""
from inmanta.module import Project

import logging
import sys

log_level = logging.DEBUG
log = logging.getLogger()
log.setLevel(log_level)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(log_level)
log.addHandler(stream)
logging.captureWarnings(True)

try:
  # 1. modules V2 requires explicit install
  # 2. Use a separate venv for the compiler to make sure that the inmanta product installed in python_path is not overridden.
  Project("{tmp_dir}", autostd=False, venv_path="{compiler_venv_dir}").load(install=True)
except TypeError:
  # We are running on an old version of inmanta-core that doesn't support V2 modules and still creates
  # a separate compiler venv by default.
  Project("{tmp_dir}", autostd=False).load()
            """.strip()
        )

    try:
        # download modules
        util.subprocess_log(
            subprocess.check_call,
            [python_path, script_path],
            logger=LOGGER,
            env={**os.environ, "PIP_INDEX_URL": pip_index_url}
            if pip_index_url is not None
            else None,
        )
        # Verify module set completeness.
        # Doing this in a test case is not sufficient because modules might get updated at any time.
        downloaded: Set[str] = set(os.listdir(set_dir))
        provided: Set[str] = set(modules.keys())
        if downloaded != provided:
            LOGGER.exception(
                "Incomplete module set. One or more modules in the set have a dependency on modules not in the set: %s",
                downloaded.difference(provided),
            )
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        LOGGER.exception(str(e))
        sys.exit(1)
    finally:
        shutil.rmtree(tmp_dir)
    return modules


def load_modules(
    module_set: str, source_dir: str
) -> Tuple[
    ModuleSetDefinition,
    Dict[str, irt.module_sources.ModuleData],
    Dict[str, irt.module_sources.ModuleSourceFile],
]:
    """
    Parses the module_set file and returns a tuple of the parsed object, the actual module data objects and the sources
    objects.

    to be phased out
    """
    set_def = ModuleSetDefinition.from_file(module_set)

    # Load module sources
    sources: Dict[str, irt.module_sources.ModuleSourceFile] = OrderedDict()
    for ms in set_def.module_sources:
        ms_file = os.path.join(source_dir, ms + ".yml")
        if not os.path.exists(ms_file):
            LOGGER.error(
                "Unable to find module source file %s (%s does not exist)."
                " Perhaps you should load it with `irt github-list` or `irt gitlab-list`.",
                ms,
                ms_file,
            )
            sys.exit(1)

        with open(ms_file, "r") as fd:
            sources[ms] = yaml.safe_load(fd)

    return (
        set_def,
        set_def.get_module_set(
            {
                module["name"]: module
                for source in sources.values()
                for module in source["modules"].values()
            }
        ),
        sources,
    )


def test_module_set(
    sources: irt.module_sources.ModuleSourceManager,
    product_repo: str,
    branch: str,
    build_type: BuildType,
    working_dir: str,
    github_token: str,
) -> None:
    product_config, python_path = install_product(
        branch, github_token, product_repo, build_type, working_dir
    )

    module_set_config = product_config.module_set

    venv_dir = os.path.dirname(os.path.dirname(python_path))
    pip = build_type.get_pip(python_path)
    pip.set_env_vars()

    install_pytest_inmanta_extensions(pip)

    # Create a snapshot of this venv as such that we can restore
    # before running the tests for a certain module.
    venv_snapshot_dir = os.path.join(working_dir, "venv_snapshot")
    shutil.copytree(venv_dir, venv_snapshot_dir)

    remote: Optional[str]
    if build_type.is_stable_release() and module_set_config.publish_repo is not None:
        # Checkout stable module releases from the location they were published to
        remote = module_set_config.publish_repo
    else:
        remote = None

    module_set, modules_dir, _ = download_module_set_for_product(
        python_path, working_dir, product_config, sources, github_token, remote
    )

    failed_flake = []
    failed_tests = []
    for module_name, module in module_set.items():
        module_path = os.path.join(modules_dir, module_name)

        # Get module version and git commit
        commit_hash = GitRepo(clone_dir=module_path).get_commit()[0:6]

        with open(os.path.join(module_path, "module.yml")) as fh:
            content = yaml.safe_load(fh)
            version = content["version"]

        # Print module name in box for readability
        info_string = f"{module_name} {version} {commit_hash}"
        LOGGER.info(
            "\n***%s***\n*** %s ***\n***%s***\n",
            "*" * (len(info_string) + 2),
            info_string,
            "*" * (len(info_string) + 2),
        )

        # Restore venv from snapshot
        shutil.rmtree(venv_dir)
        shutil.copytree(venv_snapshot_dir, venv_dir)
        # Install module dependencies
        LOGGER.info("Setup venv for tests of module %s", module_name)
        pip.install(pkg=[], requires_files=util.get_requirements_files(module_path))
        # Flake8 check
        success = _run_flake(python_path, module_name, module_path)
        if not success:
            failed_flake.append(module_name)

        # Run Tests
        success = _run_pytest(venv_dir, module_path, module_name, modules_dir)
        if not success:
            failed_tests.append(module_name)

        # module name at the end, to make it easy to find the results
        LOGGER.info(
            "\n+++ %s +++\n",
            info_string,
        )

    # For jenkins readability
    LOGGER.info("\n")
    LOGGER.info(("=" * 50) + " SUMMARY " + ("=" * 50))
    if not failed_tests and not failed_tests:
        LOGGER.info("All tests succeeded.")
    else:
        if failed_flake:
            LOGGER.info(
                "\nModules that did not pass flake8 linting:\n\t"
                + ", ".join(failed_flake)
            )
        if failed_tests:
            LOGGER.info("\nModules with failing tests:\n\t" + ", ".join(failed_tests))
        sys.exit(1)


def download_module_set_for_product(
    python_path: str,
    working_dir: str,
    product_config: ProductConfig,
    sources: irt.module_sources.ModuleSourceManager,
    github_token: str,
    remote: Optional[str] = None,
) -> Tuple[Dict[str, irt.module_sources.ModuleData], str, ModuleSetDefinition]:
    # Clone module set repository
    module_set_dir = os.path.join(working_dir, "module_set_repo")
    module_set_file = product_config.module_set.clone_module_set_repo(
        module_set_dir, token=github_token
    )
    module_set_defintion = ModuleSetDefinition.from_file(module_set_file)
    # Download modules
    modules_dir = os.path.join(working_dir, "modules")
    os.makedirs(modules_dir, exist_ok=True)
    module_set = download_set(
        python_path,
        module_set_defintion,
        sources,
        modules_dir,
        remote=remote,
    )
    return module_set, modules_dir, module_set_defintion


def install_pytest_inmanta_extensions(pip: Pip) -> None:
    """
    install pytest-inmanta-extensions to make sure it is matched with core

    The following table explains which python package is expected for each product install:

    | product | inmanta | inmanta-core | inmanta-service-orchestrator |
    |---------|---------|--------------|------------------------------|
    |  OSS    |   yes   |     yes      |             no               |
    |  ISO3   |   yes   |     no       |             yes              |
    |  ISO4+  |   no    |     yes      |             yes              |
    """
    lines = pip.list()
    version_lookup = {
        line["name"]: line["version"]
        for line in lines
        if line["name"].startswith("inmanta")
    }
    if (
        "inmanta-service-orchestrator" in version_lookup
        and "inmanta-core" in version_lookup
        and "inmanta" in version_lookup
    ):
        raise Exception(
            "The inmanta-core and the inmanta package cannot be installed simultaneously when "
            "running against the ISO product."
        )
    for core_package_name in ["inmanta-core", "inmanta"]:
        # This ensures that inmanta-core is used if it exists (any release except ISO3)
        # Otherwise inmanta is used (ISO3)
        if core_package_name in version_lookup:
            core_version = version_lookup[core_package_name]
            pip.install(
                f"{core_package_name}[pytest-inmanta-extensions]=={core_version}"
            )
            return


def _run_pytest(venv_path: str, module_path: str, module_name: str, repo: str) -> bool:
    """
    return true iff the tests finished successfully.
    """
    LOGGER.info("Running tests for: %s", module_name)
    python_path = os.path.join(venv_path, "bin", "python")
    tests = os.path.join(module_path, "tests")
    if os.path.isdir(tests):
        env = os.environ.copy()
        env["INMANTA_TEST_ENV"] = venv_path
        env["INMANTA_TEST_INFRA_SETUP"] = "true"
        if repo is not None:
            env["INMANTA_MODULE_REPO"] = repo
        pytest_stdout_log = os.path.join(module_path, "pytest-stdout.log")
        pytest_log = os.path.join(module_path, "pytest-log.log")

        process = util.subprocess_log(
            subprocess.Popen,
            [
                python_path,
                "-m",
                "pytest",
                "-vvv",
                "-s",
                f"--log-file={pytest_log}",
                "--log-file-level=DEBUG",
                tests,
            ],
            logger=LOGGER,
            cwd=module_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # Stream output to file and to stdout
        try:
            with open(pytest_stdout_log, "wb") as f:
                for line in iter(process.stdout.readline, b""):
                    print(line.decode(), end="", flush=True)
                    f.write(line)
        finally:
            # 1) Set the returncode.
            # 2) Ensure the process has terminated in case of an IOError
            process.communicate()

        if process.returncode != 0:
            LOGGER.error("Tests on module %s failed", module_name)
            return False
        else:
            LOGGER.info("Tests on module %s succeeded", module_name)

    else:
        LOGGER.warning("Module %s doesn't have any tests", module_name)

    return True


def _run_flake(python_path: str, module_name: str, module_path: str) -> bool:
    """
    return true iff the flake8 check was successful.
    """
    LOGGER.info("Checking code formatting for: %s", module_name)
    # Make sure flake8 is installed
    cmd = [
        python_path,
        "-m",
        "pip",
        "install",
        "flake8",
        "flake8-black",
        "flake8-isort",
        "flake8-copyright",
    ]
    completed_process = util.subprocess_log(
        subprocess.run,
        cmd,
        logger=LOGGER,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed_process.returncode:
        LOGGER.error(
            "Failed to install flake8 or one of it's requirements\n%s",
            completed_process.stdout,
        )

    lint_list = []
    if os.path.exists(os.path.join(module_path, "plugins")):
        lint_list.append(os.path.join(module_path, "plugins"))

    if os.path.exists(os.path.join(module_path, "tests")):
        lint_list.append(os.path.join(module_path, "tests"))

    if len(lint_list) > 0:
        cmd = [python_path, "-m", "flake8"]
        if not os.path.exists(os.path.join(module_path, "setup.cfg")):
            cmd.extend(
                [
                    "--ignore=H405,H404,H302,H306,H301,H101,E252,E203,F722,W503",
                    "--builtins=string,number,bool",
                    "--exclude=**/.env,.venv,.git,.tox,dist,doc,**egg",
                    "--max-line-length=128",
                    "--copyright-check",
                    "--copyright-author=Inmanta",
                ]
            )

        LOGGER.debug("Running style checker on %s", ", ".join(lint_list))
        completed_process = util.subprocess_log(
            subprocess.run,
            cmd + lint_list,
            logger=LOGGER,
            cwd=module_path,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed_process.returncode:
            LOGGER.error(
                "Style check failed for module %s\n%s",
                module_name,
                completed_process.stdout,
            )
            return False
        else:
            LOGGER.info("Style check succeeded for module %s", module_name)

    return True


def install_product(
    branch: str,
    github_token: str,
    product_repo: str,
    build_type: BuildType,
    working_dir: str,
) -> Tuple[ProductConfig, str]:
    if os.path.exists(working_dir) and os.listdir(working_dir):
        raise Exception(f"Working directory {working_dir} is not empty")

    # Clone product repository
    product_directory = os.path.join(working_dir, "product_repo")
    util.clone_repo(product_repo, product_directory, branch, github_token)
    product: ProductProject = ProductProject(product_directory)
    product_config: ProductConfig = product.get_project_config()

    # Install product (required for module download)
    LOGGER.info("Creating venv")
    python_version: Optional[PythonVersion] = product_config.build.rpm.python_version
    if python_version:
        python_binary = python_version.get_name_python_binary()
    else:
        python_binary = sys.executable
    python_path: str = util.ensure_tmp_env(working_dir, python_binary)
    product.install(
        python_path,
        working_dir,
        branch,
        build_type,
        github_token,
    )
    return product_config, python_path
