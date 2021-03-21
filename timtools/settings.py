import configparser
import os

PROJECT_DIR: str = os.path.dirname(__file__)
CACHE_DIR: str = os.path.expanduser("~/.cache/timtools")
CONFIG_DIR: str = os.path.expanduser("~/.config/timtools")
CONFIG_FILE: str = os.path.join(CONFIG_DIR, "timtools.ini")
GOOGLE_CLIENT_SECRET_FILE: str = os.path.join(CONFIG_DIR, "google_client_secret.json")

USER_CONFIG: configparser.ConfigParser = configparser.ConfigParser()
USER_CONFIG.read(CONFIG_FILE)
