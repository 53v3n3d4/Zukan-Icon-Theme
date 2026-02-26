import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import patch, MagicMock

package_size = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.package_size'
)


class TestPackageSize(TestCase):
    @patch('os.path.isfile')
    @patch('os.lstat')
    def test_get_file_size(self, mock_lstat, mock_isfile):
        mock_isfile.return_value = True
        mock_lstat.return_value.st_size = 100
        file_path = '/some/file/path.txt'

        result = package_size.get_file_size(file_path)

        self.assertEqual(result, 100)
        mock_isfile.assert_called_once_with(file_path)
        mock_lstat.assert_called_once_with(file_path)

    @patch('os.path.isfile')
    @patch('os.lstat')
    def test_get_file_size_file_not_found(self, mock_lstat, mock_isfile):
        mock_isfile.return_value = False
        file_path = '/some/file/path.txt'

        result = package_size.get_file_size(file_path)

        self.assertEqual(result, 0)
        mock_isfile.assert_called_once_with(file_path)
        mock_lstat.assert_not_called()

    @patch.object(package_size, 'logger')
    @patch('os.lstat')
    @patch('os.path.isfile')
    def test_get_file_size_os_error(self, mock_isfile, mock_lstat, mock_logger):
        mock_isfile.return_value = True  # Ensure os.path.isfile returns True
        mock_lstat.side_effect = OSError(
            errno.EACCES, os.strerror(errno.EACCES), 'file'
        )

        file_path = '/some/file/path.txt'

        result = package_size.get_file_size(file_path)

        # print(mock_logger.method_calls)

        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )
        self.assertEqual(result, 0)

    @patch('os.walk')
    @patch('os.lstat')
    def test_get_folder_size(self, mock_lstat, mock_oswalk):
        mock_oswalk.return_value = [
            ('/folder', ('subfolder',), ['file1.txt', 'file2.txt']),
        ]
        mock_lstat.return_value.st_size = 100
        mock_lstat.return_value.st_ino = 12345

        mock_lstat.side_effect = [
            MagicMock(st_size=100, st_ino=12345),
            MagicMock(st_size=100, st_ino=12346),
        ]

        folder_path = '/folder'

        result = package_size.get_folder_size(folder_path)

        self.assertEqual(result, 200)
        mock_oswalk.assert_called_once_with(folder_path)
        mock_lstat.assert_called()

    @patch('os.walk')
    def test_get_folder_size_empty_folder(self, mock_oswalk):
        mock_oswalk.return_value = [
            ('/folder', (), []),
        ]

        folder_path = '/folder'

        result = package_size.get_folder_size(folder_path)

        self.assertEqual(result, 0)
        mock_oswalk.assert_called_once_with(folder_path)

    @patch.object(package_size, 'logger')
    @patch('os.lstat')
    @patch('os.walk')
    def test_get_folder_size_os_error(self, mock_oswalk, mock_lstat, mock_logger):
        mock_oswalk.return_value = [
            ('folder', ('subfolder',), ['file1.txt']),
        ]
        mock_lstat.side_effect = OSError(
            errno.EACCES, os.strerror(errno.EACCES), '/folder/file1.txt'
        )

        folder_path = '/folder'

        result = package_size.get_folder_size(folder_path)

        args, _ = mock_logger.error.call_args

        self.assertEqual(args[0], '[Errno %d] %s: %r')
        self.assertEqual(args[1], 13)
        self.assertEqual(args[2], 'Permission denied')
        # self.assertEqual(args[3], '/folder/file1.txt')
        self.assertEqual(args[3], os.path.join('folder', 'file1.txt'))
        self.assertEqual(result, 0)

    @patch('os.walk')
    @patch('os.lstat')
    def test_get_folder_size_with_symlink(self, mock_lstat, mock_oswalk):
        mock_oswalk.return_value = [
            ('folder', (), ['file1.txt', 'file2.txt']),
        ]
        mock_lstat.side_effect = [
            MagicMock(st_size=100, st_ino=12345),
            MagicMock(st_size=100, st_ino=12346),
        ]

        folder_path = 'folder'

        result = package_size.get_folder_size(folder_path)

        self.assertEqual(result, 200)
        mock_oswalk.assert_called_once_with(folder_path)
        mock_lstat.assert_any_call(os.path.join('folder', 'file1.txt'))
        mock_lstat.assert_any_call(os.path.join('folder', 'file2.txt'))

    @patch('os.walk')
    @patch('os.lstat')
    def test_get_folder_size_with_duplicate_inodes(self, mock_lstat, mock_oswalk):
        mock_oswalk.return_value = [
            ('folder', (), ['file1.txt', 'file2.txt']),
        ]
        mock_lstat.side_effect = [
            MagicMock(st_size=100, st_ino=12345),
            MagicMock(st_size=200, st_ino=12345),
        ]

        folder_path = 'folder'

        result = package_size.get_folder_size(folder_path)

        self.assertEqual(result, 100)
        mock_oswalk.assert_called_once_with(folder_path)
        mock_lstat.assert_any_call(os.path.join('folder', 'file1.txt'))
        mock_lstat.assert_any_call(os.path.join('folder', 'file2.txt'))
        self.assertEqual(mock_lstat.call_count, 2)

    def test_bytes_to_readable_size(self):
        list_sizes = [
            (0, '0.0B'),
            (1023, '1023.0B'),
            (1024, '1.0KB'),
            (1048576, '1.0MB'),
            (1073741824, '1.0GB'),
            (1099511627776, '1.0TB'),
        ]

        for p1, p2 in list_sizes:
            with self.subTest(list_sizes):
                result = package_size.bytes_to_readable_size(p1)
                self.assertEqual(result, p2)
