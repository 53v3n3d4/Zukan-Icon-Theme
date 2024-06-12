import logging
import sublime

from bisect import bisect


# Code from link below.
# https://stackoverflow.com/questions/14844970/modifying-logging-message-format-based-on-message-logging-level-in-python3
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

        self.formats = sorted(
            (level, logging.Formatter(fmt, **kwargs)) for level, fmt in formats.items()
        )

    def format(self, record: logging.LogRecord) -> str:
        # print(self.formats)
        if self.formats:
            idx = bisect(self.formats, (record.levelno,), hi=len(self.formats) - 1)
            level, formatter = self.formats[idx]
        return formatter.format(record)


def get_setting_log_level():
    """
    Get 'log_level'setting in 'Zukan Icon Theme.sublime-settings'.

    It also handle all init and coonfig logger.

    Initialize logging is faster than get 'log_level'. So it is being
    initialize using 'set_timeout_async'.
    """

    log_level = sublime.load_settings('Zukan Icon Theme.sublime-settings').get(
        'log_level'
    )

    if log_level == 'DEBUG':
        log_level = logging.DEBUG
    elif log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'WARNING':
        log_level = logging.WARNING
    elif log_level == 'ERROR':
        log_level = logging.ERROR
    elif log_level == 'CRITICAL':
        log_level = logging.CRITICAL
    else:
        log_level = logging.INFO

    # Config below copied from python docs
    # https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial
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


# sublime.load_settings takes more time to get log_level than logging in
# 'file_type_icons' file to init logging.
sublime.set_timeout_async(get_setting_log_level)
