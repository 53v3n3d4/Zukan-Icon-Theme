import importlib

from unittest import TestCase
from unittest.mock import patch

move_folders = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.move_folders'
)


class TestMoveFolder(TestCase):
    def setUp(self):
        self.move = move_folders.MoveFolder()

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.move_folders.extract_folder')
    def test_move_folder(self, mock_extract, mock_makedirs, mock_exists):
        # INSTALLED_PKG_PATH exists, PKG_PATH doesn't
        mock_exists.side_effect = [
            True,
            False,
        ]
        result = self.move.move_folder('test_folder')
        mock_makedirs.assert_called_once()
        mock_extract.assert_called_once()
        self.assertEqual(result, 'test_folder')

    @patch('os.path.exists')
    def test_move_folder_not_in_installed(self, mock_exists):
        mock_exists.return_value = False
        result = self.move.move_folder('test_folder')
        self.assertIsNone(result)

    @patch('os.path.exists')
    def test_move_folder_file_not_found(self, mock_exists):
        mock_exists.side_effect = FileNotFoundError()
        result = self.move.move_folder('test_folder')
        self.assertIsNone(result)

    @patch('os.path.exists')
    def test_move_folder_os_error(self, mock_exists):
        mock_exists.side_effect = OSError()
        result = self.move.move_folder('test_folder')
        self.assertIsNone(result)

    @patch.object(move_folders.MoveFolder, 'move_folder')
    def test_move_folders(self, mock_move):
        mock_move.return_value = 'test_folder'
        result = self.move.move_folders()
        self.assertEqual(result, self.move.zukan_pkg_folders)
        self.assertEqual(mock_move.call_count, len(self.move.zukan_pkg_folders))

    @patch.object(move_folders.MoveFolder, 'move_folder')
    def test_move_folders_file_not_found(self, mock_move):
        mock_move.side_effect = FileNotFoundError()
        result = self.move.move_folders()
        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('shutil.rmtree')
    def test_remove_created_folder(self, mock_rmtree, mock_exists):
        mock_exists.side_effect = [False, True, True]
        result = self.move.remove_created_folder('test_folder')
        mock_rmtree.assert_called_once()
        self.assertEqual(result, 'test_folder')

    @patch('os.path.exists')
    def test_remove_created_folder_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = self.move.remove_created_folder('test_folder')
        self.assertIsNone(result)

    @patch('os.path.exists')
    def test_remove_created_folder_os_error(self, mock_exists):
        mock_exists.side_effect = OSError()
        result = self.move.remove_created_folder('test_folder')
        self.assertIsNone(result)
