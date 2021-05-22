import datetime as dt
import logging
from typing import *

import pytest
from testfixtures import LogCapture, log_capture

from timtools import log

logger_name: str = "TEST"
logging_levels: List[Tuple[str, int]] = [
	("debug", logging.DEBUG),
	("info", logging.INFO),
	("warning", logging.WARNING),
	("error", logging.ERROR),
	("critical", logging.CRITICAL),
]


@pytest.fixture(autouse=True)
def capture_log():
	with LogCapture() as capture:
		yield capture


@log_capture()
@pytest.mark.parametrize("verbose", [True, False])
def test_get_logger_verbose(capture, verbose: bool):
	logger = log.get_logger(logger_name, verbose=verbose)
	min_level = logging.DEBUG if verbose else logging.WARNING
	for level_name, level_int in logging_levels:
		logger.log(level_int, f"{level_name} log")

	expected_output: List[Tuple[str, str, str]] = [
		(logger_name, level_name.upper(), f"{level_name} log")
		for level_name, level_int in logging_levels
		if level_int >= min_level
	]
	capture.check(*expected_output)


@log_capture()
@pytest.mark.parametrize("verbose_set", [True, False])
def test_set_verbose(capture, verbose_set: bool):
	logger = log.get_logger(logger_name)
	log.set_verbose(verbose_set)
	min_level = logging.DEBUG if verbose_set else logging.WARNING
	for level_name, level_int in logging_levels:
		logger.log(level_int, f"{level_name} log")

	expected_output: List[Tuple[str, str, str]] = [
		(logger_name, level_name.upper(), f"{level_name} log")
		for level_name, level_int in logging_levels
		if level_int >= min_level
	]
	capture.check(*expected_output)

