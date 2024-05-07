import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.rename_svg import RenameSVG
from unittest.mock import patch


class TestRename:
    @pytest.mark.parametrize(
        'a, expected',
        [('tests/build/mocks/file_type_svg.svg', 'tests/build/mocks/svg.svg')],
    )
    def test_rename_svg(self, a, expected):
        result = RenameSVG.rename_svg(a, 'tests/build/mocks/', 'tests/build/mocks/')
        return result
        assert result == 'tests/build/mocks/svg.svg'

    @pytest.mark.parametrize('a, expected', [('file_type_svg.svg', 'svg.svg')])
    def test_rename_svgs_in_dir(self, a, expected):
        test_dir = 'file_type_svg.svg'
        result = RenameSVG.rename_svgs_in_dir(a, test_dir)
        return result
        # assert result == 'tests/build/mocks/svg.svg'
        assert result == 'svg.svg'

    @pytest.fixture(autouse=True)
    def test_read_file_error(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.rename_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            RenameSVG.rename_svg(
                'tests/build/file_type_svg.svg',
                'tests/build/mocks/',
                'tests/build/mocks/',
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.rename_svg',
                40,
                "[Errno 2] No such file or directory: 'tests/build/file_type_svg.svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_read_dir_error(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.rename_svg.open') as mock_open:
            mock_open.side_effect = OSError
            RenameSVG.rename_svgs_in_dir(
                'tests/build/mocks/svg.svg', 'tests/build/mocks/'
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.rename_svg',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/svg.svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_not_svg_file(self, capfd):
        RenameSVG.rename_svg('plist.plist', 'tests/build/mocks/', 'tests/build/mocks/')

        out, err = capfd.readouterr()
        assert out == '\x1b[35m[!] plist.plist:\x1b[0m file extension is not svg.\n'


class TestRenameSVG(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('icons/file_type_afdesign.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afphoto.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afpub.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_ai.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_angular.svg', contents='test')

    def test_file_exist(self):
        RenameSVG.rename_svg('icons/file_type_ai.svg', 'icons', 'icons')
        self.assertTrue(os.path.exists('icons/file_type_ai.svg'))

    def test_file_not_found(self):
        RenameSVG.rename_svg('icons/file_type_babel.svg', 'icons', 'icons')
        self.assertFalse(os.path.exists('icons/file_type_babel.svg'))

    def test_params(self):
        RenameSVG.rename_svg('icons/file_type_ai.svg', 'icons', 'icons')
        self.assertTrue(isinstance('icons/file_type_ai.svg', str))
        self.assertTrue(isinstance('icons', str))
        self.assertFalse(isinstance('icons/file_type_ai.svg', int))
        self.assertFalse(isinstance('icons', int))
        self.assertFalse(isinstance('icons/file_type_ai.svg', list))
        self.assertFalse(isinstance('icons', list))
