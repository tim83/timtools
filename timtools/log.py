#! /usr/bin/python3

import logging
import os
import sys

user: str = os.environ["USER"]


class LogConfig:
	logfile: str = f"/tmp/python_{user}.log"
	steam_format: str = '%(name)s (%(lineno)d): %(message)s'
	file_format: str = '%(asctime)s - %(levelname)s - %(name)s (%(lineno)d): %(message)s'
	stream_handler: logging.StreamHandler = None
	file_handler: logging.FileHandler = None

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


def set_verbose(verbose: bool) -> None:
	if verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.WARNING)


def _get_file_handler(filename: str) -> logging.FileHandler:
	file_handler = logging.FileHandler(filename)
	file_handler.setLevel(logging.DEBUG)
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
	# Gets or creates a logger
	logger = logging.getLogger(name)
	# logger.setLevel(logging.DEBUG)

	logger.addHandler(LogConfig.get_file_handler(filename))

	# set log level
	if verbose or "-v" in sys.argv[1:]:
		set_verbose(True)

	return logger
