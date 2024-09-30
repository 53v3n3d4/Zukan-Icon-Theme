import importlib
import logging

from bisect import bisect
from unittest import TestCase
from unittest.mock import Mock, patch

logger = importlib.import_module('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger')

logger_message = logging.getLogger(__name__)

# https://docs.python.org/3/howto/logging.html#logging-levels
params_list = [
    ('DEBUG', 10),
    ('INFO', 20),
    ('WARNING', 30),
    ('ERROR', 40),
    ('CRITICAL', 50),
]


class TestGetSettingLogLevel(TestCase):
    def test_mock_get_setting_log_level(self):
        mock = Mock()
        mock.logger.get_setting_log_level()
        mock.logger.get_setting_log_level.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.get_settings')
    def test_getting_log_level(self, log_level_mock):
        for p1, p2 in params_list:
            with self.subTest(params_list):
                log_level_mock.return_value = p1
                result = logger.get_setting_log_level()
                self.assertEqual(result, p2)


class TestLoggerMessages(TestCase):
    def test_log_messages(self):
        with self.assertLogs(logger_message) as cm:
            logger_message.debug('debug message')
            logger_message.info('info message')
            logger_message.warning('warning message')
            logger_message.error('error message')
            logger_message.critical('critical message')
            self.assertListEqual(
                cm.output,
                [
                    'INFO:test_logger:info message',
                    'WARNING:test_logger:warning message',
                    'ERROR:test_logger:error message',
                    'CRITICAL:test_logger:critical message',
                ],
            )


class TestLevelFormatter(TestCase):
    def setUp(self):
        # Set up the formats to be used in testing
        self.formats = {
            logging.INFO: '%(levelname)s | Zukan Icon Theme %(name)s %(message)s',
            logging.WARNING: '%(asctime)s | %(levelname)s | Zukan Icon Theme '
            '%(name)s %(lineno)s %(message)s',
        }
        self.formatter = logger.LevelFormatter(self.formats)

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
        output = self.formatter.format(record)
        expected = 'INFO | Zukan Icon Theme test info message'
        self.assertEqual(output, expected)

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
        output = self.formatter.format(record)
        self.assertTrue(
            output.endswith('WARNING | Zukan Icon Theme test 10 warning message')
        )

    def test_invalid_level_in_formats(self):
        with self.assertRaises(ValueError):
            logger.LevelFormatter({999: 'Invalid level format'})

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
        idx = bisect(self.formatter.formats, (record.levelno,))
        self.assertEqual(idx, 0)  # INFO should be at index 0
