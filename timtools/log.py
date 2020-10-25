#! /usr/bin/python3

import logging
import os
import sys

user: str = os.environ.get("USER", "tim")


class LogConfig:
	logfile: str = f"/tmp/python_{user}.log"
	steam_format: str = '%(name)s (%(lineno)d): %(message)s'
	file_format: str = '%(asctime)s - %(levelname)s - %(name)s (%(lineno)d): %(message)s'
	stream_handler: logging.StreamHandler = None
	file_handler: logging.FileHandler = None
	verbose_level: int = logging.DEBUG
	quiet_level: int = logging.WARNING

	@staticmethod
	def get_file_handler(filename) -> logging.FileHandler:
		if not LogConfig.file_handler:
			LogConfig.file_handler = _get_file_handler(filename)
		return LogConfig.file_handler

	@staticmethod
	def get_stream_handler() -> logging.StreamHandler:
		if not LogConfig.stream_handler:
			LogConfig.stream_handler = _get_stream_handler()
		return LogConfig.stream_handler


logging.basicConfig(format=LogConfig.steam_format)


def set_verbose(verbose: bool, logger: logging.Logger = None) -> None:
	if verbose:
		level = LogConfig.verbose_level
	else:
		level = LogConfig.quiet_level

	logging.basicConfig(level=level)
	if logger:
		logger.setLevel(level)


def _get_file_handler(filename: str) -> logging.FileHandler:
	file_handler = logging.FileHandler(filename)
	# file_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter(LogConfig.file_format)
	file_handler.setFormatter(formatter)
	return file_handler


def _get_stream_handler() -> logging.StreamHandler:
	stream_handler = logging.StreamHandler()
	formatter = logging.Formatter(LogConfig.steam_format)
	stream_handler.setFormatter(formatter)
	# stream_handler.setLevel(logging.WARNING)
	return stream_handler


def get_logger(name: str, verbose: bool = False, filename: str = LogConfig.logfile) -> logging.Logger:
	# Gets or creates a logger)
	logger = logging.getLogger(name)

	logger.addHandler(LogConfig.get_file_handler(filename))

	# set log level
	if verbose or "-v" in sys.argv[1:]:
		logger.setLevel(LogConfig.verbose_level)
	else:
		logger.setLevel(LogConfig.quiet_level)

	return logger
