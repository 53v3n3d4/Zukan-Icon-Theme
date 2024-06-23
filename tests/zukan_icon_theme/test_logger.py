import importlib
import logging

from unittest import TestCase
from unittest.mock import Mock, patch

logger = importlib.import_module('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger')

logger_message = logging.getLogger(__name__)

# https://docs.python.org/3/howto/logging.html#logging-levels
params_list = [
    ('CRITICAL', 50),
    ('ERROR', 40),
    ('WARNING', 30),
    ('INFO', 20),
    ('DEBUG', 10),
]


class TestGetSettingLogLevel(TestCase):
    def test_mock_get_setting_log_level(self):
        mock = Mock()
        mock.logger.get_setting_log_level()
        mock.logger.get_setting_log_level.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.logger.load_settings')
    def test_mock_log_level_debug(self, log_level_mock):
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
