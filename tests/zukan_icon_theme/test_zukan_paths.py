import importlib

# import os
import sublime

from os.path import relpath
from unittest import TestCase
from unittest.mock import Mock, patch

zukan_paths = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.zukan_paths'
)
file_extensions = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.file_extensions'
)


DATA_PATH = zukan_paths.filepath('../../data')
PACKAGE_NAME = 'Zukan Icon Theme'
ST_PACKAGES_PATH = sublime.packages_path() + '/'
ST_INSTALLED_PACKAGES_PATH = sublime.installed_packages_path() + '/'

params_list = [
    (zukan_paths.PACKAGES_PATH + '/', ST_PACKAGES_PATH),
    (zukan_paths.INSTALLED_PACKAGES_PATH + '/', ST_INSTALLED_PACKAGES_PATH),
    (
        zukan_paths.ZUKAN_PKG_ICONS_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME + '/icons',
    ),
    (
        zukan_paths.ZUKAN_PKG_ICONS_PREFERENCES_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME + '/icons_preferences',
    ),
    (
        zukan_paths.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME + '/icons_syntaxes',
    ),
    (
        zukan_paths.ZUKAN_PKG_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME,
    ),
    (
        zukan_paths.ZUKAN_PKG_SRC_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME + '/src',
    ),
    (
        zukan_paths.ZUKAN_PKG_SUBLIME_PATH,
        ST_PACKAGES_PATH + PACKAGE_NAME + '/sublime',
    ),
    (
        zukan_paths.ZUKAN_INSTALLED_PKG_PATH,
        ST_INSTALLED_PACKAGES_PATH
        + PACKAGE_NAME
        + file_extensions.SUBLIME_PACKAGE_EXTENSION,
    ),
    (
        zukan_paths.ZUKAN_ICONS_DATA_FILE,
        ST_PACKAGES_PATH
        + PACKAGE_NAME
        + '/icons_data/zukan_icons_data'
        + file_extensions.PICKLE_EXTENSION,
    ),
    (
        zukan_paths.ZUKAN_VERSION_FILE,
        ST_PACKAGES_PATH
        + PACKAGE_NAME
        + '/sublime/zukan-version'
        + file_extensions.SUBLIME_SETTINGS_EXTENSION,
    ),
    (
        zukan_paths.ZUKAN_CURRENT_SETTINGS_FILE,
        ST_PACKAGES_PATH
        + PACKAGE_NAME
        + '/sublime/zukan_current_settings'
        + file_extensions.PICKLE_EXTENSION,
    ),
]


class TestZukanPaths(TestCase):
    def test_param_is_string(self):
        TESTS_FOLDER = zukan_paths.filepath('../tests')
        self.assertIsInstance(TESTS_FOLDER, str)

    def test_param_fails_int(self):
        with self.assertRaisesRegex(ValueError, 'Url need to be string.'):
            zukan_paths.filepath(7)

    def test_param_fails_array(self):
        with self.assertRaisesRegex(ValueError, 'Url need to be string.'):
            array_fail = ['milk', 'way']
            zukan_paths.filepath(array_fail)

    # Using relpath, relative path from start directory, to make path
    # test possible in diferent machines.
    # https://docs.python.org/3/library/os.path.html#os.path.relpath
    def test_relative_path(self):
        TESTS_FOLDER = zukan_paths.filepath('../tests')
        SHORT_URL = relpath(TESTS_FOLDER, start=DATA_PATH)
        TESTS_RELATIVE_PATH = '../zukan_icon_theme/tests'
        self.assertEqual(SHORT_URL, TESTS_RELATIVE_PATH)

    def test_zukan_path(self):
        for p1, p2 in params_list:
            with self.subTest(params_list):
                # result = zukan_paths.filepath(p2)
                self.assertEqual(p1, p2)
                self.assertIsInstance(p1, str)
                self.assertIsInstance(p2, str)


# ZUKAN_INSTALLED_PKG_PATH = os.path.join(
#     sublime.installed_packages_path(),
#     'Zukan Icon Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
# )
# ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), 'Zukan Icon Theme')
