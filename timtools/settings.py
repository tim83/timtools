import configparser
import os

PROJECT_DIR: str = os.path.dirname(__file__)
CACHE_DIR: str = os.path.expanduser("~/.cache/timtools")
CONFIG_DIR: str = os.path.expanduser("~/.config/timtools")
if not os.path.isdir(CONFIG_DIR):
    code_src_config_dir: str = os.path.expanduser(
        "/home/tim/Programs/python/timtools/tim_config"
    )
    if os.path.isdir(code_src_config_dir):
        CONFIG_DIR = code_src_config_dir

CONFIG_FILE: str = os.path.join(CONFIG_DIR, "timtools.ini")
GOOGLE_CLIENT_SECRET_FILE: str = os.path.join(CONFIG_DIR, "google_client_secret.json")

USER_CONFIG: configparser.ConfigParser = configparser.ConfigParser()
USER_CONFIG.read(CONFIG_FILE)
