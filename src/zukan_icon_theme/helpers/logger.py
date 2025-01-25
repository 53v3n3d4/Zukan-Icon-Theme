import logging
import sublime

from .load_save_settings import get_settings
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from bisect import bisect


# Code from link below.
# https://stackoverflow.com/questions/14844970/
# modifying-logging-message-format-based-on-message-logging-level-in-python3
class LevelFormatter(logging.Formatter):
    """
    Different formatters for each level.
    """

    def __init__(self, formats: dict, **kwargs):
        super().__init__()

        if 'fmt' in kwargs:
            raise ValueError(
                'Format string must be passed to level-surrogate formatters, '
                'not this one'
            )

        self.formats = (
            sorted(
                (level, logging.Formatter(fmt, **kwargs))
                for level, fmt in formats.items()
            )
            if formats
            else []
        )

    def format(self, record: logging.LogRecord) -> str:
        if self.formats:
            idx = bisect(self.formats, (record.levelno,), hi=len(self.formats) - 1)
            level, formatter = self.formats[idx]
            return formatter.format(record)
        return super().format(record)


def logging_config(log_level: str):
    """
    Config logger.

    Config below copied from python docs
    https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial

    Parameters:
    log_level (str) --  log level name.
    """

    # create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # create console handler and set level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter
    # formatter = logging.Formatter(
    #     '%(asctime)s | %(process)d | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'
    # )

    # add formatter to ch
    # ch.setFormatter(formatter)
    ch.setFormatter(
        LevelFormatter(
            {
                logging.INFO: '%(levelname)s | Zukan Icon Theme %(filename)s %(message)s',
                logging.WARNING: '%(asctime)s | %(levelname)s | Zukan Icon Theme '
                'pid=%(process)d %(filename)s %(funcName)s:%(lineno)s %(message)s',
            }
        )
    )

    # add ch to logger
    logger.addHandler(ch)

    # prevent root logger from catching this
    # https://github.com/SublimeText/PackageDev/blob/master/_logging.py
    logger.propagate = False

    # 'application' code
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')


def reset_logging_config(log_level: str):
    """
    Reset logger.
    """
    logger = logging.getLogger()

    # Remove existing handlers:
    # - Helps prevent duplicate messages when reloading `file_type_icons`.
    # - If installed via `.sublime-package` file, it ensures that when package
    #   is placed in the ignored packages list and then enabled, the logger
    #   doesn't need to be restarted to avoid seeing the `TypeError`.
    #   There are still 3 `TypeError` messages after enabling, but the logger
    #   works correctly afterward.
    if logger.hasHandlers():
        logger.handlers.clear()

    logging_config(log_level)


def get_setting_log_level():
    """
    Get `log_level` setting in `Zukan Icon Theme.sublime-settings`.

    Initialize logging is faster than get `log_level`. So it is being
    initialize using 'set_timeout_async'.
    """

    log_level = get_settings(ZUKAN_SETTINGS, 'log_level')

    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    log_level = level_map.get(log_level, logging.INFO)

    # logging_config(log_level)
    reset_logging_config(log_level)

    return log_level


# sublime.load_settings takes more time to get log_level than logging in
# 'file_type_icons' file to init logging.
# sublime.set_timeout_async(get_setting_log_level)


def init_logger():
    if not logging.getLogger().hasHandlers():
        # sublime.load_settings takes more time to get log_level than
        # logging in `file_type_icons` file to init logging.
        sublime.set_timeout_async(get_setting_log_level)


# Initialize logging async
init_logger()
