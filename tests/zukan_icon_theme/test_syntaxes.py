import importlib

from unittest import TestCase
from unittest.mock import Mock, patch

syntaxes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.syntaxes'
)


class TestSyntaxes(TestCase):
    def setUp(self):
        self.syntaxes = syntaxes.Syntaxes('/test/path')
        self.mock_zukan_data = [
            {
                'name': 'ATest',
                'syntax': [
                    {
                        'name': 'ATest',
                        'scope': 'source.atest',
                        'file_extensions': ['abc'],
                    }
                ],
            }
        ]

    @patch.object(syntaxes, 'read_pickle_data')
    def test_zukan_icons_data(self, mock_read_pickle):
        mock_read_pickle.return_value = self.mock_zukan_data
        result = self.syntaxes.zukan_icons_data()
        self.assertEqual(result, self.mock_zukan_data)

    @patch.object(syntaxes, 'get_change_icon_settings')
    def test_change_icon_file_extension_setting(self, mock_settings):
        mock_settings.return_value = (None, ['txt'])
        result = self.syntaxes.change_icon_file_extension_setting()
        self.assertEqual(result, ['txt'])

    @patch.object(syntaxes, 'get_ignored_icon_settings')
    def test_ignored_icon_setting(self, mock_ignored):
        mock_ignored.return_value = ['ignored_icon']
        result = self.syntaxes.ignored_icon_setting()
        self.assertEqual(result, ['ignored_icon'])

    def test_get_installed_syntaxes(self):
        self.syntaxes.list_created_icons_syntaxes = Mock(
            return_value=['ATest-2.sublime-syntax', 'ATest-1.sublime-syntax']
        )
        result = self.syntaxes.get_installed_syntaxes()
        self.assertEqual(result, ['ATest-1.sublime-syntax', 'ATest-2.sublime-syntax'])

    def test_get_not_installed_syntaxes(self):
        self.syntaxes.zukan_icons_data = Mock(return_value=self.mock_zukan_data)
        self.syntaxes.get_compare_scopes = Mock(return_value=set())
        self.syntaxes.change_icon_file_extension_setting = Mock(return_value=[])
        self.syntaxes.get_list_icons_syntaxes = Mock(return_value=self.mock_zukan_data)

        self.syntaxes.list_created_icons_syntaxes = Mock(return_value=set())

        with patch.object(
            syntaxes,
            'edit_file_extension',
            return_value=['atest'],
        ):
            result = self.syntaxes.get_not_installed_syntaxes()
            expected = ['ATest.sublime-syntax']
            self.assertEqual(sorted(result), sorted(expected))

    @patch('os.path.splitext')
    @patch.object(syntaxes.sublime, 'error_message')
    @patch.object(syntaxes.Syntaxes, 'zukan_icons_data')
    @patch.object(syntaxes.Syntaxes, 'get_list_icons_syntaxes')
    @patch.object(syntaxes.Syntaxes, 'ignored_icon_setting')
    @patch.object(syntaxes.Syntaxes, 'install_syntax')
    def test_install_icon_syntax(
        self,
        mock_install_syntax,
        mock_ignored_icon_setting,
        mock_get_list_icons_syntaxes,
        mock_zukan_icons_data,
        mock_error_message,
        mock_splitext,
    ):
        mock_splitext.return_value = ('ATest', '.sublime-syntax')
        mock_zukan_icons_data.return_value = 'test_data'
        mock_get_list_icons_syntaxes.return_value = [
            {'name': 'ATest', 'syntax': [{'name': 'ATest'}]},
            {'name': 'ATest-2', 'syntax': [{'name': 'ATest-2'}]},
        ]
        mock_ignored_icon_setting.return_value = []

        self.syntaxes.install_icon_syntax('ATest.sublime-syntax')

        mock_install_syntax.assert_called_once_with('ATest', 'ATest.sublime-syntax')

        mock_ignored_icon_setting.return_value = ['ATest']
        self.syntaxes.install_icon_syntax('ATest.sublime-syntax')

        mock_error_message.assert_called_once_with(
            'ATest icon is disabled. Need to enable first.'
        )

    @patch.object(syntaxes, 'sublime')
    def test_install_icon_syntax_ignored(self, mock_sublime):
        self.syntaxes.zukan_icons_data = Mock(return_value=self.mock_zukan_data)
        self.syntaxes.ignored_icon_setting = Mock(return_value=['ATest'])

        self.syntaxes.install_icon_syntax('ATest.sublime-syntax')
        mock_sublime.error_message.assert_called_once()

    @patch.object(syntaxes, 'sublime')
    def test_confirm_delete(self, mock_sublime):
        mock_sublime.ok_cancel_dialog.return_value = True
        result = self.syntaxes.confirm_delete('Test message')
        self.assertTrue(result)
        mock_sublime.ok_cancel_dialog.assert_called_with('Test message')


class TestDeleteSyntaxCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = syntaxes.DeleteSyntaxCommand(self.view)
        self.command.syntaxes = Mock()
        self.command.syntaxes.syntaxes_path = '/test/path'

    def test_delete_syntax_command_is_enabled(self):
        self.command.syntaxes.get_installed_syntaxes.return_value = [
            'ATest.sublime-syntax'
        ]
        self.assertTrue(self.command.is_enabled())

        self.command.syntaxes.get_installed_syntaxes.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_delete_syntax_command_is_enabled_none(self):
        self.command.syntaxes.get_installed_syntaxes.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_delete_syntax_command_run_all(self):
        self.command.syntaxes.confirm_delete.return_value = True
        self.command.run(None, syntax_name='All')
        self.command.syntaxes.delete_all_icons_syntaxes.assert_called_once()

    def test_delete_syntax_command_run(self):
        self.command.syntaxes.confirm_delete.return_value = True
        self.command.run(None, syntax_name='ATest.sublime-syntax')
        self.command.syntaxes.delete_single_icon_syntax.assert_called_with(
            'ATest.sublime-syntax'
        )

    def test_delete_syntax_command_run_cancel(self):
        self.command.syntaxes.confirm_delete.return_value = False
        self.command.run(None, syntax_name='ATest.sublime-syntax')
        self.command.syntaxes.delete_single_icon_syntax.assert_not_called()

    def test_delete_syntax_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, syntaxes.DeleteSyntaxInputHandler)


class TestDeleteSyntaxInputHandler(TestCase):
    def setUp(self):
        self.syntaxes = Mock()
        self.handler = syntaxes.DeleteSyntaxInputHandler(self.syntaxes)

    def test_delete_syntax_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'syntax_name')

    def test_delete_syntax_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of created syntaxes')

    def test_delete_syntax_input_handler_list_items(self):
        self.syntaxes.get_installed_syntaxes.return_value = [
            'ATest-2.syntax',
            'ATest-1.syntax',
        ]
        result = self.handler.list_items()
        self.assertEqual(result, ['All', 'ATest-1.syntax', 'ATest-2.syntax'])

    def test_delete_syntax_input_handler_list_items_none(self):
        self.syntaxes.get_installed_syntaxes.return_value = []
        with self.assertRaises(TypeError):
            self.handler.list_items()


class TestInstallSyntaxCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = syntaxes.InstallSyntaxCommand(self.view)
        self.command.syntaxes = Mock()

    def test_install_syntax_command_is_enabled(self):
        self.command.syntaxes.get_not_installed_syntaxes.return_value = [
            'ATest.sublime-syntax'
        ]
        self.assertTrue(self.command.is_enabled())

        self.command.syntaxes.get_not_installed_syntaxes.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_install_syntax_command_is_enabled_none(self):
        self.command.syntaxes.get_not_installed_syntaxes.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_install_syntax_command_run_all(self):
        self.command.run(None, syntax_name='All')
        self.command.syntaxes.install_all_icons_syntaxes.assert_called_once()

    def test_install_syntax_command_run(self):
        self.command.run(None, syntax_name='ATest.sublime-syntax')
        self.command.syntaxes.install_icon_syntax.assert_called_with(
            'ATest.sublime-syntax'
        )

    def test_install_syntax_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, syntaxes.InstallSyntaxInputHandler)


class TestInstallSyntaxInputHandler(TestCase):
    def setUp(self):
        self.syntaxes = Mock()
        self.handler = syntaxes.InstallSyntaxInputHandler(self.syntaxes)

    def test_install_syntax_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'syntax_name')

    def test_install_syntax_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'Zukan syntaxes list')

    def test_install_syntax_input_handler_list_items(self):
        self.syntaxes.get_not_installed_syntaxes.return_value = [
            'ATest-2.syntax',
            'ATest-1.syntax',
        ]
        result = self.handler.list_items()
        self.assertEqual(result, ['All', 'ATest-1.syntax', 'ATest-2.syntax'])

    def test_install_syntax_input_handler_list_items_none(self):
        self.syntaxes.get_not_installed_syntaxes.return_value = []
        with self.assertRaises(TypeError):
            self.handler.list_items()
