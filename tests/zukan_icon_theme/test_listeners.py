import importlib

from unittest import TestCase
from unittest.mock import MagicMock, patch

listeners = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.listeners'
)


class TestSchemeTheme(TestCase):
    def setUp(self):
        patch_targets = [
            (listeners, 'ZukanPreference'),
            (listeners, 'ZukanSyntax'),
            (listeners, 'ZukanTheme'),
            (listeners, 'get_prefer_icon_settings'),
            (listeners, 'get_theme_settings'),
            (listeners, 'get_settings'),
            (listeners, 'read_pickle_data'),
            (listeners, 'is_zukan_restart_message'),
            (listeners, 'get_theme_name'),
            (listeners, 'package_theme_exists'),
            (listeners, 'sublime'),
        ]

        self.patches = [patch.object(module, attr) for module, attr in patch_targets]
        self.mocks = [patcher.start() for patcher in self.patches]

        (
            self.mock_zukan_preference,
            self.mock_zukan_syntax,
            self.mock_zukan_theme,
            self.mock_get_prefer_icon,
            self.mock_get_theme,
            self.mock_get_settings,
            self.mock_read_pickle,
            self.mock_restart_message,
            self.mock_theme_name,
            self.mock_package_theme,
            self.mock_sublime,
        ) = self.mocks

        self.mock_get_prefer_icon.return_value = (
            True,
            [{'Treble Dark.sublime-theme': 'light'}],
        )
        self.mock_get_theme.return_value = (['Ignored Theme.sublime-theme'], True)
        self.mock_get_settings.return_value = 'Nimbus.sublime-color-scheme'
        self.mock_read_pickle.return_value = []
        self.mock_restart_message.return_value = False
        self.mock_theme_name.return_value = 'test_theme'
        self.mock_package_theme.return_value = True

        self.scheme_theme = listeners.SchemeTheme()

    def tearDown(self):
        for patcher in self.patches:
            patcher.stop()

    def test_scheme_theme_init(self):
        self.assertEqual(self.scheme_theme.auto_prefer_icon, True)
        self.assertEqual(
            self.scheme_theme.prefer_icon, [{'Treble Dark.sublime-theme': 'light'}]
        )
        self.assertEqual(
            self.scheme_theme.ignored_theme, ['Ignored Theme.sublime-theme']
        )
        self.assertEqual(self.scheme_theme.auto_install_theme, True)
        self.assertEqual(
            self.scheme_theme.color_scheme_name, 'Nimbus.sublime-color-scheme'
        )
        self.assertEqual(self.scheme_theme.user_ui_settings, [])
        self.assertEqual(self.scheme_theme.zukan_restart_message, False)

    def test_theme_file(self):
        self.mock_theme_name.return_value = 'test_theme'

        result = self.scheme_theme.theme_file()

        self.assertTrue(result.endswith('test_theme'))

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_user_theme_delete_syntaxes(self, mock_listdir, mock_exists):
        mock_listdir.return_value = [
            f'test.{listeners.SUBLIME_SYNTAX_EXTENSION}',
            'test.toml',
        ]
        self.mock_theme_name.return_value = 'Ignored Theme.sublime-theme'

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_syntax.delete_icons_syntaxes.assert_called_once()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_user_theme_delete_preferences(self, mock_listdir, mock_exists):
        mock_listdir.return_value = [
            f'test.{listeners.TMPREFERENCES_EXTENSION}',
            'test.toml',
        ]
        self.mock_theme_name.return_value = 'Ignored Theme.sublime-theme'

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_preference.delete_icons_preferences.assert_called_once()

    @patch('os.path.exists')
    def test_get_user_theme_auto_install_create_icon_theme(self, mock_exists):
        mock_exists.return_value = False
        self.mock_theme_name.return_value = 'New Theme.sublime-theme'
        self.mock_sublime.find_resources.return_value = [
            'Packages/Theme - New Theme/New Theme.sublime-theme'
        ]

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_theme.create_icon_theme.assert_called_once_with(
            'Packages/Theme - New Theme/New Theme.sublime-theme'
        )

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_user_theme_build_syntaxes(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['test.other']
        self.scheme_theme.zukan_theme.list_created_icons_themes.return_value = [
            'test_theme'
        ]

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_syntax.build_icons_syntaxes.assert_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_user_theme_build_preferences(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = [
            f'test.{listeners.SUBLIME_SYNTAX_EXTENSION}',
            'test.other',
        ]
        self.scheme_theme.zukan_theme.list_created_icons_themes.return_value = [
            'test_theme'
        ]

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_preference.build_icons_preferences.assert_called()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_user_theme_delete_ignored_theme(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = []
        self.mock_theme_name.return_value = 'Ignored Theme.sublime-theme'

        self.mock_restart_message.return_value = True
        self.scheme_theme.zukan_restart_message = True

        self.scheme_theme.get_user_theme()

        self.scheme_theme.zukan_theme.delete_icon_theme.assert_called_once_with(
            'Ignored Theme.sublime-theme'
        )

        expected_message = 'You may have to restart ST, for all icons do not show.'
        self.mock_sublime.message_dialog.assert_called_once_with(expected_message)


class TestSchemeThemeListener(TestCase):
    def setUp(self):
        patch_targets = [
            (listeners.sublime_plugin, 'ViewEventListener'),
            (listeners, 'get_theme_settings'),
            (listeners, 'system_theme'),
            (listeners, 'save_current_ui_settings'),
            (listeners, 'get_sidebar_bgcolor'),
            (listeners, 'read_pickle_data'),
            (listeners, 'hex_dark_light'),
            (listeners, 'SchemeTheme'),
            (listeners, 'ZukanTheme'),
            (listeners, 'logger'),
        ]

        self.patches = [patch.object(module, attr) for module, attr in patch_targets]
        self.mocks = [patcher.start() for patcher in self.patches]

        (
            self.mock_view_listener,
            self.mock_get_theme,
            self.mock_system_theme,
            self.mock_save_ui,
            self.mock_sidebar_bgcolor,
            self.mock_read_pickle,
            self.mock_hex_dark_light,
            self.mock_scheme_theme,
            self.mock_zukan_theme,
            self.mock_logger,
        ) = self.mocks

        self.mock_get_theme.return_value = (['Ignored Theme.sublime-theme'], False)
        self.mock_system_theme.return_value = False
        self.mock_sidebar_bgcolor.return_value = '#FFFFFF'
        self.mock_read_pickle.return_value = []
        self.mock_hex_dark_light.return_value = 'light'

        self.mock_view = MagicMock()
        self.mock_view.style.return_value = {'background': '#FFFFFF'}
        self.mock_view.settings().get.side_effect = lambda x: {
            'color_scheme': 'D-O.sublime-color-scheme',
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'Treble Adaptive.sublime-theme',
        }.get(x)

        self.listener = listeners.SchemeThemeListener(self.mock_view)
        self.listener.view = self.mock_view

    def tearDown(self):
        for patcher in self.patches:
            patcher.stop()

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_scheme_theme_listener_on_activated_async_create_directory(
        self, mock_makedirs, mock_exists
    ):
        mock_exists.side_effect = lambda x: x != listeners.ZUKAN_PKG_SUBLIME_PATH

        self.listener.on_activated_async()

        mock_makedirs.assert_called_once_with(listeners.ZUKAN_PKG_SUBLIME_PATH)

    @patch('os.path.exists')
    def test_scheme_theme_listener_on_activated_async_save_initial_ui_settings(
        self, mock_exists
    ):
        mock_exists.side_effect = lambda x: x != listeners.USER_UI_SETTINGS_FILE

        self.listener.on_activated_async()

        self.mock_save_ui.assert_called_once()

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scheme_theme_listener_on_activated_async_theme_auto_light(
        self, mock_listdir, mock_exists
    ):
        mock_exists.return_value = True
        mock_listdir.return_value = []
        self.mock_view.settings().get.side_effect = lambda x: {
            'color_scheme': 'Fuji.sublime-color-scheme',
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'auto',
        }.get(x)
        self.mock_system_theme.return_value = False

        self.listener.on_activated_async()

        self.mock_sidebar_bgcolor.assert_called_with('Treble Light.sublime-theme')

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scheme_theme_listener_on_activated_async_theme_auto_dark(
        self, mock_listdir, mock_exists
    ):
        mock_exists.return_value = True
        mock_listdir.return_value = []
        self.mock_view.settings().get.side_effect = lambda x: {
            'color_scheme': 'Blackcomb.sublime-color-scheme',
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'auto',
        }.get(x)
        self.mock_system_theme.return_value = True

        self.listener.on_activated_async()

        self.mock_sidebar_bgcolor.assert_called_with('Treble Dark.sublime-theme')

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scheme_theme_listener_on_activated_async(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = []
        self.mock_zukan_theme().list_created_icons_themes.return_value = []

        self.listener.on_activated_async()

        self.mock_scheme_theme().get_user_theme.assert_called_once()
        self.mock_logger.debug.assert_called_once_with(
            'SchemeTheme ViewListener on_activated_async'
        )

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_scheme_theme_listener_on_activated_async_update_current_ui_settings(
        self, mock_listdir, mock_exists
    ):
        mock_exists.return_value = True
        mock_listdir.return_value = []

        self.listener.on_activated_async()

        self.mock_save_ui.assert_called_with(
            '#FFFFFF',  # color_scheme_background
            'D-O.sublime-color-scheme',  # current_color_scheme
            'Treble Dark.sublime-theme',  # current_dark_theme
            'Treble Light.sublime-theme',  # current_light_theme
            False,  # current_system_theme
            'Treble Adaptive.sublime-theme',  # current_theme
            '#FFFFFF',  # sidebar_bgcolor
        )
