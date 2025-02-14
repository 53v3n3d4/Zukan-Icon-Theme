import importlib
import logging

from bisect import bisect
from unittest import TestCase
from unittest.mock import Mock, patch

logger = importlib.import_module('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger')

logger_message = logging.getLogger(__name__)


class TestLoggingConfig(TestCase):
    def setUp(self):
        self.original_logger = logging.getLogger()
        self.original_handlers = self.original_logger.handlers[:]
        self.original_level = self.original_logger.level

    def tearDown(self):
        self.original_logger.handlers = self.original_handlers
        self.original_logger.setLevel(self.original_level)
        self.original_logger.propagate = True

    def test_logging_config(self):
        self.original_logger.handlers = []

        test_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in test_levels:
            with self.subTest(level=level):
                logger.logging_config(level)
                logger_test = logging.getLogger()

                self.assertEqual(logger_test.level, getattr(logging, level))
                self.assertTrue(logger_test.handlers)
                self.assertTrue(
                    any(
                        isinstance(h, logging.StreamHandler)
                        for h in logger_test.handlers
                    )
                )
                self.assertTrue(
                    any(
                        isinstance(h.formatter, logger.LevelFormatter)
                        for h in logger_test.handlers
                    )
                )
                self.assertFalse(logger_test.propagate)


class TestGetSettingLogLevel(TestCase):
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.get_settings')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.reset_logging_config')
    def test_get_setting_log_level(self, mock_reset_config, mock_get_settings):
        params_list = [
            ('DEBUG', logging.DEBUG),
            ('INFO', logging.INFO),
            ('WARNING', logging.WARNING),
            ('ERROR', logging.ERROR),
            ('CRITICAL', logging.CRITICAL),
            ('INVALID', logging.INFO),
        ]

        for setting_value, expected_level in params_list:
            with self.subTest(setting_value=setting_value):
                mock_get_settings.return_value = setting_value

                result = logger.get_setting_log_level()

                self.assertEqual(result, expected_level)
                mock_reset_config.assert_called_with(expected_level)
                mock_get_settings.assert_called_with(logger.ZUKAN_SETTINGS, 'log_level')


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

    def test_value_error_on_fmt_in_kwargs(self):
        formats = {
            logging.DEBUG: 'debug-format',
            logging.INFO: 'info-format',
        }

        with self.assertRaises(ValueError) as context:
            logger.LevelFormatter(formats=formats, fmt='incorrect-format')

        self.assertEqual(
            str(context.exception),
            'Format string must be passed to level-surrogate formatters, not this one',
        )

    def test_format_with_default_formatter(self):
        formats = {}
        formatter = logger.LevelFormatter(formats)

        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=10,
            msg='info message',
            args=None,
            exc_info=None,
        )

        with patch.object(
            logging.Formatter, 'format', return_value='formatted default log'
        ) as mock_super_format:
            formatted_message = formatter.format(record)

            # Check parent format method was called (super().format)
            mock_super_format.assert_called_once_with(record)
            self.assertEqual(formatted_message, 'formatted default log')


class TestResetLoggingConfig(TestCase):
    def test_reset_logging_config_with_handlers(self):
        log_level = 'DEBUG'

        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.logging_config'
            ) as mock_logging_config:
                mock_logger.hasHandlers.return_value = True

                logger.reset_logging_config(log_level)

                mock_logger.handlers.clear.assert_called_once()
                mock_logging_config.assert_called_once_with(log_level)

    def test_reset_logging_config_no_handlers(self):
        log_level = 'DEBUG'

        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.logging_config'
            ) as mock_logging_config:
                mock_logger.hasHandlers.return_value = False

                logger.reset_logging_config(log_level)

                mock_logger.handlers.clear.assert_not_called()
                mock_logging_config.assert_called_once_with(log_level)
