#! /usr/bin/python3
"""Tests the functions in bash.py related to executing bash command"""

import datetime as dt
import subprocess

import pytest

from timtools import bash

TEST_STR: str = "Hello World"


def test_bash_getoutput():
    """Tests the get_output method from bash.py"""
    assert bash.get_output(["echo", "-n", TEST_STR]) == TEST_STR


def test_bash_run():
    """Tests the run method from bash.py"""
    # Check output of command
    assert bash.run(["echo", "-n", TEST_STR]).output == ""
    assert bash.run(["echo", "-n", TEST_STR], capture_stdout=True).output == TEST_STR
    assert bash.run(["echo", "-n", TEST_STR], capture_stderr=True).output == ""
    assert bash.run(["echo", "-n", TEST_STR], capture_stderr=True).output == ""

    # Check command that does not exist
    with pytest.raises(FileNotFoundError):
        bash.run(["thiscommanddoesnotexist"])

    # Check failing command
    with pytest.raises(subprocess.CalledProcessError):
        bash.run(["false"])

    run_failed_expt = bash.run(["false"], passable_exit_codes=[1])
    assert run_failed_expt.output == "" and run_failed_expt.exit_code == 1


def test_timeout():
    start = dt.datetime.now()
    with pytest.raises(subprocess.TimeoutExpired):
        bash.run(["sleep", "5s"], timeout=1)
    end = dt.datetime.now()
    process_time = end - start
    assert process_time.total_seconds() < 2


def test_custom_env():
    assert f"TEST_ENV={TEST_STR}" in bash.get_output(
        ["env"], custom_env={"TEST_ENV": TEST_STR}
    )


def test_kwargs():
    output = bash.get_output(["pwd"], cwd="/tmp")
    assert output == "/tmp"
