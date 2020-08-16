import logging

logfile = "/tmp/python_default.log"


def get_logger(name=__name__, verbose=False, filename=logfile):
	# Gets or creates a logger
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	# define console handler and set formatter
	console_handler = logging.StreamHandler()
	formatter = logging.Formatter('%(name)s: %(message)s')
	console_handler.setFormatter(formatter)
	# set log level
	if verbose:
		console_handler.setLevel(logging.DEBUG)
	else:
		console_handler.setLevel(logging.WARN)

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
