#! /usr/bin/python3

import logging
import sys


class LogConfig:
	logfile: str = "/tmp/python_default.log"


def get_logger(name: str = __name__, filename: str = LogConfig.logfile) -> logging.Logger:
	# Gets or creates a logger
	logger = logging.getLogger(name)
	# logger.setLevel(logging.DEBUG)

	# define console handler and set formatter
	console_handler = logging.StreamHandler()
	formatter = logging.Formatter('%(name)s: %(message)s')
	console_handler.setFormatter(formatter)
	# set log level
	if "-v" in sys.argv[1:]:
		console_handler.setLevel(logging.DEBUG)
		logging.basicConfig(level=logging.DEBUG)

	# add console handler to logger
	logger.addHandler(console_handler)

	# define file handler and set formatter
	file_handler = logging.FileHandler(filename)
	file_handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
	file_handler.setFormatter(formatter)

	# add file handler to logger
	logger.addHandler(file_handler)

	return logger
