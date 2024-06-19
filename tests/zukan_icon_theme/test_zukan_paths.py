import importlib
import os
import sublime
import unittest


zukan_paths = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.zukan_paths'
)
file_extensions = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.file_extensions'
)

ZUKAN_INSTALLED_PKG_PATH = os.path.join(
    sublime.installed_packages_path(),
    'Zukan-Icon-Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
)
ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), 'Zukan-Icon-Theme')


class TestZukanPaths(unittest.TestCase):
    def test_zukan_path(self):
        self.assertEqual(
            ZUKAN_INSTALLED_PKG_PATH,
            '/Users/macbookpro14/Library/Application Support/Sublime Text/Installed Packages/Zukan-Icon-Theme.sublime-package',
        )
        self.assertEqual(
            ZUKAN_PKG_PATH,
            '/Users/macbookpro14/Library/Application Support/Sublime Text/Packages/Zukan-Icon-Theme',
        )
        self.assertNotEqual(
            ZUKAN_INSTALLED_PKG_PATH,
            '/Users/macbookpro14/Library/Application Support/Sublime Text/Packages/Zukan-Icon-Theme.sublime-package',
        )
        self.assertNotEqual(
            ZUKAN_PKG_PATH,
            '/Users/macbookpro14/Library/Application Support/Sublime Text/User/Zukan-Icon-Theme',
        )
