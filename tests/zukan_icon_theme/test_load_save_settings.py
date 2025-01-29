import importlib
import sublime

from unittest import TestCase
from unittest.mock import patch, MagicMock

load_save_settings = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings'
)
file_settings = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.file_settings'
)


class TestGetSettings(TestCase):
    def test_load_settings(self):
        x = load_save_settings.get_settings(file_settings.USER_SETTINGS, None)
        y = sublime.load_settings(file_settings.USER_SETTINGS)
        self.assertTrue(x, y)

    def test_load_settings_not_equal(self):
        x = load_save_settings.get_settings(file_settings.USER_SETTINGS, None)
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS)
        self.assertNotEqual(x, y)

    def test_load_settings_options(self):
        x = load_save_settings.get_settings(file_settings.ZUKAN_SETTINGS, 'version')
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS).get('version')
        self.assertEqual(x, y)

    def test_load_settings_options_not_equal(self):
        x = load_save_settings.get_settings(file_settings.ZUKAN_SETTINGS, 'log_level')
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS).get('version')
        self.assertNotEqual(x, y)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.sublime.load_settings'
    )
    def test_get_settings_with_option_none(self, mock_load_settings):
        mock_settings = {'setting1': 'value1', 'setting2': 'value2'}
        mock_load_settings.return_value = mock_settings

        result = load_save_settings.get_settings('file.sublime-settings', None)
        self.assertEqual(result, mock_settings)
        mock_load_settings.assert_called_once_with('file.sublime-settings')

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.sublime.load_settings'
    )
    def test_get_settings_with_option(self, mock_load_settings):
        mock_settings = {'setting1': 'value1', 'setting2': 'value2'}
        mock_load_settings.return_value = mock_settings

        result = load_save_settings.get_settings('file.sublime-settings', 'setting1')
        self.assertEqual(result, 'value1')
        mock_load_settings.assert_called_once_with('file.sublime-settings')


class TestSetSaveSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.sublime.load_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.sublime.save_settings'
    )
    def test_set_save_settings(self, mock_save_settings, mock_load_settings):
        mock_settings = MagicMock()
        mock_load_settings.return_value = mock_settings

        file_settings = 'Zukan Icon Theme.sublime-settings'
        option = 'zukan_restart_message'
        option_value = [True]

        load_save_settings.set_save_settings(file_settings, option, option_value)

        mock_load_settings.assert_called_once_with(file_settings)
        mock_settings.set.assert_called_once_with(option, option_value)
        mock_save_settings.assert_called_once_with(file_settings)


class TestValidDictList(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.logger.warning'
    )
    def test_is_valid_dict_true(self, mock_warning):
        setting_option = {'key': 'value'}

        result = load_save_settings.is_valid_dict(setting_option)

        self.assertTrue(result)
        mock_warning.assert_not_called()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.logger.warning'
    )
    def test_is_valid_dict_false(self, mock_warning):
        setting_option = ['key', 'value']

        result = load_save_settings.is_valid_dict(setting_option)

        self.assertFalse(result)
        mock_warning.assert_called_once_with('%s option malformed, needs to be a dict')

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.logger.warning'
    )
    def test_is_valid_list_true(self, mock_warning):
        setting_option = [1, 2, 3]

        result = load_save_settings.is_valid_list(setting_option)

        self.assertTrue(result)
        mock_warning.assert_not_called()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.logger.warning'
    )
    def test_is_valid_list_false(self, mock_warning):
        setting_option = {'key': 'value'}

        result = load_save_settings.is_valid_list(setting_option)

        self.assertFalse(result)
        mock_warning.assert_called_once_with('%s option malformed, needs to be a list')


class TestGetThemeName(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.system_theme'
    )
    def test_get_theme_name_auto_dark(self, mock_system_theme, mock_get_settings):
        mock_get_settings.side_effect = lambda user_settings, key: {
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'auto',
        }.get(key, None)

        mock_system_theme.return_value = True

        result = load_save_settings.get_theme_name()

        self.assertEqual(result, 'Treble Dark.sublime-theme')

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.system_theme'
    )
    def test_get_theme_name_auto_light(self, mock_system_theme, mock_get_settings):
        mock_get_settings.side_effect = lambda user_settings, key: {
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'auto',
        }.get(key, None)

        mock_system_theme.return_value = False

        result = load_save_settings.get_theme_name()

        self.assertEqual(result, 'Treble Light.sublime-theme')

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.system_theme'
    )
    def test_get_theme_name(self, mock_system_theme, mock_get_settings):
        mock_get_settings.side_effect = lambda user_settings, key: {
            'dark_theme': 'Treble Dark.sublime-theme',
            'light_theme': 'Treble Light.sublime-theme',
            'theme': 'Treble Adaptive.sublime-theme',
        }.get(key, None)

        result = load_save_settings.get_theme_name()

        self.assertEqual(result, 'Treble Adaptive.sublime-theme')


class TestGetThemeSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_theme_settings_with_valid_ignored_theme(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.return_value = 'some_theme'
        mock_get_settings.side_effect = (
            lambda file, option: ['theme1', 'theme2']
            if option == 'ignored_theme'
            else 'some_theme'
        )
        mock_is_valid_list.return_value = True

        result = load_save_settings.get_theme_settings()
        self.assertEqual(result, (['theme1', 'theme2'], 'some_theme'))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_theme_settings_with_invalid_ignored_theme(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: ['theme1', 'theme2']
            if option == 'ignored_theme'
            else 'some_theme'
        )
        mock_is_valid_list.return_value = False

        result = load_save_settings.get_theme_settings()
        self.assertEqual(result, ([], 'some_theme'))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_theme_settings_with_empty_ignored_theme(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: [] if option == 'ignored_theme' else 'some_theme'
        )
        mock_is_valid_list.return_value = False

        result = load_save_settings.get_theme_settings()
        self.assertEqual(result, ([], 'some_theme'))


class TestGetCreateCustomIconSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_create_custom_icon_settings_with_valid_list(
        self, mock_is_valid_list, mock_get_settings
    ):
        # mock_get_settings.return_value = ['icon1', 'icon2']
        mock_get_settings.return_value = [
            {
                'icon': 'atest',
                'name': 'ATest',
                'scope': 'source.toml.atest, source.json.atest',
            },
            {'icon': 'atest1', 'name': 'ATest1', 'scope': 'source.atest1'},
        ]
        mock_is_valid_list.return_value = True

        result = load_save_settings.get_create_custom_icon_settings()
        self.assertEqual(
            result,
            [
                {
                    'icon': 'atest',
                    'name': 'ATest',
                    'scope': 'source.toml.atest, source.json.atest',
                },
                {'icon': 'atest1', 'name': 'ATest1', 'scope': 'source.atest1'},
            ],
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_create_custom_icon_settings_with_invalid_list(
        self, mock_is_valid_list, mock_get_settings
    ):
        # mock_get_settings.return_value = ['icon1', 'icon2']
        mock_get_settings.return_value = [
            {
                'icon': 'atest',
                'name': 'ATest',
                'scope': 'source.toml.atest, source.json.atest',
            },
            {'icon': 'atest1', 'name': 'ATest1', 'scope': 'source.atest1'},
        ]
        mock_is_valid_list.return_value = False

        result = load_save_settings.get_create_custom_icon_settings()
        self.assertEqual(result, [])

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_create_custom_icon_settings_with_empty_list(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.return_value = []
        mock_is_valid_list.return_value = False

        result = load_save_settings.get_create_custom_icon_settings()
        self.assertEqual(result, [])

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_get_create_custom_icon_settings_with_none(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.return_value = None
        mock_is_valid_list.return_value = False

        result = load_save_settings.get_create_custom_icon_settings()
        self.assertEqual(result, [])


class TestGetChangeIconSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_dict'
    )
    def test_get_change_icon_settings_with_valid_dict(
        self, mock_is_valid_dict, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: {'Icon 1': 'icon1', 'Icon 2': 'icon2'}
            if option == 'change_icon'
            else 'png'
        )
        mock_is_valid_dict.return_value = True

        result = load_save_settings.get_change_icon_settings()
        self.assertEqual(result, ({'Icon 1': 'icon1', 'Icon 2': 'icon2'}, 'png'))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_dict'
    )
    def test_get_change_icon_settings_with_invalid_dict(
        self, mock_is_valid_dict, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: {'Icon 1': 'icon1', 'Icon 2': 'icon2'}
            if option == 'change_icon'
            else 'png'
        )
        mock_is_valid_dict.return_value = False

        result = load_save_settings.get_change_icon_settings()
        self.assertEqual(result, ({}, 'png'))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_dict'
    )
    def test_get_change_icon_settings_with_empty_dict(
        self, mock_is_valid_dict, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: {} if option == 'change_icon' else 'svg'
        )
        mock_is_valid_dict.return_value = False

        result = load_save_settings.get_change_icon_settings()
        self.assertEqual(result, ({}, 'svg'))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_dict'
    )
    def test_get_change_icon_settings_with_none(
        self, mock_is_valid_dict, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda file, option: None if option == 'change_icon' else 'svg'
        )
        mock_is_valid_dict.return_value = False

        result = load_save_settings.get_change_icon_settings()
        self.assertEqual(result, ({}, 'svg'))
