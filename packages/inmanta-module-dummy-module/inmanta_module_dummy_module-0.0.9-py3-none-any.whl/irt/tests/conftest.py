"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
import shutil
import tempfile
from typing import Any, Callable, Dict, Iterator, List, Optional

import click.testing
import pytest
import yaml

import irt.credentials
import irt.main
import irt.module_sources
import irt.modules
import irt.util
from irt.module_sources import legacy_config
from irt.modules import InstallMode, ModuleSetDefinition

# content of conftest.py


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


class TempfileTestHelper:
    def __init__(self):
        self.dir: str = tempfile.mkdtemp()

    def cleanup(self):
        shutil.rmtree(self.dir)


class ModuleSourcesManager(TempfileTestHelper):
    def __init__(self):
        super().__init__()
        self.source_github: str = "github_inmanta"
        self.source_gitlab: str = "gitlab_inmanta"
        self.source_gitlab_solutions: str = "gitlab_solutions"

        def save_source_file(
            source_name: str,
            command: Callable,
            required_env_var: str,
            additional_args: List[str] = [],
        ) -> None:
            assert (
                os.environ.get(required_env_var, "") != ""
            ), f"{required_env_var} environment variable needs to be set for these tests to succeed."
            source_file = os.path.join(self.dir, f"{source_name}.yml")
            args = additional_args + ["--save", source_file]
            result = click.testing.CliRunner().invoke(
                command, args, catch_exceptions=False
            )
            assert result.exit_code == 0, result.stdout
            assert os.path.exists(source_file)

        save_source_file(
            self.source_github,
            irt.main.list_repos,
            "GITHUB_TOKEN",
            additional_args=["--org", legacy_config[self.source_github].organisation],
        )
        save_source_file(
            self.source_gitlab,
            irt.main.list_gitlab_repos,
            "GITLAB_TOKEN",
            additional_args=["--group", legacy_config[self.source_gitlab].group],
        )
        save_source_file(
            self.source_gitlab_solutions,
            irt.main.list_gitlab_repos,
            "GITLAB_TOKEN",
            additional_args=[
                "--group",
                legacy_config[self.source_gitlab_solutions].group,
            ],
        )

    def get_legacy_manager(self) -> irt.module_sources.ModuleSourceManager:
        return irt.module_sources.ModuleSourceManager(
            self.dir,
            legacy_config,
            irt.credentials.FromEnvCredentialStore(),
        )


class ModuleSetManager(TempfileTestHelper):
    def __init__(
        self, sources_manager: ModuleSourcesManager, product_package: str = "inmanta"
    ):
        super().__init__()
        self.sources_manager: ModuleSourcesManager = sources_manager
        self.product_package: str = product_package
        self._module_set_file: str = os.path.join(self.dir, "test_module_set.yml")
        with open(self._module_set_file, "w") as fd:
            yaml.dump(
                {
                    "name": "test_module_set",
                    "modules": [],
                    "module_sources": [
                        self.sources_manager.source_github,
                        self.sources_manager.source_gitlab,
                    ],
                },
                fd,
            )
        self.modules_dir: str = os.path.join(self.dir, "modules")
        self.install_mode: InstallMode = InstallMode.release

    def use_module_set_file(
        self, module_set_file: str, exclude_sections: Optional[List[str]] = None
    ) -> None:
        shutil.copyfile(module_set_file, self._module_set_file)
        if exclude_sections is None:
            return
        content: Dict[str, object] = self.load_module_set_file()
        with open(self._module_set_file, "w") as fd:
            yaml.dump(
                {
                    key: value
                    for key, value in content.items()
                    if key not in exclude_sections
                },
                fd,
            )

    def load_module_set_file(self) -> Dict[str, Any]:
        with open(self._module_set_file, "r") as fd:
            return yaml.safe_load(fd)

    def get_modules(self) -> List[str]:
        return self.load_module_set_file()["modules"]

    def set_modules(self, modules: List[str]) -> None:
        content: Dict[str, object] = self.load_module_set_file()
        content["modules"] = modules
        with open(self._module_set_file, "w") as fd:
            yaml.dump(content, fd)

    def download_set(self, python_path: Optional[str] = None):
        with tempfile.TemporaryDirectory() as tmpdir:
            if python_path is None:
                python_path = irt.util.ensure_tmp_env(tmpdir)
                irt.util.pip_install(
                    python_path,
                    [self.product_package],
                    pre=True,
                    index_url="https://artifacts.internal.inmanta.com/inmanta/dev",
                )
            irt.modules.download_set(
                python_path,
                ModuleSetDefinition.from_file(self._module_set_file),
                self.sources_manager.get_legacy_manager(),
                self.modules_dir,
                self.install_mode,
                pip_index_url="https://artifacts.internal.inmanta.com/inmanta/dev",
            )


@pytest.fixture(scope="session")
def module_sources() -> Iterator[ModuleSourcesManager]:
    result: ModuleSourcesManager = ModuleSourcesManager()
    yield result
    result.cleanup()


@pytest.fixture
def module_set(module_sources) -> Iterator[ModuleSetManager]:
    result: ModuleSetManager = ModuleSetManager(module_sources)
    yield result
    result.cleanup()


@pytest.fixture
def iso_module_set(module_sources) -> Iterator[ModuleSetManager]:
    result: ModuleSetManager = ModuleSetManager(
        module_sources, product_package="inmanta-service-orchestrator"
    )
    yield result
    result.cleanup()


@pytest.fixture(scope="session")
def dummy_product_repo() -> str:
    return "https://github.com/inmanta/dummy-inmanta-product.git"


@pytest.fixture(scope="session")
def dummy_extension_a_repo() -> str:
    return "https://github.com/inmanta/dummy-inmanta-extension-a.git"


@pytest.fixture(scope="session")
def github_token() -> str:
    return os.environ["GITHUB_TOKEN"]


@pytest.fixture(scope="function", autouse=True)
def restore_cwd() -> None:
    """
    Restore the current working directory.
    """
    cwd = os.getcwd()
    yield
    os.chdir(cwd)
