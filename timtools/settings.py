import configparser
from pathlib import Path

import xdg

PROJECT_DIR: Path = Path(__file__).parent
CACHE_DIR: Path = xdg.XDG_CACHE_HOME / "timtools"
CONFIG_DIR: Path = xdg.XDG_CONFIG_HOME / "timtools"
if not CONFIG_DIR.is_dir():
    code_src_config_dir: Path = PROJECT_DIR / "tim_config"
    if code_src_config_dir.is_dir():
        CONFIG_DIR = code_src_config_dir

CONFIG_FILE: Path = CONFIG_DIR / "timtools.ini"

USER_CONFIG: configparser.ConfigParser = configparser.ConfigParser()
USER_CONFIG.read(CONFIG_FILE)
