"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import glob
import itertools
import logging
import os
import re
import subprocess
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import chain
from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Match,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
)

import dateutil.parser
import more_itertools
from packaging.version import Version

from irt import util
from irt.changelog import (
    CHANGE_ENTRIES_DIR,
    CHANGE_ENTRIES_PATH,
    RENDERED_CHANGELOG_FILE,
    ChangeEntry,
    Changelog,
    ComposedChangelog,
    ReleaseChangelog,
    VersionInfo,
    parse_change_entry,
)
from irt.const import GITKEEP_FILE
from irt.git import Branch, GitRepo, InvalidBranch, RecursiveStrategyOption, Tag
from irt.mergetool.config import MergeToolConfig
from irt.project import ProductConfig, ProductProject, Project, ProjectConfig
from irt.release import BuildType
from irt.release.build import FreezeFileGenerator
from irt.version import ChangeType, VersionBumpTool

LOGGER = logging.getLogger(__name__)


class ReleaseTool(ABC):
    def __init__(
        self,
        name: str,
        repo_url: str,
        dev_branch: str,
        working_dir: str,
        token: Optional[str] = None,
    ) -> None:
        if os.path.exists(working_dir) and not (
            os.path.isdir(working_dir) and len(os.listdir(working_dir)) == 0
        ):
            raise Exception("Expected empty working directory")
        self.name: str = name
        self.working_dir: str = working_dir
        self.token: Optional[str] = token
        self.repo: GitRepo = GitRepo(repo_url, os.path.join(working_dir, "repo"), token)
        self.master: "ProductVersion" = ProductVersion("master", self.repo)
        self.version: "ProductVersion" = ProductVersion(dev_branch, self.repo)

    @abstractmethod
    def rc_release(self) -> Tuple[Optional[ChangeType], Version]:
        """
        Performs the necessary release steps to enter the RC window.
        Returns the version on the RC branch after the release.
        """
        raise NotImplementedError()

    @abstractmethod
    def stable_release(self) -> Version:
        """
        Performs the necessary release steps to end the RC window and perform a stable release.
        Returns the version on the stable branch after the release.
        """
        raise NotImplementedError()

    def _merge(self, *, source: BuildType, target: BuildType) -> Set[str]:
        """
        Merges this version's source into target branch.

        :return: Set of updated branches
        """
        try:
            with self.repo.checkout_branch(self.version[target]) as target_branch:
                target_branch.merge(
                    self.version[source],
                    strategy_option=RecursiveStrategyOption.THEIRS,
                )
        except InvalidBranch:
            # The target branch does not exist yet, branch off from source branch
            with self.repo.checkout_branch(
                self.version[target], base_branch=self.version[source]
            ):
                pass
        return {self.version[target]}

    @contextmanager
    def _branch(
        self, *, branch: Optional[Branch] = None, name: Optional[str] = None
    ) -> Iterator[Branch]:
        """
        Work on a branch. If name is given, checks out the branch, otherwise work on the already checked out branch.
        Provides flexibility for methods that work on branches by allowing them to be called either with or without an existing
        branch context.
        """
        if (branch is None) == (name is None):
            raise ValueError("Exactly one of branch, name must be None")
        if branch is not None:
            yield branch
        else:
            assert name is not None
            with self.repo.checkout_branch(name) as b:
                yield b

    def _get_changelog(
        self, *, branch: Optional[Branch] = None, branch_name: Optional[str] = None
    ) -> Optional[Changelog]:
        """
        Returns the unreleased changelog for a branch if it exists. If there are no changes, returns None.
        """
        with self._branch(branch=branch, name=branch_name):
            try:
                changelog: Changelog = Changelog(
                    self.name, os.path.join(self.repo.directory, CHANGE_ENTRIES_PATH)
                )
            except FileNotFoundError:
                return None
            else:
                if not changelog.has_change_entries():
                    return None
                return changelog

    def _get_version_bump_tool(
        self, *, branch: Optional[Branch] = None, branch_name: Optional[str] = None
    ) -> VersionBumpTool:
        """
        Returns a version bump tool object as configured by the project config file on the given branch.
        Any methods called on the returned object only make sense in the context of a checked out branch.
        """
        with self._branch(branch=branch, name=branch_name):
            config: ProjectConfig = Project(self.repo.directory).get_project_config()
            return config.version_bump.tool.get_tool(self.repo.directory)

    def _get_version(
        self, *, branch: Optional[Branch] = None, branch_name: Optional[str] = None
    ) -> Version:
        with self._branch(branch=branch, name=branch_name) as branch:
            return self._get_version_bump_tool(branch=branch).get_version()

    def _set_tag_build(self, build_type: BuildType) -> None:
        """
        Sets the appropriate `tag_build` in setup.cfg on this version's branch for the given build type.
        Commits to the build type branch.
        """
        setup_cfg_file: str = os.path.join(self.repo.directory, "setup.cfg")
        with self.repo.checkout_branch(self.version[build_type]) as branch:
            content: str
            try:
                with open(setup_cfg_file, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                content = ""
            tag: str = (
                ".dev0"
                if build_type == BuildType.dev
                else "rc"
                if build_type == BuildType.next
                else ""
            )
            tag_line: str = f"tag_build = {tag}".strip()
            new_content: str
            count: int
            # find existing tag_build and set it
            new_content, count = re.subn("tag_build *=.*", tag_line, content)
            if count == 0:
                # find egg_info section and add tag_build
                new_content, count = re.subn(
                    r"(\[egg_info\])", fr"\1\n{tag_line}", content
                )
                if count == 0:
                    # add egg_info section and tag_build
                    new_content = f"[egg_info]\n{tag_line}\n\n" + content
            if count > 1:
                raise Exception(
                    "Failed to set tag_build: multiple occurences found in %s."
                    % setup_cfg_file
                )
            if new_content != content:
                with open(setup_cfg_file, "w") as f:
                    f.write(new_content)
                branch.commit(
                    f"Set tag_build in setup.cfg for {build_type.value} build type"
                )

    def _ensure_rc_change_type_increment(
        self, target: BuildType, change_type: ChangeType
    ) -> Tuple[Version, Set[str]]:
        """
        Makes sure the target version has an appropriate increment relative to the stable branch for the given change type.
        Commits to the target branch if the version is incremented.

        :returns: Tuple of version and set of updated branches.
        """
        stable_version: Version
        try:
            stable_version = self._get_version(branch_name=self.version.stable_branch)
        except InvalidBranch:
            # Set stable_version to 0.0.0 to ensure at least the change-type digit gets set
            stable_version = Version("0.0.0")
        with self.repo.checkout_branch(self.version[target]) as branch:
            version_bump_tool: VersionBumpTool = self._get_version_bump_tool(
                branch=branch
            )
            current_version: Version = version_bump_tool.get_version()
            current_diff: Optional[ChangeType]
            try:
                current_diff = ChangeType.diff(low=stable_version, high=current_version)
            except ValueError:
                raise Exception(
                    "Invalid version state. Got stable version %s and %s version %s"
                    % (stable_version, target.value, current_version)
                )
            if current_diff is None or change_type > current_diff:
                version_bump_tool.bump(change_type)
                branch.commit("Version bump based on change entries")
                return (version_bump_tool.get_version(), {self.version[target]})
            return (current_version, set())


T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, repr=True)
class ComponentCollection(Generic[T]):
    """
    Collection of items of type T, grouped by the component type they belong to.
    """

    core: T
    extensions: List[T]
    npm: List[T]

    def map(self, f: Callable[[T], U]) -> "ComponentCollection[U]":
        return ComponentCollection(
            core=f(self.core),
            extensions=list(map(f, self.extensions)),
            npm=list(map(f, self.npm)),
        )

    def all(self) -> Iterator[T]:
        return chain(
            [self.core],
            self.extensions,
            self.npm,
        )

    def all_python(self) -> Iterator[T]:
        return chain(
            [self.core],
            self.extensions,
        )


@dataclass(frozen=True, repr=True)
class ReleasedComponent:
    name: str
    version: Version
    release_tool: "ComponentReleaseTool"


ReleasedComponentHistory = Tuple[ReleasedComponent, Sequence[VersionInfo]]
"""
Release history of a released component. Keeps track of previously released versions.
"""


class ProductReleaseTool(ReleaseTool):
    def __init__(
        self,
        name: str,
        repo_url: str,
        dev_branch: str,
        working_dir: str,
        merge_tool_config: MergeToolConfig,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(name, repo_url, dev_branch, working_dir, token=token)
        self.merge_tool_config: MergeToolConfig = merge_tool_config

    def _get_component_release_tools(
        self, branch: str
    ) -> ComponentCollection[Tuple[str, "ComponentReleaseTool"]]:
        """
        Returns all component release tools based on the product config for a given branch.
        """

        def get_release_tool(
            comp: Tuple[str, str], component_type: str
        ) -> Tuple[str, "ComponentReleaseTool"]:
            name, repo = comp
            return (
                name,
                ComponentReleaseTool(
                    name,
                    repo,
                    self.version.dev_branch,
                    os.path.join(
                        self.working_dir,
                        "components",
                        branch,
                        component_type,
                        name,
                    ),
                    self.token,
                ),
            )

        config: ProductConfig
        with self.repo.checkout_branch(branch):
            config = ProductProject(self.repo.directory).get_project_config()
        return ComponentCollection(
            core=get_release_tool(config.dependencies.get_core_component(), "core"),
            extensions=[
                get_release_tool(extension, "extensions")
                for extension in config.dependencies.extensions.items()
            ],
            npm=[
                get_release_tool(npm, "npm")
                for npm in config.dependencies.get_all_npm_component_repos().items()
            ],
        )

    def _pin_npm(
        self, build_type: BuildType, components: Iterable[ReleasedComponent]
    ) -> None:
        """
        Pins NPM dependencies depending on the build type. Commits to the RC branch.
        """
        if build_type == BuildType.dev:
            raise ValueError("Dependencies should not be pinned to dev versions")
        constraint, build_type_tag = (
            ("~=", ".0rc") if build_type == BuildType.next else ("==", "")
        )
        with self.repo.checkout_branch(self.version.rc_branch) as branch:
            project: ProductProject = ProductProject(self.repo.directory)
            config: ProductConfig = project.get_project_config(fill_placeholders=False)
            new_config: ProductConfig = config.copy(deep=True)
            for component in components:
                version: str = f"{constraint}{component.version}{build_type_tag}"
                new_config.dependencies.npm[component.name].version = version
            if new_config != config:
                project.write_project_config(new_config)
                branch.commit("Pinned npm dependencies in pyproject.toml.")

    def _pin_python(
        self, build_type: BuildType, components: Iterable[ReleasedComponent]
    ) -> None:
        """
        Pins Python dependencies depending on the build type. Commits to the RC branch.
        """
        if build_type == BuildType.dev:
            raise ValueError("Dependencies should not be pinned to dev versions")
        constraint: str
        build_type_tag: str
        constraint, build_type_tag = (
            ("~=", ".0rc") if build_type == BuildType.next else ("==", "")
        )
        setup_py_file: str = os.path.join(self.repo.directory, "setup.py")
        with self.repo.checkout_branch(self.version.rc_branch) as branch:
            content: str
            with open(setup_py_file, "r") as f:
                content = f.read()
            new_content: str = content
            for component in components:
                regex: str = fr"\"{re.escape(component.name)}( *[~><=]+ *[0-9]+(\.[0-9]+){{0,2}}(\.0)?(\.?[a-z]+)?)?\""
                replacement: str = (
                    f'"{component.name}{constraint}{component.version}{build_type_tag}"'
                )
                count: int
                new_content, count = re.subn(regex, replacement, new_content)
                if count == 0:
                    raise Exception(
                        "Failed to pin Python dependency %s: could not find dependency in %s."
                        % (replacement, setup_py_file)
                    )
                if count > 1:
                    raise Exception(
                        "Failed to pin Python dependency %s: multiple occurences found in %s."
                        % (replacement, setup_py_file)
                    )
            if new_content != content:
                with open(setup_py_file, "w") as f:
                    f.write(new_content)
                branch.commit("Pinned python dependencies in setup.py.")

    def _pin_rpm(self, components: Iterable[ReleasedComponent]) -> None:
        """
        Pins the versions of the RPM dependencies in the inmanta.spec file. Commits to the RC branch.

        Only required for iso3, later versions don't have separate RPMs for each component.
        """
        spec_file: str = os.path.join(self.repo.directory, "inmanta.spec")
        with self.repo.checkout_branch(self.version.rc_branch) as branch:
            content: str
            with open(spec_file, "r") as f:
                content = f.read()
            new_content: str = content
            for component in components:
                regex: str = (
                    fr"(Requires:[ \t]*python3-{re.escape(component.name)}(-server)?)"
                    r"( *[~><=]+ *[0-9]+(\.[0-9]+){0,2})?"
                )
                replacement: str = fr"\1 = {component.version}"
                new_content = re.sub(regex, replacement, new_content)
            if new_content != content:
                with open(spec_file, "w") as f:
                    f.write(new_content)
                branch.commit("Pinned RPM dependencies in inmanta.spec.")

    def _release_components(
        self, release_type: BuildType
    ) -> ComponentCollection[ReleasedComponent]:
        """
        Releases this product's components on the RC branch. Both RC releases and stable releases are staged on the RC branch.
        In the case of a stable release, the RC branch is promoted to stable at the end of the release process.

        :param release_type: The type of release to perform.
        """
        LOGGER.info("Releasing components for product %s", self.name)

        def release_component(
            comp: Tuple[str, ComponentReleaseTool]
        ) -> ReleasedComponent:
            name, release_tool = comp
            if (
                release_tool.master != self.master
                or release_tool.version != self.version
            ):
                raise Exception(
                    "Inconsistent version branches between product and component %s."
                    " Continuing could have unexpected consequences." % name
                )
            version: Version
            if release_type == BuildType.next:
                _, version = release_tool.rc_release()
            elif release_type == BuildType.stable:
                version = release_tool.stable_release()
            else:
                raise ValueError(
                    f"Can not release components for release type {release_type}"
                )
            return ReleasedComponent(
                name=name,
                version=version,
                release_tool=release_tool,
            )

        component_release_tools: ComponentCollection[
            Tuple[str, ComponentReleaseTool]
        ] = self._get_component_release_tools(self.version.rc_branch)
        return component_release_tools.map(release_component)

    def _rc_freeze_external_dependencies(
        self, components: List[ReleasedComponent]
    ) -> None:
        """
        Generates the freeze file for all external dependencies. Commits to the RC branch.

        :param components: List of Python components.
        """
        with self.repo.checkout_branch(self.version.rc_branch) as rc_branch:
            config: ProductConfig = ProductProject(
                self.repo.directory
            ).get_project_config()
            # overwrite requirements file with the one on the dev branch so we can regenerate from a clean slate
            requirements_file_rel: str = "requirements.txt"
            requirements_file_abs: str = os.path.join(
                self.repo.directory, requirements_file_rel
            )
            rc_branch.checkout_path(
                branch=self.version.dev_branch, path=requirements_file_rel
            )
            with ExitStack() as stack:
                for component in components:
                    stack.enter_context(
                        component.release_tool.repo.checkout_branch(
                            component.release_tool.version.rc_branch
                        )
                    )
                freeze_generator: FreezeFileGenerator = FreezeFileGenerator(
                    project_dir=self.repo.directory,
                    component_dirs=[
                        component.release_tool.repo.directory
                        for component in components
                    ],
                    build_type=BuildType.next,
                    min_c_constraint_files=list(
                        chain(
                            [requirements_file_abs],
                            config.clone_additional_lock_file_repos(
                                clone_dir=os.path.join(self.working_dir, "constraints"),
                                branch=self.version.rc_branch,
                                git_token=self.token,
                            ),
                        )
                    ),
                    pip_index_url=BuildType.next.get_pip_index_url(),
                    # Use the python_version defined in the rpm build config
                    # as such that RPMs can be build using this freeze file.
                    # The python package build config can contain multiple
                    # python versions.
                    python_version=config.build.rpm.python_version,
                )
                freeze_generator.write_freeze_file_with_external_dependencies(
                    requirements_file_abs
                )
            rc_branch.commit(
                "Generated freeze file for external dependencies", ignore_empty=True
            )

    def rc_release(self) -> Tuple[ChangeType, Version]:
        """
        Performs the necessary release steps to enter the RC window for a product and all its components.
        """
        LOGGER.info("Releasing product %s", self.name)

        pre_changelog: Optional[Changelog]
        try:
            pre_changelog = self._get_changelog(branch_name=self.version.rc_branch)
        except InvalidBranch:
            pre_changelog = None
        if not (pre_changelog is None or pre_changelog.get_change_type() is None):
            raise Exception(
                f"Can not release {self.name}: it has already entered the RC release stage. Any additional changes need to be"
                " cherry-picked by hand."
            )

        version_bump_tool: VersionBumpTool = self._get_version_bump_tool(
            branch_name=self.version.dev_branch
        )

        # merge dev into RC branch
        self._merge(source=BuildType.dev, target=BuildType.next)
        self._set_tag_build(BuildType.next)

        # Release components and track their versions
        components: ComponentCollection[ReleasedComponent] = self._release_components(
            BuildType.next
        )

        # Determine change type. Keep it simple: reasoning on a more specific change type is complicated due to multiple
        # products (as well as multiple versions of the same product) potentially using the same component versions. The change
        # type returned by the components' release might not reflect the changes since this product version's latest release.
        change_type: ChangeType = (
            # Products are not strictly semantically versioned: each product version stays within its major digit.
            # Change type is set to minor except if version being released only allows patches.
            ChangeType.PATCH
            if (
                ChangeType.PATCH in self.merge_tool_config.dev_branches
                and self.version.dev_branch
                == self.merge_tool_config.dev_branches[ChangeType.PATCH]
            )
            else ChangeType.MINOR
        )

        # Pin dependencies
        self._pin_npm(BuildType.next, components.npm)
        self._pin_python(BuildType.next, components.all_python())
        if self.version.version == 3:
            self._pin_rpm(components.all_python())
        self._rc_freeze_external_dependencies(list(components.all_python()))

        # Bump version on RC branch
        new_version: Version
        new_version, _ = self._ensure_rc_change_type_increment(
            BuildType.next, change_type
        )

        # Apply additional patch bump on dev branch
        with self.repo.checkout_branch(self.version.dev_branch) as dev_branch:
            version_bump_tool.set_version(new_version)
            version_bump_tool.bump(ChangeType.PATCH)
            dev_branch.commit("Increment dev version after RC release")

        # Push changes
        for branch_name in (self.version.rc_branch, self.version.dev_branch):
            with self.repo.checkout_branch(branch_name) as branch:
                branch.push()

        return change_type, new_version

    def _get_component_changes_since_previous_product(
        self, version: Version, components: ComponentCollection[ReleasedComponent]
    ) -> ComponentCollection[ReleasedComponentHistory]:
        """
        For each component, returns its released versions since the previous product release, including any component versions
        that have just been released.

        Newly introduced elements are considered new rather than changed and are therefore excluded. All new components will
        contain no versions in the change history:
            - Components that were not included in the previous product release are considered new.
            - For new products that have never been released before, all components are considered new.

        :param version: The version currently being released. This is used as the baseline to determine the previouse release
            version: the highest numbered release older than this one is considered the previous release.
        """
        previous_release_tag: Optional[Tag] = more_itertools.first(
            (tag for (tag, v) in self.repo.get_tagged_versions() if v < version),
            default=None,
        )
        if previous_release_tag is None:
            return components.map(lambda c: (c, []))

        def get_pinned_version_python(
            component: ReleasedComponent,
        ) -> Optional[Version]:
            return more_itertools.only(
                (
                    Version(v)
                    for v, _ in re.findall(
                        fr"\"{re.escape(component.name)} *== *([0-9]+(\.[0-9]+){{0,2}})\"",
                        setup_py_contents,
                    )
                ),
                default=None,
                too_long=Exception(
                    f"Found multiple constraints on {component.name} in setup.py"
                ),
            )

        def get_pinned_version_npm(
            config: ProductConfig, component: ReleasedComponent
        ) -> Optional[Version]:
            if component.name not in config.dependencies.npm:
                return None
            version_str: str = config.dependencies.npm[component.name].version
            if not version_str.startswith("=="):
                raise Exception(
                    f"Expected version pin on stable release, not {version_str}"
                )
            return Version(version_str[2:])

        pinned_components: ComponentCollection[
            Tuple[ReleasedComponent, Optional[Version]]
        ]
        with self.repo.checkout_branch(previous_release_tag.name) as branch:
            setup_py_contents: str
            with open(os.path.join(self.repo.directory, "setup.py"), "r") as fd:
                setup_py_contents = fd.read()
            project: ProductProject = ProductProject(branch.repo.directory)
            config: ProductConfig = project.get_project_config(fill_placeholders=False)

            pinned_components = ComponentCollection(
                core=(components.core, get_pinned_version_python(components.core)),
                extensions=[
                    (c, get_pinned_version_python(c)) for c in components.extensions
                ],
                npm=[(c, get_pinned_version_npm(config, c)) for c in components.npm],
            )

        def get_component_changes_since_pinned(
            component_pin: Tuple[ReleasedComponent, Optional[Version]],
        ) -> ReleasedComponentHistory:
            component, _pinned_version = component_pin
            if _pinned_version is None:
                # component was not included in last release
                return (component, [])
            pinned_version: Version = _pinned_version  # mypy fails to infer type of _pinned_version in body below
            # get all versions between previous pinned version and current version
            versions_since: Sequence[VersionInfo] = [
                VersionInfo(version=v, release_date=tag.date)
                for (tag, v) in itertools.takewhile(
                    lambda tup: tup[1] > pinned_version,
                    itertools.dropwhile(
                        lambda tup: tup[1] > component.version,
                        component.release_tool.repo.get_tagged_versions(),
                    ),
                )
            ]
            return (component, versions_since)

        return pinned_components.map(get_component_changes_since_pinned)

    def _generate_changelog(
        self, version: Version, components: ComponentCollection[ReleasedComponent]
    ) -> List[str]:
        """
        Generates the composed changelog and writes it to the appropriate place. Commits to the RC branch.

        :returns: List of commit hashes.
        """
        component_history: ComponentCollection[
            ReleasedComponentHistory
        ] = self._get_component_changes_since_previous_product(version, components)

        with self.repo.checkout_branch(self.version.rc_branch) as rc_branch:
            changelog: Optional[Changelog] = self._get_changelog(branch=rc_branch)
            if changelog is not None:
                changelog.release(version)

            def component_changelog(
                component_history: ReleasedComponentHistory,
            ) -> ReleaseChangelog:
                component, history = component_history
                with component.release_tool.repo.checkout_branch(
                    component.release_tool.version.stable_branch
                ):
                    return ReleaseChangelog(
                        component.name,
                        component.release_tool.repo.directory,
                        current_version=component.version,
                        include_versions=history,
                    )

            component_changelogs: ComponentCollection[
                ReleaseChangelog
            ] = component_history.map(component_changelog)
            composed_changelog: ComposedChangelog = ComposedChangelog(
                product_name=self.name,
                core_changelog=component_changelogs.core,
                extension_changelogs=component_changelogs.extensions,
                ui_changelogs=component_changelogs.npm,
                product_changelog=changelog,
                product_version=version if changelog is None else None,
            )
            composed_changelog.write(
                os.path.join(self.repo.directory, RENDERED_CHANGELOG_FILE)
            )
            rc_branch.commit(
                "Generated changelog and moved change entries to version directory."
            )
            commit: Optional[str] = self.repo.get_branch_head(self.version.rc_branch)
            assert commit is not None
            return [commit]

    def stable_release(self) -> Version:
        """
        Performs the necessary release steps to end the RC window and perform a stable release for a product and all its
        components. Returns the version on the stable branch after the release.
        """
        LOGGER.info("Releasing product %s", self.name)

        rc_head: Optional[str] = self.repo.get_branch_head(self.version.rc_branch)
        stable_head: Optional[str] = self.repo.get_branch_head(
            self.version.stable_branch
        )
        if rc_head is None:
            raise Exception(
                f"Can not release component {self.name} because it has no RC branch"
            )

        version: Version = self._get_version(branch_name=self.version.rc_branch)
        if stable_head is not None and version == self._get_version(
            branch_name=self.version.stable_branch
        ):
            LOGGER.warning(
                f"Skipping releasing product {self.name} on branch {self.version.rc_branch} because it has already been"
                " released"
            )
            return version

        # Release components and track their versions
        components: ComponentCollection[ReleasedComponent] = self._release_components(
            BuildType.stable
        )

        # Pin dependencies
        self._pin_npm(BuildType.stable, components.npm)
        self._pin_python(BuildType.stable, components.all_python())

        # end RC window: move unreleased change entries to version directory and generate composed changelog
        changelog_commits: List[str] = self._generate_changelog(version, components)

        # Cherry-pick changelog and change entry commit
        self.repo.cherry_pick(target=self.version.dev_branch, commits=changelog_commits)

        # Merge RC into stable
        self._merge(source=BuildType.next, target=BuildType.stable)
        self._set_tag_build(BuildType.stable)

        # Add version tag
        tag: Tag
        with self.repo.checkout_branch(self.version.stable_branch) as stable_branch:
            tag = stable_branch.tag(f"v{version}", f"Release: {version}")

        # Push changes
        for branch_name in (
            self.version.stable_branch,
            self.version.rc_branch,
            self.version.dev_branch,
        ):
            with self.repo.checkout_branch(branch_name) as branch:
                branch.push()
        tag.push()

        return version


class ComponentReleaseTool(ReleaseTool):
    """
    Release a single component. Parses unreleased change entries at construction.
    """

    def _merge(self, *, source: BuildType, target: BuildType) -> Set[str]:
        """
        Merges this version's source into target branch and all branches with the target build type corresponding to aligned
        branches with the source build type.

        :return: Set of updated branches
        """
        # if target branch does not exist yet and source has aligned branches, branch off target from one of the branches it
        # should be aligned with
        if self.repo.get_branch_head(self.version[target]) is None:
            source_head: str = self.repo.get_branch_head(self.version[source])
            for version in ProductVersion.get_all_versions(self.repo):
                if version[source] == self.version[source]:
                    # Source branch itself -> ignore
                    continue
                if (
                    self.repo.get_branch_head(version[source]) == source_head
                    and self.repo.get_branch_head(version[target]) is not None
                ):
                    with self.repo.checkout_branch(
                        self.version[target], base_branch=version[target]
                    ):
                        pass
                    break

        # call super's merge logic
        return (
            super()._merge(source=source, target=target)
            # fast-forward to aligned target branches
            .union(self._fast_forward_aligned(reference=source, merge=target))
        )

    def _set_tag_build(self, build_type: BuildType) -> None:
        """
        Sets the appropriate `tag_build` in setup.cfg on this version's branch for the given build type.
        Commits to the build type branch and fast-forwards to aligned branches.
        """
        reference_head: Optional[str] = self.repo.get_branch_head(
            self.version[build_type]
        )
        super()._set_tag_build(build_type)
        self._fast_forward_aligned(
            reference=build_type, merge=build_type, reference_head=reference_head
        )

    def _ensure_rc_change_type_increment(
        self, target: BuildType, change_type: ChangeType
    ) -> Tuple[Version, Set[str]]:
        """
        Makes sure the target version has an appropriate increment relative to the stable branch for the given change type.
        Commits to the target branch if the version is incremented and fast-forwards to aligned branches.

        :returns: Tuple of version and set of updated branches.
        """
        reference_head: Optional[str] = self.repo.get_branch_head(self.version[target])
        version, branches = super()._ensure_rc_change_type_increment(
            target, change_type
        )
        return (
            version,
            branches.union(
                self._fast_forward_aligned(
                    reference=target, merge=target, reference_head=reference_head
                )
            ),
        )

    def _fast_forward_aligned(
        self,
        *,
        reference: BuildType,
        merge: BuildType,
        reference_head: Optional[str] = None,
    ) -> Set[str]:
        """
        Fast-forward this version's merge branch to all merge branches for which the corresponding reference branches share
        heads with this version's reference branch. If reference_head is provided, uses that head instead of this version's
        reference head. Creates branches if they don't exist yet.

        :param reference: The build type for the reference branches for each version.
        :param merge: The build type for the merge branches for each version.
        :param reference_head: The head of the reference branches to select.
        :return: Set of branches this version's merge branch was fast-forwarded to.
        """
        if reference_head is None:
            reference_head = self.repo.get_branch_head(self.version[reference])
            if reference_head is None:
                raise Exception(
                    "Can not merge branch %s, it does not exist"
                    % self.version[reference]
                )
        result: List[str] = []
        for version in ProductVersion.get_all_versions(self.repo):
            if version[reference] == self.version[reference]:
                # The target branch is the same as the source branch
                continue
            if self.repo.get_branch_head(version[reference]) == reference_head:
                try:
                    with self.repo.checkout_branch(version[merge]) as target_branch:
                        target_branch.fast_forward(self.version[merge])
                except InvalidBranch:
                    # merge branch does not exist yet, create it
                    with self.repo.checkout_branch(
                        version[merge], base_branch=self.version[merge]
                    ):
                        pass
                result.append(version[merge])
        return set(result)

    def _cherry_pick_aligned(
        self,
        *,
        reference: BuildType,
        merge: BuildType,
        commits: List[str],
    ) -> Set[str]:
        """
        Cherry-picks commits to this version's merge branch and all merge branches for which the corresponding reference
        branches are aligned. Makes sure existing alignment on merge branches is kept.

        :returns: The set of updated branches.
        """
        reference_head: Optional[str] = self.repo.get_branch_head(
            self.version[reference]
        )
        if reference_head is None:
            raise Exception(
                f"Can not determine cherry-pick targets: {self.version[reference]} does not exist"
            )

        # group relevant merge branches by current branch head
        groups: Dict[str, List[str]] = defaultdict(list)
        for version in ProductVersion.get_all_versions(self.repo):
            if self.repo.get_branch_head(version[reference]) == reference_head:
                # reference branches are aligned => commits need to be cherry-picked onto merge branch
                merge_head: Optional[str] = self.repo.get_branch_head(version[merge])
                if merge_head is None:
                    raise Exception(
                        f"Can not cherry-pick onto branch {version[merge]}, it does not exist"
                    )
                groups[merge_head].append(version[merge])

        # cherry-pick onto one of each group, then fast-forward to other group members
        for head, branches in groups.items():
            if len(branches) == 0:
                continue
            self.repo.cherry_pick(branches[0], commits)
            for branch in branches[1:]:
                self.repo.fast_forward(target=branch, source=branches[0])

        return set(chain.from_iterable(groups.values()))

    def _get_rc_release_change_type(self) -> Optional[ChangeType]:
        """
        Returns the change type for the unreleased changes that would be released by performing an RC release.
        Returns None iff no release should be performed.
        """
        rc_changelog: Optional[Changelog]
        try:
            rc_changelog = self._get_changelog(branch_name=self.version.rc_branch)
        except InvalidBranch:
            rc_changelog = None
        rc_change_type: Optional[ChangeType] = (
            rc_changelog.get_change_type() if rc_changelog is not None else None
        )
        if rc_change_type is not None:
            LOGGER.warning(
                "Skipping releasing component %s on branch %s because it has already entered the release stage. The"
                " most likely explanation is that this version is still aligned with another version, that has been"
                " released already.",
                self.name,
                self.version.dev_branch,
            )
            return None
        dev_changelog: Optional[Changelog] = self._get_changelog(
            branch_name=self.version.dev_branch
        )
        dev_change_type: Optional[ChangeType] = (
            dev_changelog.get_change_type() if dev_changelog is not None else None
        )
        if dev_change_type is None:
            LOGGER.warning(
                "Skipping releasing component %s on branch %s because there are no unreleased changes.",
                self.name,
                self.version.dev_branch,
            )
            return None
        return dev_change_type

    def rc_release(self) -> Tuple[Optional[ChangeType], Version]:
        """
        Performs the necessary release steps to enter the RC window for a single component. Returns the version on the RC branch
        after the release.
        """
        LOGGER.info("Releasing component %s", self.name)

        change_type: Optional[ChangeType] = self._get_rc_release_change_type()
        if change_type is None:
            try:
                return None, self._get_version(branch_name=self.version.rc_branch)
            except InvalidBranch:
                raise Exception(
                    "Invalid request: skipping releasing component %s on branch %s because it doesn't meet the requirements"
                    " for a release but it doesn't have a released version yet. Please add a change entry and retry."
                    % (self.name, self.version.dev_branch)
                )

        dev_head_prior: Optional[str] = self.repo.get_branch_head(
            self.version.dev_branch
        )
        if dev_head_prior is None:
            raise Exception(
                "Can not perform RC release for component %s, branch %s: branch does not exist"
                % (self.name, self.version.dev_branch)
            )

        staged_branches: List[str] = []

        # bump version based on change entries on dev branch before branching off
        new_version: Version
        new_version, increment_branches = self._ensure_rc_change_type_increment(
            BuildType.dev, change_type
        )
        staged_branches.extend(increment_branches)

        # merge into RC branch
        staged_branches.extend(
            self._merge(
                source=BuildType.dev,
                target=BuildType.next,
            )
        )

        # make sure tag_build is set correctly in setup.cfg
        self._set_tag_build(BuildType.next)

        # apply additional patch bump on dev branch
        dev_head: Optional[str] = self.repo.get_branch_head(self.version.dev_branch)
        with self.repo.checkout_branch(self.version.dev_branch) as dev_branch:
            self._get_version_bump_tool(branch=dev_branch).bump(ChangeType.PATCH)
            dev_branch.commit("Increment dev version after RC release")
        staged_branches.append(self.version.dev_branch)
        staged_branches.extend(
            self._fast_forward_aligned(
                reference_head=dev_head,
                reference=BuildType.dev,
                merge=BuildType.dev,
            )
        )

        # Push changes to staged branches.
        for branch_name in set(staged_branches):
            with self.repo.checkout_branch(branch_name) as branch:
                branch.push()

        return change_type, new_version

    def stable_release(self) -> Version:
        """
        Performs the necessary release steps to end the RC window and perform a stable release for a single component.
        Returns the version on the stable branch after the release.
        """
        LOGGER.info("Releasing component %s", self.name)

        rc_head: Optional[str] = self.repo.get_branch_head(self.version.rc_branch)
        stable_head: Optional[str] = self.repo.get_branch_head(
            self.version.stable_branch
        )
        if rc_head is None:
            raise Exception(
                f"Can not release component {self.name} because it has no RC branch"
            )

        version: Version = self._get_version(branch_name=self.version.rc_branch)
        if stable_head is not None and version == self._get_version(
            branch_name=self.version.stable_branch
        ):
            LOGGER.warning(
                f"Skipping releasing component {self.name} on branch {self.version.rc_branch} because it has already been"
                " released"
            )
            return version

        staged_branches: List[str] = []

        # end RC window: move unreleased change entries to version directory
        change_entry_commit: str
        with self.repo.checkout_branch(self.version.rc_branch) as rc_branch:
            changelog: Optional[Changelog] = self._get_changelog(branch=rc_branch)
            if changelog is None:
                raise Exception(
                    f"Invalid state: the RC branch for component {self.name} has no unreleased changes"
                )
            changelog.release(version)
            rc_branch.commit("Move unreleased change entries to version directory.")
            commit: Optional[str] = self.repo.get_branch_head(self.version.rc_branch)
            assert commit is not None
            change_entry_commit = commit
        staged_branches.append(self.version.rc_branch)

        # fast-forward to aligned RC branches
        staged_branches.extend(
            self._fast_forward_aligned(
                reference_head=rc_head,
                reference=BuildType.next,
                merge=BuildType.next,
            )
        )

        # Cherry-pick change entry move.
        # Don't delegate to merge tool because that would immediately populate the unreleased directory with a change entry,
        # which would break the reasoning for whether an RC release is required.
        staged_branches.extend(
            self._cherry_pick_aligned(
                reference=BuildType.next,
                merge=BuildType.dev,
                commits=[change_entry_commit],
            )
        )

        # Merge RC into stable
        staged_branches.extend(
            self._merge(source=BuildType.next, target=BuildType.stable)
        )
        self._set_tag_build(BuildType.stable)

        # Add version tag
        tag: Tag
        with self.repo.checkout_branch(self.version.stable_branch) as stable_branch:
            tag = stable_branch.tag(f"v{version}", f"Release: {version}")

        # push changes to staged branches
        for branch_name in set(staged_branches):
            with self.repo.checkout_branch(branch_name) as branch:
                branch.push()
        tag.push()

        return version


P = TypeVar("P", bound="ProductVersion")


class ProductVersion(Mapping[BuildType, str]):
    def __init__(self, dev_branch: str, repo: GitRepo) -> None:
        """
        A version of the product with associated branches.

        :param dev_branch: The development branch associated with this version.
        :param repo: The repo for this product, required to inspect existing versions at construction.
        """
        self.version: int
        iso_version_regex: str = "iso([1-9][0-9]*)"
        if dev_branch == "master":
            branches: Set[str] = repo.get_all_branches()

            def highest_version(regex: str) -> int:
                return max(
                    (
                        int(match.group(1))
                        for match in [
                            re.fullmatch(regex, branch) for branch in branches
                        ]
                        if match is not None
                    ),
                    default=0,
                )

            self.version = max(
                highest_version(iso_version_regex) + 1,
                highest_version(f"{iso_version_regex}-next"),
            )
        else:
            match: Optional[Match] = re.fullmatch(iso_version_regex, dev_branch)
            if match is None:
                raise ValueError(
                    f"Invalid dev branch {dev_branch}, expected either master or iso<x> with x an integer"
                )
            self.version = int(match.group(1))
        self.dev_branch: str = dev_branch
        self.rc_branch: str = f"iso{self.version}-next"
        self.stable_branch: str = f"iso{self.version}-stable"
        self._mapping: Dict[BuildType, str] = {
            BuildType.dev: self.dev_branch,
            BuildType.next: self.rc_branch,
            BuildType.stable: self.stable_branch,
        }

    @classmethod
    def get_all_versions(cls, repo: GitRepo) -> Iterator["ProductVersion"]:
        """
        Returns an iterator over all product versions in a repo.
        """
        for branch in repo.get_all_branches():
            try:
                yield cls(branch, repo)
            except ValueError:
                pass

    @classmethod
    def verify_version_alignment(
        cls, repo: GitRepo
    ) -> Iterator[Tuple[Version, Set[str]]]:
        """
        Verifies that any two version branches for the same build type are either aligned or have different project versions.
        If this is not the case, this could lead to artifacts being built for the same version with different contents.

        :returns: all sets of branches that mutually violate the invariant.
        """
        version_bump_tool: VersionBumpTool
        with repo.checkout_branch("master"):
            config: ProjectConfig = Project(repo.directory).get_project_config()
            version_bump_tool = config.version_bump.tool.get_tool(repo.directory)
        product_versions: List[ProductVersion] = list(cls.get_all_versions(repo))

        def get_project_version(branch: str) -> Optional[Version]:
            try:
                with repo.checkout_branch(branch):
                    return version_bump_tool.get_version()
            except InvalidBranch:
                return None

        for build_type in BuildType:
            project_versions: Dict[Version, List[str]] = defaultdict(list)
            for product_version in product_versions:
                project_version: Optional[Version] = get_project_version(
                    product_version[build_type]
                )
                if project_version is not None:
                    project_versions[project_version].append(
                        product_version[build_type]
                    )
            for project_version, branches in project_versions.items():
                if len({repo.get_branch_head(branch) for branch in branches}) > 1:
                    # not all branches are aligned, yet they have the same version
                    yield (project_version, set(branches))

    @classmethod
    def verify_change_entries(cls, repo: GitRepo) -> Iterator[Tuple[str, Set[str]]]:
        """
        Verifies that each unreleased change entry exists on each of its destination branches.
        Change entries are considered the same if their file names match and if their commit timestamps are not
        more than a week apart.

        :returns: An iterator over pairs of change entry file names and the set of branches where it's missing.
        """

        def files() -> Iterator[str]:
            for product_version in cls.get_all_versions(repo):
                with repo.checkout_branch(product_version.dev_branch) as branch:
                    yield from zip(
                        (
                            os.path.relpath(path, start=repo.directory)
                            for path in glob.iglob(
                                os.path.join(repo.directory, "changelogs", "*", "*")
                            )
                        ),
                        itertools.repeat(branch),
                    )

        all_tuples: Iterator[Tuple[str, Set[str]]] = (
            (
                distinct.name,
                distinct.expected_branches.difference(distinct.found_branches),
            )
            for distinct in cls._get_distinct_change_entries(files())
        )
        return (tup for tup in all_tuples if len(tup[1]) > 0)

    @classmethod
    def rewrite_master_change_history(cls: Type[P], repo: GitRepo) -> None:
        """
        Rewrites change history on the master branch based on change history of the latest iso branch. Change entries
        that were included in a release on the latest iso, are moved to the appropriate release directory on master.
        """
        # exhaust iterator to ensure ownership of repo instance
        released_entries: Sequence[Tuple[str, Version]] = list(
            cls.get_change_entries_released_below_master(repo)
        )
        if not released_entries:
            return
        with repo.checkout_branch("master") as branch:
            for entry_name, version in released_entries:
                version_dir: str = os.path.join(
                    repo.directory, "changelogs", str(version)
                )
                os.makedirs(version_dir, exist_ok=True)
                os.rename(
                    os.path.join(
                        repo.directory, "changelogs", CHANGE_ENTRIES_DIR, entry_name
                    ),
                    os.path.join(version_dir, entry_name),
                )
            branch.commit("Rewrote change history from latest iso")

    @classmethod
    def get_change_entries_released_below_master(
        cls: Type[P], repo: GitRepo
    ) -> Iterator[Tuple[str, Version]]:
        """
        Returns an iterator over change entry names that are considered unreleased on master but have been released
        on the latest iso branch. Includes the version each change entry was released in.
        """
        master: P = cls("master", repo)
        latest_iso: P = cls("iso%d" % (master.version - 1), repo)

        def files() -> Iterator[str]:
            # for master, consider unreleased change entries
            with repo.checkout_branch(master.dev_branch) as branch:
                yield from zip(
                    (
                        os.path.relpath(path, start=repo.directory)
                        for path in glob.iglob(
                            os.path.join(
                                repo.directory, "changelogs", CHANGE_ENTRIES_DIR, "*"
                            )
                        )
                    ),
                    itertools.repeat(branch),
                )

            # for latest iso, consider all change entries
            with repo.checkout_branch(latest_iso.dev_branch) as branch:
                yield from zip(
                    (
                        os.path.relpath(path, start=repo.directory)
                        for path in glob.iglob(
                            os.path.join(repo.directory, "changelogs", "*", "*")
                        )
                    ),
                    itertools.repeat(branch),
                )

        change_entries: Sequence[
            DistinctChangeEntry
        ] = cls._get_distinct_change_entries(files())
        for change_entry in change_entries:
            if master.dev_branch not in change_entry.found_branches:
                # This change entry was not found on master, not relevant for this search
                continue
            release_version: Optional[Version] = more_itertools.only(
                (version for version in change_entry.versions if version is not None),
                default=None,
                too_long=Exception(
                    f"Change entry found in multiple named version directories on branch {latest_iso.dev_branch}"
                ),
            )
            if release_version is None:
                # This change has not been released yet
                continue
            yield (change_entry.name, release_version)

    @classmethod
    def _get_distinct_change_entries(
        cls, paths: Iterable[Tuple[str, Branch]]
    ) -> Sequence["DistinctChangeEntry"]:
        """
        Returns a list of distinct change entries, given a list of paths to change entry files.
        Change entries are considered the same if their file names match and if their commit timestamps are not
        more than a week apart.
        This method does not check out branches. Instead it expects the appropriate branch to be checked out when consuming
        a path from the itererable.

        :param paths: Paths, relative to repo root, to the change entry files. Files are consumed one by one: a file is fully
            processed before the next path string is accessed, allowing for iterators over multiple branches.
        """
        change_entries: Dict[str, List[DistinctChangeEntry]] = defaultdict(list)
        path: str
        branch: Branch
        for path, branch in paths:
            abs_path: str = os.path.join(branch.repo.directory, path)
            filename: str = os.path.basename(path)
            if filename == GITKEEP_FILE:
                continue
            if os.path.isfile(abs_path):
                change_dir_name: str = os.path.basename(os.path.dirname(path))
                change_version: Optional[Version] = (
                    Version(change_dir_name)
                    if change_dir_name != "unreleased"
                    else None
                )
                change_entry: ChangeEntry = parse_change_entry(abs_path)
                timestamp_iso: str = (
                    util.subprocess_log(
                        subprocess.check_output,
                        [
                            "git",
                            "log",
                            "-1",
                            "--follow",
                            "--find-renames=100%",
                            "--diff-filter=A",
                            "--format=%cI",
                            "--",
                            path,
                        ],
                        logger=LOGGER,
                        cwd=branch.repo.directory,
                    )
                    .decode()
                    .strip()
                )
                timestamp: datetime = dateutil.parser.isoparse(timestamp_iso)
                # same object: change_entries[filename] will be updated
                distincts: List[DistinctChangeEntry] = change_entries[filename]
                for distinct in distincts:
                    if distinct.matches(
                        branch.branch,
                        filename,
                        change_entry,
                        timestamp,
                    ):
                        # this change entry is considered the same as `distinct`: add this occurrence to the instance
                        distinct.add(
                            branch.branch,
                            filename,
                            change_version,
                            change_entry,
                            timestamp,
                        )
                        break
                else:
                    # this change entry is considered distinct from all the ones in `distincts`: add it to the list
                    distincts.append(
                        DistinctChangeEntry.from_change_entry(
                            branch.branch,
                            filename,
                            change_version,
                            change_entry,
                            timestamp,
                        )
                    )
        return [
            distinct for distincts in change_entries.values() for distinct in distincts
        ]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ProductVersion):
            return (
                self.version == other.version
                and self.dev_branch == other.dev_branch
                and self.rc_branch == other.rc_branch
                and self.stable_branch == other.stable_branch
            )
        return NotImplemented

    def __getitem__(self, key: BuildType) -> str:
        try:
            return self._mapping[key]
        except KeyError:
            raise KeyError("Unknown build type %s" % key)

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)


# Change entries might get committed at different times to different branches (when additional changes are required for example)
# To take this into account, a timestamp range is required within which change entries with the same name are considered the
# same.
DISTINCT_CHANGE_ENTRY_TIME_RANGE: timedelta = timedelta(weeks=1)
D = TypeVar("D", bound="DistinctChangeEntry")


@dataclass
class DistinctChangeEntry:
    """
    Represents a distinct change entry accross branches. A change entry is considered distinct based on the file name and the
    timestamp of the commit where it was added.
    """

    name: str
    versions: Set[
        Optional[Version]
    ]  # release versions for this change entry, None for unreleased
    expected_branches: Set[str]
    found_branches: Set[str]
    first_timestamp: datetime
    last_timestamp: datetime

    def matches(
        self,
        branch: str,
        name: str,
        change_entry: ChangeEntry,
        timestamp: datetime,
    ) -> bool:
        """
        Returns true iff the change entry is considered the same as represented by this distinct change entry.
        """
        return (
            name == self.name
            and timestamp <= self.first_timestamp + DISTINCT_CHANGE_ENTRY_TIME_RANGE
            and timestamp >= self.last_timestamp - DISTINCT_CHANGE_ENTRY_TIME_RANGE
        )

    def add(
        self,
        branch: str,
        name: str,
        version: Version,
        change_entry: ChangeEntry,
        timestamp: datetime,
    ) -> None:
        if not self.matches(branch, name, change_entry, timestamp):
            raise ValueError(
                "Can not add change entry, it does not match this DistinctChangeEntry"
            )
        if branch in self.found_branches:
            raise Exception(
                f"Change entry {name} found twice on branch {branch} within the"
                " distinct change entry time range. This violates the assumption that both files represent the same change."
            )
        self.expected_branches.update(change_entry.destination_branches)
        self.found_branches.add(branch)
        self.versions.add(version)
        self.first_timestamp = (
            timestamp if timestamp < self.first_timestamp else self.first_timestamp
        )
        self.last_timestamp = (
            timestamp if timestamp > self.last_timestamp else self.last_timestamp
        )

    @classmethod
    def from_change_entry(
        cls: Type[D],
        branch: str,
        name: str,
        version: Version,
        change_entry: ChangeEntry,
        timestamp: datetime,
    ) -> D:
        return cls(
            name=name,
            versions={version},
            expected_branches=set(change_entry.destination_branches),
            found_branches={branch},
            first_timestamp=timestamp,
            last_timestamp=timestamp,
        )
