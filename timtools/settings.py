"""Module containing the setting to be used for the package"""

import configparser
from pathlib import Path

import timtools.locations

PROJECT_DIR: Path = Path(__file__).parent
CACHE_DIR: Path = timtools.locations.get_user_cache_dir() / "timtools"
if not CACHE_DIR.is_dir():
    CACHE_DIR.mkdir()

CONFIG_DIR: Path = timtools.locations.get_user_config_dir() / "timtools"
if not CONFIG_DIR.is_dir():
    code_src_config_dir: Path = PROJECT_DIR / "tim_config"
    if not code_src_config_dir.is_dir():
        code_src_config_dir = Path("/home/tim/Programs/python/timtools/tim_config")

    if code_src_config_dir.is_dir():
        CONFIG_DIR = code_src_config_dir

CONFIG_FILE: Path = CONFIG_DIR / "timtools.ini"

USER_CONFIG: configparser.ConfigParser = configparser.ConfigParser()
USER_CONFIG.read(CONFIG_FILE)
