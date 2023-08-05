"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import enum
import json
import logging
import os
import shutil
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Dict, Iterator, List, Optional, Sequence

import pydantic
import yaml
from packaging.version import Version
from pydantic import BaseModel, Field, PositiveInt, validator

from irt import util
from irt.const import COMPILED_SEMVER_REGEX_STABLE_VERSION, GITKEEP_FILE
from irt.version import ChangeType

LOGGER = logging.getLogger(__name__)

CHANGE_ENTRIES_DIR: str = "unreleased"
CHANGE_ENTRIES_PATH: str = os.path.normpath(
    os.path.join("changelogs", CHANGE_ENTRIES_DIR)
)
RENDERED_CHANGELOG_FILE = "CHANGELOG.md"


@enum.unique
class ChangelogSection(str, Enum):
    FEATURE: str = "feature"
    BUGFIX: str = "bugfix"
    KNOWN_ISSUE: str = "known-issue"
    UPGRADE_NOTE: str = "upgrade-note"
    DEPRECATION_NOTE: str = "deprecation-note"
    OTHER_NOTE: str = "other-note"

    def get_section_title_for_changelog_file(self) -> str:
        """
        :return: The title that should be associated with this
                 changelog section in the rendered changelog file.
        """
        if self == ChangelogSection.FEATURE:
            return "New features"
        elif self == ChangelogSection.BUGFIX:
            return "Bug fixes"
        elif self == ChangelogSection.KNOWN_ISSUE:
            return "Known Issues"
        elif self == ChangelogSection.UPGRADE_NOTE:
            return "Upgrade notes"
        elif self == ChangelogSection.DEPRECATION_NOTE:
            return "Deprecation notes"
        elif self == ChangelogSection.OTHER_NOTE:
            return "Other notes"
        else:
            # A test case ensure that this cannot occur
            raise Exception(f"Unknown ChangelogSection {self.name}")

    @classmethod
    def get_sections_ordered(cls) -> List["ChangelogSection"]:
        """
        :return: A list of all ChangelogSection constants in the order in which
                  they should appear in the rendered changelog file.
        """
        return [
            cls.FEATURE,
            cls.KNOWN_ISSUE,
            cls.UPGRADE_NOTE,
            cls.DEPRECATION_NOTE,
            cls.BUGFIX,
            cls.OTHER_NOTE,
        ]


class ChangeEntry(BaseModel):
    """
    A structured representation of a change entry, specifying among others the type of the change in a SemVer context.
    """

    class Config:
        allow_population_by_field_name = True
        extra = "forbid"
        validate_assignment = True

    description: str
    issue_nr: Optional[PositiveInt] = Field(default=None, alias="issue-nr")
    issue_repo: Optional[str] = Field(alias="issue-repo", regex=r"^[a-zA-Z0-9-_]+$")
    change_type: ChangeType = Field(alias="change-type")
    sections: Dict[ChangelogSection, str] = Field(default={})
    destination_branches: List[str] = Field(min_items=1, alias="destination-branches")

    @validator("sections")
    @classmethod
    def section_message_format(
        cls, v: Dict[ChangelogSection, str], values: Dict[str, object]
    ) -> Dict[ChangelogSection, str]:
        return dict(
            (key, value.replace("{{description}}", values["description"]))  # type: ignore
            for key, value in v.items()
        )

    @validator("issue_repo")
    @classmethod
    def issue_repo_requires_nr(
        cls, v: Optional[str], values: Dict[str, object]
    ) -> Optional[str]:
        if v is not None and values["issue_nr"] is None:
            raise ValueError("Can't set issue-repo without setting issue-nr")
        return v

    def write(self, path: str) -> None:
        """
        Write this change entry to a file. The contents of the file will be overwritten.
        """
        with open(path, "w") as f:
            # Convert to json first to allow Python object serialization (for Enum values in this case)
            yaml.dump(
                json.loads(self.json(by_alias=True, exclude_none=True)), f, indent=4
            )

    def get_issue_reference(self) -> Optional[str]:
        """
        :return: When this ChangelogEntry define an issue number, this
                 method returns a reference to the issue according to the
                 GitHub issue reference syntax.
        """
        if not self.issue_nr:
            return None
        if self.issue_repo:
            return f"inmanta/{self.issue_repo}#{self.issue_nr}"
        else:
            return f"#{self.issue_nr}"

    def get_messages_for_changelog_file(self) -> Dict[ChangelogSection, str]:
        result = {}
        for section, content in self.sections.items():
            if self.get_issue_reference():
                result[section] = f"{content} (Issue {self.get_issue_reference()})"
            else:
                result[section] = content
        return result


def parse_change_entry(path: str) -> ChangeEntry:
    LOGGER.debug("parsing change entry at %s", path)
    if not path.endswith(".yml"):
        raise Exception(
            f"Invalid changelog entry file {path}. Changelog entry files should always end with a .yml extension."
        )
    with open(path, "r") as f:
        try:
            return ChangeEntry.parse_obj(yaml.safe_load(f))
        except yaml.YAMLError as e:
            LOGGER.error("Invalid yaml in change entry %s: %s", path, e)
            raise Exception("Invalid yaml in change entry %s: %s" % (path, e))
        except pydantic.ValidationError as e:
            LOGGER.error("Change entry %s does not match pydantic schema: %s", path, e)
            raise Exception(
                "Change entry %s does not match pydantic schema: %s" % (path, e)
            )


class ChangelogABC(ABC):
    def __init__(self, project_name: str) -> None:
        self.project_name: str = project_name

    @abstractmethod
    def get_rendered_changelog(self) -> str:
        """
        Returns a changelog file in markdown format for the changes represented by this instance.
        This method returns the content of the changelog as needed by the write() method of the ComposedChangelog class.
        """
        raise NotImplementedError()


@dataclass(frozen=True, repr=True)
class VersionInfo:
    version: Version
    release_date: date


class ReleaseChangelog(ChangelogABC):
    """
    A changelog instance representing the changes for a single component at release time. Allows for an unspecified (even zero)
    number of versions. Expects change entries corresponding to specified versions to exist at construction.
    """

    def __init__(
        self,
        project_name: str,
        project_root: str,
        current_version: Version,
        include_versions: Sequence[VersionInfo],
    ) -> None:
        super().__init__(project_name)
        self.current_version: Version = current_version
        self.changes: Sequence[Changelog] = [
            Changelog(
                project_name,
                os.path.join(project_root, "changelogs", str(version.version)),
                version.release_date,
            )
            for version in sorted(
                include_versions, key=lambda v: v.version, reverse=True
            )
        ]

    def get_rendered_changelog(self) -> str:
        if len(self.changes) == 0:
            return (
                f"## {self.project_name}: release {self.current_version}"
                "\nThis component has had no new releases since the last product version."
                "\n"
            )
        return "".join(changelog.get_rendered_changelog() for changelog in self.changes)


class Changelog(ChangelogABC):
    """
    Represents a changelog for the changes in one specific release. Change entries are collected at construction.
    All methods without inherent side effects work on this static set.
    """

    def __init__(
        self,
        project_name: str,
        dir_with_changelog_files: str,
        release_date: Optional[date] = None,
    ) -> None:
        """
        :param project_name: The name of the project this changelog belongs to.
        :param dir_with_changelog_files: The directory that contains all the .yml changelogs file
        """
        if not os.path.exists(dir_with_changelog_files):
            raise FileNotFoundError(f"{dir_with_changelog_files} does not exist")
        if not os.path.isdir(dir_with_changelog_files):
            raise NotADirectoryError(f"{dir_with_changelog_files} is not a directory.")

        super().__init__(project_name)
        self._release_date = release_date
        self._dir_with_changelog_files: str = os.path.abspath(dir_with_changelog_files)
        self.entries: List[ChangeEntry] = list(self._get_changelog_entries())

        self._changelog_messages: Dict[ChangelogSection, List[str]] = defaultdict(list)
        for changelog_entry in self.entries:
            for (
                section,
                message,
            ) in changelog_entry.get_messages_for_changelog_file().items():
                self._changelog_messages[section].append(message)

    @classmethod
    def get_changelog_title_for(
        cls,
        project_name: Optional[str] = None,
        version: Optional[Version] = None,
        release_date: Optional[date] = None,
    ) -> str:
        release_name: str = (
            "unreleased changes" if version is None else f"release {version}"
        )
        if not release_date:
            release_date = date.today()
        date_string: str = release_date.isoformat()
        if project_name is not None:
            result = f"{project_name}: {release_name} ({date_string})"
        else:
            result = f"{release_name} ({date_string})"
        return result.capitalize()

    def _get_changelog_entries(self) -> Iterator[ChangeEntry]:
        for filename in sorted(os.listdir(self._dir_with_changelog_files)):
            if filename == GITKEEP_FILE:
                # Ignore .gitkeep file. It's not a changelog entry
                continue
            pq_path_filename = os.path.join(self._dir_with_changelog_files, filename)
            if os.path.isfile(pq_path_filename):
                yield parse_change_entry(pq_path_filename)
            else:
                LOGGER.warning(
                    "Found %s in changelog directory %s which is not a file",
                    filename,
                    self._dir_with_changelog_files,
                )

    def has_change_entries(self) -> bool:
        """
        :return: True iff this changelog has changelog entry files.
        """
        return len(self.entries) > 0

    def has_changelog_messages(self) -> bool:
        """
        :return: True iff this changelog has messages that should be mentioned in the changelog.
        """
        return any(len(messages) > 0 for messages in self._changelog_messages.values())

    def get_change_messages_for(self, changelog_section: ChangelogSection) -> List[str]:
        return list(self._changelog_messages[changelog_section])

    def release(self, version: Version) -> None:
        """
        Release a collection of unreleased change entries by moving them to the appropriate directory.
        """
        if not self.has_change_entries():
            raise Exception("Cannot release, because no change entries exist.")
        if self.get_version() is not None:
            raise Exception("Can only release unreleased change entries")
        if self.get_change_type() is None:
            raise Exception("Can not release changelog without entries")
        new_dir: str = os.path.join(
            os.path.dirname(self._dir_with_changelog_files), str(version)
        )
        if os.path.exists(new_dir):
            raise Exception(
                f"Can not release change entries as {version}, it exists already"
            )
        # Copy changelog entry files to new_dir
        os.makedirs(new_dir)
        for file in os.listdir(self._dir_with_changelog_files):
            if file != GITKEEP_FILE:
                shutil.move(os.path.join(self._dir_with_changelog_files, file), new_dir)
        self._dir_with_changelog_files = new_dir

    def get_version(self) -> Optional[Version]:
        """
        Returns the version associated with this collection of change entries based on the directory name.
        """
        base_name = os.path.basename(self._dir_with_changelog_files)
        if base_name == CHANGE_ENTRIES_DIR:
            return None
        if COMPILED_SEMVER_REGEX_STABLE_VERSION.match(base_name):
            return Version(base_name)
        raise Exception(
            f"Couldn't determine changelog version for {self._dir_with_changelog_files}"
        )

    def get_change_type(self) -> Optional[ChangeType]:
        """
        Returns the accumulated change type for this collection of change entries, i.e. the largest change type among them.
        """
        return max((entry.change_type for entry in self.entries), default=None)

    def get_changelog_title(self, include_project_name: bool = True) -> str:
        """
        :return: The title of this changelog file.
        """
        version: Optional[Version] = self.get_version()
        if include_project_name:
            return self.get_changelog_title_for(
                project_name=self.project_name,
                version=version,
                release_date=self._release_date,
            )
        else:
            return self.get_changelog_title_for(
                project_name=None, version=version, release_date=self._release_date
            )

    def get_rendered_changelog(
        self,
        title: Optional[str] = None,
        default_upgrade_note_notice: Optional[str] = None,
    ) -> str:
        """
        Returns a changelog file in markdown format for this collection of change entries.
        When no change entries exist, the empty string is returned. This method return the
        content of the changelog as needed by the write() method of the ComposedChangelog class.

        :param title: If provided, the given title is used instead of the default title.
        :param default_upgrade_note_notice: If provided, this default_upgrade_note_notice will be added to the changelogs.
        """
        if title is not None:
            result = f"## {title}\n\n"
        else:
            result = f"## {self.get_changelog_title()}\n\n"
        if not self.has_changelog_messages():
            result += "No changelog entries.\n\n"
            return result
        for section in ChangelogSection.get_sections_ordered():
            messages_in_section = self.get_change_messages_for(section)
            if section == ChangelogSection.UPGRADE_NOTE and default_upgrade_note_notice:
                messages_in_section.append(default_upgrade_note_notice)
            if messages_in_section:
                result += f"### {section.get_section_title_for_changelog_file()}\n\n"
                for changelog_line in messages_in_section:
                    result += f"- {changelog_line}\n"
                result += "\n"
        return result


class ComposedChangelog:
    """
    Represents a changelog for a product and all its components.
    """

    def __init__(
        self,
        product_name: str,
        core_changelog: ChangelogABC,
        extension_changelogs: Sequence[ChangelogABC] = [],
        ui_changelogs: Sequence[ChangelogABC] = [],
        product_changelog: Optional[Changelog] = None,
        product_version: Optional[Version] = None,
    ) -> None:
        if product_changelog is not None and product_version is not None:
            raise Exception(
                "product_changelog and product_version cannot be set together."
            )
        if (
            product_changelog is not None
            and product_changelog.project_name != product_name
        ):
            raise Exception(
                f"The given product_name ({product_name}) and product_changelog.project_name "
                f"({product_changelog.project_name}) don't match."
            )
        self._product_name = product_name
        self._core_changelog = core_changelog
        self._extension_changelogs = extension_changelogs
        self._ui_changelogs = ui_changelogs
        self._product_changelog = product_changelog
        self._product_version = product_version

    @classmethod
    def from_checked_out_repositories(
        cls,
        product_dir: str,
        core_dir: str,
        ext_name_to_dir: Dict[str, str],
        ui_name_to_dir: Dict[str, str],
    ) -> "ComposedChangelog":
        """
        Return a ComposedChangelog for unreleased changes from the given directories,
        which contain the checked out projects for the different components.
        """
        product_name = util.get_name_python_project(product_dir)
        unreleased_change_entries_dir = os.path.join(product_dir, CHANGE_ENTRIES_PATH)
        if os.path.exists(unreleased_change_entries_dir):
            product_changelog = Changelog(product_name, unreleased_change_entries_dir)
        else:
            product_changelog = None
        return ComposedChangelog(
            product_name=product_name,
            product_changelog=product_changelog,
            core_changelog=Changelog(
                project_name=util.get_name_python_project(core_dir),
                dir_with_changelog_files=os.path.join(core_dir, CHANGE_ENTRIES_PATH),
            ),
            extension_changelogs=[
                Changelog(
                    project_name=ext_name,
                    dir_with_changelog_files=os.path.join(
                        directory, CHANGE_ENTRIES_PATH
                    ),
                )
                for ext_name, directory in ext_name_to_dir.items()
            ],
            ui_changelogs=[
                Changelog(
                    project_name=ui_name,
                    dir_with_changelog_files=os.path.join(
                        directory, CHANGE_ENTRIES_PATH
                    ),
                )
                for ui_name, directory in ui_name_to_dir.items()
            ],
        )

    def _get_changelogs_sorted(
        self, changelogs: Sequence[ChangelogABC]
    ) -> List[ChangelogABC]:
        """
        Return the changelogs sorted according to their project name.
        """
        return sorted(changelogs, key=lambda x: x.project_name)

    def write(self, output_file: str) -> None:
        """
        Write the composed changelog in markdown format to a file.

        :param output_file: The file where the resulting changelog file should be written to.
                            If this file already exists, the newly generated changelog
                            will be prefix to the already existing changelog file.
        """
        LOGGER.info("Writing changelog for %s to %s", self._product_name, output_file)
        output_file = os.path.abspath(output_file)
        if os.path.exists(output_file) and not os.path.isfile(output_file):
            raise Exception(
                f"Output file {output_file} already exists and is not a file"
            )
        rendered_changelog = self._get_rendered_changelog()
        changelog_file_already_exists = os.path.exists(output_file)
        file_mode = "r+" if changelog_file_already_exists else "w"
        with open(output_file, file_mode, encoding="utf-8") as fd:
            if changelog_file_already_exists:
                LOGGER.info(
                    "Output file %s already exists. Adding the new part of the changelog at the beginning of the file.",
                    output_file,
                )
                content_existing_changelog_file = fd.read().strip()
                if content_existing_changelog_file:
                    rendered_changelog = (
                        f"{rendered_changelog}\n\n\n{content_existing_changelog_file}"
                    )
                fd.seek(0, 0)
            fd.write(f"{rendered_changelog}\n")

    def _get_default_notice(self, default_upgrade_note_notice: str) -> str:
        default_notice = "## Upgrade notes\n\n"
        default_notice += f"- {default_upgrade_note_notice}\n\n"
        return default_notice

    def _get_rendered_changelog(self) -> str:
        default_upgrade_note_notice = (
            "Ensure the database is backed up before executing an upgrade."
        )
        if self._product_changelog is not None:
            result = f"# {self._product_changelog.get_changelog_title(include_project_name=False)}\n\n"
            if self._product_changelog.has_changelog_messages():
                # Write general changes section changelog messages exist at the product level.
                result += self._product_changelog.get_rendered_changelog(
                    title="General changes",
                    default_upgrade_note_notice=default_upgrade_note_notice,
                )
            else:
                result += self._get_default_notice(default_upgrade_note_notice)
        else:
            # No product changelog. Only write title and default notices.
            result = f"# {Changelog.get_changelog_title_for(version=self._product_version)}\n\n"
            result += self._get_default_notice(default_upgrade_note_notice)
        # Core component
        result += self._core_changelog.get_rendered_changelog()
        # Extensions components
        for changelog in self._get_changelogs_sorted(self._extension_changelogs):
            result += changelog.get_rendered_changelog()
        # UI components
        for changelog in self._get_changelogs_sorted(self._ui_changelogs):
            result += changelog.get_rendered_changelog()
        result = result.rstrip("\n")
        return result
