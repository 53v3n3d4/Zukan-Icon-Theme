import importlib
import sublime

from unittest import TestCase

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
