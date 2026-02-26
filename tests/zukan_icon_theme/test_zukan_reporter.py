import importlib
import os

from datetime import datetime
from unittest import TestCase
from unittest.mock import call, Mock, mock_open, patch

zukan_reporter = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.zukan_reporter'
)


class TestReporter(TestCase):
    def setUp(self):
        self.mock_view = Mock()
        self.mock_window = Mock()
        self.mock_view.window.return_value = self.mock_window
        self.reporter = zukan_reporter.Reporter(self.mock_view)

    def test_reporter_init(self):
        expected_path = os.path.join(
            zukan_reporter.ZUKAN_PKG_SUBLIME_PATH, 'zukan_reports.txt'
        )
        self.assertEqual(self.reporter.view, self.mock_view)
        self.assertEqual(self.reporter.profile_file_path, expected_path)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_file(self, mock_file, mock_exists):
        mock_exists.return_value = False
        test_output = 'test report'

        self.reporter.save_file(test_output)

        mock_file.assert_called_once_with(self.reporter.profile_file_path, 'w')
        mock_file().write.assert_called_once_with(test_output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='previous report')
    def test_save_file_exists(self, mock_file, mock_exists):
        mock_exists.return_value = True
        test_output = 'new report'

        self.reporter.save_file(test_output)

        expected_calls = [
            call(self.reporter.profile_file_path, 'r'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None),
            call(self.reporter.profile_file_path, 'w'),
            call().__enter__(),
            call().write('new report\n\nprevious report'),
            call().__exit__(None, None, None),
        ]

        mock_file.assert_has_calls(expected_calls, any_order=False)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_report_file(self, mock_remove, mock_exists):
        mock_exists.return_value = True

        result = self.reporter._delete_report_file()

        mock_remove.assert_called_once_with(self.reporter.profile_file_path)
        self.assertEqual(result, self.reporter.profile_file_path)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_report_file_not_exists(self, mock_remove, mock_exists):
        mock_exists.return_value = False

        result = self.reporter._delete_report_file()

        mock_remove.assert_not_called()
        self.assertIsNone(result)

    @patch.object(zukan_reporter, 'datetime')
    def test_add_title_time(self, mock_datetime):
        mock_now = datetime(2022, 12, 8, 12, 34, 56)
        mock_datetime.now.return_value = mock_now
        self.reporter.save_file = Mock()

        title = 'Test Title'
        result = 'Test Report'
        expected_date = '2022-12-08 12:34:56'

        self.reporter._add_title_time(title, result)

        expected_output = (
            '\t'
            + title
            + ' =====================\n\n'
            + '\t'
            + expected_date
            + '\n\n'
            + result
        )

        # Normalize CRLF for Windows CI
        expected_output = expected_output.replace('\r\n', '\n')
        actual_output = self.reporter.save_file.call_args[0][0].replace('\r\n', '\n')

        self.assertEqual(expected_output, actual_output)

    @patch.object(zukan_reporter.Reporter, '_delete_report_file')
    @patch.object(zukan_reporter.Reporter, '_zukan_preferences_settings')
    @patch.object(zukan_reporter.Reporter, '_profile_results')
    def test_report_to_file(self, mock_profile, mock_preferences, mock_delete):
        self.reporter.report_to_file('Clear reports file')
        mock_delete.assert_called_once()

        self.reporter.report_to_file('Zukan preferences settings')
        mock_preferences.assert_called_once_with('Zukan preferences settings')

        test_cases = [
            ('Profile build_preferences', 'build_preferences'),
            ('Profile build_syntax', 'build_syntax'),
            ('Profile build_syntaxes', 'build_syntaxes'),
            ('Profile create_icons_themes', 'create_icons_themes'),
            ('Profile get_user_theme', 'get_user_theme'),
        ]

        for option, _ in test_cases:
            self.reporter.report_to_file(option)
            mock_profile.assert_called()


class TestZukanReporterCommand(TestCase):
    def setUp(self):
        self.command = zukan_reporter.ZukanReporterCommand(Mock())

    def test_zukan_reporter_command_run(self):
        with patch.object(zukan_reporter, 'Reporter') as MockReporter:
            self.command.run(Mock(), 'test_option')
            MockReporter.assert_called_once_with(self.command.view)
            MockReporter().report_to_file.assert_called_once_with('test_option')

    def test_zukan_reporter_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, zukan_reporter.ZukanReporterrOptionsInputHandler)


class TestZukanReporterOptionsInputHandler(TestCase):
    def setUp(self):
        self.handler = zukan_reporter.ZukanReporterrOptionsInputHandler()

    def test_zukan_reporter_options_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'report_option')

    def test_zukan_reporter_options_input_handler_placeholder(self):
        with patch('sublime.status_message') as mock_status:
            result = self.handler.placeholder()
            mock_status.assert_called_once()
            self.assertEqual(result, 'Select option')

    def test_zukan_reporter_options_input_handler_list_items(self):
        self.assertEqual(
            self.handler.list_items(), zukan_reporter.ZUKAN_REPORTS_OPTIONS
        )
