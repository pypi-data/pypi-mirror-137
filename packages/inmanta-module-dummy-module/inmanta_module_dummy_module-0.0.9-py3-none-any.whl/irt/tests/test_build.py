"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import glob
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Match, MutableMapping, Optional

import click.testing
import py
import pytest
import toml
from click.testing import CliRunner

from irt.main import build_python, clone_product_repos, publish_python
from irt.release import BuildType


def clone_dummy_product(
    runner: CliRunner, directory: str, branch: str = "master", debug: bool = False
) -> None:
    result: click.testing.Result = runner.invoke(
        clone_product_repos,
        [
            "--product-repo",
            "https://github.com/inmanta/dummy-inmanta-product.git",
            "--branch",
            branch,
            "--output",
            directory,
            "--token",
            os.environ["GITHUB_TOKEN"],
        ],
    )
    if debug:
        debug_runner_result(result)
    assert result.exit_code == 0


def build_product(
    runner: CliRunner,
    directory: str,
    build_type: BuildType = BuildType.dev,
    output_dir: Optional[str] = None,
    debug: bool = False,
) -> None:
    result: click.testing.Result = runner.invoke(
        build_python,
        [
            "--directory",
            directory,
            "--build-type",
            build_type.value,
            *([] if output_dir is None else ["--output-dir", output_dir]),
        ],
        catch_exceptions=False,
    )
    if debug:
        debug_runner_result(result)
    assert result.exit_code == 0


def debug_runner_result(result: click.testing.Result) -> None:
    print(
        f"Command exited with exit code {result.exit_code}, exception info: {result.exc_info}, stdout:"
    )
    print(result.stdout)


def publish_product(runner: CliRunner, directory: str, build_type: BuildType) -> None:
    result = runner.invoke(
        publish_python, ["--directory", directory, "--build-type", build_type.value]
    )
    assert result.exit_code == 0


def test_clone_product_repos(tmpdir: py.path.local):
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    cloned_repos = os.listdir(tmpdir)
    assert "dummy-inmanta-product" in cloned_repos
    assert "dummy-inmanta-extension-a" in cloned_repos


@pytest.mark.parametrize("build_type", iter(BuildType))
def test_build_python(tmpdir: py.path.local, build_type: BuildType):
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    build_product(runner, str(tmpdir), build_type=build_type)
    artifact_type: str = (
        ""
        if build_type == BuildType.stable
        else "rc"
        if build_type == BuildType.next
        else f".{build_type.value}"
    )
    for ext in ("whl", "tar.gz"):
        for project in os.listdir(tmpdir):
            assert (
                len(
                    glob.glob(
                        os.path.join(
                            str(tmpdir), project, "dist", f"*-*{artifact_type}*.{ext}"
                        )
                    )
                )
                == 1
            )


def test_build_python_prebuild_script(tmpdir: py.path.local):
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    product_dir: str = os.path.join(str(tmpdir), "dummy-inmanta-product")
    toml_file: str = os.path.join(product_dir, "pyproject.toml")
    toml_content: MutableMapping[str, object] = toml.load(toml_file)
    toml_content["tool"]["irt"]["build"] = {"python": {"hooks": {"pre": "pre-build.sh"}}}  # type: ignore
    with open(toml_file, "w+") as f:
        toml.dump(toml_content, f)
    script: str = os.path.join(product_dir, "pre-build.sh")
    with open(script, "w+") as f:
        f.write(
            """
#!/usr/bin/env sh

touch touch_file
            """.strip()
        )
    os.chmod(script, 0o700)

    touch_file: str = os.path.join(product_dir, "touch_file")
    assert not os.path.isfile(touch_file)
    build_product(
        runner, str(tmpdir), output_dir=os.path.join(str(tmpdir), "artifacts")
    )
    assert os.path.isfile(touch_file)


def test_build_python_env(tmpdir: py.path.local):
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    product_dir: str = os.path.join(str(tmpdir), "dummy-inmanta-product")
    toml_file: str = os.path.join(product_dir, "pyproject.toml")
    env_var: str = "COMPILE_CODE"
    toml_content: MutableMapping[str, object] = toml.load(toml_file)
    toml_content["tool"]["irt"]["build"] = {"python": {"env": {env_var: ""}}}  # type: ignore
    with open(toml_file, "w+") as f:
        toml.dump(toml_content, f)
    with open(os.path.join(product_dir, "setup.py"), "w") as f:
        f.write(
            f"""
import os
from pathlib import Path

if "{env_var}" in os.environ:
    Path("touch_file").touch()
            """.strip()
        )

    touch_file: str = os.path.join(product_dir, "touch_file")
    assert not os.path.isfile(touch_file)
    build_product(runner, str(tmpdir))
    assert os.path.isfile(touch_file)


@pytest.mark.parametrize(
    "python_versions", [[], ["python3.6"], ["python3.6", "python3.8"]]
)
def test_build_compiled_distribution(python_versions: List[str], tmpdir: py.path.local):
    runner = CliRunner()
    projects_dir = tmpdir.join("projects")
    product_dir: str = os.path.join(str(projects_dir), "test-product")
    os.makedirs(product_dir)
    with open(os.path.join(product_dir, "test.py"), "w") as f:
        f.write("")
    with open(os.path.join(product_dir, "setup.py"), "w") as f:
        f.write(
            """
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="test-project",
    ext_modules=cythonize("test.py"),
    setup_requires=["cython"],
)
            """.strip()
        )
    with open(os.path.join(product_dir, "requirements.setup.txt"), "w") as f:
        f.write("cython")
    toml_file: str = os.path.join(product_dir, "pyproject.toml")
    toml_content = {"tool": {"irt": {"build": {"python": {"dists": ["bdist_wheel"]}}}}}
    if python_versions:
        toml_content["tool"]["irt"]["build"]["python"][
            "python_versions"
        ] = python_versions
    with open(toml_file, "w+") as f:
        toml.dump(toml_content, f)
    output_dir = tmpdir.join("output")
    build_product(runner, str(projects_dir), output_dir=str(output_dir))
    if python_versions:
        assert len(os.listdir(output_dir)) == len(python_versions)
    else:
        # By default use python3 interpreter to build python packages
        assert len(os.listdir(output_dir)) == 1


def test_build_python_subprojects(tmpdir: py.path.local) -> None:
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    product_dir: str = os.path.join(str(tmpdir), "dummy-inmanta-product")
    subproject_dir: str = "subproject"
    toml_file: str = os.path.join(product_dir, "pyproject.toml")
    toml_content: MutableMapping[str, object] = toml.load(toml_file)
    toml_content["tool"]["irt"]["build"] = {  # type: ignore
        "python": {"subprojects": {"subproject": {"directory": subproject_dir}}}
    }
    with open(toml_file, "w+") as f:
        toml.dump(toml_content, f)
    subproject_src_dir: str = os.path.join(
        product_dir, subproject_dir, "src", "subproject"
    )
    os.makedirs(subproject_src_dir)
    with open(os.path.join(subproject_src_dir, "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(product_dir, subproject_dir, "setup.py"), "w") as f:
        f.write(
            """
import setuptools

setuptools.setup(
    version="1.0.0",
    python_requires=">=3.6",
    name="subproject",
    description="Sub project",
    author="Inmanta",
    author_email="code@inmanta.com",
    url="https://github.com/inmanta/dummy-inmanta-extension-a",
    license="Inmanta EULA",
    install_requires=[
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
)
            """.strip()
        )

    build_product(runner, str(tmpdir))
    assert len(glob.glob(os.path.join(product_dir, "dist", "subproject*"))) != 0


def test_build_python_bdist(tmpdir: py.path.local):
    runner = CliRunner()
    clone_dummy_product(runner, str(tmpdir))
    product_dir: str = os.path.join(str(tmpdir), "dummy-inmanta-product")
    toml_file: str = os.path.join(product_dir, "pyproject.toml")
    toml_content: MutableMapping[str, object] = toml.load(toml_file)
    toml_content["tool"]["irt"]["build"] = {"python": {"dists": ["bdist_wheel"]}}  # type: ignore
    with open(toml_file, "w+") as f:
        toml.dump(toml_content, f)
    build_product(runner, str(tmpdir))
    assert len(glob.glob(os.path.join(product_dir, "dist", "*.whl"))) == 1
    assert len(glob.glob(os.path.join(product_dir, "dist", "*.tar.gz"))) == 0


def test_build_python_output_dir(tmpdir: py.path.local):
    runner = CliRunner()
    projects_dir: str = os.path.join(str(tmpdir), "projects")
    clone_dummy_product(runner, projects_dir)
    build_product(
        runner, projects_dir, output_dir=os.path.join(str(tmpdir), "artifacts")
    )
    for ext in ("whl", "tar.gz"):
        assert len(
            glob.glob(os.path.join(str(tmpdir), "artifacts", f"*-*.dev*.{ext}"))
        ) == len(os.listdir(projects_dir))


@pytest.mark.parametrize(
    "build_type,with_toml,public",
    [
        *[
            (build_type, True, public)
            for build_type in (BuildType.dev, BuildType.next)
            for public in (True, False)
        ],
        *[(BuildType.dev, with_toml, None) for with_toml in (True, False)],
    ],
)
@pytest.mark.slow
def test_publish_python_devpi(
    tmpdir: py.path.local,
    build_type: BuildType,
    with_toml: bool,
    public: Optional[bool],
):
    """
    Test publishing Python packages. Only dev and next builds are tested: stable builds have the additional complexity of
    version conflicts and uploading to public repos when public == True.

    :param with_toml: pyproject.toml file present
    :param public: pyproject.toml tool.irt.publish.python.public value, if with_toml == True
    """
    runner = CliRunner()
    branch: str = (
        "master" if build_type.is_dev_release() else f"dummy-{build_type.value}"
    )
    clone_dummy_product(runner, str(tmpdir), branch=branch)
    build_product(runner, str(tmpdir), build_type=build_type)

    # force pyproject.toml config
    for project in os.listdir(tmpdir):
        toml_file: str = os.path.join(str(tmpdir), project, "pyproject.toml")
        if with_toml:
            Path(toml_file).touch()
            toml_content: MutableMapping[str, object] = toml.load(toml_file)
            if "tool" not in toml_content:
                toml_content["tool"] = {}
            if "irt" not in toml_content["tool"]:  # type: ignore
                toml_content["tool"]["irt"] = {}  # type: ignore
            toml_content["tool"]["irt"]["publish"] = {"python": {"public": public}}  # type: ignore
            with open(toml_file, "w+") as f:
                toml.dump(toml_content, f)
        else:
            try:
                os.remove(toml_file)
            except FileNotFoundError:
                pass

    def devpi_cli(*args: str) -> str:
        return subprocess.check_output([sys.executable, "-m", "devpi", *args]).decode()

    devpi_cli(
        "use", f"https://artifacts.internal.inmanta.com/inmanta/{build_type.value}"
    )

    def nb_published() -> int:
        count: int = 0
        for project in os.listdir(tmpdir):
            for wheel in glob.iglob(
                os.path.join(str(tmpdir), project, "dist", "*-py3-*.whl")
            ):
                match: Optional[Match] = re.search(
                    "(.*)-(.*)-py3-.*.whl", os.path.basename(wheel)
                )
                assert match is not None
                assert len(match.groups()) == 2
                lst: str = devpi_cli("list", "%s==%s" % (match[1], match[2]))
                if lst.strip() != "":
                    count += 1
        return count

    assert nb_published() == 0
    publish_product(runner, str(tmpdir), build_type)
    assert nb_published() == len(os.listdir(tmpdir))
