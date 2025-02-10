import importlib

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

disable_theme = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme'
)


class TestDisableEnableTheme(TestCase):
    def setUp(self):
        self.theme = disable_theme.DisableEnableTheme()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.is_zukan_listener_enabled'
    )
    def test_disable_enable_theme_init(self, mock_listener):
        mock_listener.return_value = True
        theme = disable_theme.DisableEnableTheme()
        self.assertTrue(theme.zukan_listener_enabled)
        mock_listener.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.get_theme_settings'
    )
    def test_ignored_theme_setting(self, mock_get_settings):
        mock_get_settings.return_value = (['theme1', 'theme2'], 'other_setting')
        result = self.theme.ignored_theme_setting()
        self.assertEqual(result, ['theme1', 'theme2'])
        mock_get_settings.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    def test_add_to_ignored_themes(self, mock_save):
        ignored_list = ['theme1']
        self.theme.add_to_ignored_themes('theme2', ignored_list)
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS, 'ignored_theme', ['theme1', 'theme2']
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.search_resources_sublime_themes'
    )
    def test_get_list_ignored_theme(self, mock_search):
        mock_search.return_value = [
            'folder/Treble Adaptive.sublime-theme',
            'folder/Treble Dark.sublime-theme',
        ]
        ignored_list = ['Treble Dark.sublime-theme']
        result = self.theme.get_list_ignored_theme(ignored_list)
        self.assertEqual(result, ['folder/Treble Adaptive.sublime-theme'])
        mock_search.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.logger')
    def test_enable_icon_theme(self, mock_logger, mock_save):
        self.theme.zukan_listener_enabled = True
        ignored_list = ['theme1', 'theme2']
        self.theme.enable_icon_theme('theme1', ignored_list)
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS, 'ignored_theme', ['theme2']
        )
        mock_logger.info.assert_called_once_with('enabling %s', 'theme1')

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.logger')
    def test_enable_icon_theme_listener_disabled(self, mock_logger, mock_save):
        self.theme.zukan_listener_enabled = False
        ignored_list = ['theme1', 'theme2']
        self.theme.enable_icon_theme('theme1', ignored_list)
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS, 'ignored_theme', ['theme2']
        )
        mock_logger.info.assert_not_called()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.logger')
    def test_enable_all_icons_themes(self, mock_logger, mock_save):
        self.theme.zukan_listener_enabled = True
        ignored_list = ['theme1', 'theme2']

        self.theme.enable_all_icons_themes(ignored_list)

        mock_logger.info.assert_called_once_with('enabling all themes')
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS, 'ignored_theme', []
        )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    def test_save_ignored_theme_setting(self, mock_save):
        ignored_list = ['theme2', 'theme1', 'theme3']
        self.theme._save_ignored_theme_setting(ignored_list)
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS,
            'ignored_theme',
            ['theme1', 'theme2', 'theme3'],
        )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.set_save_settings')
    def test_save_ignored_theme_setting_empty_list(self, mock_save):
        self.theme._save_ignored_theme_setting([])
        mock_save.assert_called_once_with(
            disable_theme.ZUKAN_SETTINGS, 'ignored_theme', []
        )


class TestDisableThemeCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = disable_theme.DisableThemeCommand(self.view)

    def test_disable_theme_command_init(self):
        self.assertIsInstance(
            self.command.disable_enable_theme, disable_theme.DisableEnableTheme
        )
        self.assertEqual(self.command.view, self.view)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.logger')
    @patch('os.path.basename')
    def test_disable_theme_command_run(self, mock_basename, mock_logger):
        mock_basename.return_value = 'Treble Dark.sublime-theme'
        mock_ignored_theme = ['Treble Light.sublime-theme']
        self.command.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=mock_ignored_theme
        )
        self.command.disable_enable_theme.add_to_ignored_themes = Mock()

        self.command.run(Mock(), 'folder/Treble Dark.sublime-theme')

        mock_basename.assert_called_once_with('folder/Treble Dark.sublime-theme')
        self.command.disable_enable_theme.add_to_ignored_themes.assert_called_once_with(
            'Treble Dark.sublime-theme', mock_ignored_theme
        )
        mock_logger.info.assert_called_once_with(
            '%s ignored', 'Treble Dark.sublime-theme'
        )

    @patch('os.path.basename')
    def test_disable_theme_command_run_ignored(self, mock_basename):
        mock_basename.return_value = 'Treble Dark.sublime-theme'
        mock_ignored_theme = ['Treble Dark.sublime-theme']
        self.command.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=mock_ignored_theme
        )
        self.command.disable_enable_theme.add_to_ignored_themes = Mock()

        self.command.run(Mock(), 'folder/Treble Dark.sublime-theme')

        self.command.disable_enable_theme.add_to_ignored_themes.assert_not_called()

    def test_disable_theme_command_is_enabled(self):
        self.command.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=['theme1']
        )
        self.command.disable_enable_theme.get_list_ignored_theme = Mock(
            return_value=['theme2', 'theme3']
        )

        self.assertTrue(self.command.is_enabled())

    def test_disable_theme_command_is_enabled_none(self):
        self.command.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=['theme1']
        )
        self.command.disable_enable_theme.get_list_ignored_theme = Mock(return_value=[])

        self.assertFalse(self.command.is_enabled())

    def test_disable_theme_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, disable_theme.DisableThemeInputHandler)
        self.assertEqual(result.disable_enable_theme, self.command.disable_enable_theme)


class TestDisableThemeInputHandler(TestCase):
    def setUp(self):
        self.disable_enable_theme = Mock()
        self.handler = disable_theme.DisableThemeInputHandler(self.disable_enable_theme)

    def test_disable_theme_input_handler_init(self):
        self.assertEqual(self.handler.disable_enable_theme, self.disable_enable_theme)

    def test_disable_theme_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'theme_st_path')

    def test_disable_theme_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of installed themes')

    def test_disable_theme_input_handler_list_items(self):
        mock_ignored = ['theme1']
        mock_list = ['theme2', 'theme3']
        self.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=mock_ignored
        )
        self.disable_enable_theme.get_list_ignored_theme = Mock(return_value=mock_list)

        result = self.handler.list_items()
        self.assertEqual(result, ['theme2', 'theme3'])

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.disable_theme.logger')
    def test_disable_theme_input_handler_list_items_none(self, mock_logger):
        mock_ignored = ['theme1']
        self.disable_enable_theme.ignored_theme_setting = Mock(
            return_value=mock_ignored
        )
        self.disable_enable_theme.get_list_ignored_theme = Mock(return_value=[])

        with self.assertRaises(TypeError):
            self.handler.list_items()
        mock_logger.info.assert_called_once_with(
            'all themes are already disabled, list is empty.'
        )


class TestEnableThemeCommand(TestCase):
    def setUp(self):
        self.view = MagicMock()
        self.command = disable_theme.EnableThemeCommand(self.view)

        self.mock_disable_enable_theme = MagicMock()
        self.command.disable_enable_theme = self.mock_disable_enable_theme

    def test_enable_theme_command_run(self):
        ignored_themes = ['theme1', 'theme2', 'theme3']
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = (
            ignored_themes
        )

        self.command.run(MagicMock(), theme_name='theme1')

        self.mock_disable_enable_theme.enable_icon_theme.assert_called_once_with(
            'theme1', ignored_themes
        )
        self.mock_disable_enable_theme.enable_all_icons_themes.assert_not_called()

    def test_enable_theme_command_run_all(self):
        ignored_themes = ['theme1', 'theme2', 'theme3']
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = (
            ignored_themes
        )

        self.command.run(MagicMock(), theme_name='All')

        self.mock_disable_enable_theme.enable_all_icons_themes.assert_called_once_with(
            ignored_themes
        )
        self.mock_disable_enable_theme.enable_icon_theme.assert_not_called()

    def test_enable_theme_command_is_enabled(self):
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = [
            'theme1',
            'theme2',
        ]

        self.assertTrue(self.command.is_enabled())

    def test_enable_theme_command_is_enabled_empty(self):
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = []

        self.assertFalse(self.command.is_enabled())

    def test_enable_theme_command_is_enabled_none(self):
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = None

        self.assertFalse(self.command.is_enabled())

    def test_enable_theme_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, disable_theme.EnableThemeInputHandler)


class TestEnableThemeInputHandler(TestCase):
    def setUp(self):
        self.mock_disable_enable_theme = MagicMock()
        self.input_handler = disable_theme.EnableThemeInputHandler(
            self.mock_disable_enable_theme
        )

    def test_enable_theme_input_handler_name(self):
        self.assertEqual(self.input_handler.name(), 'theme_name')

    def test_enable_theme_input_handler_placeholder(self):
        self.assertEqual(self.input_handler.placeholder(), 'List of ignored themes')

    def test_enable_theme_input_handler_list_items(self):
        ignored_themes = ['theme2', 'theme1', 'theme3']
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = (
            ignored_themes
        )

        result = self.input_handler.list_items()

        expected = ['All', 'theme1', 'theme2', 'theme3']
        self.assertEqual(result, expected)

    def test_enable_theme_input_handler_list_items_none(self):
        self.mock_disable_enable_theme.ignored_theme_setting.return_value = None

        with self.assertRaises(TypeError):
            self.input_handler.list_items()
