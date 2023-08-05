"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
from typing import List

import pytest
import yaml
from conftest import ModuleSetManager


def test_download_set(module_set: ModuleSetManager) -> None:
    modules: List[str] = ["std", "ip", "net"]
    module_set.set_modules(modules)
    module_set.download_set()


@pytest.mark.parametrize(
    "version_constraint,downloaded_version",
    [("std~=0.21.0", "0.21.1"), ("std~=0.21", "0.26.3")],
)
def test_download_set_with_version_constraints(
    module_set: ModuleSetManager, version_constraint, downloaded_version
) -> None:
    modules: List[str] = [version_constraint]
    module_set.set_modules(modules)
    module_set.download_set()

    # Check whether correct version of module has been downloaded
    module_yml_file = os.path.join(module_set.modules_dir, "std", "module.yml")
    with open(module_yml_file, "r", encoding="utf-8") as fd:
        module_yml_content = yaml.safe_load(fd)
        assert module_yml_content["version"] == downloaded_version


def test_download_set_private_repo(iso_module_set: ModuleSetManager) -> None:
    modules: List[str] = ["lsm", "std"]
    iso_module_set.set_modules(modules)
    iso_module_set.download_set()


def test_download_set_unknown_repo(module_set: ModuleSetManager) -> None:
    module_set.set_modules(["nonexistent_module"])
    with pytest.raises(SystemExit) as e:
        module_set.download_set()
    assert e.value.code == 1


def test_download_set_gitlab_repo(module_set: ModuleSetManager) -> None:
    modules: List[str] = ["n5k_lan", "net", "std"]
    module_set.set_modules(modules)
    module_set.download_set()


def test_download_set_incomplete_message(module_set: ModuleSetManager, capsys) -> None:
    modules: List[str] = ["std", "ip"]
    module_set.set_modules(modules)
    with pytest.raises(SystemExit) as e:
        module_set.download_set()
    assert e.value.code == 1
    assert (
        "Incomplete module set. One or more modules in the set have a dependency on modules not in the set: {'net'}"
        in capsys.readouterr().err
    )
