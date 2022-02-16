from __future__ import annotations  # python -3.9 compatibility

import getpass
from pathlib import Path

import xdg


def _is_current_user(user: str = None) -> bool:
    return (user is None) or (user == getpass.getuser())


def _use_xdg(user: str = None) -> bool:
    return _is_current_user(user)


def get_user_home(user: str = None) -> Path:
    if _is_current_user(user):
        return Path.home()

    return Path("/home", user)


def get_user_cache_dir(user: str = None) -> Path:
    if _use_xdg(user):
        return xdg.xdg_cache_home()

    return get_user_home(user) / ".cache"


def get_user_config_dir(user: str = None) -> Path:
    if _use_xdg(user):
        return xdg.xdg_config_home()
    return get_user_home(user) / ".config"
