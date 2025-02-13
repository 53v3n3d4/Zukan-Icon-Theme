import _pickle as pickle
import importlib
import os
import sublime
import threading

from unittest import TestCase
from unittest.mock import patch, Mock

constants_pickle = importlib.import_module(
    'Zukan Icon Theme.tests.mocks.constants_pickle'
)
thread_progress = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.thread_progress'
)


class TestThreadProgress(TestCase):
    def setUp(self):
        self.mock_thread = Mock()
        self.mock_thread.is_alive.return_value = True

        self.message = 'Processing'
        self.success_message = 'Done!'
        self.dialog_message = 'Operation completed successfully!'
        self.dialog_message_none = None

        self.test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan Icon Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )

        self.mock_view = Mock()
        self.mock_window = Mock()
        self.mock_window.active_view.return_value = self.mock_view

    @patch('sublime.set_timeout')
    def test_thread_progress_init(self, mock_set_timeout):
        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message, self.dialog_message
        )

        self.assertEqual(progress.thread, self.mock_thread)
        self.assertEqual(progress.message, self.message)
        self.assertEqual(progress.success_message, self.success_message)
        self.assertEqual(progress.dialog_message, self.dialog_message)
        self.assertEqual(progress.addend, 1)
        self.assertEqual(progress.size, 3)
        self.assertIsNone(progress.last_view)
        self.assertIsNone(progress.window)

        mock_set_timeout.assert_called_once()
        self.assertEqual(mock_set_timeout.call_args[0][1], 100)

    def progress_cleanup(self, progress, mock_set_timeout):
        progress.run(0)
        self.mock_view.set_status.assert_called_with('_zukan', self.success_message)

        cleanup_callback = mock_set_timeout.call_args_list[-1][0][0]
        cleanup_callback()

        self.mock_view.erase_status.assert_called_with('_zukan')

    @patch('sublime.set_timeout')
    @patch('sublime.active_window')
    def test_thread_progress_run(self, mock_active_window, mock_set_timeout):
        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message
        )
        mock_active_window.return_value = self.mock_window

        progress.run(0)

        self.assertEqual(progress.window, self.mock_window)
        self.mock_view.set_status.assert_called_with(
            '_zukan', f'{self.message}  ⦿  ⦾  ⦾ '
        )
        self.mock_thread.is_alive.return_value = False

        self.progress_cleanup(progress, mock_set_timeout)

        self.assertEqual(mock_set_timeout.call_args[0][1], 1000)

    @patch('sublime.set_timeout')
    @patch('sublime.active_window')
    def test_thread_progress_run_2(self, mock_active_window, mock_set_timeout):
        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message
        )
        progress.window = self.mock_window

        expected_frames = [
            f'{self.message}  ⦿  ⦾  ⦾ ',
            f'{self.message}  ⦾  ⦿  ⦾ ',
            f'{self.message}  ⦾  ⦾  ⦿ ',
        ]

        for i, expected in enumerate(expected_frames):
            progress.run(i)
            self.mock_view.set_status.assert_called_with('_zukan', expected)

        self.mock_thread.is_alive.return_value = False

        self.progress_cleanup(progress, mock_set_timeout)

    def progress_cleanup_2(self, mock_set_timeout):
        callback = mock_set_timeout.call_args_list[0][0][0]
        callback()

        self.mock_view.erase_status.assert_called_with('_zukan')

    @patch('sublime.active_window')
    @patch('sublime.set_timeout')
    def test_thread_progress_fail(self, mock_set_timeout, mock_active_window):
        self.mock_thread.is_alive.return_value = False
        self.mock_thread.result = False

        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message
        )
        progress.window = self.mock_window
        progress.last_view = self.mock_view

        progress.run(0)

        self.progress_cleanup_2(mock_set_timeout)

    @patch('sublime.active_window')
    @patch('sublime.set_timeout')
    def test_thread_progress_run_view_changed(
        self, mock_set_timeout, mock_active_window
    ):
        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message
        )
        progress.window = self.mock_window

        previous_view = Mock()
        progress.last_view = previous_view

        new_view = Mock()
        self.mock_window.active_view.return_value = new_view

        progress.run(0)

        previous_view.erase_status.assert_called_once_with('_zukan')

        new_view.set_status.assert_called_once()
        self.assertEqual(progress.last_view, new_view)

        progress.last_view = self.mock_view
        self.progress_cleanup_2(mock_set_timeout)

    @patch('sublime.set_timeout')
    def test_thread_progress_circle_direction(self, mock_set_timeout):
        progress = thread_progress.ThreadProgress(
            self.mock_thread, self.message, self.success_message
        )

        self.assertEqual(progress.addend, 1)
        progress.run(2)
        self.assertEqual(progress.addend, -1)
        progress.run(0)
        self.assertEqual(progress.addend, 1)

        progress.last_view = self.mock_view
        self.progress_cleanup_2(mock_set_timeout)

    def load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def test_mock_thread_progress(self):
        ts = threading.Thread(
            target=TestThreadProgress.load_pickle, args=(self, self.test_file_path)
        )
        ts.start()

        mock = Mock()
        mock.thread_progress.ThreadProgress(
            ts, self.message, self.success_message, None
        )
        mock.thread_progress.ThreadProgress.assert_called_with(
            ts, self.message, self.success_message, None
        )
        mock.thread_progress.ThreadProgress.assert_called_once()

    def test_thread_progress_params(self):
        ts = threading.Thread(
            target=TestThreadProgress.load_pickle, args=(self, self.test_file_path)
        )
        ts.start()

        thread_progress.ThreadProgress(ts, self.message, self.success_message)
        self.assertIsInstance(self.message, str)
        self.assertNotIsInstance(self.message, int)
        self.assertNotIsInstance(self.message, list)
        self.assertNotIsInstance(self.message, bool)
        self.assertNotIsInstance(self.message, dict)
        self.assertIsInstance(self.success_message, str)
        self.assertNotIsInstance(self.success_message, int)
        self.assertNotIsInstance(self.success_message, list)
        self.assertNotIsInstance(self.success_message, bool)
        self.assertNotIsInstance(self.success_message, dict)
        self.assertIsNone(self.dialog_message_none, None)
        self.assertNotIsInstance(self.dialog_message_none, int)
        self.assertNotIsInstance(self.dialog_message_none, list)
        self.assertNotIsInstance(self.dialog_message_none, bool)
        self.assertNotIsInstance(self.dialog_message_none, dict)
