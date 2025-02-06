import importlib

from unittest import TestCase
from unittest.mock import Mock, patch

preferences = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.preferences'
)


class TestPreferences(TestCase):
    def setUp(self):
        self.preferences = preferences.Preferences('test/path')
        self.mock_icon_settings = ['ignored_icon1', 'ignored_icon2']
        self.mock_preferences_list = [
            {
                'name': 'ATest-1',
                'preferences': {'scope': 'scope1', 'settings': {'icon': 'atest1-dark'}},
            },
            {
                'name': 'ATest-2',
                'preferences': {
                    'scope': 'scope2',
                    'settings': {'icon': 'atest2-light'},
                },
            },
        ]

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.preferences.sublime.error_message'
    )
    def test_ignored_icon_setting(self, mock_error):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.preferences.get_ignored_icon_settings',
            return_value=self.mock_icon_settings,
        ):
            result = self.preferences.ignored_icon_setting()
            self.assertEqual(result, self.mock_icon_settings)

    def test_delete_icon_preference(self):
        self.preferences.delete_icons_preference = Mock()

        self.preferences.delete_icon_preference('atest.tmPreferences')

        self.preferences.delete_icons_preference.assert_called_once_with(
            'atest.tmPreferences'
        )

    def test_delete_all_icons_preferences(self):
        self.preferences.delete_icons_preferences = Mock()

        self.preferences.delete_all_icons_preferences()

        self.preferences.delete_icons_preferences.assert_called_once()

    def test_get_installed_preferences(self):
        mock_list = [
            'atest2.tmPreferences',
            'atest1.tmPreferences',
            'atest3.tmPreferences',
        ]
        self.preferences.list_created_icons_preferences = Mock(return_value=mock_list)

        result = self.preferences.get_installed_preferences()

        self.assertEqual(result, sorted(mock_list))

    def test_get_not_installed_preferences(self):
        self.preferences.get_list_icons_preferences = Mock(
            return_value=self.mock_preferences_list
        )
        self.preferences.list_created_icons_preferences = Mock(
            return_value=['atest1.tmPreferences']
        )

        expected = ['atest2.tmPreferences']
        result = self.preferences.get_not_installed_preferences()

        self.assertEqual(result, expected)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.preferences.sublime.error_message'
    )
    def test_install_icon_preference_icon_ignored(self, mock_error):
        self.preferences.get_list_icons_preferences = Mock(
            return_value=self.mock_preferences_list
        )
        self.preferences.ignored_icon_setting = Mock(return_value=['ATest-1'])

        self.preferences.install_icon_preference('atest1.tmPreferences')

        mock_error.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.preferences.sublime.error_message'
    )
    def test_install_icon_preference(self, mock_error):
        self.preferences.get_list_icons_preferences = Mock(
            return_value=self.mock_preferences_list
        )
        self.preferences.ignored_icon_setting = Mock(return_value=[])
        self.preferences.build_icon_preference = Mock()

        self.preferences.install_icon_preference('atest1.tmPreferences')

        self.preferences.build_icon_preference.assert_called_once()
        mock_error.assert_not_called()

    def test_install_all_icons_preferences(self):
        self.preferences.build_icons_preferences = Mock()
        self.preferences.install_all_icons_preferences()
        self.preferences.build_icons_preferences.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.preferences.sublime.ok_cancel_dialog'
    )
    def test_confirm_delete(self, mock_dialog):
        mock_dialog.return_value = True

        result = self.preferences.confirm_delete('Test message')

        self.assertTrue(result)
        mock_dialog.assert_called_once_with('Test message')


class TestDeletePreferenceCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = preferences.DeletePreferenceCommand(self.view)
        self.command.preferences = Mock()
        self.command.preferences.preferences_path = 'test/path'

    def test_delete_preference_command_is_enabled(self):
        self.command.preferences.get_installed_preferences.return_value = [
            'atest1.tmPreferences'
        ]
        self.assertTrue(self.command.is_enabled())

    def test_delete_preference_command_is_enabled_none(self):
        self.command.preferences.get_installed_preferences.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_delete_preference_command_run_all(self):
        self.command.preferences.confirm_delete.return_value = True

        self.command.run(None, preference_name='All')

        self.command.preferences.delete_all_icons_preferences.assert_called_once()

    def test_delete_preference_command_run(self):
        self.command.preferences.confirm_delete.return_value = True

        self.command.run(None, preference_name='atest.tmPreferences')

        self.command.preferences.delete_icon_preference.assert_called_once_with(
            'atest.tmPreferences'
        )

    def test_delete_preference_command_input(self):
        input_handler = self.command.input({})
        self.assertIsInstance(input_handler, preferences.DeletePreferenceInputHandler)


class TestDeletePreferenceInputHandler(TestCase):
    def setUp(self):
        self.preferences = Mock()
        self.handler = preferences.DeletePreferenceInputHandler(self.preferences)

    def test_delete_preference_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'preference_name')

    def test_delete_preference_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of created preferences')

    def test_delete_preference_input_handler_list_items(self):
        self.preferences.get_installed_preferences.return_value = [
            'atest1.tmPreferences',
            'atest2.tmPreferences',
        ]
        expected = ['All', 'atest1.tmPreferences', 'atest2.tmPreferences']
        self.assertEqual(self.handler.list_items(), expected)

    def test_delete_preference_input_handler_list_items_none(self):
        self.preferences.get_installed_preferences.return_value = []
        with self.assertRaises(TypeError):
            self.handler.list_items()


class TestInstallPreferenceCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = preferences.InstallPreferenceCommand(self.view)
        self.command.preferences = Mock()

    def test_install_preference_command_is_enabled(self):
        self.command.preferences.get_not_installed_preferences.return_value = [
            'atest1.tmPreferences'
        ]
        self.assertTrue(self.command.is_enabled())

    def test_install_preference_command_is_enabled_none(self):
        self.command.preferences.get_not_installed_preferences.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_install_preference_command_run_all(self):
        self.command.run(None, preference_name='All')
        self.command.preferences.install_all_icons_preferences.assert_called_once()

    def test_install_preference_command_run(self):
        self.command.run(None, preference_name='atest.tmPreferences')
        self.command.preferences.install_icon_preference.assert_called_once_with(
            'atest.tmPreferences'
        )

    def test_install_preference_command_input(self):
        input_handler = self.command.input({})
        self.assertIsInstance(input_handler, preferences.InstallPreferenceInputHandler)


class TestInstallPreferenceInputHandler(TestCase):
    def setUp(self):
        self.preferences = Mock()
        self.handler = preferences.InstallPreferenceInputHandler(self.preferences)

    def test_install_preference_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'preference_name')

    def test_install_preference_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'Zukan preferences list')

    def test_install_preference_input_handler_list_items(self):
        self.preferences.get_not_installed_preferences.return_value = [
            'atest1.tmPreferences',
            'atest2.tmPreferences',
        ]
        self.assertEqual(
            self.handler.list_items(),
            ['All', 'atest1.tmPreferences', 'atest2.tmPreferences'],
        )

    def test_install_preference_input_handler_list_items_none(self):
        self.preferences.get_not_installed_preferences.return_value = []
        with self.assertRaises(TypeError):
            self.handler.list_items()
