import importlib
import logging

from unittest import TestCase

logger = logging.getLogger(__name__)


class TestLoggerMessages(TestCase):
    def test_log_messages(self):
        with self.assertLogs(logger) as cm:
            logger.debug('debug message')
            logger.info('info message')
            logger.warning('warning message')
            logger.error('error message')
            logger.critical('critical message')
            self.assertListEqual(
                cm.output,
                [
                    'INFO:test_logger:info message',
                    'WARNING:test_logger:warning message',
                    'ERROR:test_logger:error message',
                    'CRITICAL:test_logger:critical message',
                ],
            )
