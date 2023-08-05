"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
from typing import List, Tuple

import py
import pytest
from packaging.version import Version

from irt.version import Bumpversion, ChangeType, Yarn


def test_change_type() -> None:
    assert ChangeType.MAJOR.value == "major"
    assert ChangeType.MINOR.value == "minor"
    assert ChangeType.PATCH.value == "patch"

    assert ChangeType.MAJOR.less() == ChangeType.MINOR
    assert ChangeType.MINOR.less() == ChangeType.PATCH
    assert ChangeType.PATCH.less() is None

    assert ChangeType.PATCH < ChangeType.MINOR < ChangeType.MAJOR
    assert ChangeType.MAJOR > ChangeType.MINOR > ChangeType.PATCH


def test_change_type_diff() -> None:
    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("2.0.0")) == ChangeType.MAJOR
    )
    assert (
        ChangeType.diff(low=Version("1.0.1"), high=Version("2.0.0")) == ChangeType.MAJOR
    )
    assert (
        ChangeType.diff(low=Version("1.0.1"), high=Version("2.0.1")) == ChangeType.MAJOR
    )
    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("3.0.0")) == ChangeType.MAJOR
    )

    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("1.1.0")) == ChangeType.MINOR
    )
    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("1.2.0")) == ChangeType.MINOR
    )
    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("1.3.1")) == ChangeType.MINOR
    )

    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("1.0.1")) == ChangeType.PATCH
    )
    assert (
        ChangeType.diff(low=Version("1.0.0"), high=Version("1.0.2")) == ChangeType.PATCH
    )

    assert ChangeType.diff(low=Version("1.0.0"), high=Version("1.0.0")) is None

    with pytest.raises(ValueError):
        ChangeType.diff(low=Version("2.0.0"), high=Version("1.0.0"))
    with pytest.raises(ValueError):
        ChangeType.diff(low=Version("1.0.0.dev0"), high=Version("2.0.0.dev0"))
    with pytest.raises(ValueError):
        ChangeType.diff(low=Version("1.0.0"), high=Version("2.0.0.dev0"))


def test_bumpversion(tmpdir: py.path.local) -> None:
    def files(version: str) -> List[Tuple[str, str]]:
        return [
            ("version.txt", f"version = {version}"),
            (
                ".bumpversion.cfg",
                f"""
[bumpversion]
current_version = {version}

[bumpversion:file:version.txt]
search = version = {{current_version}}
replace = version = {{new_version}}
                """.strip(),
            ),
        ]

    for file, content in files("1.1.1"):
        with open(os.path.join(str(tmpdir), file), "w+") as f:
            f.write(content)
    bumpversion: Bumpversion = Bumpversion(str(tmpdir))
    assert bumpversion.get_version() == Version("1.1.1")
    bumpversion.bump(ChangeType.MINOR)
    assert bumpversion.get_version() == Version("1.2.0")
    for file, content in files("1.2.0"):
        with open(os.path.join(str(tmpdir), file), "r") as f:
            assert f.read().strip() == content

    # test this twice to account for a bug in bumpversion (c4urself/bump2version#214)
    for i in range(2):
        bumpversion.set_version(Version("0.1.2"))
        for file, content in files("0.1.2"):
            with open(os.path.join(str(tmpdir), file), "r") as f:
                assert f.read().strip() == content


def test_yarn(tmpdir: py.path.local) -> None:
    with open(os.path.join(str(tmpdir), "package.json"), "w+") as f:
        f.write(
            """
{
    "name": "test",
    "version": "1.1.1"
}
            """.strip()
        )
    yarn: Yarn = Yarn(str(tmpdir))
    assert yarn.get_version() == Version("1.1.1")
    yarn.bump(ChangeType.MINOR)
    assert yarn.get_version() == Version("1.2.0")
    yarn.set_version(Version("0.1.2"))
    assert yarn.get_version() == Version("0.1.2")
