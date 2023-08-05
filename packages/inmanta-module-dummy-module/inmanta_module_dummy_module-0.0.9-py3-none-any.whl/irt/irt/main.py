"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import datetime
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from subprocess import CalledProcessError
from typing import Any, Dict, List, Optional, Tuple, Union

import click
import click_log
import gnupg
import packaging.version
import requests
import toml

import irt.config as configtoml
import irt.mergetool.config
from irt import git, modules, util
from irt.credentials import CredentialStore, FromEnvCredentialStore
from irt.module_sources import (
    GitHubConfig,
    GitlabConfig,
    ModuleSourceManager,
    legacy_config,
)
from irt.modules import ModuleSetDefinition
from irt.project import ProductConfig, ProductProject, Project, PythonVersion
from irt.release import BuildType, build, documentation
from irt.release import modules as release_modules
from irt.release.release import ProductReleaseTool, ProductVersion
from irt.version import ChangeType

# Set logger config
log_level = logging.DEBUG
log = logging.getLogger()
log.setLevel(log_level)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(log_level)
log.addHandler(stream)

logging.captureWarnings(True)
LOGGER = logging.getLogger(__name__)

# Add the irt root logger to click_log
click_log.basic_config(logging.getLogger("irt"))

DEFAULT_CONFIG_FILE = "config.toml"

# Silence github debug logging
logging.getLogger("github").setLevel(logging.INFO)


def exceptionhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CalledProcessError as e:
            if e.output is not None:
                print("------------- Program failed with output: ----------------")
                print(e.output.decode())
                print("----------------------------------------------------------")
            raise

    return wrapper


def find_config():
    """
    Find a configuration file
    """

    def find_in_folder_above(cur_dir: str) -> Optional[str]:
        while cur_dir != "/":
            cfg_file = os.path.join(cur_dir, DEFAULT_CONFIG_FILE)
            if os.path.exists(cfg_file):
                return cfg_file
            else:
                cur_dir = os.path.dirname(cur_dir)
        return None

    # try to find in current folder
    result = find_in_folder_above(os.path.abspath(os.curdir))
    if result:
        return result

    # try to find in source tree
    return find_in_folder_above(os.path.abspath(__file__))


def create_tmp_dir(ctx) -> str:
    tmp_dir = tempfile.mkdtemp()

    def cleanup():
        LOGGER.info("Cleanup tmpdir %s", tmp_dir)
        shutil.rmtree(tmp_dir)

    ctx.call_on_close(cleanup)
    return tmp_dir


@click.group()
@click_log.simple_verbosity_option()
@click.pass_context
@click.option("--config", help="The configuration file to load")
def cmd(ctx, config):
    if config is None:
        config = find_config()
    if config is not None:
        with open(config, "r") as fh:
            ctx.obj = configtoml.Config(**toml.load(fh))
    else:
        ctx.obj = configtoml.Config(module_sources=legacy_config)


@cmd.command(name="github-list")
@click.option("--org", help="The github organization to find module repositories in")
@click.option(
    "--token",
    help="The github token to use",
    default=lambda: os.environ.get("GITHUB_TOKEN", ""),
)
@click.option(
    "--save",
    help="The location to store the resulting yaml file",
    default="modules.yml",
)
@exceptionhandler
def list_repos(org: str, token: str, save: str):
    """
    Create a listing of all repos with inmanta modules at the given github user.
    """
    if org is None:
        raise click.UsageError("The org needs to be supplied.")
    config = GitHubConfig(
        type="github",
        organisation=org,
        output=save,
    )
    credentials = CredentialStore()
    if token:
        credentials.set_credentials_for("github", None, token)
    config.get_source().load_into(credentials, save)


@cmd.command(name="gitlab-list")
@click.option(
    "--group", help="The gitlab group to find module repositories in", default="BICS"
)
@click.option(
    "--token",
    help="The gitlab private token to use",
    default=lambda: os.environ.get("GITLAB_TOKEN", ""),
)
@click.option(
    "--username",
    help="The username that belongs to the gitlab token",
    default=lambda: os.environ.get("GITLAB_USERNAME", ""),
)
@click.option(
    "--save",
    help="The location to store the resulting yaml file",
    default="modules.yml",
)
@exceptionhandler
def list_gitlab_repos(group: str, token: str, username: str, save: str):
    """
    Create a listing of all repos with inmanta modules at the given github user.
    """
    if (token and not username) or (not token and username):
        raise click.ClickException(
            "--username and --token should always be set together."
        )
    # fallback to new framework by building a config
    config = GitlabConfig(
        type="gitlab",
        group=group,
        output=save,
    )
    credentials = CredentialStore()
    if token:
        credentials.set_credentials_for("gitlab", username, token)
    config.get_source().load_into(credentials, save)


class BuildContext(object):
    def __init__(
        self,
        build_dir: str,
        branch: str,
        version: str,
        build_id: str,
        release: bool,
        python_path: str,
        destination_dir: str,
    ):
        self.build_dir = build_dir
        self.branch = branch
        self.version = version
        self.build_id = build_id
        self.release = release
        self.python_path = python_path
        self.destination_dir = destination_dir
        self.full_version = None

    def set_version_info(self, path_to_source_code):
        if self.version is not None:
            self.full_version = self.version
        else:
            self.version = subprocess.check_output(
                [self.python_path, "setup.py", "-V"],
                cwd=path_to_source_code,
                universal_newlines=True,
            ).strip()
            self.full_version = self.version + self.build_id


def create_build_context(tmp_dir, version, master, next_, build_id, destination_dir):
    if master + next_ + (version is not None) > 1:
        raise click.UsageError("--master, --next and --version are mutually exclusive")

    # Create virtual env
    python_path = util.ensure_tmp_env(tmp_dir)

    if build_id is None:
        build_id = ".dev" + datetime.datetime.now().strftime("%y%m%d%H%M")

    if master:
        branch = "master"
        release = False
    elif next_:
        branch = "next"
        release = False
    else:
        if version is None:
            raise click.UsageError("Version is required when master is not built")
        branch = f"tags/v{version}"
        release = True

    return BuildContext(
        build_dir=tmp_dir,
        branch=branch,
        version=version,
        build_id=build_id,
        release=release,
        python_path=python_path,
        destination_dir=destination_dir,
    )


def package_source_code(build_context, path_to_source_code, package_name):
    if build_context.branch == "master" or build_context.branch == "next":
        cmd = ["egg_info", "-Db", build_context.build_id, "sdist"]
    else:
        cmd = ["egg_info", "-Db", "", "sdist"]

    subprocess.check_output(
        [build_context.python_path, os.path.join(path_to_source_code, "setup.py")]
        + cmd,
        cwd=path_to_source_code,
    )

    dist_file = os.path.join(path_to_source_code, "dist", package_name)
    if not os.path.exists(dist_file):
        click.echo(
            "setup.py sdist did not generate expected file %s" % dist_file, err=True
        )
        sys.exit(1)

    shutil.copy(dist_file, build_context.destination_dir)
    return dist_file


@cmd.command(name="package-dependencies")
@click.option(
    "--package-dir",
    help="The package for which the dependencies have to be packaged",
    required=True,
)
@click.option("--constraint-file", help="The requirements.txt file", required=True)
@click.option("--destination", "-d", help="The path to the output file", required=True)
@click.option(
    "--allow-pre-releases-inmanta-pkgs",
    is_flag=True,
    default=False,
    help="Allow pre-releases for inmanta packages",
)
@exceptionhandler
def package_dependencies_command(
    package_dir: str,
    constraint_file: str,
    destination: str,
    allow_pre_releases_inmanta_pkgs: bool,
):
    constraint_file = os.path.abspath(constraint_file)
    package_dir = os.path.abspath(package_dir)

    build.package_dependencies(
        package_dir, constraint_file, destination, allow_pre_releases_inmanta_pkgs
    )


def subdir(root, name):
    sub = os.path.join(root, name)
    if not os.path.exists(sub):
        os.mkdir(sub)
    return sub


@cmd.command("set-list")
@click.option(
    "--module_set", "-s", help="The yaml file that defines this set", required=True
)
@click.option(
    "--source-dir",
    help="The directory where the module sources files are located",
    required=True,
)
@exceptionhandler
def set_list(module_set, source_dir):
    """
    Print out the modules that are included in the given set
    """
    set_def: modules.ModuleSetDefinition
    set_def, module_set, _ = modules.load_modules(module_set, source_dir)

    click.echo(f"Module set {set_def.name} includes:")
    for name in sorted(module_set.keys()):
        click.echo(" - " + name + " " + str(module_set[name]["version"]))


@cmd.command("set-download")
@click.option(
    "--module-set", "-s", help="The yaml file that defines this set", required=True
)
@click.option(
    "--source-dir",
    help="The directory where the module sources files are located",
    required=True,
)
@click.option(
    "--set-dir",
    help="The directory to store all modules defined in this set",
    required=True,
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product this module set is associated with.",
)
@click.option(
    "--product-version",
    help="The version of the product this module set is associated with: iso<x> or master.",
    default="master",
)
@click.option(
    "--install-mode",
    type=click.Choice([m.value for m in modules.InstallMode]),
    help="The install mode for the compiler.",
    default=modules.InstallMode.release.value,
)
@click.option(
    "--remote",
    help="Download the modules from the specified remote.",
    required=False,
)
@click.option("--workdir", help="The working directory to use", default="working_dir")
@click.option(
    "--github-token",
    help="Token to use to clone Git repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
@click.pass_obj
@exceptionhandler
def set_download(
    obj: configtoml.Config,
    module_set: str,
    source_dir: str,
    set_dir: str,
    product_repo: str,
    product_version: str,
    install_mode: str,
    workdir: str,
    github_token: str,
    remote: Optional[str],
):
    """
    Download all modules using the stable product version associated with the given dev branch.
    """
    install_module_enum = modules.InstallMode(install_mode)
    python_path: str = util.ensure_tmp_env(workdir)

    # install stable product
    product_directory: str = os.path.join(workdir, "product_repo")
    repo: git.GitRepo = git.GitRepo(
        url=product_repo, clone_dir=product_directory, token=github_token
    )
    stable_branch: str = ProductVersion(
        dev_branch=product_version, repo=repo
    ).stable_branch
    with repo.checkout_branch(stable_branch):
        ProductProject(product_directory).install(
            python_path,
            workdir,
            stable_branch,
            BuildType.stable,
            github_token,
        )

    setdef = ModuleSetDefinition.from_file(module_set)
    credentials = FromEnvCredentialStore()
    credentials.set_credentials_for("github", None, github_token)

    sources = ModuleSourceManager(source_dir, obj.module_sources, credentials)

    modules.download_set(
        python_path,
        setdef,
        sources,
        set_dir,
        install_module_enum,
        "https://artifacts.internal.inmanta.com/inmanta/stable",
        remote=remote,
    )


@cmd.command("set-docgen")
@click.option(
    "--module-set", "-s", help="The yaml file that defines this set", required=True
)
@click.option(
    "--source-dir",
    help="The directory where the module sources files are located",
    required=True,
)
@click.option(
    "--set-dir",
    help="The directory to store all modules defined in this set",
    required=True,
)
@click.option("--doc-dir", help="The root dir of the core docs", required=True)
@exceptionhandler
def generate_docs(module_set: str, source_dir: str, doc_dir: str, set_dir: str) -> None:
    """
    NOTE:
        * This command can be removed when the OSS doc build has been migrated to the new `build-docs` command.
        * This command assumes that all sphinx dependencies, required to perform the build, are already installed.
    """
    documentation.generate_module_documentation(
        sys.executable, module_set, source_dir, doc_dir, set_dir
    )


@cmd.command("test-moduleset")
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product.",
)
@click.option(
    "--branch",
    required=True,
    help="The branch of --product-repo that should be cloned.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The type of build to perform.",
)
@click.option(
    "--working-dir",
    help="Directory used to store all the files required to run the module set test.",
)
@click.option(
    "--github-token",
    help="Token to use to clone Git repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
@exceptionhandler
@click.pass_obj
def test_module_set(
    obj: configtoml.Config,
    product_repo: str,
    branch: str,
    build_type: str,
    working_dir: str,
    github_token: str,
) -> None:
    """
    Test a set of modules.
    """
    if not github_token:
        raise click.ClickException("Argument --github-token has to be provided.")
    working_dir = os.path.abspath(working_dir)
    os.makedirs(working_dir, exist_ok=True)
    if os.listdir(working_dir):
        raise Exception(f"Directory {working_dir} is not empty.")
    build_type_enum = BuildType(build_type)

    credentials = FromEnvCredentialStore()
    credentials.set_credentials_for("github", None, github_token)

    module_sources_dir = os.path.join(working_dir, "sources")
    sources = ModuleSourceManager(module_sources_dir, obj.module_sources, credentials)

    modules.test_module_set(
        sources, product_repo, branch, build_type_enum, working_dir, github_token
    )


def install_inmanta(python_path, release_type: BuildType, module_set_name: str):
    """
    Install the latest version of the given release of the Inmanta orchestrator using pip.
    """
    pip_index_url = (
        f"https://artifacts.internal.inmanta.com/inmanta/{release_type.value}"
    )
    pip_install_cmd = [python_path, "-m", "pip", "install", "-i", pip_index_url]
    package_name = (
        "inmanta"
        if "inmanta-service-orchestrator" not in module_set_name
        else "inmanta-service-orchestrator"
    )
    if release_type == BuildType.dev:
        pip_install_cmd += ["--pre", package_name]
    elif release_type == BuildType.next:
        # Pip only installs RC releases when the exact version is specified.
        # Retrieve the version number of the latest rc release from devpi.
        url_http_get_request = f"{pip_index_url}/{package_name}"
        latest_rc_release = latest_rc_release_for_package(url_http_get_request)
        pip_install_cmd += [f"{package_name}=={latest_rc_release}"]
    else:
        pip_install_cmd += [package_name]

    subprocess.run(pip_install_cmd, check=True)


def is_rc_release(version_number: str) -> bool:
    """
    Check whether the given version number is an rc version number.
    """
    v = packaging.version.Version(version_number)
    if v.pre is None:
        return False
    return v.pre[0] == "rc"


def latest_rc_release_for_package(
    request_url: str, major_version: Optional[int] = None
):
    response = requests.get(request_url, headers={"Accept": "application/json"})
    rc_releases = [v for v in response.json()["result"].keys() if is_rc_release(v)]
    if major_version is not None:
        rc_releases = [
            v
            for v in rc_releases
            if packaging.version.Version(v).major == major_version
        ]
    latest_rc_release = sorted(rc_releases, key=lambda x: packaging.version.Version(x))[
        -1
    ]
    return latest_rc_release


@cmd.command(
    "get-latest-rc-version",
    help="Get the latest rc version of a package and print it to stdout",
)
@click.option(
    "--package-url",
    help="The url of the package in the package repository",
    required=True,
)
@click.option(
    "--major-version",
    help="Get the latest rc for this major version",
    required=False,
    type=int,
)
def get_latest_rc_version_for_package(
    package_url: str, major_version: Optional[int] = None
):
    print(latest_rc_release_for_package(package_url, major_version))


@cmd.command("push-moduleset")
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product",
)
@click.option(
    "--branch",
    required=True,
    help="The branch of --product-repo that should be cloned. Only stable release branches are allowed (iso<number>-stable).",
)
@click.option(
    "--working-dir",
    required=True,
    help="The directory to put build artifacts in.",
)
@click.option(
    "--github-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    required=True,
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Don't perform the actual release, but output the versions that would be pushed for each module.",
)
@click.option(
    "--push-single-module",
    help="Push only this module instead of the full module set.",
)
@exceptionhandler
@click.pass_obj
def push_module_set(
    obj: configtoml.Config,
    product_repo: str,
    branch: str,
    working_dir: str,
    github_token: str,
    dry_run: bool,
    push_single_module: Optional[str] = None,
) -> None:
    """
    Release the module set for the given inmanta Product.
    An SSH key which grants access to the push_repo, specified in the pyproject.toml, is
    required when this command is executed.
    """
    match = re.fullmatch(r"iso\d+-stable", branch)
    if not match:
        click.ClickException(
            "Invalid value for argument --branch. Expected: iso<number>-stable"
        )
    if not push_single_module or not push_single_module.strip():
        push_single_module = None

    credentials = FromEnvCredentialStore()
    credentials.set_credentials_for("github", None, github_token)

    module_sources_dir = os.path.join(working_dir, "sources")
    sources = ModuleSourceManager(module_sources_dir, obj.module_sources, credentials)

    release_modules.push_module_set(
        product_repo,
        branch,
        working_dir,
        github_token,
        dry_run,
        sources,
        push_single_module,
    )


def copy_extensions(
    extension_source_directory: str,
    target_directory: str,
    enabled_extensions: List[str],
):
    for extension in enabled_extensions:
        shutil.copytree(
            os.path.join(extension_source_directory, extension),
            os.path.join(target_directory, extension),
        )


def get_module_set_path(module_set_source_dir: str, module_set_name: str):
    return os.path.join(module_set_source_dir, module_set_name + ".yml")


def create_archive_for_target(
    click_ctx,
    product_repo: str,
    conf: Dict[str, Union[Dict[str, str], List[str], str]],
    module_set_source_dir: str,
    sources_folder: str,
    source_dir: str,
    extension_source_dir: str,
    github_token: str,
) -> str:
    archive_name = time.strftime("%Y%m%d%H%M%S", time.gmtime()) + "-" + conf["name"]
    LOGGER.debug(f"Processing archive for {archive_name}")
    archive_dir = os.path.join(source_dir, archive_name)
    os.makedirs(archive_dir, exist_ok=True)
    modules_dir = os.path.join(source_dir, archive_name, "modules")
    os.makedirs(modules_dir, exist_ok=True)
    # new workdir to force new venv
    module_set_work_dir = os.path.join(source_dir, archive_name, "workdir")
    os.makedirs(module_set_work_dir, exist_ok=True)
    LOGGER.debug("Downloading modules")
    module_set_path = get_module_set_path(module_set_source_dir, conf["module_set"])
    click_ctx.invoke(
        set_download,
        module_set=module_set_path,
        source_dir=sources_folder,
        set_dir=modules_dir,
        product_repo=product_repo,
        product_version=conf["product_version"],
        github_token=github_token,
        workdir=module_set_work_dir,
    )
    extensions_dir = os.path.join(archive_dir, "extensions")
    os.makedirs(extensions_dir, exist_ok=True)
    copy_extensions(extension_source_dir, extensions_dir, conf["enabled_extensions"])
    shutil.copytree(
        os.path.join(source_dir, "core"),
        os.path.join(archive_dir, "core"),
        symlinks=True,
    )
    if conf.get("additional_repos"):
        util.clone_multiple_repos(
            conf["additional_repos"],
            os.path.join(archive_dir, "additional-repositories"),
        )
    return shutil.make_archive(
        os.path.join(source_dir, archive_name), "zip", archive_dir
    )


def get_key_by_id(gpg: gnupg.GPG, id: str) -> Optional[Dict[str, Any]]:
    gpg_keys: gnupg.ListKeys = gpg.list_keys()
    matching_key = None
    for key in gpg_keys:
        uids = key.get("uids")
        for uid in uids:
            if id in uid:
                matching_key = key
    if not matching_key:
        raise Exception(f"Key not found for {id}")
    return matching_key


def encrypt_archive(
    gpg: gnupg.GPG,
    archive_file: str,
    encryption_key_email: str,
    output_dir: str,
) -> None:
    encryption_key = get_key_by_id(gpg, encryption_key_email)
    output_file_name = os.path.join(output_dir, os.path.basename(archive_file) + ".gpg")

    with open(archive_file, "rb") as archive:
        encrypted_data = gpg.encrypt_file(
            archive,
            encryption_key["fingerprint"],
            output=output_file_name,
            always_trust=True,  # required because pub key may not be registered as trusted.
        )
        if not encrypted_data.ok:
            raise Exception(
                f"Encryption of {archive_file} not successful, {encrypted_data.status}, {encrypted_data.GPG_ERROR_CODES}"
            )


@cmd.command("generate-archives")
@click.option(
    "--archive-config",
    "-a",
    help="The toml file that describes the configuration for the archives."
    " Each target is expected to have a name, a module_set describing the required modules,"
    " a list of enabled_extensions, and optionally a dict of additional_repos,"
    " that should be included in the archive in addition to the inmanta core, extension and module repositories."
    " See https://github.com/inmanta/irt/blob/master/archive-config.toml for an example.",
    required=True,
)
@click.option(
    "--module-set-source-dir",
    "-m",
    help="The directory where the module sets are defined",
    required=True,
)
@click.option(
    "--github-token",
    help="The github token to use",
    default=lambda: os.environ.get("GITHUB_TOKEN", ""),
)
@click.option(
    "--gitlab-token",
    help="The gitlab token to use",
    default=lambda: os.environ.get("GITLAB_TOKEN", ""),
)
@click.option(
    "--gitlab-username",
    help="The username that belongs to the gitlab-token",
    default=lambda: os.environ.get("GITLAB_USERNAME", ""),
)
@click.option(
    "--group", help="The gitlab group to find module repositories in", default="BICS"
)
@click.option("--target", "-t", help="Create the archive only for the specified target")
@click.option(
    "--output-dir", "-o", help="Output directory for the archives", required=True
)
@click.option(
    "--encryption-key",
    "-e",
    help="ID corresponding to the key to use for encryption",
    required=True,
)
@click.pass_context
@exceptionhandler
def generate_archives(
    ctx,
    archive_config,
    module_set_source_dir: str,
    github_token: str,
    gitlab_token: str,
    gitlab_username: str,
    group: str,
    target: Optional[str],
    output_dir: str,
    encryption_key: str,
):
    if (gitlab_token and not gitlab_username) or (not gitlab_token and gitlab_username):
        raise click.ClickException(
            "--gitlab-username and --gitlab-token should always be set together."
        )
    gpg = gnupg.GPG()

    tmp_dir = create_tmp_dir(ctx)

    config = toml.load(archive_config)
    os.makedirs(output_dir, exist_ok=True)

    LOGGER.debug("Downloading core repos")
    core_dir = os.path.join(tmp_dir, "core")
    util.clone_multiple_repos(config["repos"]["core"], core_dir, token=github_token)

    LOGGER.debug("Downloading extensions")
    extension_source_dir = os.path.join(tmp_dir, "extensions")
    util.clone_multiple_repos(
        config["repos"]["extensions"], extension_source_dir, token=github_token
    )

    sources_folder = os.path.join(tmp_dir, "modulelists")

    if target:
        archive_file = create_archive_for_target(
            ctx,
            config["repos"]["product"],
            config["targets"][target],
            module_set_source_dir,
            sources_folder,
            tmp_dir,
            extension_source_dir,
            github_token,
        )
        encrypt_archive(gpg, archive_file, encryption_key, output_dir)
    else:
        for archive_name, conf in config["targets"].items():
            archive_file = create_archive_for_target(
                ctx,
                config["repos"]["product"],
                conf,
                module_set_source_dir,
                sources_folder,
                tmp_dir,
                extension_source_dir,
                github_token,
            )
            encrypt_archive(gpg, archive_file, encryption_key, output_dir)


@cmd.command(
    "build-and-publish",
    help="Build and publish Python packages, RPMs and docs for a product and all its dependencies. "
    "This command requires the CLOUDSMITH_API_KEY environment variable to be set.",
)
@click.option(
    "--product-repo", required=True, help="The Git repository URL of an Inmanta product"
)
@click.option(
    "--branch",
    required=True,
    help="The branch of each repository that should be cloned",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    help="The type of build to perform.",
)
@click.option(
    "--centos-version",
    type=int,
    multiple=True,
    help="Build RPMs for this version of Centos. When not set, this config option will be extracted from "
    "the build.rpm.centos_versions field of the pyproject.toml file on the product repository.",
)
@click.option(
    "--token",
    help="Token to use to clone Git repository. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
@click.option("--builddir", help="The build directory to use", default="build")
@click.pass_context
def build_and_publish(
    ctx,
    product_repo: str,
    branch: str,
    build_type: str,
    centos_version: Optional[Tuple[str]],
    token: Optional[str],
    builddir: str,
) -> None:
    builddir = os.path.abspath(builddir)
    util.ensure_dir(builddir)

    # create a python dir
    python_dir = os.path.join(builddir, "python")
    util.ensure_dir(python_dir)

    # Build and publish Python packages
    ctx.invoke(
        clone_product_repos,
        product_repo=product_repo,
        branch=branch,
        output=python_dir,
        token=token,
    )
    ctx.invoke(build_python, directory=python_dir, build_type=build_type)
    ctx.invoke(publish_python, directory=python_dir, build_type=build_type)

    product_config: ProductConfig = ProductProject.get_project_config_from_git_repo(
        product_repo=product_repo, branch=branch, token=token
    )

    # Ensure that the pyproject.toml file of the project and its extensions is consistent.
    # This check ensures that the `build.python.python_versions` section of each extension
    # and the product contains either python3 (which indicates that it builds a universal
    # wheel) or an exact python version that is compatible with python version of the venv
    # included in the RPM (`build.rpm.python_version` section of pyproject.toml file of product).
    python_version_rpm = product_config.build.rpm.python_version
    for extension_url in product_config.dependencies.extensions.values():
        repo_name = util.get_git_repo_name_for_url(extension_url)
        extension_path = os.path.join(python_dir, repo_name)
        extension_config = Project(extension_path).get_project_config()
        python_versions_ext = extension_config.build.python.python_versions
        if (
            PythonVersion.PYTHON_3 not in python_versions_ext
            and python_version_rpm not in python_versions_ext
        ):
            raise Exception(
                f"The RPM venv requires {python_version_rpm.get_name_python_binary()} but "
                f"the pyproject.toml file for the extension {repo_name} doesn't mention this python "
                f"version or 'python3' in the `build.python.python_versions` section: "
                f"{[p.get_name_python_binary() for p in python_versions_ext]}."
            )
    product_python_versions = product_config.build.python.python_versions
    if (
        PythonVersion.PYTHON_3 not in product_python_versions
        and python_version_rpm not in product_python_versions
    ):
        raise Exception(
            f"The RPM venv requires {python_version_rpm.get_name_python_binary()} but "
            f"the pyproject.toml file of the product doesn't mention this python "
            f"version or 'python3' in the `build.python.python_versions` section: "
            f"{[p.get_name_python_binary() for p in product_python_versions]}."
        )

    if not centos_version:
        centos_version = product_config.build.rpm.centos_versions
        if not centos_version:
            raise Exception(
                "Either provide the --centos-version option or set the build.rpm.centos_versions "
                "field in the pyproject.toml file of the product repository."
            )

    for version in centos_version:
        rpm_build_dir = os.path.join(builddir, f"rpm-el{version}")
        util.ensure_dir(rpm_build_dir)

        # Build and publish RPMs
        ctx.invoke(
            build_rpm,
            product_repo=product_repo,
            branch=branch,
            build_type=build_type,
            centos_version=version,
            output_dir=rpm_build_dir,
            git_token=token,
        )
        rpms_dir = os.path.join(rpm_build_dir, "rpms")
        ctx.invoke(
            publish_rpm,
            product_repo=product_repo,
            branch=branch,
            rpm_directory=rpms_dir,
            build_type=build_type,
            git_token=token,
        )

    # TODO: build docs (#440)
    # TODO: publish docs (#440)


@cmd.command(name="clone-product-repos")
@click.option(
    "--product-repo", required=True, help="The Git repository URL of an Inmanta product"
)
@click.option(
    "--branch",
    required=True,
    help="The branch of each repository that should be cloned",
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="The directory in which the repositories should be cloned.",
)
@click.option(
    "--token",
    help="Token to use to clone Git repository",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
def clone_product_repos(
    product_repo: str, branch: str, output: str, token: Optional[str]
):
    """Clone all Git repositories of an Inmanta product."""
    LOGGER.info(
        "Running clone_product_repos for %s on branch %s to %s",
        product_repo,
        branch,
        output,
    )
    build.clone_product_repos(product_repo, branch, output, token)


@cmd.command(
    "build-python",
    help="Build Python packages for all subdirectories of a given dir. Only setuptools projects supported.",
)
@click.option(
    "--directory",
    required=True,
    help="The directory containing all project directories.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    default="dev",
    help="The type of build to perform.",
)
@click.option(
    "--output-dir",
    help=(
        "The directory to put build artifacts in."
        " If omitted, build artifacts are put in a dist subdirectory within each respective project directory."
    ),
)
def build_python(directory: str, build_type: str, output_dir: Optional[str]) -> None:
    LOGGER.info(
        "Running build_python in %s for type %s to %s",
        directory,
        build_type,
        output_dir,
    )

    if not os.path.isdir(directory):
        raise click.ClickException(f"{directory} is not a directory")
    build_type_enum: BuildType
    try:
        build_type_enum = BuildType(build_type)
    except ValueError:
        raise click.ClickException(
            "Not a valid build type: %s, choose one of %s"
            % (build_type, ", ".join(t.value for t in BuildType))
        )
    build.build_python_bulk(directory, build_type_enum, output_dir)


@cmd.command(
    "publish-python",
    help=(
        "Publish Python packages for all subdirectories of a given dir."
        ' Expects build artifacts to be present in each projects "dist" directory.'
        " Expects the following environment variables to be set:"
        " PGP_PASS, TWINE_USERNAME, TWINE_PASSWORD, DEVPI_USER, DEVPI_PASS"
    ),
)
@click.option(
    "--directory",
    required=True,
    help="The directory containing all project directories.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The build type of the artifacts in the project's dist directory.",
)
def publish_python(directory: str, build_type: str) -> None:
    LOGGER.info("Running publish_python in %s for type %s", directory, build_type)

    if not os.path.isdir(directory):
        raise click.ClickException(f"{directory} is not a directory")
    build_type_enum: BuildType
    try:
        build_type_enum = BuildType(build_type)
    except ValueError:
        raise click.ClickException(
            "Not a valid build type: %s, choose one of %s"
            % (build_type, ", ".join(t.value for t in BuildType))
        )
    build.publish_python_bulk(directory, build_type_enum)


@cmd.command(
    "publish-python-module",
    help=(
        "Publish a single Python module based on a given directory."
        ' Expects build artifacts to be in the "dist" directory of the directory.'
        " If the module is 'public' it will be published to pypi."
        " It the module is 'private' it will be publised to the stable index of artifacts."
        " Expects the following environment variables to be set:"
        " PGP_PASS, TWINE_USERNAME, TWINE_PASSWORD, DEVPI_USER, DEVPI_PASS."
    ),
)
@click.option(
    "--directory",
    required=True,
    help="The directory containing all project directories.",
)
@click.option(
    "--public",
    is_flag=True,
    help="This flag is used to publish to the private location (stable index of artifacts), otherwise push to pypi",
)
def publish_python_module(directory: str, public: bool) -> None:
    LOGGER.info("Running publish_python_module in %s", directory)
    if not os.path.isdir(directory):
        raise click.ClickException(f"{directory} is not a directory")
    build_type_enum = BuildType("stable")
    if public:
        build.publish_python_pypi(directory)
    else:
        build.publish_python_devpi(directory, build_type_enum)


@cmd.command(
    "build-rpm",
    help="Build RPMs for a given Inmanta product",
)
@click.option(
    "--product-repo", required=True, help="The Git repository URL of an Inmanta product"
)
@click.option(
    "--branch",
    required=True,
    help="The branch of each repository that should be cloned",
)
@click.option(
    "--build-type",
    required=True,
    type=click.Choice([t.value for t in BuildType]),
    help="The type of build to perform.",
)
@click.option(
    "--centos-version",
    required=True,
    type=int,
    help="Build RPMs for this version of Centos",
)
@click.option(
    "--output-dir",
    required=True,
    type=str,
    help="The directory where all the files, produced by the build-rpm command, will be stored. "
    "The resulting RPM files can be found in the ./rpms sub-directory of --output-dir",
)
@click.option(
    "--git-token",
    help="Token to use to clone Git repository. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
def build_rpm(
    product_repo: str,
    branch: str,
    build_type: str,
    centos_version: int,
    output_dir: str,
    git_token: Optional[str],
):
    LOGGER.info(
        "Running build_rpm for repo %s with branch %s. Buildtype %s and os version %s. Result go to %s",
        product_repo,
        branch,
        build_type,
        centos_version,
        output_dir,
    )
    build_type_enum = BuildType(build_type)
    os.environ[
        "PIP_INDEX_URL"
    ] = f"https://artifacts.internal.inmanta.com/inmanta/{build_type_enum.value}"
    build.build_rpm(
        product_repo, branch, build_type_enum, centos_version, output_dir, git_token
    )


@cmd.command(
    "publish-rpm",
    help=(
        "Upload RPMs for a given Inmanta product. "
        "This command requires the CLOUDSMITH_API_KEY environment variable to be set."
    ),
)
@click.option(
    "--product-repo", required=True, help="The Git repository URL of an Inmanta product"
)
@click.option(
    "--branch",
    required=True,
    help="The branch of each repository that should be cloned",
)
@click.option(
    "--rpm-directory",
    required=True,
    help="The directory containing the RPMs that should be uploaded",
)
@click.option(
    "--build-type",
    required=True,
    type=click.Choice([t.value for t in BuildType]),
    help="Upload the RPMs to the RPM repository for this type of build.",
)
@click.option(
    "--git-token",
    help="Token to use to clone Git repositories. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
def publish_rpm(
    product_repo: str,
    branch: str,
    rpm_directory: str,
    build_type: str,
    git_token: Optional[str],
):
    if "CLOUDSMITH_API_KEY" not in os.environ:
        raise Exception("Environment variable CLOUDSMITH_API_KEY not set")
    build_type_enum = BuildType(build_type)
    build.publish_rpm(product_repo, branch, rpm_directory, build_type_enum, git_token)


@cmd.command(
    "build-docs",
    help="Build the documentation for a certain product version. "
    "The environment variables LICENSE_KEY_FILE and ENTITLEMENTS_FILE "
    "have to be set when this command is used to build the ISO documentation.",
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product",
)
@click.option(
    "--branch",
    required=True,
    help="The branch of --product-repo that should be cloned.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The type of build to perform.",
)
@click.option(
    "--output-dir",
    help="The directory to put build artifacts in.",
)
@click.option(
    "--git-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
@click.option(
    "--gitlab-username",
    help="Username to use to clone GitLab repositories. This value can also be set via the IRT_GITLAB_USERNAME environment "
    "variable.",
    default=lambda: os.environ.get("IRT_GITLAB_USERNAME", None),
)
@click.option(
    "--gitlab-token",
    help="Token to use to clone GitLab repositories. This value can also be set via the IRT_GITLAB_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GITLAB_TOKEN", None),
)
@click.option(
    "--module-set",
    required=False,
    help="Build with non-default module set",
)
@click.pass_obj
def build_docs(
    obj: configtoml.Config,
    product_repo: str,
    branch: str,
    build_type: str,
    output_dir: str,
    git_token: Optional[str],
    gitlab_username: Optional[str],
    gitlab_token: Optional[str],
    module_set: Optional[str],
):
    if gitlab_username is None or gitlab_token is None or git_token is None:
        raise click.ClickException(
            "--gitlab-username, --gitlab-token and --git-token have to be provided."
        )
    build_type_enum = BuildType(build_type)

    credentials = FromEnvCredentialStore()
    credentials.set_credentials_for("github", None, git_token)
    credentials.set_credentials_for("gitlab", gitlab_username, gitlab_token)

    module_sources_dir = os.path.join(output_dir, "sources")
    sources = ModuleSourceManager(module_sources_dir, obj.module_sources, credentials)

    documentation.build_docs(
        product_repo,
        branch,
        build_type_enum,
        output_dir,
        git_token,
        sources,
        module_set,
    )


@cmd.command(
    "publish-docs",
    help="Publish the documentation for a certain product version. "
    "An SSH key without passphrase, which gives access to the publish destination, "
    "has to be present in the ~/.ssh folder on the machine that runs this command.",
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product",
)
@click.option(
    "--branch",
    required=True,
    help="The branch of --product-repo that should be cloned.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The type of build of the documentation.",
)
@click.option(
    "--tar-file",
    help="The tar file (tar.bz2) containing the documentation that should be published.",
)
@click.option(
    "--git-token",
    help="Token to use to clone Git repositories. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
def publish_docs(
    product_repo: str,
    branch: str,
    build_type: str,
    tar_file: str,
    git_token: Optional[str],
):
    build_type_enum = BuildType(build_type)
    documentation.publish_docs(
        product_repo, branch, build_type_enum, tar_file, git_token
    )


@cmd.command(
    "publish-docs-on-server",
    help="Publish the documentation on web server. "
    "An SSH key without passphrase, which gives access to the publish destination, "
    "has to be present in the ~/.ssh folder on the machine that runs this command.",
)
@click.option(
    "--username",
    required=True,
    help="The username for the web server.",
)
@click.option(
    "--hostname",
    required=True,
    help="The hostname of the web server.",
)
@click.option(
    "--tar-file",
    required=True,
    help="The tar file (tar.bz2) containing the documentation that should be published.",
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--publish-path",
    required=True,
    help="The directory on the webserver where the documentation should be published to",
)
def publish_docs_on_server(
    username: str,
    hostname: str,
    tar_file: str,
    publish_path: str,
):
    documentation.publish_docs_on_server(username, hostname, tar_file, publish_path)


@cmd.command(
    "build-and-publish-docs",
    help="Build and publish the documentation for a certain product version. "
    "The environment variables LICENSE_KEY_FILE and ENTITLEMENTS_FILE "
    "have to be set when this command is used to build the ISO documentation. "
    "An SSH key without passphrase, which gives access to the publish destination, "
    "has to be present in the ~/.ssh folder on the machine that runs this command.",
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product",
)
@click.option(
    "--branch",
    required=True,
    help="The branch of --product-repo that should be cloned.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The type of build to perform.",
)
@click.option(
    "--output-dir",
    help="The directory to put build artifacts in.",
)
@click.option(
    "--git-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the IRT_GIT_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GIT_TOKEN", None),
)
@click.option(
    "--gitlab-username",
    help="Username to use to clone GitLab repositories. This value can also be set via the IRT_GITLAB_USERNAME environment "
    "variable.",
    default=lambda: os.environ.get("IRT_GITLAB_USERNAME", None),
)
@click.option(
    "--gitlab-token",
    help="Token to use to clone GitLab repositories. This value can also be set via the IRT_GITLAB_TOKEN environment variable.",
    default=lambda: os.environ.get("IRT_GITLAB_TOKEN", None),
)
@click.option(
    "--module-set",
    required=False,
    help="Build with non-default module set",
)
@click.pass_obj
def build_and_publish_docs(
    obj: configtoml.Config,
    product_repo: str,
    branch: str,
    build_type: str,
    output_dir: str,
    git_token: Optional[str],
    gitlab_username: Optional[str],
    gitlab_token: Optional[str],
    module_set: Optional[str],
) -> None:
    if gitlab_username is None or gitlab_token is None or git_token is None:
        raise click.ClickException(
            "--gitlab-username, --gitlab-token and --git-token have to be provided."
        )
    build_type_enum = BuildType(build_type)

    credentials = FromEnvCredentialStore()
    credentials.set_credentials_for("github", None, git_token)
    credentials.set_credentials_for("gitlab", gitlab_username, gitlab_token)

    module_sources_dir = os.path.join(output_dir, "sources")
    sources = ModuleSourceManager(module_sources_dir, obj.module_sources, credentials)

    tar_file = documentation.build_docs(
        product_repo,
        branch,
        build_type_enum,
        output_dir,
        git_token,
        sources,
        module_set,
    )
    documentation.publish_docs(
        product_repo, branch, build_type_enum, tar_file, git_token
    )


@cmd.command(
    "create-product-freeze-file",
    help="Generate the product freeze file containing the external dependencies of the given product. "
    "The generated freeze file will only contain stable versions for dependencies.",
)
@click.option(
    "--product-dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        path_type=str,
    ),
    required=True,
    help="The git repository of the Inmanta product.",
)
@click.option(
    "--build-type",
    type=click.Choice([t.value for t in BuildType]),
    required=True,
    help="The type of build to perform on the components of this product.",
)
@click.option(
    "--github-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
        path_type=str,
    ),
    help="The path where the generated freeze file should be stored. If not provided, the freeze "
    "file is stored in `./requirements.txt` relative to the current working directory.",
)
def create_product_freeze_file(
    product_dir: str,
    build_type: str,
    github_token: Optional[str],
    output_file: Optional[str],
) -> None:
    if not github_token:
        raise click.ClickException("Argument --github-token has to be provided.")
    if output_file is None:
        output_file = os.path.abspath("requirements.txt")
    build_type_enum = BuildType(build_type)
    build.create_product_freeze_file(
        product_dir, build_type_enum, output_file, github_token
    )


@cmd.command(
    "release-product", help="Perform the release steps for an Inmanta product."
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product.",
)
@click.option(
    "--dev-branch",
    required=True,
    help="The dev branch associated with the version to release.",
)
@click.option(
    "--release-type",
    type=click.Choice([BuildType.next.value, BuildType.stable.value]),
    required=True,
    help="The type of release to perform.",
)
@click.option("--workdir", help="The working directory to use", default="working_dir")
@click.option(
    "--merge-tool-config",
    help="The configuration file for the merge tool. Required for the release tool to know which version bumps are allowed.",
    default="merge-tool.yml",
)
@click.option(
    "--github-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
def release_product(
    product_repo: str,
    dev_branch: str,
    release_type: str,
    workdir: str,
    merge_tool_config: str,
    github_token: Optional[str],
) -> None:
    if github_token is None:
        raise click.ClickException("GitHub token is required.")
    release_type_obj: BuildType = BuildType(release_type)
    product_name: str = util.get_git_repo_name_for_url(product_repo)
    release_tool: ProductReleaseTool = ProductReleaseTool(
        product_name,
        product_repo,
        dev_branch,
        workdir,
        irt.mergetool.config.parse_config(merge_tool_config),
        github_token,
    )
    change_type: Optional[ChangeType]
    version: packaging.version.Version
    if release_type_obj == BuildType.next:
        change_type, version = release_tool.rc_release()
    elif release_type_obj == BuildType.stable:
        change_type = None
        version = release_tool.stable_release()
    else:
        raise click.ClickException(
            "Performing a %s release is not supported." % release_type
        )

    LOGGER.info(
        "Performed a%s release for %s to version %s",
        f" {change_type.value}" if change_type is not None else "",
        product_name,
        version,
    )


@cmd.command(
    "verify-project-invariants",
    help=(
        "Verify version alignment accross branches and change entry destination branches for a product. If either invariant is"
        " not met this might result in unexpected build artifacts."
    ),
)
@click.option(
    "--product-repo",
    required=True,
    help="The git repository of the Inmanta product.",
)
@click.option("--workdir", help="The working directory to use", default="working_dir")
@click.option(
    "--github-token",
    help="Token to use to clone GitHub repositories. This value can also be set via the GITHUB_TOKEN environment variable.",
    default=lambda: os.environ.get("GITHUB_TOKEN", None),
)
def verify_project_invariants(
    product_repo: str,
    workdir: str,
    github_token: Optional[str],
) -> None:
    if github_token is None:
        raise click.ClickException("GitHub token is required.")
    if os.path.exists(workdir) and os.listdir(workdir):
        raise Exception(f"Directory {workdir} is not empty.")
    product_repo_obj: git.GitRepo = git.GitRepo(
        product_repo, os.path.join(workdir, "repo"), github_token
    )
    repos: List[git.GitRepo]
    with product_repo_obj.checkout_branch("master"):
        config: ProductConfig = ProductProject(
            product_repo_obj.directory
        ).get_project_config()
        repos = [
            product_repo_obj,
            *(
                git.GitRepo(url, os.path.join(workdir, component), github_token)
                for component, url in config.dependencies.get_all_component_repos().items()
            ),
        ]

    def get_version_violation_message() -> Optional[str]:
        violation_messages: List[str] = [
            f"Branches {', '.join(branches)} of {repo.url} have the same version {version} but they are not all aligned."
            for repo in repos
            for version, branches in ProductVersion.verify_version_alignment(repo)
        ]
        if len(violation_messages) == 0:
            return None
        return (
            "The following violations of the version alignment invariant were found:"
            + "".join(
                f"\n    - {violation_message}"
                for violation_message in violation_messages
            )
            + "\nTo resolve these issues either manually re-align branch heads or pull the versions apart."
        )

    def get_change_entry_violation_message() -> Optional[str]:
        violation_messages: List[str] = [
            f"Change entry {path} of {repo.url} was not found on destination branches {', '.join(branches)}."
            for repo in repos
            for path, branches in sorted(ProductVersion.verify_change_entries(repo))
        ]
        if len(violation_messages) == 0:
            return None
        return (
            "The following violations of the change entry invariant were found:"
            + "".join(
                f"\n    - {violation_message}"
                for violation_message in violation_messages
            )
            + "\nTo resolve these issues apply this change on the specified branches."
        )

    message: str = "\n\n".join(
        msg
        for msg in (
            get_version_violation_message(),
            get_change_entry_violation_message(),
        )
        if msg is not None
    )
    if message:
        raise click.ClickException(message)

    print("Verification successful!")


@cmd.command(
    "query-toml-file",
    help="Obtain the value for a certain config option in a toml file. "
    "The value of the option will be written to stdout.",
)
@click.option(
    "--file",
    required=True,
    help="The path to the toml file.",
)
@click.option(
    "--query",
    required=True,
    help="The query for a certain config option. The path to a config "
    "option is expressed via a dot-separated list. For example: "
    "`tool.irt.build.rpm.python_version`",
)
def query_toml_file(file: str, query: str) -> None:
    if not os.path.isfile(file):
        raise click.ClickException(f"{file} is not a file.")
    with open(file, "r") as fh:
        parsed_toml = toml.load(fh)
        for option in query.split("."):
            parsed_toml = parsed_toml.get(option)
            if parsed_toml is None:
                raise click.ClickException(
                    f"Option `{option}` from query `{query}` not found"
                )
        print(parsed_toml, end="")


if __name__ == "__main__":
    cmd()
