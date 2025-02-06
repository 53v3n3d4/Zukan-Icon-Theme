import importlib
import os

from unittest import TestCase
from unittest.mock import Mock, patch

themes = importlib.import_module('Zukan Icon Theme.src.zukan_icon_theme.core.themes')


class TestThemes(TestCase):
    def setUp(self):
        self.zukan_pkg_icons_path = '/folder_path/icons'
        self.themes = themes.Themes(self.zukan_pkg_icons_path)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.themes.get_theme_settings')
    def test_ignored_theme_setting(self, mock_get_settings):
        expected_ignored_themes = [
            'Treble Dark.sublime-theme',
            'Treble Light.sublime-theme',
        ]
        mock_get_settings.return_value = (expected_ignored_themes, False)

        result = self.themes.ignored_theme_setting()

        self.assertEqual(result, expected_ignored_themes)
        mock_get_settings.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.themes.is_zukan_restart_message')
    def test_zukan_restart_message_setting(self, mock_restart_message):
        mock_restart_message.return_value = True

        result = self.themes.zukan_restart_message_setting()

        self.assertTrue(result)
        mock_restart_message.assert_called_once()

    def test_delete_single_icon_theme(self):
        self.themes.delete_icon_theme = Mock()
        theme_name = 'Treble Dark.sublime-theme'

        self.themes.delete_single_icon_theme(theme_name)

        self.themes.delete_icon_theme.assert_called_once_with(theme_name)

    def test_delete_all_icons_themes(self):
        self.themes.delete_icons_themes = Mock()

        self.themes.delete_all_icons_themes()

        self.themes.delete_icons_themes.assert_called_once()

    def test_get_installed_themes(self):
        mock_themes = [
            'Treble Light.sublime-theme',
            'Treble Dark.sublime-theme',
            'Treble Adaptive.sublime-theme',
        ]
        self.themes.list_created_icons_themes = Mock(return_value=mock_themes)

        result = self.themes.get_installed_themes()

        self.assertEqual(result, sorted(mock_themes))
        self.themes.list_created_icons_themes.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.themes.search_resources_sublime_themes'
    )
    def test_get_not_installed_themes(self, mock_search_themes):
        mock_search_themes.return_value = [
            'path/Treble Dark.sublime-theme',
            'path/Treble Light.sublime-theme',
            'path/Treble Adaptive.sublime-theme',
        ]
        self.themes.list_created_icons_themes = Mock(
            return_value=['Treble Dark.sublime-theme', 'Treble Adaptive.sublime-theme']
        )

        result = self.themes.get_not_installed_themes()

        self.assertEqual(result, ['path/Treble Light.sublime-theme'])
        mock_search_themes.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.themes.sublime.error_message')
    def test_install_icon_theme_ignored(self, mock_error_message):
        theme_path = 'path/Treble Dark.sublime-theme'
        self.themes.ignored_theme_setting = Mock(
            return_value=['Treble Dark.sublime-theme']
        )

        self.themes.install_icon_theme(theme_path)

        mock_error_message.assert_called_once_with(
            'Treble Dark.sublime-theme is disabled. Need to enable first.'
        )

    def test_install_icon_theme(self):
        theme_path = 'path/normal_theme'
        self.themes.ignored_theme_setting = Mock(return_value=[])
        self.themes.create_icon_theme = Mock()

        self.themes.install_icon_theme(theme_path)

        self.themes.create_icon_theme.assert_called_once_with(theme_path)

    def test_install_all_icons_themes(self):
        self.themes.create_icons_themes = Mock()

        self.themes.install_all_icons_themes()

        self.themes.create_icons_themes.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.themes.sublime.ok_cancel_dialog')
    def test_confirm_delete(self, mock_dialog):
        message = 'Delete confirmation message'
        mock_dialog.return_value = True

        result = self.themes.confirm_delete(message)

        self.assertTrue(result)
        mock_dialog.assert_called_once_with(message)


class TestDeleteThemeCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = themes.DeleteThemeCommand(self.view)
        self.command.themes = Mock()
        self.command.themes.zukan_pkg_icons_path = themes.ZUKAN_PKG_ICONS_PATH

    def test_delete_theme_command_init(self):
        command = themes.DeleteThemeCommand(self.view)

        self.assertEqual(command.view, self.view)
        self.assertIsNotNone(command.themes)

    def test_delete_theme_command_run_all_with_restart_message(self):
        self.command.themes.zukan_restart_message_setting.return_value = True
        self.command.themes.confirm_delete.return_value = True
        expected_message = (
            'Are you sure you want to delete all themes in "{f}"?\n\n'
            'You may have to restart ST, for all icons do not show.'
        ).format(f=themes.ZUKAN_PKG_ICONS_PATH)

        self.command.run(Mock(), theme_name='All')

        self.command.themes.confirm_delete.assert_called_once_with(expected_message)
        self.command.themes.delete_all_icons_themes.assert_called_once()

    def test_delete_theme_command_run_all_without_restart_message(self):
        self.command.themes.zukan_restart_message_setting.return_value = False
        self.command.themes.confirm_delete.return_value = True
        expected_message = (
            'Are you sure you want to delete all themes in "{f}"?'
        ).format(f=themes.ZUKAN_PKG_ICONS_PATH)

        self.command.run(Mock(), theme_name='All')

        self.command.themes.confirm_delete.assert_called_once_with(expected_message)
        self.command.themes.delete_all_icons_themes.assert_called_once()

    def test_delete_theme_command_run_with_restart_message(self):
        theme_name = 'Treble Dark.sublime-theme'
        self.command.themes.zukan_restart_message_setting.return_value = True
        self.command.themes.confirm_delete.return_value = True
        expected_message = (
            'Are you sure you want to delete "{t}"?\n\n'
            'You may have to restart ST, for all icons do not show.'
        ).format(t=os.path.join(themes.ZUKAN_PKG_ICONS_PATH, theme_name))

        self.command.run(Mock(), theme_name=theme_name)

        self.command.themes.confirm_delete.assert_called_once_with(expected_message)
        self.command.themes.delete_single_icon_theme.assert_called_once_with(theme_name)

    def test_delete_theme_command_run_without_restart_message(self):
        theme_name = 'Treble Dark.sublime-theme'
        self.command.themes.zukan_restart_message_setting.return_value = False
        self.command.themes.confirm_delete.return_value = True
        expected_message = ('Are you sure you want to delete "{t}"?').format(
            t=os.path.join(themes.ZUKAN_PKG_ICONS_PATH, theme_name)
        )

        self.command.run(Mock(), theme_name=theme_name)

        self.command.themes.confirm_delete.assert_called_once_with(expected_message)
        self.command.themes.delete_single_icon_theme.assert_called_once_with(theme_name)

    def test_delete_theme_command_run_cancel(self):
        self.command.themes.zukan_restart_message_setting.return_value = False
        self.command.themes.confirm_delete.return_value = False

        self.command.run(Mock(), theme_name='Treble Dark.sublime-theme')

        self.command.themes.delete_single_icon_theme.assert_not_called()
        self.command.themes.delete_all_icons_themes.assert_not_called()

    def test_delete_theme_command_is_enabled(self):
        self.command.themes.get_installed_themes.return_value = [
            'Treble Dark.sublime-theme',
            'Treble Light.sublime-theme',
        ]

        result = self.command.is_enabled()

        self.assertTrue(result)

    def test_delete_theme_command_is_enabled_none(self):
        self.command.themes.get_installed_themes.return_value = []

        result = self.command.is_enabled()

        self.assertFalse(result)

    def test_delete_theme_command_input(self):
        result = self.command.input({})

        self.assertIsInstance(result, themes.DeleteThemeInputHandler)


class TestDeleteThemeInputHandler(TestCase):
    def setUp(self):
        self.themes = Mock()
        self.handler = themes.DeleteThemeInputHandler(self.themes)

    def test_delete_theme_input_handler_name(self):
        result = self.handler.name()

        self.assertEqual(result, 'theme_name')

    def test_delete_theme_input_handler_placeholder(self):
        result = self.handler.placeholder()

        self.assertEqual(result, 'List of created themes')

    def test_delete_theme_input_handler_list_items(self):
        installed_themes = ['Treble Dark.sublime-theme', 'Treble Light.sublime-theme']
        self.themes.get_installed_themes.return_value = installed_themes
        expected_list = ['All'] + installed_themes

        result = self.handler.list_items()

        self.assertEqual(result, expected_list)

    def test_delete_theme_input_handler_list_items_none(self):
        self.themes.get_installed_themes.return_value = []

        with self.assertRaises(TypeError):
            self.handler.list_items()


class TestInstallThemeCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = themes.InstallThemeCommand(self.view)
        self.command.themes = Mock()
        self.command.themes.zukan_pkg_icons_path = themes.ZUKAN_PKG_ICONS_PATH

    def test_install_theme_command_init(self):
        command = themes.InstallThemeCommand(self.view)

        self.assertEqual(command.view, self.view)
        self.assertIsNotNone(command.themes)

    @patch('sublime.message_dialog')
    def test_install_theme_command_run_all_with_restart_message(
        self, mock_message_dialog
    ):
        self.command.themes.zukan_restart_message_setting.return_value = True
        expected_message = (
            'You may have to restart ST, if all icons do not load in current theme.'
        )

        self.command.run(Mock(), theme_st_path='All')

        mock_message_dialog.assert_called_once_with(expected_message)
        self.command.themes.install_all_icons_themes.assert_called_once()

    def test_install_theme_command_run__all_without_restart_message(self):
        self.command.themes.zukan_restart_message_setting.return_value = False

        self.command.run(Mock(), theme_st_path='All')

        self.command.themes.install_all_icons_themes.assert_called_once()

    @patch('sublime.message_dialog')
    def test_install_theme_command_run_with_restart_message(self, mock_message_dialog):
        theme_path = 'path/Treble Dark.sublime-theme'
        self.command.themes.zukan_restart_message_setting.return_value = True
        self.command.themes.ignored_theme_setting.return_value = []
        expected_message = (
            'You may have to restart ST, if all icons do not load in current theme.'
        )

        self.command.run(Mock(), theme_st_path=theme_path)

        mock_message_dialog.assert_called_once_with(expected_message)
        self.command.themes.install_icon_theme.assert_called_once_with(theme_path)

    @patch('sublime.message_dialog')
    def test_install_theme_command_run_with_restart_message_ignored(
        self, mock_message_dialog
    ):
        theme_path = 'path/Treble Dark.sublime-theme'
        self.command.themes.zukan_restart_message_setting.return_value = True
        self.command.themes.ignored_theme_setting.return_value = [
            'Treble Dark.sublime-theme'
        ]

        self.command.run(Mock(), theme_st_path=theme_path)

        mock_message_dialog.assert_not_called()
        self.command.themes.install_icon_theme.assert_called_once_with(theme_path)

    def test_install_theme_command_run_without_restart_message(self):
        theme_path = 'path/Treble Dark.sublime-theme'
        self.command.themes.zukan_restart_message_setting.return_value = False

        self.command.run(Mock(), theme_st_path=theme_path)

        self.command.themes.install_icon_theme.assert_called_once_with(theme_path)

    def test_install_theme_command_is_enabled(self):
        self.command.themes.get_not_installed_themes.return_value = [
            'Treble Dark.sublime-theme',
            'Treble Light.sublime-theme',
        ]

        result = self.command.is_enabled()

        self.assertTrue(result)

    def test_install_theme_command_is_enabled_none(self):
        self.command.themes.get_not_installed_themes.return_value = []

        result = self.command.is_enabled()

        self.assertFalse(result)

    def test_install_theme_command_input(self):
        result = self.command.input({})

        self.assertIsInstance(result, themes.InstallThemeInputHandler)


class TestInstallThemeInputHandler(TestCase):
    def setUp(self):
        self.themes = Mock()
        self.handler = themes.InstallThemeInputHandler(self.themes)

    def test_install_theme_input_handler_name(self):
        result = self.handler.name()

        self.assertEqual(result, 'theme_st_path')

    def test_install_theme_input_handler_placeholder(self):
        result = self.handler.placeholder()

        self.assertEqual(result, 'List of installed themes')

    def test_install_theme_input_handler_list_items(self):
        not_installed_themes = [
            'Packages/Package Name/Treble Dark.sublime-theme',
            'Packages/Package Name/Treble Light.sublime-theme',
        ]
        self.themes.get_not_installed_themes.return_value = not_installed_themes
        expected_list = ['All'] + sorted(not_installed_themes)

        result = self.handler.list_items()

        self.assertEqual(result, expected_list)

    def test_install_theme_input_handler_list_items_none(self):
        self.themes.get_not_installed_themes.return_value = []

        with self.assertRaises(TypeError):
            self.handler.list_items()

    def test_install_theme_input_handler_list_items_sorted(self):
        unsorted_themes = [
            'Packages/Package Name/Treble Light.sublime-theme',
            'Packages/Package Name/Treble Adaptive.sublime-theme',
            'Packages/Package Name/Treble Dark.sublime-theme',
        ]
        self.themes.get_not_installed_themes.return_value = unsorted_themes
        expected_list = [
            'All',
            'Packages/Package Name/Treble Adaptive.sublime-theme',
            'Packages/Package Name/Treble Dark.sublime-theme',
            'Packages/Package Name/Treble Light.sublime-theme',
        ]

        result = self.handler.list_items()

        self.assertEqual(result, expected_list)
