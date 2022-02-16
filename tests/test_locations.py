import os
from pathlib import Path

import timtools.locations


def test_is_current_user():
    current_user = os.getenv("USER")
    other_user = current_user + "RANDOMSTRING"
    assert timtools.locations._is_current_user(current_user) is True
    assert timtools.locations._is_current_user(other_user) is False


def test_get_user_home():
    assert timtools.locations.get_user_home("tim") == Path("/home/tim")


def test_get_user_cache_dir():
    assert timtools.locations.get_user_cache_dir("tim") == Path("/home/tim/.cache")


def test_get_user_config_dir():
    assert timtools.locations.get_user_config_dir("tim") == Path("/home/tim/.config")
