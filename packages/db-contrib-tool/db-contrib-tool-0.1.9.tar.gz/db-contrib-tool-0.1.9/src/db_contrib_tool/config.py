"""Common config module."""
import os
from enum import Enum
from typing import Any, Dict, List

from db_contrib_tool.utils.filesystem import read_yaml_file

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
SETUP_REPRO_ENV_CONFIG_FILE = os.path.join(CONFIG_DIR, "setup_repro_env_config.yml")
# Records the paths of installed multiversion binaries on Windows.
WINDOWS_BIN_PATHS_FILE = "windows_binary_paths.txt"


class SegmentWriteKey(Enum):
    DEV = "RmMosrk1bf025xLRbZUxF2osVzGLPpL3"
    PROD = "jrHGRmtQBO8HYU1CyCfnB279SnktLgGH"


SEGMENT_WRITE_KEY = SegmentWriteKey.PROD.value
if os.environ.get("ENV") == "DEV":
    SEGMENT_WRITE_KEY = SegmentWriteKey.DEV.value


class Tasks:
    """Class represents evergreen tasks in setup repro env config."""

    binary: List[str]
    symbols: List[str]
    push: List[str]

    def __init__(self, tasks_yaml: Dict[str, List[str]]):
        """Initialize."""
        self.binary = tasks_yaml.get("binary", [])
        self.symbols = tasks_yaml.get("symbols", [])
        self.push = tasks_yaml.get("push", [])


class Buildvariant:
    """Class represents evergreen buildvariant in setup repro env config."""

    name: str
    edition: str
    platform: str
    architecture: str
    versions: List[str]

    def __init__(self, buildvariant_yaml: Dict[str, str]):
        """Initialize."""
        self.name = buildvariant_yaml.get("name", "")
        self.edition = buildvariant_yaml.get("edition", "")
        self.platform = buildvariant_yaml.get("platform", "")
        self.architecture = buildvariant_yaml.get("architecture", "")
        self.versions = buildvariant_yaml.get("versions", [])


class SetupReproEnvConfig:
    """Class represents setup repro env config."""

    evergreen_tasks: Tasks
    evergreen_buildvariants: List[Buildvariant]

    def __init__(self, raw_yaml: Dict[str, Any]):
        """Initialize."""
        self.evergreen_tasks = Tasks(raw_yaml.get("evergreen_tasks", {}))
        self.evergreen_buildvariants = []
        buildvariants_raw_yaml = raw_yaml.get("evergreen_buildvariants", "")
        for buildvariant_yaml in buildvariants_raw_yaml:
            self.evergreen_buildvariants.append(Buildvariant(buildvariant_yaml))


SETUP_REPRO_ENV_CONFIG = SetupReproEnvConfig(read_yaml_file(SETUP_REPRO_ENV_CONFIG_FILE))
