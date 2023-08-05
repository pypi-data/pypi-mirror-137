"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os
from subprocess import CalledProcessError
from typing import Optional

import click
import pytest

from irt import util
from irt.main import create_product_freeze_file
from irt.release.build import BuildType, FreezeFileGenerator


def run_create_freeze_file_command(
    product_dir: str,
    build_type: BuildType,
    github_token: str,
    output_file: Optional[str] = None,
) -> None:
    cli_runner = click.testing.CliRunner()
    extra_options = ["--output-file", output_file] if output_file else []
    result: click.testing.Result = cli_runner.invoke(
        create_product_freeze_file,
        [
            "--product-dir",
            product_dir,
            "--build-type",
            build_type.value,
            "--github-token",
            github_token,
            *extra_options,
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output


@pytest.mark.parametrize("set_output_file_option", [True, False])
def test_create_freeze_file_output_file_option(
    tmpdir,
    monkeypatch,
    dummy_product_repo: str,
    github_token: str,
    set_output_file_option: bool,
) -> None:
    """
    Ensure that the `--output-file` option works correctly whether it is set or not.
    """
    product_dir = os.path.join(tmpdir, "product-dir")
    util.clone_repo(
        dummy_product_repo,
        directory=product_dir,
        branch="iso3-stable",
        token=github_token,
    )
    os.chdir(tmpdir)
    if set_output_file_option:
        output_dir = os.path.join(tmpdir, "output-dir")
        os.makedirs(output_dir)
        freeze_file = os.path.join(output_dir, "other_file.txt")
    else:
        # Default location is relative the cwd
        freeze_file = os.path.join(tmpdir, "requirements.txt")

    assert not os.path.exists(freeze_file)
    if set_output_file_option:
        run_create_freeze_file_command(
            product_dir, BuildType.stable, github_token, output_file=freeze_file
        )
    else:
        run_create_freeze_file_command(
            product_dir, BuildType.stable, github_token, output_file=None
        )
    assert os.path.exists(freeze_file)
    with open(freeze_file, "r", encoding="utf-8") as fd:
        assert fd.read()


def test_freeze_file_generator_filtering_internal_dependencies(tmpdir) -> None:
    """
    Ensure that the internal dependencies are properly filtered out from the resulting freeze file.
    """
    product_directory = os.path.join(tmpdir, "product_dir")
    os.makedirs(product_directory, exist_ok=True)
    setup_py_file = os.path.join(product_directory, "setup.py")
    with open(setup_py_file, "w") as fd:
        fd.write(
            """
from setuptools import setup
setup(
    name='test',
    version='1.0',
    install_requires=['lorem', 'inmanta'],
)
        """
        )
    freeze_file_generator = FreezeFileGenerator(project_dir=product_directory)
    output_txt = os.path.join(tmpdir, "output.txt")
    freeze_file_generator.write_freeze_file_with_external_dependencies(output_txt)
    with open(output_txt, "r", encoding="utf-8") as fd:
        freeze_file_content = fd.read()
        assert "lorem" in freeze_file_content
        assert "inmanta" not in freeze_file_content


def test_freeze_file_generator_version_conflict(tmpdir) -> None:
    """
    Ensure that an exception is raised when a conflict exists between two version constraints.
    """
    product_directory = os.path.join(tmpdir, "product_dir")
    os.makedirs(product_directory, exist_ok=True)
    setup_py_file = os.path.join(product_directory, "setup.py")
    with open(setup_py_file, "w") as fd:
        fd.write(
            """
from setuptools import setup
setup(
    name='test',
    version='1.0',
    install_requires=['lorem > 0.1.0'],
)
        """
        )
    requirements_1_txt = os.path.join(tmpdir, "requirements_1.txt")
    with open(requirements_1_txt, "w", encoding="utf-8") as fd:
        fd.write("lorem < 0.1.0")
    freeze_file_generator = FreezeFileGenerator(
        project_dir=product_directory,
        min_c_constraint_files=[requirements_1_txt],
    )
    output_txt = os.path.join(tmpdir, "output.txt")
    with pytest.raises(CalledProcessError):
        freeze_file_generator.write_freeze_file_with_external_dependencies(output_txt)
