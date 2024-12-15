import logging

from bisect import bisect
from src.build.helpers.color import Color


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

        self.formats = sorted(
            (level, logging.Formatter(fmt, **kwargs)) for level, fmt in formats.items()
        )

    def format(self, record: logging.LogRecord) -> str:
        idx = bisect(self.formats, (record.levelno,), hi=len(self.formats) - 1)
        level, formatter = self.formats[idx]
        return formatter.format(record)


# Config below copied from python docs
# https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial
# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create console handler and set level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
# formatter = logging.Formatter(
#     '%(asctime)s | %(process)d | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'
# )

# add formatter to ch
# ch.setFormatter(formatter)
ch.setFormatter(
    LevelFormatter(
        {
            logging.INFO: Color.GRAY
            + '%(levelname)s | Zukan Icon Theme %(name)s %(message)s'
            + Color.END,
            logging.WARNING: Color.RED
            + '%(asctime)s | %(levelname)s | Zukan Icon Theme pid=%(process)d'
            ' %(name)s %(funcName)s:%(lineno)s %(message)s' + Color.END,
        }
    )
)

# add ch to logger
logger.addHandler(ch)

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
