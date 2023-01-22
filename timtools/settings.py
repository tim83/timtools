"""Module containing the setting to be used for the package"""

import configparser
from pathlib import Path

import timtools.locations

PROJECT_DIR: Path = Path(__file__).parent
CACHE_DIR: Path = timtools.locations.get_user_cache_dir() / "timtools"
if not CACHE_DIR.is_dir():
    CACHE_DIR.mkdir()

CONFIG_DIR: Path
possible_config_dirs = (
    timtools.locations.get_user_config_dir() / "timtools",  # user config
    Path("/etc/timtools"),  # global config
    PROJECT_DIR / "tim_config",  # package config
)
if not any(path.is_dir() for path in possible_config_dirs):
    print("No existing config locations where found")

possible_config_files: list[Path] = [
    path / "timtools.ini" for path in possible_config_dirs
]

USER_CONFIG: configparser.ConfigParser = configparser.ConfigParser()
USER_CONFIG.read(possible_config_files)


def replace_config_with_dummy():
    """
    Replaces the USER_CONFIG variable with dummy values to enable testing,
    without providing actual user config
    """
    timtools.settings.USER_CONFIG = {
        "telegram": {
            "chat_id": "12345",
            "chat_user": "testuser",
            "api_key": "ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        },
        "ntfy": {
            "default_topic": "https://example.com/testtopic",
            "default_user": "testuser",
            "default_password": "testpassword",
        },
    }
