import logging
import pytest

from bisect import bisect
from src.build.helpers.color import Color
from src.build.helpers.logger import LevelFormatter


logger_message = logging.getLogger(__name__)


class TestLogger:
    def test_logging_config(self, caplog):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        ch.setFormatter(
            LevelFormatter(
                {
                    logging.INFO: Color.GRAY
                    + '%(levelname)s | Zukan Icon Theme %(name)s %(message)s'
                    + Color.END,
                    logging.WARNING: Color.RED
                    + '%(asctime)s | %(levelname)s | Zukan Icon Theme pid=%(process)d %(name)s %(funcName)s:%(lineno)s %(message)s'
                    + Color.END,
                }
            )
        )
        logger.addHandler(ch)

        # Capture log output
        with caplog.at_level(logging.INFO):
            logger.info('Test info message')

        # assert "INFO | Zukan Icon Theme" in caplog.text
        assert 'Test info message' in caplog.text

        with caplog.at_level(logging.WARNING):
            logger.warning('Test warning message')

        assert 'Test warning message' in caplog.text
        assert 'WARNING' in caplog.text


class TestLevelFormatter:
    def setUp(self):
        # Set up the formats to be used in testing
        self.formats = {
            logging.INFO: '%(levelname)s | Zukan Icon Theme %(name)s %(message)s',
            logging.WARNING: '%(asctime)s | %(levelname)s | Zukan Icon Theme '
            '%(name)s %(lineno)s %(message)s',
        }
        self.formatter = LevelFormatter(self.formats)

    def test_format_info_level(self):
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            msg='info message',
            # Attributes above necessary
            pathname='test_path',
            lineno=10,
            args=None,
            exc_info=None,
        )
        TestLevelFormatter.setUp(self)
        output = self.formatter.format(record)
        expected = 'INFO | Zukan Icon Theme test info message'
        assert output == expected

    def test_format_warning_level(self):
        record = logging.LogRecord(
            name='test',
            # Not working if use funcName attribute
            funcName='test_func',
            level=logging.WARNING,
            # Not working if use process attribute
            process=111,
            msg='warning message',
            # Attributes above necessary
            pathname='test_path',
            lineno=10,
            args=None,
            exc_info=None,
        )
        TestLevelFormatter.setUp(self)
        output = self.formatter.format(record)
        assert output.endswith('WARNING | Zukan Icon Theme test 10 warning message')

    def test_invalid_level_in_formats(self):
        with pytest.raises(ValueError):
            LevelFormatter({999: 'Invalid level format'})

    def test_value_error_on_fmt_in_kwargs(self):
        formats = {
            logging.DEBUG: 'debug-format',
            logging.INFO: 'info-format',
        }

        with pytest.raises(
            ValueError,
            match='Format string must be passed to level-surrogate formatters, not this one',
        ):
            LevelFormatter(formats=formats, fmt='incorrect-format')

    def test_bisect_index(self):
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            msg='info message',
            # Attributes above necessary
            pathname='test_path',
            lineno=10,
            args=None,
            exc_info=None,
        )
        TestLevelFormatter.setUp(self)
        idx = bisect(self.formatter.formats, (record.levelno,))
        assert idx == 0  # INFO should be at index 0
