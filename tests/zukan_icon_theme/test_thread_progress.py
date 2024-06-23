import _pickle as pickle
import importlib
import os
import sublime
import threading

from unittest import TestCase
from unittest.mock import Mock

constants_pickle = importlib.import_module(
    'Zukan Icon Theme.tests.mocks.constants_pickle'
)
thread_progress = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.thread_progress'
)

message = 'Load yaml file'
success_message = 'Load done'
dialog_message = None

test_file_path = os.path.join(
    sublime.packages_path(),
    'Zukan Icon Theme',
    constants_pickle.TEST_PICKLE_AUDIO_FILE,
)


class TestThreadProgress(TestCase):
    def load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def test_mock_thread_progress(self):
        ts = threading.Thread(
            target=TestThreadProgress.load_pickle, args=(self, test_file_path)
        )
        ts.start()

        mock = Mock()
        mock.thread_progress.ThreadProgress(ts, message, success_message, None)
        mock.thread_progress.ThreadProgress.assert_called_with(
            ts, message, success_message, None
        )
        mock.thread_progress.ThreadProgress.assert_called_once()

    def test_thread_progress_params(self):
        ts = threading.Thread(
            target=TestThreadProgress.load_pickle, args=(self, test_file_path)
        )
        ts.start()

        thread_progress.ThreadProgress(ts, message, success_message)
        self.assertIsInstance(message, str)
        self.assertNotIsInstance(message, int)
        self.assertNotIsInstance(message, list)
        self.assertNotIsInstance(message, bool)
        self.assertNotIsInstance(message, dict)
        self.assertIsInstance(success_message, str)
        self.assertNotIsInstance(success_message, int)
        self.assertNotIsInstance(success_message, list)
        self.assertNotIsInstance(success_message, bool)
        self.assertNotIsInstance(success_message, dict)
        self.assertIsNone(dialog_message, None)
        self.assertNotIsInstance(dialog_message, int)
        self.assertNotIsInstance(dialog_message, list)
        self.assertNotIsInstance(dialog_message, bool)
        self.assertNotIsInstance(dialog_message, dict)
