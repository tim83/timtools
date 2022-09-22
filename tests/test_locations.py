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
    tim_cache = timtools.locations.get_user_cache_dir("tim")
    assert isinstance(tim_cache, Path)
    assert str(tim_cache).startswith("/home/tim")
    assert str(tim_cache).endswith("cache")


def test_get_user_config_dir():
    tim_config = timtools.locations.get_user_config_dir("tim")
    assert isinstance(tim_config, Path)
    assert str(tim_config).startswith("/home/tim")
    assert str(tim_config).endswith("config")
