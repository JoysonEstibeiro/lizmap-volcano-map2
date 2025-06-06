__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

import functools
import os
import time
import traceback

from contextlib import contextmanager

from qgis.core import Qgis, QgsMessageLog

from lizmap_server.tools import to_bool

PLUGIN = 'Lizmap'
DEBUG = False


# noinspection PyTypeChecker
class Logger:

    @staticmethod
    def info(message: str):
        QgsMessageLog.logMessage(str(message), PLUGIN, Qgis.MessageLevel.Info)

    @staticmethod
    def warning(message: str):
        QgsMessageLog.logMessage(str(message), PLUGIN, Qgis.MessageLevel.Warning)

    @staticmethod
    def critical(message: str):
        QgsMessageLog.logMessage(str(message), PLUGIN, Qgis.MessageLevel.Critical)

    @staticmethod
    def log_exception(e: BaseException):
        """ Log a Python exception. """
        Logger.critical(
            "Critical exception:\n{e}\n{traceback}".format(
                e=e,
                traceback=traceback.format_exc(),
            ),
        )


def exception_handler(func):
    """ Decorator to catch all exceptions. """
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if to_bool(os.getenv("CI")):
                Logger.log_exception(e)
                raise
            Logger.log_exception(e)
    return inner_function


@contextmanager
def trap():
    """ Define a trap context for catching all exceptions """
    try:
        yield
    except Exception as e:
        if to_bool(os.getenv("CI")):
            Logger.log_exception(e)
            raise
        Logger.log_exception(e)


def log_function(func):
    """ Decorator to log function. """
    @functools.wraps(func)
    def log_function_core(*args, **kwargs):
        Logger.info(func.__name__)
        value = func(*args, **kwargs)
        return value

    return log_function_core


def profiling(func):
    """ Decorator to make some profiling. """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        Logger.info(f"{func.__name__} ran in {round(end - start, 2)}s")
        return result

    return wrapper


def log_output_value(func):
    """ Decorator to log the output of the function. """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if DEBUG:
            Logger.info(f"{func.__name__} output is {result} for parameter {args!s}")
        else:
            Logger.info(f"{func.__name__} output is {result[0:200]}… for parameter {args!s}")
        return result

    return wrapper
