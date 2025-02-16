import os
import pytest
import re

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.clean_svg import CleanSVG
from tests.build.mocks.constants_svg import (
    SVG_ALL_UNUSED,
    SVG_ALMOST_CLEAN,
    SVG_CLEANED,
    SVG_PARTIAL_UNUSED,
    UNUSED_LIST,
)
from unittest.mock import mock_open, patch

zukan_clean_svg = CleanSVG()


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

        cleaned_content = zukan_clean_svg.edit_svg_id(original_content, 'test.svg')

        assert '_clip1' not in cleaned_content
        assert '_Effect2' not in cleaned_content
        assert '_Linear3' not in cleaned_content

        assert re.search(r'_clip-\w{7}', cleaned_content)
        assert re.search(
            r'_Effect-\w{7}', cleaned_content
        )  # Checking for a new effect ID
        assert re.search(r'_Linear-\w{7}', cleaned_content)

    def test_edit_svg_id_no_ids(self, sample_svg_file):
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" fill="red"/>
        </svg>"""
        cleaned_content = zukan_clean_svg.edit_svg_id(svg_content, 'test.svg')
        assert cleaned_content == svg_content

    def test_edit_svg_id_with_path_prefix(self):
        input_data = (
            '<svg><g id="Path_1"><rect x="0" y="0" width="1024" height="1024"/></g>'
            '<g id="_clip1"><path d="M118,165L238,165"/></g></svg>'
        )

        result = zukan_clean_svg.edit_svg_id(input_data, 'testfile.svg')

        assert 'Path-' in result

    def test_edit_svg_id_with_path_prefix_1(self):
        input_data = (
            '<svg><g id="Path_1"><rect x="0" y="0" width="1024" height="1024"/></g>'
            '<g id="Path_2"><g id="atest"></g></g>'
            '<g id="_Linear1"><path d="M118,165L238,165"/></g></svg>'
        )

        result = zukan_clean_svg.edit_svg_id(input_data, 'testfile.svg')

        assert 'Path-' in result


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
        zukan_clean_svg.clean_svg(sample_svg_file, UNUSED_LIST)
        with open(sample_svg_file, 'r') as f:
            cleaned_content = f.read()
        assert (
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            not in cleaned_content
        )
        assert (
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
            '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' not in cleaned_content
        )
        assert 'xmlns:serif="http://www.serif.com/"' not in cleaned_content

    def test_clean_svg_handles_non_svg_files(self, tmpdir):
        non_svg_file = tmpdir.join('test.txt')
        with open(str(non_svg_file), 'w') as f:
            f.write('Just a text file')

        zukan_clean_svg.clean_svg(str(non_svg_file), UNUSED_LIST)
        with open(str(non_svg_file), 'r') as f:
            content = f.read()
        assert content == 'Just a text file'


class TestClean:
    @pytest.mark.parametrize('a, expected', [(SVG_ALL_UNUSED, SVG_CLEANED)])
    def test_clean_svg_all_unused(self, a, expected):
        result = zukan_clean_svg.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALMOST_CLEAN, SVG_CLEANED)])
    def test_clean_svg_almost_clean(self, a, expected):
        result = zukan_clean_svg.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_PARTIAL_UNUSED, SVG_CLEANED)])
    def test_clean_svg_partial_unused(self, a, expected):
        result = zukan_clean_svg.clean_svg(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALL_UNUSED, SVG_CLEANED)])
    def test_clean_all_svgs_all_unused(self, a, expected):
        result = zukan_clean_svg.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_ALMOST_CLEAN, SVG_CLEANED)])
    def test_clean_all_svgs_almost_clean(self, a, expected):
        result = zukan_clean_svg.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    @pytest.mark.parametrize('a, expected', [(SVG_PARTIAL_UNUSED, SVG_CLEANED)])
    def test_clean_all_svgs_partial_unused(self, a, expected):
        result = zukan_clean_svg.clean_all_svgs(a, UNUSED_LIST)
        return result
        assert result == SVG_CLEANED

    def test_clean_svg_with_regex(self):
        test_svg_content = (
            '<svg><g serif:id="1234"><rect x="0" y="0" width="1024" height="1024"/>'
            '</g></svg>'
        )

        with patch('builtins.open', mock_open(read_data=test_svg_content)) as mock_file:
            clean_svg_instance = CleanSVG()
            clean_svg_instance.clean_svg('test.svg', replace_list=set())

            mock_file.assert_called_with('test.svg', 'w')
            handle = mock_file()
            handle.write.assert_called_with(
                '<svg><g><rect x="0" y="0" width="1024" height="1024"/></g></svg>'
            )

    @pytest.fixture(autouse=True)
    def test_clean_svg_file_not_found(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            zukan_clean_svg.clean_svg(
                'tests/build/mocks/not_found_svg.svg', UNUSED_LIST
            )
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/not_found_svg.svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_clean_svg_file_os_error(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            zukan_clean_svg.clean_svg('tests/build/mocks/svg.svg', UNUSED_LIST)
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/svg.svg'",
            )
        ]

    def test_clean_all_svgs_directory_exists(self):
        mock_svg_files = ['afdesign.svg', 'afphoto.svg', 'afpub.svg']

        with patch('os.listdir', return_value=mock_svg_files):
            with patch.object(zukan_clean_svg, 'clean_svg'):
                dir_svg = '/mock/directory'
                replace_list = {'unused_tag', 'unused_attribute'}

                result = zukan_clean_svg.clean_all_svgs(dir_svg, replace_list)

                assert result == mock_svg_files

                for svg in mock_svg_files:
                    zukan_clean_svg.clean_svg.assert_any_call(
                        os.path.join(dir_svg, svg), replace_list
                    )

    @pytest.fixture(autouse=True)
    def test_clean_all_svgs_file_not_found(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            zukan_clean_svg.clean_all_svgs('tests/build/mocks/svg', UNUSED_LIST)
        # Check if it is cache, should be Errno 2
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/svg'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_clean_all_svgs_os_error(self, caplog):
        caplog.clear()
        with patch('src.build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            zukan_clean_svg.clean_all_svgs('tests/build/mocks/svg.svg', UNUSED_LIST)
        assert caplog.record_tuples == [
            (
                'src.build.clean_svg',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/svg.svg'",
            )
        ]

    def test_replace_line(self):
        test_line = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        test_removed = ''
        result = zukan_clean_svg.replace_line('', test_line)
        assert result == test_removed

    def test_replace_line_not_remove(self):
        test_line = 'Text not unused'
        test_removed = ''
        result = zukan_clean_svg.replace_line('Text', test_line)
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
        zukan_clean_svg.clean_svg('icons/file_type_ai.svg', UNUSED_LIST)
        self.assertTrue(os.path.exists('icons/file_type_ai.svg'))

    # def test_dir_exist(self):
    #     zukan_clean_svg.clean_all_svgs('icons', UNUSED_LIST)
    #     self.assertTrue(os.path.exists('icons'))

    # def test_file_not_found(self):
    #     zukan_clean_svg.clean_svg('icons/file_type_babel.svg', UNUSED_LIST)
    #     self.assertFalse(os.path.exists('icons/file_type_babel.svg'))


#     def test_dir_not_found(self):
#         zukan_clean_svg.clean_all_svgs('icons_not_found', UNUSED_LIST)
#         self.assertFalse(os.path.exists('icons_not_found'))

# def test_params_clean_svg(self):
#     zukan_clean_svg.clean_svg('icons/file_type_ai.svg', UNUSED_LIST)
#     self.assertTrue(isinstance('icons/file_type_ai.svg', str))
#     self.assertTrue(isinstance(UNUSED_LIST, collections.abc.Set))
#     self.assertFalse(isinstance('icons/file_type_ai.svg', int))
#     self.assertFalse(isinstance('icons/file_type_ai.svg', list))
#     self.assertFalse(isinstance('icons/file_type_ai.svg', bool))
#     self.assertFalse(isinstance(UNUSED_LIST, int))
#     self.assertFalse(isinstance(UNUSED_LIST, list))
#     self.assertFalse(isinstance(UNUSED_LIST, bool))

#     def test_params_clean_all_svgs(self):
#         zukan_clean_svg.clean_all_svgs('icons', UNUSED_LIST)
#         self.assertTrue(isinstance('icons', str))
#         self.assertTrue(isinstance(UNUSED_LIST, collections.abc.Set))
#         self.assertFalse(isinstance('icons', int))
#         self.assertFalse(isinstance('icons', list))
#         self.assertFalse(isinstance('icons', bool))
#         self.assertFalse(isinstance(UNUSED_LIST, int))
#         self.assertFalse(isinstance(UNUSED_LIST, list))
#         self.assertFalse(isinstance(UNUSED_LIST, bool))
