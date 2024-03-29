"""Module that wraps the logging module"""
from __future__ import annotations  # python -3.9 compatibility

import logging
import os
import sys
import typing
from pathlib import Path

import timtools.locations

user: str = os.environ.get("USER", "NEMO")


class LogConfig:
    """Configuration for logging"""

    logfile: Path = timtools.locations.get_user_cache_dir() / f"python_{user}.log"
    steam_format: str = "%(name)s (%(lineno)d): %(message)s"
    file_format: str = (
        "%(asctime)s - %(levelname)s - %(name)s (%(lineno)d): %(message)s"
    )
    stream_handler: logging.StreamHandler = None
    file_handler: logging.FileHandler = None
    verbose_level: int = logging.DEBUG
    quiet_level: int = logging.WARNING
    current_level: int = logging.WARNING
    loggers: typing.List[logging.Logger] = []

    @staticmethod
    def get_file_handler(filename: typing.Union[str, Path]) -> logging.FileHandler:
        """Returns a filehandler"""
        if not LogConfig.file_handler:
            LogConfig.file_handler = _get_file_handler(filename)
        return LogConfig.file_handler

    @staticmethod
    def get_stream_handler() -> logging.StreamHandler:
        """Returns a streamhandler"""
        if not LogConfig.stream_handler:
            LogConfig.stream_handler = _get_stream_handler()
        return LogConfig.stream_handler


logging.basicConfig(format=LogConfig.steam_format)


def set_verbose(verbose: bool, logger: logging.Logger = None) -> None:
    """Sets the verbose level of the logging modules"""
    if verbose:
        level = LogConfig.verbose_level
    else:
        level = LogConfig.quiet_level

    logging.basicConfig(level=level)
    if logger:
        logger.setLevel(level)
    else:
        LogConfig.current_level = level
        for active_logger in LogConfig.loggers:
            active_logger.setLevel(level)


def _get_file_handler(filename: typing.Union[str, Path]) -> logging.FileHandler:
    """
    Returns the filehandles
    :param filename: A string or Path of the file that the logger will write to
    :return: The filehandler for the logger
    """
    if isinstance(filename, str):
        filename = Path(filename)

    if not filename.parent.is_dir():
        filename.parent.mkdir()

    file_handler = logging.FileHandler(filename)
    formatter = logging.Formatter(LogConfig.file_format)
    file_handler.setFormatter(formatter)
    return file_handler


def _get_stream_handler() -> logging.StreamHandler:
    """Returns a streamhandler"""
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(LogConfig.steam_format)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(
    name: str,
    verbose: bool = False,
    filename: typing.Union[str, Path] = LogConfig.logfile,
) -> logging.Logger:
    """
    Return a logging object
    :arg name: The name of the logger
    :arg verbose: Does the logger need to print all avaible output?
    :arg filename: The file where the outputs needs to be stored
    """
    # Gets or creates a logger)
    logger = logging.getLogger(name)
    LogConfig.loggers.append(logger)

    file_handler = LogConfig.get_file_handler(filename)
    if file_handler in logger.handlers:
        logger.addHandler(file_handler)

    # set log level
    if verbose or "-v" in sys.argv[1:]:
        logger.setLevel(LogConfig.verbose_level)
    else:
        logger.setLevel(LogConfig.current_level)

    return logger
