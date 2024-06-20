import importlib
import os
import sublime

from unittest import TestCase
from unittest.mock import Mock

read_extract_zip = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_extract_zip'
)
file_extensions = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.file_extensions'
)
zukan_pkg_folders = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.zukan_pkg_folders'
)


class TestReadExtractZip(TestCase):
    def test_mock_extract_folder(self):
        mock = Mock()
        mock.read_extract_zip.extract_folder('a', 'b', 'c')
        mock.read_extract_zip.extract_folder.assert_called_with('a', 'b', 'c')

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
            'icons_preferences', dir_destiny, test_file_path
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
