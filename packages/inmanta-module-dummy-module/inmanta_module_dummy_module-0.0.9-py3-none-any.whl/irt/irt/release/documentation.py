"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import itertools
import logging
import os
import shutil
import subprocess
from typing import Dict, List, Optional

from irt import modules, release, util
from irt.changelog import RENDERED_CHANGELOG_FILE, ComposedChangelog
from irt.module_sources import ModuleData, ModuleSourceManager
from irt.modules import ModuleSetDefinition
from irt.project import ProductConfig, ProductProject
from irt.release import BuildType

LOGGER = logging.getLogger(__name__)


def generate_module_documentation(
    python_path: str,
    module_set: str,
    source_dir: str,
    docs_build_dir: str,
    set_dir: str,
) -> None:
    """
    Generate documentation from the modules in the given set and write it in the core docs.
    """
    LOGGER.info("Adding module documentation to %s", docs_build_dir)

    set_def: modules.ModuleSetDefinition
    set_def, module_dict, _ = modules.load_modules(module_set, source_dir)
    generate_docs_from_set(docs_build_dir, module_dict, python_path, set_def, set_dir)


def generate_docs_from_set(
    docs_build_dir: str,
    module_set: Dict[str, ModuleData],
    python_path: str,
    set_def: modules.ModuleSetDefinition,
    set_dir: str,
) -> None:
    out_dir = os.path.join(docs_build_dir, "reference", "modules")
    util.ensure_empty_dir(out_dir)
    extra_dict = set_def.extra_modules
    set_dir = os.path.abspath(set_dir)
    mod_guides = os.path.join(docs_build_dir, "moduleguides")
    if os.path.exists(mod_guides) and len(os.listdir(mod_guides)) > 0:
        shutil.rmtree(mod_guides)
    for name, module in module_set.items():
        out_file = os.path.join(out_dir, name + ".rst")
        extra_modules = extra_dict.get(name, [])
        _generate_module_documentation(
            python_path, set_dir, name, extra_modules, module["url"], out_file
        )

        module_dir = os.path.join(set_dir, name, "docs")
        if os.path.exists(module_dir) and os.path.isdir(module_dir):
            # check if index.rst exists
            if os.path.exists(os.path.join(module_dir, "index.rst")):
                shutil.copytree(module_dir, os.path.join(mod_guides, name))
            else:
                LOGGER.warning("index.rst needs to exist in docs dir %s", module_dir)


def _generate_module_documentation(
    python_path: str,
    module_repo: str,
    module: str,
    extra_modules: List[str],
    source_repo: str,
    out_file: str,
) -> None:
    LOGGER.info("Generating documentation for module %s", module)
    cmd = [
        python_path,
        "-m",
        "sphinxcontrib.inmanta.api",
        "--module_repo",
        module_repo,
        "--module",
        module,
        "--source-repo",
        source_repo,
        "--file",
        out_file,
    ]

    for em in extra_modules:
        cmd.append("-m")
        cmd.append(em)

    util.subprocess_log(subprocess.check_output, cmd, logger=LOGGER)


def build_docs(
    product_repo: str,
    branch: str,
    build_type: BuildType,
    output_dir: str,
    github_token: str,
    sources: ModuleSourceManager,
    module_set: Optional[str],
) -> str:
    os.environ[
        "PIP_INDEX_URL"
    ] = f"https://artifacts.internal.inmanta.com/inmanta/{build_type.value}"
    os.makedirs(output_dir, exist_ok=True)
    if os.listdir(output_dir):
        raise Exception(f"output directory {output_dir} is not empty")

    # Clone product repo
    product_directory = os.path.join(output_dir, "product_repo")
    util.clone_repo(product_repo, product_directory, branch, github_token)
    product_config = ProductProject(product_directory).get_project_config()

    # Clone documentation repo
    documentation_repo = product_config.documentation.documentation_repo
    documentation_proj_dir = os.path.join(output_dir, "documentation_repo")
    if documentation_repo is None:
        shutil.copytree(product_directory, documentation_proj_dir)
    else:
        util.clone_repo(
            documentation_repo, documentation_proj_dir, branch, github_token
        )

    # Clone documentation base repo
    documentation_base_repo = product_config.documentation.documentation_base_repo
    documentation_base_proj_dir: Optional[str]
    if documentation_base_repo is not None:
        documentation_base_proj_dir = os.path.join(
            output_dir, "documentation_base_repo"
        )
        util.clone_repo(
            documentation_base_repo, documentation_base_proj_dir, branch, github_token
        )
    else:
        documentation_base_proj_dir = None

    # Clone core-component
    core_component_dir = os.path.join(output_dir, "core_component")
    util.clone_repo(
        url=product_config.dependencies.get_core_component()[1],
        directory=core_component_dir,
        branch=branch,
        token=github_token,
    )

    # Clone extension repos
    extension_repos_dir = os.path.join(output_dir, "extensions_repos")
    ext_name_to_clone_dir: Dict[str, str] = util.clone_multiple_repos(
        repos=dict(product_config.dependencies.extensions),
        output_dir=extension_repos_dir,
        branch=branch,
        token=github_token,
    )

    # Clone UI component repos
    ui_repos_dir = os.path.join(output_dir, "ui_repos")
    ui_name_to_clone_dir: Dict[str, str] = util.clone_multiple_repos(
        repos={
            ui_name: npm_dependency.repo
            for ui_name, npm_dependency in product_config.dependencies.npm.items()
        },
        output_dir=ui_repos_dir,
        branch=branch,
        token=github_token,
    )

    # Clone module set repo
    module_set_dir = os.path.join(output_dir, "module_set_repo")
    module_set_file = product_config.module_set.clone_module_set_repo(
        clone_dir=module_set_dir,
        branch="master",
        token=github_token,
        module_set_def_file_path=module_set,
    )

    # Determine directory where docs will be built
    if documentation_base_proj_dir is not None:
        docs_build_dir = os.path.join(documentation_base_proj_dir, "docs")
        merge_docs_to_base_docs(documentation_proj_dir, documentation_base_proj_dir)
    else:
        docs_build_dir = os.path.join(documentation_proj_dir, "docs")

    python_path = _setup_venv_for_docs_build(
        product_directory,
        documentation_proj_dir,
        documentation_base_proj_dir,
        build_type,
        output_dir,
    )

    # Add docs dir of each extension to the output directory
    add_extension_documentation(extension_repos_dir, docs_build_dir)

    # Add module documentation
    _add_module_set_documentation(
        python_path,
        docs_build_dir,
        module_set_file,
        output_dir,
        sources,
    )

    # Copy changelog file from the root of the project to the docs directory
    changelog_file_in_product_repo = os.path.join(
        product_directory, RENDERED_CHANGELOG_FILE
    )
    changelog_file_in_docs_dir = shutil.copy(
        changelog_file_in_product_repo, docs_build_dir
    )
    if not build_type.is_stable_release():
        # Add changelog entries for unreleased changes to the rendered changelog file
        composed_changelog = ComposedChangelog.from_checked_out_repositories(
            product_dir=product_directory,
            core_dir=core_component_dir,
            ext_name_to_dir=dict(ext_name_to_clone_dir),
            ui_name_to_dir=dict(ui_name_to_clone_dir),
        )
        composed_changelog.write(changelog_file_in_docs_dir)

    # Compile documentation
    docs_version = _compile_docs_to_html(python_path, product_directory, docs_build_dir)

    # Create tar archive
    html_dir = os.path.join(docs_build_dir, "build/html")
    product_name = util.get_name_python_project(product_directory)
    tar_file = os.path.join(output_dir, f"{product_name}-{docs_version}.tar.bz2")
    cmd = ["tar", "-C", html_dir, "-cvjf", tar_file, "."]
    LOGGER.info("Package documentation in tar archive %s", tar_file)
    util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)
    return tar_file


def _setup_venv_for_docs_build(
    product_directory: str,
    documentation_proj_dir: str,
    documentation_base_proj_dir: Optional[str],
    build_type: BuildType,
    working_dir: str,
) -> str:
    python_path = util.ensure_tmp_env(working_dir)
    bin_dir = python_path.rsplit("/", maxsplit=1)[0]
    pip_path = os.path.join(bin_dir, "pip")
    util.subprocess_log(
        subprocess.check_call, [pip_path, "install", "-U", "pip"], logger=LOGGER
    )
    requirements_files = util.get_requirements_files(documentation_proj_dir)
    if documentation_base_proj_dir is not None:
        requirements_files.extend(
            util.get_requirements_files(documentation_base_proj_dir)
        )
    min_r_cmd = list(
        itertools.chain.from_iterable(["-r", lf] for lf in requirements_files)
    )
    version_constraint_on_product = release.get_version_constraint_on_product(
        product_directory, build_type
    )
    # Install product in venv
    cmd_install_product = (
        [pip_path, "install"] + min_r_cmd + [version_constraint_on_product]
    )
    LOGGER.debug("Creating venv for docs build")
    util.subprocess_log(subprocess.check_call, cmd_install_product, logger=LOGGER)
    return python_path


def _compile_docs_to_html(
    python_path: str, product_directory: str, docs_build_dir: str
) -> str:
    # Ensure that the make command uses the correct python interpreter
    bin_dir = os.path.abspath(os.path.dirname(python_path))
    env_vars = os.environ.copy()
    env_vars["PATH"] = f"{bin_dir}:{env_vars['PATH']}"
    # Run compile
    LOGGER.info("Building documentation in %s", docs_build_dir)
    util.subprocess_log(
        subprocess.check_call,
        ["make", "clean"],
        logger=LOGGER,
        cwd=docs_build_dir,
        env=env_vars,
    )
    util.subprocess_log(
        subprocess.check_call,
        ["make", "html"],
        logger=LOGGER,
        cwd=docs_build_dir,
        env=env_vars,
    )
    # Return version of documentation
    package_name = util.get_name_python_project(product_directory)
    cmd = [os.path.join(bin_dir, "pip"), "show", package_name]
    output = util.subprocess_log(subprocess.check_output, cmd, logger=LOGGER).decode()
    output_filtered = [
        line for line in output.split("\n") if line.startswith("Version:")
    ]
    assert len(output_filtered) == 1, output_filtered
    version_line = output_filtered[0]
    return version_line.split(":", maxsplit=1)[1].strip()


def _add_module_set_documentation(
    python_path: str,
    docs_build_dir: str,
    module_set_file: str,
    working_dir: str,
    sources: ModuleSourceManager,
) -> None:
    LOGGER.info("Adding module set documentation")
    modules_dir = os.path.join(working_dir, "modules")

    module_set_defintion = ModuleSetDefinition.from_file(module_set_file)

    mods = modules.download_set(
        python_path,
        module_set_defintion,
        sources,
        modules_dir,
    )

    generate_docs_from_set(
        docs_build_dir,
        mods,
        python_path,
        module_set_defintion,
        modules_dir,
    )


def merge_docs_to_base_docs(project_path: str, base_project_path: str) -> None:
    """
    Override docs files from `base_project_path` with files from `project_path`.
    """
    docs_dir_base_proj = os.path.join(base_project_path, "docs")
    # make copy of sphinx conf so that it can be imported when overwritten by next step.
    shutil.copyfile(
        *(os.path.join(docs_dir_base_proj, f) for f in ("conf.py", "conf_core.py"))
    )

    # Copy docs directory of project_path over the docs directory of base_project_path in output directory
    # This will:
    #   1) Add additional documentation
    #   2) Override parts of the core documentation when same filename is used.
    docs_dir_proj = os.path.join(project_path, "docs")
    for (dirpath, dirnames, filenames) in os.walk(docs_dir_proj):
        for current_dir in dirnames:
            src_dir = os.path.join(dirpath, current_dir)
            dst_dir = os.path.join(
                docs_dir_base_proj,
                dirpath[len(docs_dir_proj) :].strip("/"),
                current_dir,
            )
            if not os.path.exists(dst_dir):
                shutil.copytree(src_dir, dst_dir)
                # Stop the recursion
                dirnames.remove(current_dir)

        for current_file in filenames:
            src_file = os.path.join(dirpath, current_file)
            dst_file = os.path.join(
                docs_dir_base_proj,
                dirpath[len(docs_dir_proj) :].strip("/"),
                current_file,
            )
            shutil.copyfile(src_file, dst_file)


def add_extension_documentation(extensions_dir: str, docs_dir: str) -> None:
    """
    Copy the docs folders of each extension to output_dir.

    :param extensions_dir: The directory where each extension repo is cloned into.
    :param docs_dir: The docs dir of a certain project in which the module documentation has to be copied.
    """
    LOGGER.info("Adding extension documentation to %s", docs_dir)
    extensions_dir_in_docs_dir = os.path.join(docs_dir, "extensions")
    util.ensure_empty_dir(extensions_dir_in_docs_dir)
    for current_ext_dir in os.listdir(extensions_dir):
        doc_dir_extension = os.path.join(extensions_dir, current_ext_dir, "docs")
        if os.path.exists(doc_dir_extension):
            LOGGER.info("Adding extension: %s", current_ext_dir)
            copy_dst = os.path.join(extensions_dir_in_docs_dir, current_ext_dir)
            shutil.copytree(doc_dir_extension, copy_dst)
        else:
            LOGGER.warning("No docs directory exists for extension %s", current_ext_dir)


def publish_docs(
    product_repo: str,
    branch: str,
    build_type: BuildType,
    tar_file: str,
    git_token: Optional[str],
) -> None:
    product_config: ProductConfig = ProductProject.get_project_config_from_git_repo(
        product_repo, branch, git_token
    )
    publish_config = product_config.documentation.publish
    publish_path = product_config.documentation.publish.get_release_path(build_type)

    # Call the more generic publish function that is introduced
    # for `Connect` module docs, enabling it to benefit from IRT
    publish_docs_on_server(
        publish_config.username,
        publish_config.hostname,
        tar_file,
        publish_path,
        build_type,
        publish_config.post_publish_hook_remote,
    )


def publish_docs_on_server(
    username: str,
    hostname: str,
    tar_file: str,
    publish_path: str,
    build_type: Optional[BuildType] = None,
    post_publish_hook_remote: Optional[str] = None,
) -> None:
    """
    If the calling function is providing post_publish_hook_remote
    we expect the build_type argument to be present along with it.
    the condition below, checks it.
    """
    if post_publish_hook_remote and build_type is None:
        raise Exception("build_type is not provided")

    # Copy tar file to webserver
    cmd = ["scp", tar_file, f"{username}@{hostname}:"]
    util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)

    try:
        # Extract tar
        tar_file_base_name = os.path.basename(tar_file)
        cmd = [
            "ssh",
            f"{username}@{hostname}",
            f"mkdir -p {publish_path} && rm -rf {publish_path}/* && cd {publish_path} && tar -xvjf ~docs/{tar_file_base_name}",
        ]
        LOGGER.info("Copying tar archive %s to %s", tar_file, hostname)
        util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)

        # Run post publish hook
        if post_publish_hook_remote:
            LOGGER.info("Run post publish hook %s", post_publish_hook_remote)
            cmd = [
                "ssh",
                f"{username}@{hostname}",
                post_publish_hook_remote,
                publish_path,
                build_type.value,
            ]
            util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)
    finally:
        cmd = [
            "ssh",
            f"{username}@{hostname}",
            f"rm -f {tar_file_base_name}",
        ]
        util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)
