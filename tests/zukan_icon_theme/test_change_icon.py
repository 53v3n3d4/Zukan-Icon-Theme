import importlib
import sublime
import sublime_plugin

from unittest import TestCase
from unittest.mock import Mock, patch

change_icon = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon'
)


class TestChangeResetIcon(TestCase):
    def setUp(self):
        self.preferences_file = 'test_preferences.sublime-settings'
        self.icon_handler = change_icon.ChangeResetIcon(self.preferences_file)
        self.test_icon_name = 'ATest'
        self.test_icon_file = 'atest'
        self.test_change_icon = {'ATest-2': 'atest2'}

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.get_change_icon_settings'
    )
    def test_change_icon_setting(self, mock_get_settings):
        expected_settings = {'ATest-3': 'atest3', 'ATest-4': 'atest4'}
        mock_get_settings.return_value = [expected_settings, None]

        result = self.icon_handler.change_icon_setting()

        self.assertEqual(result, expected_settings)
        mock_get_settings.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.sublime.error_message'
    )
    def test_message_required_icon_name_file_missing_name(self, mock_error_message):
        self.icon_handler.message_required_icon_name_file('', 'atest')

        mock_error_message.assert_called_once_with(
            'Name and icon name inputs are required'
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.sublime.error_message'
    )
    def test_message_required_icon_name_file_missing_file(self, mock_error_message):
        self.icon_handler.message_required_icon_name_file('ATest', '')

        mock_error_message.assert_called_once_with(
            'Name and icon name inputs are required'
        )

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.sublime.error_message'
    )
    def test_png_exists_file_not_found(self, mock_error_message, mock_exists):
        mock_exists.return_value = False

        self.icon_handler.png_exists(self.test_icon_name, self.test_icon_file)

        expected_message = (
            '{i} icon PNGs not found.\n\n'
            'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                i=self.test_icon_name, p=self.icon_handler.icon_path
            )
        )
        mock_error_message.assert_called_once_with(expected_message)

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.sublime.error_message'
    )
    def test_png_exists_primary_icon(self, mock_error_message, mock_exists):
        mock_exists.return_value = False
        primary_icon = change_icon.PRIMARY_ICONS[0][2][0]

        self.icon_handler.png_exists('Primary Icon', primary_icon)

        mock_error_message.assert_not_called()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.sublime.error_message'
    )
    def test_message_icon_exists_in_change_icon(self, mock_error_message):
        self.icon_handler.message_icon_exists_in_change_icon(self.test_icon_name)

        expected_message = (
            f'{self.test_icon_name} icon already in setting "change_icon"'
        )
        mock_error_message.assert_called_once_with(expected_message)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.logger')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.set_save_settings')
    def test_reset_change_icon(self, mock_save_settings, mock_logger):
        test_icon = 'ATest'
        change_icon = {'ATest': 'atest', 'ATest-1': 'atest1'}
        expected_result = {'ATest-1': 'atest1'}

        self.icon_handler.reset_change_icon(change_icon, test_icon)

        self.assertNotIn(test_icon, change_icon)
        mock_save_settings.assert_called_once_with(
            self.preferences_file, 'change_icon', expected_result
        )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.logger')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.set_save_settings')
    def test_reset_all_change_icons(self, mock_save_settings, mock_logger):
        change_icon = {'ATest-1': 'atest1', 'ATest-2': 'atest2'}

        self.icon_handler.reset_all_change_icons(change_icon)

        self.assertEqual(len(change_icon), 0)
        mock_save_settings.assert_called_once_with(
            self.preferences_file, 'change_icon', {}
        )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.set_save_settings')
    def test_save_change_icon_setting(self, mock_save_settings):
        test_settings = {'ATest': 'atest'}

        self.icon_handler._save_change_icon_setting(test_settings)

        mock_save_settings.assert_called_once_with(
            self.preferences_file, 'change_icon', test_settings
        )

    def test_initialization(self):
        self.assertEqual(
            self.icon_handler.zukan_preferences_file, self.preferences_file
        )
        self.assertEqual(self.icon_handler.icon_path, change_icon.ZUKAN_PKG_ICONS_PATH)
        self.assertIsInstance(self.icon_handler.zukan_listener_enabled, bool)


class TestChangeIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.change_reset_icon = Mock(spec=change_icon.ChangeResetIcon)
        self.change_reset_icon.zukan_preferences_file = (
            'test_preferences.sublime-settings'
        )
        self.command = change_icon.ChangeIconCommand(self.view)
        self.command.change_reset_icon = self.change_reset_icon

    def test_change_icon_command_init(self):
        command = change_icon.ChangeIconCommand(self.view)
        self.assertIsInstance(command.change_reset_icon, change_icon.ChangeResetIcon)
        self.assertEqual(command.view, self.view)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.change_icon.set_save_settings')
    def test_change_icon_command_run_new_icon(self, mock_set_save_settings):
        change_icon = {'existing': 'file1'}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        self.command.run(Mock(), change_icon_name='newicon', change_icon_file='newfile')

        self.change_reset_icon.message_required_icon_name_file.assert_called_once_with(
            'newicon', 'newfile'
        )
        self.change_reset_icon.png_exists.assert_called_once_with('newicon', 'newfile')
        mock_set_save_settings.assert_called_once_with(
            'test_preferences.sublime-settings',
            'change_icon',
            {'existing': 'file1', 'newicon': 'newfile'},
        )

    def test_change_icon_command_run_existing_icon(self):
        change_icon = {'existing': 'file1'}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        self.command.run(Mock(), change_icon_name='existing', change_icon_file='file1')

        self.change_reset_icon.message_icon_exists_in_change_icon.assert_called_once_with(
            'existing'
        )
        self.change_reset_icon.png_exists.assert_not_called()

    def test_change_icon_command_run_empty_inputs(self):
        change_icon = {}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        self.command.run(Mock(), change_icon_name='', change_icon_file='')

        self.change_reset_icon.message_required_icon_name_file.assert_called_once_with(
            '', ''
        )
        self.change_reset_icon.png_exists.assert_not_called()

    def test_change_icon_command_input_no_args(self):
        result = self.command.input({})
        self.assertIsInstance(result, change_icon.ChangeIconNameInputHandler)

    def test_change_icon_command_input_missing_file(self):
        result = self.command.input({'change_icon_name': 'test'})
        self.assertIsInstance(result, change_icon.ChangeIconFileInputHandler)


class TestChangeIconNameInputHandler(TestCase):
    def setUp(self):
        self.handler = change_icon.ChangeIconNameInputHandler()

    @patch('sublime.status_message')
    def test_change_icon_name_input_handler_placeholder(self, mock_status_message):
        result = self.handler.placeholder()

        self.assertEqual(result, 'Type icon name. E.g. Node.js')
        mock_status_message.assert_called_once_with(
            'Zukan repo has a list of icons name, file-icon.md'
        )

    def test_change_icon_name_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(result, change_icon.ChangeIconFileInputHandler)

    def test_change_icon_name_input_handler_next_input_with_file(self):
        result = self.handler.next_input({'change_icon_file': 'test'})
        self.assertIsNone(result)


class TestChangeIconFileInputHandler(TestCase):
    def setUp(self):
        self.handler = change_icon.ChangeIconFileInputHandler()

    @patch('sublime.status_message')
    def test_change_icon_file_input_handler_placeholder(self, mock_status_message):
        result = self.handler.placeholder()

        self.assertEqual(
            result, 'Type icon file name, without extension. E.g. nodejs-1'
        )
        mock_status_message.assert_called_once_with(
            'Configuration in Zukan Icon Theme > Settings'
        )

    def test_change_icon_file_input_handler_confirm(self):
        self.handler.confirm('ATest')
        self.assertEqual(self.handler.text, 'ATest')

    def test_change_icon_file_input_handler_next_input_back(self):
        self.handler.confirm('back')
        result = self.handler.next_input({})
        self.assertIsInstance(result, sublime_plugin.BackInputHandler)

    def test_change_icon_file_input_handler_next_input_normal(self):
        self.handler.confirm('atest')
        result = self.handler.next_input({})
        self.assertIsNone(result)


class TestResetIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.change_reset_icon = Mock(spec=change_icon.ChangeResetIcon)
        self.command = change_icon.ResetIconCommand(self.view)
        self.command.change_reset_icon = self.change_reset_icon

    def test_reset_icon_command_init(self):
        command = change_icon.ResetIconCommand(self.view)
        self.assertIsInstance(command.change_reset_icon, change_icon.ChangeResetIcon)
        self.assertEqual(command.view, self.view)

    def test_reset_icon_command_run_with_all_icons(self):
        change_icon = {'icon1': 'file1', 'icon2': 'file2'}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        self.command.run(Mock(), icon_name='All')

        self.change_reset_icon.reset_all_change_icons.assert_called_once_with(
            change_icon
        )
        self.change_reset_icon.reset_change_icon.assert_not_called()

    def test_run_with_specific_icon(self):
        change_icon = {'ATest': 'atest', 'ATest-2': 'atest2'}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        self.command.run(Mock(), icon_name='ATest')

        self.change_reset_icon.reset_change_icon.assert_called_once_with(
            change_icon, 'ATest'
        )
        self.change_reset_icon.reset_all_change_icons.assert_not_called()

    def test_reset_icon_command_run_with_no_changes(self):
        self.change_reset_icon.change_icon_setting.return_value = None

        self.command.run(Mock(), icon_name='ATest')

        self.change_reset_icon.reset_change_icon.assert_not_called()
        self.change_reset_icon.reset_all_change_icons.assert_not_called()

    def test_is_enabled_with_changes(self):
        self.change_reset_icon.change_icon_setting.return_value = {'ATest': 'atest'}
        self.assertTrue(self.command.is_enabled())

    def test_is_enabled_with_no_changes(self):
        self.change_reset_icon.change_icon_setting.return_value = {}
        self.assertFalse(self.command.is_enabled())

    def test_is_enabled_with_none(self):
        self.change_reset_icon.change_icon_setting.return_value = None
        self.assertFalse(self.command.is_enabled())

    def test_reset_icon_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, change_icon.ResetIconInputHandler)


class TestResetIconInputHandler(TestCase):
    def setUp(self):
        self.change_reset_icon = Mock(spec=change_icon.ChangeResetIcon)
        self.handler = change_icon.ResetIconInputHandler(self.change_reset_icon)

    def test_reset_icon_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'icon_name')

    def test_reset_icon_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of changed icons')

    def test_reset_icon_input_handler_list_items_with_changes(self):
        change_icon = {'ATest': 'atest', 'ATest-2': 'atest2'}
        self.change_reset_icon.change_icon_setting.return_value = change_icon

        list_input_items = [
            sublime.ListInputItem(text='ATest', value='ATest', annotation='atest'),
            sublime.ListInputItem(text='ATest-2', value='ATest-2', annotation='atest2'),
        ]

        result = self.handler.list_items()

        self.assertEqual(result[0], 'All')

        for i in range(1, len(result)):
            self.assertEqual(result[i].text, list_input_items[i - 1].text)
            self.assertEqual(result[i].value, list_input_items[i - 1].value)
            self.assertEqual(result[i].annotation, list_input_items[i - 1].annotation)

    def test_reset_icon_input_handler_list_items_with_no_changes(self):
        self.change_reset_icon.change_icon_setting.return_value = None

        with self.assertRaises(TypeError):
            self.handler.list_items()
