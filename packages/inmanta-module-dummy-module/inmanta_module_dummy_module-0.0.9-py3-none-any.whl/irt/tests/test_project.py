"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import os

import pytest
from click.testing import CliRunner, Result

from irt.git import git_repo
from irt.main import query_toml_file
from irt.project import ProductConfig, ProductDependencies, ProductProject


def test_read_write_project_config(dummy_product_repo: str, github_token: str) -> None:
    with git_repo(dummy_product_repo, github_token) as repo:
        product: ProductProject = ProductProject(repo.directory)
        config: ProductConfig = product.get_project_config(fill_placeholders=False)
        alt_config: ProductConfig = config.copy(deep=True)
        alt_config.dependencies.extensions["my-extension"] = "my-extension-repo"
        product.write_project_config(alt_config)
        assert alt_config != config
        persisted_config: ProductConfig = product.get_project_config()
        assert persisted_config != config
        assert persisted_config == alt_config


def test_get_core_component(capsys):
    url_core_component = "https://github.com/inmanta/inmanta-core.git"
    warning_message = (
        "The field tool.irt.dependencies.additional-python-dependencies is deprecated"
    )

    # Only additional_python_dependencies field is set
    config = {"additional-python-dependencies": {"core": url_core_component}}
    product_dependencies = ProductDependencies(**config)
    assert warning_message not in capsys.readouterr().err
    assert product_dependencies.get_core_component() == ("core", url_core_component)
    assert warning_message in capsys.readouterr().err

    # Only core_component field is set
    config = {"core-component": url_core_component}
    product_dependencies = ProductDependencies(**config)
    assert product_dependencies.get_core_component() == (
        "inmanta-core",
        url_core_component,
    )
    assert warning_message not in capsys.readouterr().err

    # additional_python_dependencies and core_component field are set at the same time
    config = {
        "core-component": url_core_component,
        "additional-python-dependencies": {"core": url_core_component},
    }
    with pytest.raises(Exception):
        ProductDependencies(**config)

    # additional_python_dependencies and core_component field both not set
    with pytest.raises(Exception):
        ProductDependencies()


def test_query_toml(dummy_product_repo: str, github_token: str, capsys) -> None:
    """
    Test the `query-toml-file` command.
    """
    cli_runner = CliRunner()
    with git_repo(dummy_product_repo, github_token) as repo:
        path_pyproject_toml = os.path.join(repo.directory, "pyproject.toml")
        # Clear stdout/stderr buffer
        capsys.readouterr()
        result: Result = cli_runner.invoke(
            query_toml_file,
            args=[
                "--file",
                path_pyproject_toml,
                "--query",
                "tool.irt.build.rpm.python_version",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "python3.9" == result.output
        # Pass a non-existing option
        query = "tool.irt.build.rpm.non_existing_option"
        result: Result = cli_runner.invoke(
            query_toml_file,
            args=["--file", path_pyproject_toml, "--query", query],
            catch_exceptions=False,
        )
        assert result.exit_code != 0
        assert (
            f"Option `non_existing_option` from query `{query}` not found"
            in result.output
        )
