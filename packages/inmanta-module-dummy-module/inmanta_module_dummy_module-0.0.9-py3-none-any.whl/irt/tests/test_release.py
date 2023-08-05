"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import itertools
import os
import shutil
import subprocess
import uuid
from typing import List, Optional, Set, Tuple

import py
import pytest
from packaging.version import Version

from irt.changelog import CHANGE_ENTRIES_PATH, ChangeEntry
from irt.git import Branch, GitRepo, InvalidBranch
from irt.mergetool.config import MergeToolConfig
from irt.project import (
    ProductConfig,
    ProductDependenciesNpm,
    ProductProject,
    Project,
    ProjectConfig,
)
from irt.release import BuildType
from irt.release.release import (
    ComponentCollection,
    ComponentReleaseTool,
    ProductReleaseTool,
    ProductVersion,
    ReleasedComponent,
)
from irt.version import ChangeType, VersionBumpTool


class DummyRepo(GitRepo):
    def __init__(self, branches: Optional[Set[str]] = None) -> None:
        self.branches: Set[str] = branches if branches is not None else set()

    def get_all_branches(self) -> Set[str]:
        return self.branches


@pytest.fixture
def dummy_product_release_tool(
    dummy_product_repo: str, github_token: str, tmpdir: py.path.local
) -> ProductReleaseTool:
    return ProductReleaseTool(
        name="dummy-inmanta-product",
        repo_url=dummy_product_repo,
        dev_branch="master",
        working_dir=os.path.join(str(tmpdir), "release_tool_working_dir"),
        merge_tool_config=MergeToolConfig(
            repositories=["dummy-inmanta-product", "dummy-inmanta-extension-a"],
            dev_branches={ChangeType.PATCH: "iso3"},
            bot_responsibles=["inmantaci"],
        ),
        token=github_token,
    )


@pytest.fixture
def dummy_component_release_tool(
    dummy_extension_a_repo: str, github_token: str, tmpdir: py.path.local
) -> ComponentReleaseTool:
    return ComponentReleaseTool(
        name="dummy-inmanta-extension-a",
        repo_url=dummy_extension_a_repo,
        dev_branch="master",
        working_dir=os.path.join(str(tmpdir), "release_tool_working_dir"),
        token=github_token,
    )


def ensure_branch(repo: GitRepo, branch: str, base: str) -> None:
    try:
        with repo.checkout_branch(branch):
            pass
    except InvalidBranch:
        with repo.checkout_branch(branch, base_branch=base):
            pass


@pytest.mark.parametrize(
    "build_type, already_set, no_tag, no_egg_info, no_file",
    [
        *[(build_type, False, False, False, False) for build_type in BuildType],
        (BuildType.next, True, False, False, False),
        (BuildType.next, False, True, False, False),
        (BuildType.next, False, True, True, False),
        (BuildType.next, False, True, True, True),
    ],
)
def test_release_tool_set_tag_build(
    dummy_component_release_tool: ComponentReleaseTool,
    build_type: BuildType,
    already_set: bool,
    no_tag: bool,
    no_egg_info: bool,
    no_file: bool,
) -> None:
    """
    Later parameters take precedence over earlier ones.
    """

    def setup_cfg_file(
        tag: str, no_tag: bool = False, no_egg_info: bool = False
    ) -> str:
        if no_egg_info:
            return ""
        if no_tag:
            return "[egg_info]"
        return f"""
[egg_info]
tag_build ={(" " + tag) if tag else ""}
        """.strip()

    correct_tag: str = (
        ".dev0"
        if build_type == BuildType.dev
        else "rc"
        if build_type == BuildType.next
        else ""
    )
    repo: GitRepo = dummy_component_release_tool.repo
    ensure_branch(repo, dummy_component_release_tool.version[build_type], "master")
    setup_cfg_path: str = os.path.join(repo.directory, "setup.cfg")

    # write setup.cfg
    with repo.checkout_branch(
        dummy_component_release_tool.version[build_type]
    ) as branch:
        if no_file:
            if os.path.exists(setup_cfg_path):
                os.remove(setup_cfg_path)
                branch.commit("Removed setup.cfg")
        else:
            with open(setup_cfg_path, "w") as f:
                f.write(
                    setup_cfg_file(
                        correct_tag if already_set else "something", no_tag, no_egg_info
                    )
                )
            branch.commit("Set up setup.cfg")

    # make sure some branch is aligned
    aligned: ProductVersion = ProductVersion(
        f"iso{dummy_component_release_tool.master.version + 1}", repo
    )
    # create the dev branch first because _fast_forward_aligned reasons on those to determine all versions
    with repo.checkout_branch(
        aligned.dev_branch, base_branch=dummy_component_release_tool.version.dev_branch
    ):
        pass
    ensure_branch(
        repo, aligned[build_type], dummy_component_release_tool.version[build_type]
    )

    # set tag_build
    dummy_component_release_tool._set_tag_build(build_type)

    # read setup.cfg
    with repo.checkout_branch(
        dummy_component_release_tool.version[build_type]
    ) as branch:
        with open(setup_cfg_path, "r") as f:
            assert f.read().strip() == setup_cfg_file(correct_tag)

    # verify change has been fast-forwarded to aligned branches
    assert repo.get_branch_head(aligned[build_type]) == repo.get_branch_head(
        dummy_component_release_tool.version[build_type]
    )


@pytest.mark.parametrize("build_type", iter(BuildType))
def test_get_component_release_tools(
    dummy_product_release_tool: ProductReleaseTool,
    build_type: BuildType,
) -> None:
    component_release_tools: ComponentCollection[
        Tuple[str, ComponentReleaseTool]
    ] = dummy_product_release_tool._get_component_release_tools("master")
    extension: str = "dummy-inmanta-extension-a"
    component_release_tools.core[0] == extension
    extension_release_tool: ComponentReleaseTool = component_release_tools.core[1]
    assert extension_release_tool.name == extension
    assert extension_release_tool.master == dummy_product_release_tool.master
    assert extension_release_tool.version == dummy_product_release_tool.version


@pytest.mark.parametrize("build_type", (BuildType.next, BuildType.stable))
def test_release_tool_pin_npm(
    dummy_product_release_tool: ProductReleaseTool, build_type: BuildType
) -> None:
    components: List[ReleasedComponent] = [
        ReleasedComponent(
            name="component-a",
            version=Version("1.1.1"),
            release_tool=None,
        ),
        ReleasedComponent(
            name="component-b",
            version=Version("2.2.2"),
            release_tool=None,
        ),
    ]
    repo: GitRepo = dummy_product_release_tool.repo
    ensure_branch(
        repo,
        dummy_product_release_tool.version.rc_branch,
        "master",
    )

    with repo.checkout_branch(dummy_product_release_tool.version.rc_branch) as branch:
        project: ProductProject = ProductProject(repo.directory)
        config: ProductConfig = project.get_project_config()
        config.dependencies.npm = {
            "component-a": ProductDependenciesNpm(repo="repo-a", version="master"),
            "component-b": ProductDependenciesNpm(repo="repo-b", version="~=1.0.dev"),
        }
        project.write_project_config(config)
        branch.commit("Set up dependencies")

    dummy_product_release_tool._pin_npm(build_type, components)

    with repo.checkout_branch(dummy_product_release_tool.version.rc_branch) as branch:
        project = ProductProject(repo.directory)
        config = project.get_project_config()
        constraint, suffix = (
            ("~=", ".0rc") if build_type == BuildType.next else ("==", "")
        )
        assert config.dependencies.npm == {
            "component-a": ProductDependenciesNpm(
                repo="repo-a", version=f"{constraint}1.1.1{suffix}"
            ),
            "component-b": ProductDependenciesNpm(
                repo="repo-b", version=f"{constraint}2.2.2{suffix}"
            ),
        }


@pytest.mark.parametrize("build_type", (BuildType.next, BuildType.stable))
def test_release_tool_pin_python(
    dummy_product_release_tool: ProductReleaseTool, build_type: BuildType
) -> None:
    components: List[ReleasedComponent] = [
        ReleasedComponent(
            name="component-a",
            version=Version("1.1.1"),
            release_tool=None,
        ),
        ReleasedComponent(
            name="component-b",
            version=Version("2.2.2"),
            release_tool=None,
        ),
    ]

    def setup_file(constraint_a: str, constraint_b: str) -> str:
        return f"""
import setuptools


component_b = "{constraint_b}"


setuptools.setup(
    version="1.1.1",
    python_requires=">=3.6",
    name="dummy-inmanta-product",
    description="Dummy product to test build and release tools (irt) against",
    author="Inmanta",
    author_email="code@inmanta.com",
    url="https://github.com/inmanta/dummy-inmanta-product",
    license="Inmanta EULA",
    install_requires=[
        "{constraint_a}",
        component_b,
    ],
    package_dir={{"": "src"}},
    packages=setuptools.find_packages("src"),
    entry_points={{
        "console_scripts": [
            "dummy-inmanta-product = dummy_inmanta_product:welcome",
        ],
    }},
)
        """.strip()

    ensure_branch(
        dummy_product_release_tool.repo,
        dummy_product_release_tool.version.rc_branch,
        "master",
    )
    with dummy_product_release_tool.repo.checkout_branch(
        dummy_product_release_tool.version.rc_branch
    ) as branch:
        with open(
            os.path.join(dummy_product_release_tool.repo.directory, "setup.py"), "w"
        ) as f:
            f.write(setup_file("component-a>=1.0.0.dev", "component-b~=2.0.dev"))
        branch.commit("commit")
    dummy_product_release_tool._pin_python(build_type, components)
    with dummy_product_release_tool.repo.checkout_branch(
        dummy_product_release_tool.version.rc_branch
    ) as branch:
        with open(
            os.path.join(dummy_product_release_tool.repo.directory, "setup.py"), "r"
        ) as f:
            constraint, suffix = (
                ("~=", ".0rc") if build_type == BuildType.next else ("==", "")
            )
            assert f.read().strip() == setup_file(
                f"component-a{constraint}1.1.1{suffix}",
                f"component-b{constraint}2.2.2{suffix}",
            )


def test_release_tool_pin_rpm(dummy_product_release_tool: ProductReleaseTool) -> None:
    repo: GitRepo = dummy_product_release_tool.repo
    ensure_branch(
        repo,
        dummy_product_release_tool.version.rc_branch,
        "master",
    )
    components: List[ReleasedComponent] = [
        ReleasedComponent(
            name="component-a",
            version=Version("1.1.1"),
            release_tool=None,
        ),
        ReleasedComponent(
            name="component-b",
            version=Version("2.2.2"),
            release_tool=None,
        ),
    ]

    def spec_file(constraint_a: str, constraint_b: str) -> str:
        return f"""
Requires:  python3-component-a {constraint_a}
Requires:  python3-component-b {constraint_b}

BuildRequires:  python3-component-a {constraint_a}
BuildRequires:  python3-component-a-server {constraint_a}
BuildRequires:  python3-component-b {constraint_b}
        """.strip()

    with repo.checkout_branch(dummy_product_release_tool.version.rc_branch) as branch:
        with open(os.path.join(repo.directory, "inmanta.spec"), "w") as f:
            f.write(spec_file("< 2020.5.0", "= 2020.4.1"))
        branch.commit("commit")
    dummy_product_release_tool._pin_rpm(components)
    with repo.checkout_branch(dummy_product_release_tool.version.rc_branch) as branch:
        with open(os.path.join(repo.directory, "inmanta.spec"), "r") as f:
            assert f.read().strip() == spec_file("= 1.1.1", "= 2.2.2")


@pytest.mark.parametrize(
    "fast_forward, explicit_head",
    [(False, False), (True, False), (True, True)],
)
def test_release_tool_merge(
    dummy_component_release_tool: ComponentReleaseTool,
    dummy_extension_a_repo: str,
    fast_forward: bool,
    explicit_head: bool,
) -> None:
    repo: GitRepo = dummy_component_release_tool.repo
    master: ProductVersion = dummy_component_release_tool.master
    dummy_component_release_tool.version = ProductVersion(
        f"iso{master.version + 1}", repo
    )

    def apply_change(branch: Branch) -> None:
        with open(os.path.join(repo.directory, "somefile"), "w") as f:
            f.write(str(uuid.uuid4()))
        branch.commit("my commit")

    # Create some aligned and some diverged dev branches
    with repo.checkout_branch(
        f"iso{master.version + 1}", base_branch="master"
    ) as branch:
        apply_change(branch)
    with repo.checkout_branch(
        f"iso{master.version + 2}", base_branch=f"iso{master.version + 1}"
    ):
        pass
    with repo.checkout_branch(
        f"iso{master.version + 3}", base_branch=f"iso{master.version + 1}"
    ):
        pass
    with repo.checkout_branch(f"iso{master.version + 4}", base_branch="master"):
        pass

    # add a commit to one of the next branches
    with repo.checkout_branch(
        f"iso{master.version + 1}-next", base_branch="master"
    ) as branch:
        apply_change(branch)
    # one of the other next branches exists already but doesn't have the change yet
    with repo.checkout_branch(f"iso{master.version + 2}-next", base_branch="master"):
        pass

    head_prior: Optional[str] = repo.get_branch_head(f"iso{master.version + 1}-next")
    assert head_prior is not None
    aligned: List[str] = [f"iso{master.version + i}-next" for i in range(2, 4)]
    if fast_forward:
        ref_head: Optional[str]
        if explicit_head:
            ref_head = repo.get_branch_head(f"iso{master.version + 1}")
            assert ref_head is not None
            with repo.checkout_branch(f"iso{master.version + 1}") as branch:
                apply_change(branch)
        else:
            ref_head = None
        result: Set[str] = dummy_component_release_tool._fast_forward_aligned(
            reference=BuildType.dev,
            merge=BuildType.next,
            reference_head=ref_head,
        )
        assert set(aligned) == result
    else:
        result: Set[str] = dummy_component_release_tool._merge(
            source=BuildType.dev,
            target=BuildType.next,
        )
        assert {f"iso{master.version + 1}-next"}.union(set(aligned)) == result

    head: Optional[str] = repo.get_branch_head(f"iso{master.version + 1}-next")
    assert head is not None
    for branch_name in aligned:
        assert repo.get_branch_head(branch_name) == head
    assert repo.get_branch_head(f"iso{master.version + 4}-next") != head
    assert (head == head_prior) == fast_forward


@pytest.mark.parametrize("iso5_exists", [True, False])
def test_product_version(iso5_exists: bool) -> None:
    repo: DummyRepo = DummyRepo(
        {
            "master",
            "iso4",
            *(["iso5-next"] if iso5_exists else []),
            "iso4-next",
            "iso4-stable",
            "issue/feature-branch",
            "other-branch",
        }
    )
    master: ProductVersion = ProductVersion("master", repo)
    iso4: ProductVersion = ProductVersion("iso4", repo)

    assert master == ProductVersion("master", repo)

    assert master.dev_branch == "master"
    assert master.rc_branch == "iso5-next"
    assert master.stable_branch == "iso5-stable"

    assert iso4.dev_branch == "iso4"
    assert iso4.rc_branch == "iso4-next"
    assert iso4.stable_branch == "iso4-stable"


def test_product_version_highest_next() -> None:
    repo: DummyRepo = DummyRepo(
        {
            "master",
            "iso3",
            "iso5-next",
        }
    )
    master: ProductVersion = ProductVersion("master", repo)
    assert master.dev_branch == "master"
    assert master.rc_branch == "iso5-next"


def test_product_version_mapping() -> None:
    repo: DummyRepo = DummyRepo(
        {
            "master",
            "iso3",
            "iso5-next",
        }
    )
    master: ProductVersion = ProductVersion("master", repo)
    assert len(master) == len(BuildType)
    assert master[BuildType.dev] == master.dev_branch
    assert master[BuildType.next] == master.rc_branch
    assert master[BuildType.stable] == master.stable_branch


def test_product_version_verify_alignment(
    dummy_extension_a_repo: str, github_token: str, tmpdir: py.path.local
) -> None:
    # clone existing repo so we don't need to set up project config and versioning
    repo: GitRepo = GitRepo(dummy_extension_a_repo, str(tmpdir), github_token)
    version_bump_tool: VersionBumpTool
    with repo.checkout_branch("master"):
        config: ProjectConfig = Project(repo.directory).get_project_config()
        version_bump_tool = config.version_bump.tool.get_tool(repo.directory)

    # start from a clean slate: reset all iso branches to master
    product_versions: List[ProductVersion] = list(ProductVersion.get_all_versions(repo))
    highest_version: int = max(
        (product_version.version for product_version in product_versions), default=0
    )
    for product_version, build_type in itertools.product(product_versions, BuildType):
        subprocess.check_call(
            ["git", "checkout", "-B", product_version[build_type], "master"],
            cwd=repo.directory,
        )

    # create working branches
    setup_branch: str = str(uuid.uuid4())
    iso1_branch: str = f"iso{highest_version + 1}"
    iso2_branch: str = f"iso{highest_version + 2}"
    with repo.checkout_branch(setup_branch, base_branch="master") as branch:
        version_bump_tool.set_version(Version("0.1.1"))
        branch.commit("diverge from master")
    for branch_name in (iso1_branch, iso2_branch):
        with repo.checkout_branch(branch_name, base_branch=setup_branch):
            pass
    iso1: ProductVersion = ProductVersion(iso1_branch, repo)
    iso2: ProductVersion = ProductVersion(iso2_branch, repo)

    def verify(build_type: BuildType) -> None:
        # assert initial state is good
        assert len(list(ProductVersion.verify_version_alignment(repo))) == 0
        # diverge without bumping version
        with repo.checkout_branch(iso1[build_type]) as branch:
            with open(os.path.join(repo.directory, str(uuid.uuid4())), "w") as f:
                f.write("Hello World!")
            branch.commit("diverge from iso2")
        # assert violation is detected
        assert list(ProductVersion.verify_version_alignment(repo)) == [
            (Version("0.1.1"), {iso1[build_type], iso2[build_type]})
        ]
        # fix issue
        repo.fast_forward(target=iso2[build_type], source=iso1[build_type])
        # assert violation is gone
        assert len(list(ProductVersion.verify_version_alignment(repo))) == 0
        # diverge, bumping version
        with repo.checkout_branch(iso1[build_type]) as branch:
            version_bump_tool.bump(ChangeType.PATCH)
            branch.commit("diverge from iso2 with version bump")
        # assert no violations detected
        assert len(list(ProductVersion.verify_version_alignment(repo))) == 0

    # before creating next and stable branches, make sure the method can handle their absence
    verify(BuildType.dev)

    # make sure the method handles next and stable branches too
    for build_type in (BuildType.next, BuildType.stable):
        for product_version in (iso1, iso2):
            with repo.checkout_branch(
                product_version[build_type], base_branch=setup_branch
            ):
                pass
        verify(build_type)


def test_product_version_verify_change_entries(
    dummy_extension_a_repo: str, github_token: str, tmpdir: py.path.local
) -> None:
    # clone existing repo so we don't need to set up project config and versioning
    repo: GitRepo = GitRepo(dummy_extension_a_repo, str(tmpdir), github_token)

    # start from a clean slate: remove all change entries
    product_versions: List[ProductVersion] = list(ProductVersion.get_all_versions(repo))
    highest_version: int = max(
        (product_version.version for product_version in product_versions), default=0
    )
    change_entries_dir: str = os.path.join(repo.directory, CHANGE_ENTRIES_PATH)
    for product_version in product_versions:
        with repo.checkout_branch(product_version.dev_branch) as branch:
            shutil.rmtree(change_entries_dir)
            branch.commit("Cleanup")

    # create working branches
    iso1_branch: str = f"iso{highest_version + 1}"
    iso2_branch: str = f"iso{highest_version + 2}"
    with repo.checkout_branch(iso1_branch, base_branch="master"):
        pass
    with repo.checkout_branch(iso2_branch, base_branch="master"):
        pass
    iso1: ProductVersion = ProductVersion(iso1_branch, repo)
    iso2: ProductVersion = ProductVersion(iso2_branch, repo)

    # assert initial state is good
    assert len(list(ProductVersion.verify_change_entries(repo))) == 0

    # add some valid change entries
    with repo.checkout_branch(iso1.dev_branch) as branch:
        os.mkdir(change_entries_dir)
        ChangeEntry(
            description="iso1 only",
            change_type=ChangeType.PATCH,
            destination_branches=[iso1.dev_branch],
        ).write(os.path.join(change_entries_dir, "iso1-only.yml"))
        branch.commit("iso1 only")

        ChangeEntry(
            description="iso1 and iso2",
            change_type=ChangeType.PATCH,
            destination_branches=[iso1.dev_branch, iso2.dev_branch],
        ).write(os.path.join(change_entries_dir, "iso1-iso2.yml"))
        branch.commit("iso1 and iso2")

    shared_commit: Optional[str] = repo.get_branch_head(iso1.dev_branch)
    assert shared_commit is not None
    repo.cherry_pick(target=iso2.dev_branch, commits=[shared_commit])

    # assert state is still good
    assert len(list(ProductVersion.verify_change_entries(repo))) == 0

    # Add an invalid change entry
    with repo.checkout_branch(iso1.dev_branch) as branch:
        ChangeEntry(
            description="another iso1 and iso2",
            change_type=ChangeType.PATCH,
            destination_branches=[iso1.dev_branch, iso2.dev_branch],
        ).write(os.path.join(change_entries_dir, "another-iso1-iso2.yml"))
        branch.commit("another iso1 and iso2")

    # assert method returns correct results
    assert list(ProductVersion.verify_change_entries(repo)) == [
        ("another-iso1-iso2.yml", {iso2.dev_branch})
    ]
