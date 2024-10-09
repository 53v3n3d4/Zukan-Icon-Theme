import collections.abc
import os
import pytest
import re


from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.clean_svg import CleanSVG, _replace_line

# from src.build.utils.svg_common_ids import AFDESIGNER_COMMON_IDS_NAMES
from tests.mocks.constants_svg import (
    SVG_ALL_UNUSED,
    SVG_ALMOST_CLEAN,
    SVG_CLEANED,
    SVG_PARTIAL_UNUSED,
    UNUSED_LIST,
)
from unittest.mock import patch


class TestEditSVGID:
    @pytest.fixture
    def sample_svg_file(self, tmpdir):
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg">
            <defs>
                <g id="_clip1">...</g>
                <g id="_Effect2">...</g>
                <g id="_Linear3">...</g>
                # <g id="_Gradient4">...</g>
            </defs>
            <rect width="100" height="100" fill="red"/>
        </svg>"""
        svg_file = tmpdir.join('test.svg')
        with open(str(svg_file), 'w') as f:
            f.write(svg_content)
        return str(svg_file)

    def test_edit_svg_id_renames_ids(self, sample_svg_file):
        with open(sample_svg_file, 'r') as f:
            original_content = f.read()

        cleaned_content = CleanSVG.edit_svg_id(original_content, 'test.svg')

        # Ensure that old IDs are no longer present
        assert '_clip1' not in cleaned_content
        assert '_Effect2' not in cleaned_content
        assert '_Linear3' not in cleaned_content
        # assert "_Gradient4" not in cleaned_content

        # Check that new IDs have been added
        assert re.search(r'_clip-\w{7}', cleaned_content)  # Checking for a new clip ID
        assert re.search(
            r'_Effect-\w{7}', cleaned_content
        )  # Checking for a new effect ID
        assert re.search(
            r'_Linear-\w{7}', cleaned_content
        )  # Checking for a new linear ID
        # assert re.search(r'_Gradient-\w{7}', cleaned_content)  # Checking for a new gradient ID

    def test_edit_svg_id_no_ids(self, sample_svg_file):
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="red"/>
        </svg>"""
        cleaned_content = CleanSVG.edit_svg_id(svg_content, 'test.svg')
        assert cleaned_content == svg_content  # No changes should be made


class TestCleanSample:
    @pytest.fixture
    def sample_svg_file(self, tmpdir):
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg">
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <defs>
                <g id="clip1">...</g>
                <g id="linear1">...</g>
            </defs>
            <rect width="100" height="100" fill="red"/>
        </svg>"""
        svg_file = tmpdir.join('test.svg')
        with open(str(svg_file), 'w') as f:
            f.write(svg_content)
        return str(svg_file)

    def test_clean_svg_removes_unused_tags(self, sample_svg_file):
        CleanSVG.clean_svg(sample_svg_file, UNUSED_LIST)
        with open(sample_svg_file, 'r') as f:
            cleaned_content = f.read()
        assert (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            not in cleaned_content
        )
        assert (
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
            not in cleaned_content
        )
        assert 'xmlns:serif="http://www.serif.com/"' not in cleaned_content

    def test_clean_svg_handles_non_svg_files(self, tmpdir):
        non_svg_file = tmpdir.join('test.txt')
        with open(str(non_svg_file), 'w') as f:
            f.write('Just a text file')

        CleanSVG.clean_svg(str(non_svg_file), UNUSED_LIST)
        with open(str(non_svg_file), 'r') as f:
            content = f.read()
        assert content == 'Just a text file'  # Should remain unchanged


class TestClean:
    @pytest.mark.parametrize('a, expected', [(SVG_ALL_UNUSED, SVG_CLEANED)])
    def test_clean_svg_all_unused(self, a, expected):
        result = CleanSVG.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALMOST_CLEAN, SVG_CLEANED)])
    def test_clean_svg_almost_clean(self, a, expected):
        result = CleanSVG.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_PARTIAL_UNUSED, SVG_CLEANED)])
    def test_clean_svg_partial_unused(self, a, expected):
        result = CleanSVG.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALL_UNUSED, SVG_CLEANED)])
    def test_clean_all_svgs_all_unused(self, a, expected):
        result = CleanSVG.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALMOST_CLEAN, SVG_CLEANED)])
    def test_clean_all_svgs_almost_clean(self, a, expected):
        result = CleanSVG.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_PARTIAL_UNUSED, SVG_CLEANED)])
    def test_clean_all_svgs_partial_unused(self, a, expected):
        result = CleanSVG.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.fixture(autouse=True)
    def test_load_svg_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            CleanSVG.clean_svg('tests/mocks/not_found_svg.svg', UNUSED_LIST)
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_svg.svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_svg_file_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            CleanSVG.clean_svg('tests/mocks/svg.svg', UNUSED_LIST)
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/svg.svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_load_svgs_filenotfound_error(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            CleanSVG.clean_all_svgs('tests/mocks/svg', UNUSED_LIST)
        # Check if it is cache, should be Errno 2
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_load_svgs_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            CleanSVG.clean_all_svgs('tests/mocks/svg.svg', UNUSED_LIST)
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/svg.svg'",
            )
        ]

    def test_replace_line(self):
        test_line = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        test_removed = ''
        result = _replace_line('', test_line)
        assert result == test_removed

    def test_replace_line_not_remove(self):
        test_line = 'Text not unused'
        test_removed = ''
        result = _replace_line('Text', test_line)
        assert result != test_removed


class TestCleanSVG(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('icons/file_type_afdesign.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afphoto.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afpub.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_ai.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_angular.svg', contents='test')

    def test_file_exist(self):
        CleanSVG.clean_svg('icons/file_type_ai.svg', UNUSED_LIST)
        self.assertTrue(os.path.exists('icons/file_type_ai.svg'))

    def test_dir_exist(self):
        CleanSVG.clean_all_svgs('icons', UNUSED_LIST)
        self.assertTrue(os.path.exists('icons'))

    def test_file_not_found(self):
        CleanSVG.clean_svg('icons/file_type_babel.svg', UNUSED_LIST)
        self.assertFalse(os.path.exists('icons/file_type_babel.svg'))

    def test_dir_not_found(self):
        CleanSVG.clean_all_svgs('icons_not_found', UNUSED_LIST)
        self.assertFalse(os.path.exists('icons_not_found'))

    def test_params_clean_svg(self):
        CleanSVG.clean_svg('icons/file_type_ai.svg', UNUSED_LIST)
        self.assertTrue(isinstance('icons/file_type_ai.svg', str))
        self.assertTrue(isinstance(UNUSED_LIST, collections.abc.Set))
        self.assertFalse(isinstance('icons/file_type_ai.svg', int))
        self.assertFalse(isinstance('icons/file_type_ai.svg', list))
        self.assertFalse(isinstance('icons/file_type_ai.svg', bool))
        self.assertFalse(isinstance(UNUSED_LIST, int))
        self.assertFalse(isinstance(UNUSED_LIST, list))
        self.assertFalse(isinstance(UNUSED_LIST, bool))

    def test_params_clean_all_svgs(self):
        CleanSVG.clean_all_svgs('icons', UNUSED_LIST)
        self.assertTrue(isinstance('icons', str))
        self.assertTrue(isinstance(UNUSED_LIST, collections.abc.Set))
        self.assertFalse(isinstance('icons', int))
        self.assertFalse(isinstance('icons', list))
        self.assertFalse(isinstance('icons', bool))
        self.assertFalse(isinstance(UNUSED_LIST, int))
        self.assertFalse(isinstance(UNUSED_LIST, list))
        self.assertFalse(isinstance(UNUSED_LIST, bool))
