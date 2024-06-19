import importlib
import sublime
import unittest

get_settings = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.get_settings'
)
file_settings = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.file_settings'
)


class TestLoadSettings(unittest.TestCase):
    def test_load_settings(self):
        x = get_settings.load_settings(file_settings.USER_SETTINGS)
        y = sublime.load_settings(file_settings.USER_SETTINGS)
        self.assertTrue(x, y)

    def test_load_settings_not_equal(self):
        x = get_settings.load_settings(file_settings.USER_SETTINGS)
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS)
        self.assertNotEqual(x, y)

    def test_load_settings_options(self):
        x = get_settings.load_settings(file_settings.ZUKAN_SETTINGS, 'version')
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS).get('version')
        self.assertEqual(x, y)

    def test_load_settings_options_not_equal(self):
        x = get_settings.load_settings(file_settings.ZUKAN_SETTINGS, 'log_level')
        y = sublime.load_settings(file_settings.ZUKAN_SETTINGS).get('version')
        self.assertNotEqual(x, y)
