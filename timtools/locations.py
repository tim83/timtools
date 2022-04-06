"""Module for determining important directories"""
from __future__ import annotations  # python -3.9 compatibility

import getpass
from pathlib import Path

import xdg


def _is_current_user(user: str = None) -> bool:
    """
    Checks whether a user is the current user
    :param user: The username to check, defaults to the current user
    :return: Is the user the current user?
    """
    return (user is None) or (user == getpass.getuser())


def _use_xdg(user: str = None) -> bool:
    """
    Checks whether the XDG module can be used for a certain user
    :param user: The username to check for, defaults to the current user
    :return: Can the XDG module be used?
    """
    return _is_current_user(user) and any(
        filter(lambda d: not d.startswith("_"), dir(xdg))
    )


def get_user_home(user: str = None) -> Path:
    """
    Returns the home directory for a user
    :param user: The username whose home directory is needed, defaults to the current user
    :return: A path of the user's home directory
    """
    if _is_current_user(user):
        return Path.home()

    return Path("/home", user)


def get_user_cache_dir(user: str = None) -> Path:
    """
    Returns the cache directory for a user
    :param user: The username whose cache directory is needed, defaults to the current user
    :return: A path of the user's cache directory
    """
    if _use_xdg(user):
        return xdg.xdg_cache_home()  # pylint: disable=no-member

    return get_user_home(user) / ".cache"


def get_user_config_dir(user: str = None) -> Path:
    """
    Returns the configuration directory for a user
    :param user: The username whose configuration directory is needed, defaults to the current user
    :return: A path of the user's configuration directory
    """
    if _use_xdg(user):
        return xdg.xdg_config_home()  # pylint: disable=no-member
    return get_user_home(user) / ".config"
