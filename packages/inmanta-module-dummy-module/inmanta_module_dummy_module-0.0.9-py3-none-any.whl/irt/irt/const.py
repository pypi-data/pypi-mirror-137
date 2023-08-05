"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import re

SEMVER_REGEX_STABLE_VERSION = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
COMPILED_SEMVER_REGEX_STABLE_VERSION = re.compile(SEMVER_REGEX_STABLE_VERSION)
GITKEEP_FILE = ".gitkeep"
