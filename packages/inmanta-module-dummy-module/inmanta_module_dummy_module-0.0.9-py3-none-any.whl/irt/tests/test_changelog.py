"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
import tempfile
from datetime import date
from typing import Any, Dict, List, Optional

import py
import pydantic
import pytest
from packaging.version import Version

from irt.changelog import (
    ChangeEntry,
    Changelog,
    ChangelogSection,
    ComposedChangelog,
    parse_change_entry,
)
from irt.version import ChangeType


def test_changelog_section() -> None:
    assert ChangelogSection.FEATURE.value == "feature"
    assert ChangelogSection.BUGFIX.value == "bugfix"
    assert ChangelogSection.KNOWN_ISSUE.value == "known-issue"
    assert ChangelogSection.UPGRADE_NOTE.value == "upgrade-note"
    assert ChangelogSection.DEPRECATION_NOTE.value == "deprecation-note"
    assert ChangelogSection.OTHER_NOTE.value == "other-note"


def test_change_entry_parse(tmpdir: py.path.local) -> None:
    my_file: str = os.path.join(str(tmpdir), "change.yml")
    description: str = "This is a dummy change"
    issue_nr: int = 1
    issue_repo: str = "irt"
    change_type: str = "minor"
    feature: str = "No new feature was added"
    with open(my_file, "w+") as f:
        f.write(
            f"""
description: {description}
issue-nr: {issue_nr}
issue-repo: {issue_repo}
change-type: {change_type}
sections:
    feature: {feature}
    other-note: "{{{{description}}}}"
destination-branches:
    - master
    - iso4
            """
        )
    entry: ChangeEntry = parse_change_entry(my_file)
    assert entry.description == description
    assert entry.issue_nr == issue_nr
    assert entry.issue_repo == issue_repo
    assert entry.change_type == ChangeType(change_type)
    assert entry.sections == {
        ChangelogSection.FEATURE: feature,
        ChangelogSection.OTHER_NOTE: description,
    }
    assert entry.destination_branches == ["master", "iso4"]


def test_change_entry_required_fields() -> None:
    schema: Dict = ChangeEntry.schema()
    # issue-nr, issue-repo and sections are optional, all other fields are required
    assert set(schema["required"]) == set(schema["properties"].keys()).difference(
        {"issue-nr", "issue-repo", "sections"}
    )


def test_change_entry_write(tmpdir: py.path.local) -> None:
    entry: ChangeEntry = ChangeEntry(
        description="my description",
        change_type=ChangeType.PATCH,
        sections={ChangelogSection.KNOWN_ISSUE: "my section body"},
        destination_branches=["master", "iso4"],
    )
    expected: str = """
change-type: patch
description: my description
destination-branches:
- master
- iso4
sections:
    known-issue: my section body
    """.strip()

    my_file: str = os.path.join(str(tmpdir), "change.yml")
    assert not os.path.isfile(my_file)
    entry.write(my_file)
    assert os.path.isfile(my_file)
    with open(my_file, "r") as f:
        assert f.read().strip() == expected


def test_change_entry_issue_repo_validation() -> None:
    with pytest.raises(
        pydantic.ValidationError, match="Can't set issue-repo without setting issue-nr"
    ):
        ChangeEntry(
            description="my description",
            change_type=ChangeType.PATCH,
            destination_branches=["master", "iso4"],
            issue_repo="irt",
        )


@pytest.mark.parametrize(
    "additional_change_entry_args, expected_issue_reference",
    [
        ({}, None),
        ({"issue_nr": 123}, "#123"),
        ({"issue_nr": 123, "issue_repo": "test-repo"}, "inmanta/test-repo#123"),
    ],
)
def test_change_entry_get_issue_reference(
    additional_change_entry_args: Dict[str, str],
    expected_issue_reference: Optional[str],
) -> None:
    """
    Test the get_issue_reference() method of the ChangeEntry class.
    """
    change_entry = ChangeEntry(
        description="my description",
        change_type=ChangeType.PATCH,
        destination_branches=["master"],
        **additional_change_entry_args,
    )
    assert change_entry.get_issue_reference() == expected_issue_reference


@pytest.mark.parametrize(
    "additional_change_entry_args, expected_issue_reference",
    [
        ({}, None),
        ({"issue_nr": 123}, "#123"),
        ({"issue_nr": 123, "issue_repo": "test-repo"}, "inmanta/test-repo#123"),
    ],
)
def test_change_entry_get_messages_for_changelog_file(
    additional_change_entry_args: Dict[str, str],
    expected_issue_reference: Optional[str],
) -> None:
    """
    Test the get_messages_for_changelog_file() method of the ChangeEntry class.
    """
    change_entry = ChangeEntry(
        description="my description",
        change_type=ChangeType.PATCH,
        destination_branches=["master"],
        sections={ChangelogSection.BUGFIX: "A certain bugfix"},
        **additional_change_entry_args,
    )
    change_messages_dct = change_entry.get_messages_for_changelog_file()
    assert len(change_messages_dct) == 1
    assert ChangelogSection.BUGFIX in change_messages_dct
    if expected_issue_reference:
        assert (
            change_messages_dct[ChangelogSection.BUGFIX]
            == f"A certain bugfix (Issue {expected_issue_reference})"
        )
    else:
        assert change_messages_dct[ChangelogSection.BUGFIX] == "A certain bugfix"


def test_changelog_section_get_title_for_changelog_file() -> None:
    """
    Ensure test `ChangelogSection.get_title_for_changelog_file()` works for each
    ChangelogSection instance.
    """
    changelog_section: ChangelogSection
    for changelog_section in ChangelogSection:
        # This should not raise an Exception
        changelog_section.get_section_title_for_changelog_file()


def test_changelog_section_get_sections_ordered() -> None:
    """
    Ensure that `ChangelogSection.get_sections_ordered()` returns
    a list that contains an item for each constant in the ChangelogSection enum.
    """
    assert len({elem for elem in ChangelogSection}) == len(
        ChangelogSection.get_sections_ordered()
    )


@pytest.mark.parametrize("version", ("unreleased", "1.2.3"))
def test_changelog_get_version(tmpdir: py.path.local, version: str) -> None:
    changelog_dir: py.path.local = tmpdir.mkdir(version)
    assert Changelog("myproject", str(changelog_dir)).get_version() == (
        None if version == "unreleased" else Version(version)
    )
    ChangeEntry(
        description="Description change entry 1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4", "iso3"],
        sections={ChangelogSection.BUGFIX: "A certain bugfix"},
    ).write(os.path.join(changelog_dir, "change_entry_1.yml"))


def test_changelog(tmpdir: py.path.local) -> None:
    """
    Verify the behavior of the has_change_entries() and has_changelog_messages() methods.
    """
    changelog_dir: py.path.local = tmpdir.mkdir("unreleased")

    def verify(has_change_entries: bool, has_change_messages: bool) -> None:
        changelog = Changelog("myproject", str(changelog_dir))
        assert changelog.has_change_entries() == has_change_entries
        assert changelog.has_changelog_messages() == has_change_messages

    assert len(os.listdir(changelog_dir)) == 0
    verify(has_change_entries=False, has_change_messages=False)
    ChangeEntry(
        description="Description change entry 1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4", "iso3"],
    ).write(os.path.join(changelog_dir, "change_entry_1.yml"))
    assert len(os.listdir(changelog_dir)) == 1
    verify(has_change_entries=True, has_change_messages=False)

    ChangeEntry(
        description="Description change entry 2",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4", "iso3"],
        sections={ChangelogSection.BUGFIX: "A certain bugfix"},
    ).write(os.path.join(changelog_dir, "change_entry_2.yml"))
    assert len(os.listdir(changelog_dir)) == 2
    verify(has_change_entries=True, has_change_messages=True)


@pytest.mark.parametrize(
    "change_types, result",
    [
        ([], None),
        ([ChangeType.PATCH, ChangeType.PATCH], ChangeType.PATCH),
        ([ChangeType.PATCH, ChangeType.MINOR, ChangeType.PATCH], ChangeType.MINOR),
        (
            [ChangeType.PATCH, ChangeType.MINOR, ChangeType.MAJOR, ChangeType.PATCH],
            ChangeType.MAJOR,
        ),
    ],
)
def test_changelog_get_change_type(
    tmpdir: py.path.local, change_types: List[ChangeType], result: Optional[ChangeType]
) -> None:
    changelog_dir: py.path.local = tmpdir.mkdir("unreleased")
    for i, change_type in enumerate(change_types):
        ChangeEntry(
            description=f"Description change entry {i}",
            change_type=change_type,
            destination_branches=["master", "iso4", "iso3"],
        ).write(os.path.join(changelog_dir, f"change_entry_{i}.yml"))
    assert Changelog("myproject", str(changelog_dir)).get_change_type() == result


def test_changelog_release(tmpdir: py.path.local) -> None:
    changelog_dir: py.path.local = tmpdir.mkdir("unreleased")
    change_entries: List[ChangeEntry] = [
        ChangeEntry(
            description=f"Description change entry {i}",
            change_type=ChangeType.PATCH,
            destination_branches=["master", "iso4", "iso3"],
        )
        for i in range(5)
    ]
    for i, change_entry in enumerate(change_entries):
        change_entry.write(os.path.join(changelog_dir, f"change_entry_{i}.yml"))
    with open(os.path.join(changelog_dir, ".gitkeep"), "w"):
        pass
    assert os.listdir(tmpdir) == ["unreleased"]
    assert len(os.listdir(changelog_dir)) == 6
    unreleased: Changelog = Changelog("myproject", str(changelog_dir))
    assert unreleased.entries == change_entries
    version: str = "1.2.3"
    unreleased.release(Version(version))
    assert sorted(os.listdir(tmpdir)) == sorted([version, "unreleased"])
    assert os.listdir(changelog_dir) == [".gitkeep"]
    assert len(os.listdir(os.path.join(tmpdir, version))) == 5
    released: Changelog = Changelog("myproject", os.path.join(tmpdir, version))
    assert released.entries == change_entries


def _write_changelog_entry(output_file: str, **kwargs: Any) -> None:
    change_entry = ChangeEntry(**kwargs)
    change_entry.write(output_file)


def _get_changelog_dir_name(version: Optional[str]):
    """
    Return the name of the subdirectory in the ./changelogs
    directory for this version of a product or component. The
    version should be provided in <major>.<minor>.<patch> format.
    """
    if version is None:
        return "unreleased"
    else:
        return version


def _get_version_part_of_title(version: Optional[str]) -> str:
    """
    Return the part of the changelog title that indicates
    the version of the product or component.The version
    should be provided in <major>.<minor>.<patch> format.
    """
    if version is None:
        return "unreleased changes"
    else:
        return f"release {version}"


def _assert_changelog(
    changelog: ComposedChangelog,
    expected_changelog: str,
    output_file: Optional[str] = None,
) -> None:
    """
    Assert whether the given `changelog` produces the changelog file in `expected_changelog`.

    :param output_file: If provided, this method will write the `changelog` to `output_file`.
                        This file will not be removed at the end of this method.
    """

    def do_assert_changelog(fd):
        fd.seek(0, 0)
        actual_changelog = fd.read()
        try:
            assert expected_changelog == actual_changelog
        except AssertionError as e:
            print("Actual changelog:")
            print(actual_changelog, end="")
            print("=================")
            print("Expected changelog:")
            print(expected_changelog, end="")
            print("=================")
            raise e

    if output_file:
        changelog.write(output_file)
        with open(output_file, "r", encoding="utf-8") as fd:
            do_assert_changelog(fd)
    else:
        with tempfile.NamedTemporaryFile(mode="r", encoding="utf-8") as fd:
            changelog.write(fd.name)
            do_assert_changelog(fd)


@pytest.mark.parametrize(
    "product_version, core_version, ext1_version, ext2_version, ui1_version, ui2_version",
    [
        (None, None, None, None, None, None),
        ("1.0.0", "2.0.0", "1.1.1", "1.0.5", "3.2.1", "1.2.1"),
    ],
)
def test_composed_changelog_product_has_changelog_messages(
    tmpdir,
    product_version: Optional[str],
    core_version: Optional[str],
    ext1_version: Optional[str],
    ext2_version: Optional[str],
    ui1_version: Optional[str],
    ui2_version: Optional[str],
) -> None:
    product_changelog_dir = os.path.join(
        tmpdir, "product", _get_changelog_dir_name(product_version)
    )
    core_changelog_dir = os.path.join(
        tmpdir, "core", _get_changelog_dir_name(core_version)
    )
    ext_1_changelog_dir = os.path.join(
        tmpdir, "ext_1", _get_changelog_dir_name(ext1_version)
    )
    ext_2_changelog_dir = os.path.join(
        tmpdir, "ext_2", _get_changelog_dir_name(ext2_version)
    )
    ui_1_changelog_dir = os.path.join(
        tmpdir, "ui_1", _get_changelog_dir_name(ui1_version)
    )
    ui_2_changelog_dir = os.path.join(
        tmpdir, "ui_2", _get_changelog_dir_name(ui2_version)
    )

    for directory in [
        product_changelog_dir,
        core_changelog_dir,
        ext_1_changelog_dir,
        ext_2_changelog_dir,
        ui_1_changelog_dir,
        ui_2_changelog_dir,
    ]:
        os.makedirs(directory)

    # Changelog entries product
    _write_changelog_entry(
        os.path.join(product_changelog_dir, "change_entry_1.yml"),
        description="Description change entry 1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4", "iso3"],
        sections={
            ChangelogSection.BUGFIX: "A certain bugfix",
            ChangelogSection.UPGRADE_NOTE: "A general upgrade note",
        },
    )
    _write_changelog_entry(
        os.path.join(product_changelog_dir, "change_entry_2.yml"),
        description="Description change entry 2",
        change_type=ChangeType.MINOR,
        destination_branches=["master", "iso4"],
        sections={
            ChangelogSection.FEATURE: "A new feature",
            ChangelogSection.DEPRECATION_NOTE: "Something has been deprecated",
        },
        issue_nr=1423,
    )

    # Changelog entries core
    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="A change to core",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        sections={ChangelogSection.BUGFIX: "Bugfix in core"},
        issue_nr=123,
        issue_repo="a-repo",
    )

    # Changelog entries ext_1
    _write_changelog_entry(
        os.path.join(ext_1_changelog_dir, "change_entry_1.yml"),
        description="A change to extension1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        sections={ChangelogSection.FEATURE: "ext1 feature"},
        issue_nr=345,
    )

    # Changelog entries ext_2
    _write_changelog_entry(
        os.path.join(ext_2_changelog_dir, "change_entry_1.yml"),
        description="Bugfix ext2",
        change_type=ChangeType.PATCH,
        sections={ChangelogSection.BUGFIX: "A bugfix"},
        destination_branches=["master", "iso4"],
        issue_nr=670,
    )
    _write_changelog_entry(
        os.path.join(ext_2_changelog_dir, "change_entry_2.yml"),
        description="Feature ext2",
        change_type=ChangeType.MAJOR,
        destination_branches=["master"],
        sections={
            ChangelogSection.FEATURE: "New feature",
            ChangelogSection.UPGRADE_NOTE: "Another upgrade note",
        },
        issue_nr=666,
        issue_repo="another-repo",
    )

    # Changelog entries ui_1
    _write_changelog_entry(
        os.path.join(ui_1_changelog_dir, "change_entry_1.yml"),
        description="Bugfix ui_1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        issue_nr=678,
        issue_repo="a-repo",
    )

    # Changelog entries ui_2
    _write_changelog_entry(
        os.path.join(ui_2_changelog_dir, "change_entry_1.yml"),
        description="Bugfix ui_2",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        issue_nr=679,
        issue_repo="a-repo",
    )
    _write_changelog_entry(
        os.path.join(ui_2_changelog_dir, "change_entry_2.yml"),
        description="Feature  ui_2",
        change_type=ChangeType.PATCH,
        destination_branches=["master"],
        sections={
            ChangelogSection.BUGFIX: "Another bugfix",
            ChangelogSection.OTHER_NOTE: "Some note",
        },
        issue_nr=888,
    )

    release_date = date.today().isoformat()
    expected_changelog = f"""# {_get_version_part_of_title(product_version).capitalize()} ({release_date})

## General changes

### New features

- A new feature (Issue #1423)

### Upgrade notes

- A general upgrade note
- Ensure the database is backed up before executing an upgrade.

### Deprecation notes

- Something has been deprecated (Issue #1423)

### Bug fixes

- A certain bugfix

## Inmanta-core: {_get_version_part_of_title(core_version)} ({release_date})

### Bug fixes

- Bugfix in core (Issue inmanta/a-repo#123)

## Ext1: {_get_version_part_of_title(ext1_version)} ({release_date})

### New features

- ext1 feature (Issue #345)

## Ext2: {_get_version_part_of_title(ext2_version)} ({release_date})

### New features

- New feature (Issue inmanta/another-repo#666)

### Upgrade notes

- Another upgrade note (Issue inmanta/another-repo#666)

### Bug fixes

- A bugfix (Issue #670)

## Ui1: {_get_version_part_of_title(ui1_version)} ({release_date})

No changelog entries.

## Ui2: {_get_version_part_of_title(ui2_version)} ({release_date})

### Bug fixes

- Another bugfix (Issue #888)

### Other notes

- Some note (Issue #888)
"""

    composed_changelog = ComposedChangelog(
        product_name="inmanta-service-orchestrator",
        product_changelog=Changelog(
            "inmanta-service-orchestrator", product_changelog_dir
        ),
        core_changelog=Changelog("inmanta-core", core_changelog_dir),
        extension_changelogs=[
            Changelog("ext1", ext_1_changelog_dir),
            Changelog("ext2", ext_2_changelog_dir),
        ],
        ui_changelogs=[
            Changelog("ui1", ui_1_changelog_dir),
            Changelog("ui2", ui_2_changelog_dir),
        ],
    )

    _assert_changelog(composed_changelog, expected_changelog)


@pytest.mark.parametrize(
    "product_version, core_version",
    [
        (None, None),
        ("1.0.0", "2.0.0"),
    ],
)
def test_composed_changelog_product_no_upgrade_notes(
    tmpdir,
    product_version: Optional[str],
    core_version: Optional[str],
) -> None:
    """
    Verify that the default notice for upgrade notes will be added to the changelogs
    even if there are no other upgrade notes changelogs. (issue #240)
    """
    product_changelog_dir = os.path.join(
        tmpdir, "product", _get_changelog_dir_name(product_version)
    )
    core_changelog_dir = os.path.join(
        tmpdir, "core", _get_changelog_dir_name(core_version)
    )
    for directory in [
        product_changelog_dir,
        core_changelog_dir,
    ]:
        os.makedirs(directory)

    # Changelog entries product
    _write_changelog_entry(
        os.path.join(product_changelog_dir, "change_entry_1.yml"),
        description="Description change entry 1",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4", "iso3"],
        sections={
            ChangelogSection.BUGFIX: "A certain bugfix",
        },
    )
    _write_changelog_entry(
        os.path.join(product_changelog_dir, "change_entry_2.yml"),
        description="Description change entry 2",
        change_type=ChangeType.MINOR,
        destination_branches=["master", "iso4"],
        sections={
            ChangelogSection.FEATURE: "A new feature",
            ChangelogSection.DEPRECATION_NOTE: "Something has been deprecated",
        },
        issue_nr=1423,
    )

    # Changelog entries core
    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="A change to core",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        sections={ChangelogSection.BUGFIX: "Bugfix in core"},
        issue_nr=123,
        issue_repo="a-repo",
    )

    release_date = date.today().isoformat()
    expected_changelog = f"""# {_get_version_part_of_title(product_version).capitalize()} ({release_date})

## General changes

### New features

- A new feature (Issue #1423)

### Upgrade notes

- Ensure the database is backed up before executing an upgrade.

### Deprecation notes

- Something has been deprecated (Issue #1423)

### Bug fixes

- A certain bugfix

## Inmanta-core: {_get_version_part_of_title(core_version)} ({release_date})

### Bug fixes

- Bugfix in core (Issue inmanta/a-repo#123)
"""

    composed_changelog = ComposedChangelog(
        product_name="inmanta-service-orchestrator",
        product_changelog=Changelog(
            "inmanta-service-orchestrator", product_changelog_dir
        ),
        core_changelog=Changelog("inmanta-core", core_changelog_dir),
    )

    _assert_changelog(composed_changelog, expected_changelog)


@pytest.mark.parametrize(
    "product_version, core_version",
    [(None, None), ("1.0.0", "2.0.0")],
)
def test_composed_changelog_no_changelog_messages(
    tmpdir,
    product_version: Optional[str],
    core_version: Optional[str],
) -> None:
    product_changelog_dir = os.path.join(
        tmpdir, "product", _get_changelog_dir_name(product_version)
    )
    core_changelog_dir = os.path.join(
        tmpdir, "core", _get_changelog_dir_name(core_version)
    )
    for directory in [product_changelog_dir, core_changelog_dir]:
        os.makedirs(directory)

    # Changelog entries core
    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="A change to core",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        issue_nr=123,
        issue_repo="a-repo",
    )

    release_date = date.today().isoformat()
    expected_changelog = f"""# {_get_version_part_of_title(product_version).capitalize()} ({release_date})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: {_get_version_part_of_title(core_version)} ({release_date})

No changelog entries.
"""

    composed_changelog = ComposedChangelog(
        product_name="inmanta",
        product_changelog=Changelog("inmanta", product_changelog_dir),
        core_changelog=Changelog("inmanta-core", core_changelog_dir),
        extension_changelogs=[],
        ui_changelogs=[],
    )
    _assert_changelog(composed_changelog, expected_changelog)


@pytest.mark.parametrize(
    "product_version, core_version",
    [(None, None), ("1.0.0", "2.0.0")],
)
def test_composed_changelog_no_changelogs_dir_in_product_repo(
    tmpdir,
    product_version: Optional[str],
    core_version: Optional[str],
) -> None:
    core_changelog_dir = os.path.join(
        tmpdir, "core", _get_changelog_dir_name(core_version)
    )
    os.makedirs(core_changelog_dir)

    # Changelog entries core
    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="A change to core",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        issue_nr=123,
        issue_repo="a-repo",
    )

    release_date = date.today().isoformat()
    expected_changelog = f"""# {_get_version_part_of_title(product_version).capitalize()} ({release_date})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: {_get_version_part_of_title(core_version)} ({release_date})

No changelog entries.
"""

    composed_changelog = ComposedChangelog(
        product_name="inmanta",
        product_version=product_version,
        core_changelog=Changelog("inmanta-core", core_changelog_dir),
        extension_changelogs=[],
        ui_changelogs=[],
    )
    _assert_changelog(composed_changelog, expected_changelog)


def test_composed_changelog_file_already_exists(tmpdir) -> None:
    """
    Ensure that new content for a changelog file is correctly prefixed to an
    already existing changelog file.
    """
    product_changelog_dir = os.path.join(tmpdir, "product", "unreleased")
    core_changelog_dir = os.path.join(tmpdir, "core", "unreleased")
    for directory in [product_changelog_dir, core_changelog_dir]:
        os.makedirs(directory)

    def _assert_expected_changelog_file(expected_changelog: str) -> None:
        path_rendered_changelog = os.path.join(tmpdir, "changelog.md")
        composed_changelog = ComposedChangelog(
            product_name="inmanta",
            product_changelog=Changelog("inmanta", product_changelog_dir),
            core_changelog=Changelog("inmanta-core", core_changelog_dir),
            extension_changelogs=[],
            ui_changelogs=[],
        )
        _assert_changelog(
            composed_changelog, expected_changelog, output_file=path_rendered_changelog
        )

    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="Implemented new feature",
        change_type=ChangeType.MAJOR,
        sections={ChangelogSection.FEATURE: "{{description}}"},
        destination_branches=["master"],
        issue_nr=123,
    )

    release_date = date.today().isoformat()
    expected_changelog_part1 = f"""# Unreleased changes ({release_date})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: unreleased changes ({release_date})

### New features

- Implemented new feature (Issue #123)
"""
    _assert_expected_changelog_file(expected_changelog_part1)

    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_2.yml"),
        description="Fix a bug",
        change_type=ChangeType.PATCH,
        sections={ChangelogSection.BUGFIX: "{{description}}"},
        destination_branches=["master"],
        issue_nr=124,
    )

    _assert_expected_changelog_file(
        f"""# Unreleased changes ({release_date})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: unreleased changes ({release_date})

### New features

- Implemented new feature (Issue #123)

### Bug fixes

- Fix a bug (Issue #124)


{expected_changelog_part1}"""
    )


def test_composed_changelog_no_changes(tmpdir) -> None:
    unreleased_dir = os.path.join(tmpdir, "unreleased")
    os.mkdir(unreleased_dir)
    composed_changelog = ComposedChangelog(
        product_name="inmanta",
        product_changelog=Changelog(
            project_name="inmanta", dir_with_changelog_files=unreleased_dir
        ),
        core_changelog=Changelog(
            project_name="inmanta-core", dir_with_changelog_files=unreleased_dir
        ),
        extension_changelogs=[
            Changelog(
                project_name="inmanta-lsm", dir_with_changelog_files=unreleased_dir
            ),
        ],
        ui_changelogs=[
            Changelog(
                project_name="web-console", dir_with_changelog_files=unreleased_dir
            ),
        ],
    )

    release_date = date.today().isoformat()
    _assert_changelog(
        changelog=composed_changelog,
        expected_changelog=f"""# Unreleased changes ({release_date})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: unreleased changes ({release_date})

No changelog entries.

## Inmanta-lsm: unreleased changes ({release_date})

No changelog entries.

## Web-console: unreleased changes ({release_date})

No changelog entries.
""",
    )


@pytest.mark.parametrize(
    "product_version, core_version",
    [(None, None), ("1.0.0", "2.0.0")],
)
def test_custom_release_date(
    tmpdir,
    product_version: Optional[str],
    core_version: Optional[str],
) -> None:
    product_changelog_dir = os.path.join(
        tmpdir, "product", _get_changelog_dir_name(product_version)
    )
    core_changelog_dir = os.path.join(
        tmpdir, "core", _get_changelog_dir_name(core_version)
    )
    for directory in [product_changelog_dir, core_changelog_dir]:
        os.makedirs(directory)

    # Changelog entries core
    _write_changelog_entry(
        os.path.join(core_changelog_dir, "change_entry_1.yml"),
        description="A change to core",
        change_type=ChangeType.PATCH,
        destination_branches=["master", "iso4"],
        issue_nr=123,
        issue_repo="a-repo",
    )

    custom_release_date = date(2020, 1, 2)
    expected_changelog = f"""# {_get_version_part_of_title(product_version).capitalize()} ({date.today().isoformat()})

## Upgrade notes

- Ensure the database is backed up before executing an upgrade.

## Inmanta-core: {_get_version_part_of_title(core_version)} ({custom_release_date})

No changelog entries.
"""

    composed_changelog = ComposedChangelog(
        product_name="inmanta",
        product_changelog=Changelog("inmanta", product_changelog_dir),
        core_changelog=Changelog(
            "inmanta-core", core_changelog_dir, release_date=custom_release_date
        ),
        extension_changelogs=[],
        ui_changelogs=[],
    )
    _assert_changelog(composed_changelog, expected_changelog)
