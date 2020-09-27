#! /usr/bin/python3

import logging
import sys

logging.basicConfig(format='%(name)s: %(message)s')


class LogConfig:
	logfile: str = "/tmp/python_default.log"


def set_verbose(verbose: bool) -> None:
	if verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.WARNING)


def get_logger(name: str = __name__, verbose: bool = False, filename: str = LogConfig.logfile) -> logging.Logger:
	# Gets or creates a logger
	logger = logging.getLogger(name)
	# logger.setLevel(logging.DEBUG)

	# set log level
	if verbose or "-v" in sys.argv[1:]:
		set_verbose(True)

	# add console handler to logger
	# logger.addHandler(console_handler)

	# define file handler and set formatter
	file_handler = logging.FileHandler(filename)
	file_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
	file_handler.setFormatter(formatter)

	# add file handler to logger
	logger.addHandler(file_handler)

	return logger
