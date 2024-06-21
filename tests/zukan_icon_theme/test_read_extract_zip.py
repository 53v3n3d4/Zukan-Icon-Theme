import importlib
import os
import sublime

from unittest import TestCase
from unittest.mock import Mock

constants_icons_preferences = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_icons_preferences'
)
read_extract_zip = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_extract_zip'
)
file_extensions = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.file_extensions'
)


class TestReadExtractZip(TestCase):
    def test_mock_extract_folder(self):
        mock = Mock()
        mock.read_extract_zip.extract_folder('a')
        mock.read_extract_zip.extract_folder.assert_called_with('a')

    def test_extract_folder(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'Zukan-Icon-Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
        )
        dir_destiny = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
        )
        read_extract_zip.extract_folder(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES,
            dir_destiny,
            test_file_path,
        )
        self.assertTrue(os.path.exists(test_file_path))

    def test_extract_folder_not_exist_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            test_file_path = os.path.join(
                sublime.packages_path(),
                'Zukan-Icon-Theme',
                'tests',
                'Zukan-Icon-Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
            )
            dir_destiny = os.path.join(
                sublime.packages_path(),
                'Zukan-Icon-Theme',
                'tests',
                'mocks',
            )
            read_extract_zip.extract_folder(
                'icons_preferences', dir_destiny, test_file_path
            )
        self.assertEqual(
            "[Errno 2] No such file or directory: '/Users/macbookpro14/Library/Application Support/Sublime Text/Packages/Zukan-Icon-Theme/tests/Zukan-Icon-Theme.sublime-package'",
            str(e.exception),
        )


class TestExtractZipFolder(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'Zukan-Icon-Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
        )
        dir_destiny = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
        )
        read_extract_zip.extract_folder(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES,
            dir_destiny,
            test_file_path,
        )
        self.assertTrue(os.path.exists(test_file_path))

    def test_extract_zip_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'Zukan-Icon-Theme' + file_extensions.SUBLIME_PACKAGE_EXTENSION,
        )
        dir_destiny = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
        )
        read_extract_zip.extract_folder(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES,
            dir_destiny,
            test_file_path,
        )
        self.assertIsInstance(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES, str
        )
        self.assertNotIsInstance(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES, int
        )
        self.assertNotIsInstance(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES, list
        )
        self.assertNotIsInstance(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES, bool
        )
        self.assertNotIsInstance(
            constants_icons_preferences.TEST_DIR_ICONS_PREFERENCES, dict
        )
        self.assertIsInstance(dir_destiny, str)
        self.assertNotIsInstance(dir_destiny, int)
        self.assertNotIsInstance(dir_destiny, list)
        self.assertNotIsInstance(dir_destiny, bool)
        self.assertNotIsInstance(dir_destiny, dict)
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
