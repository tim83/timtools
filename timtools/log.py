#! /usr/bin/python3

import logging
import sys


class LogConfig:
	logfile: str = "python.log"
	steam_format: str = '%(name)s (%(lineno)d): %(message)s'
	file_format: str = '%(asctime)s - %(levelname)s - %(name)s (%(lineno)d): %(message)s'


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
	stream_handler.setLevel(logging.WARNING)
	return stream_handler


def get_logger(name: str, verbose: bool = False, filename: str = LogConfig.logfile) -> logging.Logger:
	# Gets or creates a logger
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	logger.addHandler(_get_stream_handler())
	logger.addHandler(_get_file_handler(filename))

	# set log level
	if verbose or "-v" in sys.argv[1:]:
		set_verbose(True)

	return logger
