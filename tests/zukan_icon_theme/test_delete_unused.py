import importlib
import os
import shutil
import tempfile

from unittest import TestCase
from unittest.mock import patch

delete_unused = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.delete_unused'
)


class TestDeleteUnusedIcons(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_files = [
            'ada.png',
            'ada-dark.png',
            'ada-light.png',
            'angular.png',
            'rust-1.png',
            'file_type_source-dark.png',
            'file_type_source-light.png',
            'cert.png',
            'cert-dark.png',
            'cert-light.png',
        ]

        for file_name in self.test_files:
            with open(os.path.join(self.test_dir, file_name), 'w') as f:
                f.write('dummy content')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.delete_unused.logging.Logger.debug'
    )
    def test_delete_unused_icons(self, mock_debug):
        delete_unused.delete_unused_icons(self.test_dir)

        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'ada.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'ada-dark.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'ada-light.png')))

        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'cert.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'cert-dark.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'cert-light.png')))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.delete_unused.logging.Logger.debug'
    )
    def test_delete_unused_icons_not_delete(self, mock_debug):
        delete_unused.delete_unused_icons(self.test_dir)

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'angular.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'rust-1.png')))
        self.assertTrue(
            os.path.exists(os.path.join(self.test_dir, 'file_type_source-dark.png'))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.test_dir, 'file_type_source-light.png'))
        )

    def test_empty_folder(self):
        empty_dir = tempfile.mkdtemp()

        delete_unused.delete_unused_icons(empty_dir)

        shutil.rmtree(empty_dir)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.delete_unused.logging.Logger.debug'
    )
    def test_logging_output(self, mock_debug):
        delete_unused.delete_unused_icons(self.test_dir)

        mock_debug.assert_any_call('removing unused PNGs.')
        mock_debug.assert_any_call('unused icon %s%s%s deleted.', 'ada', '', '.png')
        mock_debug.assert_any_call('unused icon %s%s%s deleted.', 'cert', '', '.png')

    def test_nonexistent_folder(self):
        with self.assertRaises(FileNotFoundError):
            delete_unused.delete_unused_icons('/nonexistent/folder_path')
