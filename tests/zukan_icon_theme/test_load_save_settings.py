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


class TestGetPreferIconSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_dict'
    )
    def test_prefer_icon_empty_dict_invalid(
        self, mock_is_valid_dict, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda settings, key: None
            if key == 'prefer_icon'
            else {'auto_prefer_icon': True}
        )
        mock_is_valid_dict.return_value = False

        auto_prefer_icon, prefer_icon = load_save_settings.get_prefer_icon_settings()

        self.assertEqual(prefer_icon, {})


class TestGetIgnoredIconSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.is_valid_list'
    )
    def test_ignored_icon_empty_list_invalid(
        self, mock_is_valid_list, mock_get_settings
    ):
        mock_get_settings.side_effect = (
            lambda settings, key: None if key == 'ignored_icon' else []
        )
        mock_is_valid_list.return_value = False

        ignored_icon = load_save_settings.get_ignored_icon_settings()

        self.assertEqual(ignored_icon, [])


class TestReadCurrentSettings(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.os.path.exists'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.default_settings'
    )
    def test_read_current_settings_using_default_settings_1(
        self, mock_default_settings, mock_get_settings, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_settings.side_effect = lambda settings, key: {
            'auto_install_theme': True,
            'log_level': 'DEBUG',
            'rebuild_on_upgrade': False,
            'ignored_icon': ['icon1', 'icon2'],
            'prefer_icon': {'key': 'value'},
            'auto_prefer_icon': True,
        }.get(key, None)
        mock_default_settings.return_value = {
            'version': '0.4.8',
            'zukan_listener_enabled': True,
        }

        result = load_save_settings.read_current_settings()

        expected_result = {
            'version': '0.4.8',
            'auto_install_theme': True,
            'log_level': 'DEBUG',
            'rebuild_on_upgrade': False,
            'ignored_icon': ['icon1', 'icon2'],
            'prefer_icon': {'key': 'value'},
            'auto_prefer_icon': True,
            'zukan_listener_enabled': True,
        }

        self.assertEqual(result, expected_result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.os.path.exists'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.default_settings'
    )
    def test_read_current_settings_using_default_settings_2(
        self, mock_default_settings, mock_get_settings, mock_exists
    ):
        mock_exists.return_value = True

        mock_get_settings.side_effect = lambda settings, key: {
            'auto_install_theme': True,
            'log_level': 'DEBUG',
            'rebuild_on_upgrade': None,
            'ignored_icon': None,
            'prefer_icon': {'key': 'value'},
            'auto_prefer_icon': True,
        }.get(key, None)
        mock_default_settings.return_value = {
            'version': '0.4.8',
            'zukan_listener_enabled': True,
        }

        result = load_save_settings.read_current_settings()

        expected_result = {
            'version': '0.4.8',
            'auto_install_theme': True,
            'log_level': 'DEBUG',
            'prefer_icon': {'key': 'value'},
            'auto_prefer_icon': True,
            'zukan_listener_enabled': True,
        }

        self.assertEqual(result, expected_result)


class TestRemoveJsonComments(TestCase):
    def test_removejson_comments_no_comments(self):
        json_data = """
        {
            "key": "value",
            "another_key": "another_value"
        }
        """
        expected = """
        {
            "key": "value",
            "another_key": "another_value"
        }
        """
        result = load_save_settings.remove_json_comments(json_data)
        self.assertEqual(result.strip(), expected.strip())

    def test_removejson_comments_empty_json(self):
        json_data = ''
        expected = ''
        result = load_save_settings.remove_json_comments(json_data)
        self.assertEqual(result, expected.strip())

    def test_removejson_comments(self):
        json_data = """
        {
            "key": "value",
            // this is a comment
            // another line
        }
        """
        expected = """
        {
            "key": "value",
        }
        """
        result = load_save_settings.remove_json_comments(json_data)
        self.assertEqual(result.strip(), expected.strip())


class TestIsZukanListenerEnabled(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    def test_is_zukan_listener_enabled_true(self, mock_get_settings):
        mock_get_settings.return_value = True

        result = load_save_settings.is_zukan_listener_enabled()

        self.assertTrue(result)
        mock_get_settings.assert_called_once_with(
            load_save_settings.ZUKAN_SETTINGS, 'zukan_listener_enabled'
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    def test_is_zukan_listener_enabled_false(self, mock_get_settings):
        mock_get_settings.return_value = False

        result = load_save_settings.is_zukan_listener_enabled()

        self.assertFalse(result)
        mock_get_settings.assert_called_once_with(
            load_save_settings.ZUKAN_SETTINGS, 'zukan_listener_enabled'
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    def test_is_zukan_listener_enabled_none(self, mock_get_settings):
        mock_get_settings.return_value = None

        result = load_save_settings.is_zukan_listener_enabled()

        self.assertTrue(result)
        mock_get_settings.assert_called_once_with(
            load_save_settings.ZUKAN_SETTINGS, 'zukan_listener_enabled'
        )


class TestIsZukanRestartMessage(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    def test_is_zukan_restart_message(self, mock_get_settings):
        mock_get_settings.return_value = True

        result = load_save_settings.is_zukan_restart_message()

        self.assertTrue(result)
        mock_get_settings.assert_called_once_with(
            load_save_settings.ZUKAN_SETTINGS, 'zukan_restart_message'
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.load_save_settings.get_settings'
    )
    def test_is_zukan_restart_message_false(self, mock_get_settings):
        mock_get_settings.return_value = False

        result = load_save_settings.is_zukan_restart_message()

        self.assertFalse(result)
        mock_get_settings.assert_called_once_with(
            load_save_settings.ZUKAN_SETTINGS, 'zukan_restart_message'
        )
