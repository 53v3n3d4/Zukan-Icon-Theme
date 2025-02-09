import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.concat_svgs import ConcatSVG
from src.build.utils.file_extensions import SVG_EXTENSION
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_ORIGIN,
)
from unittest.mock import patch
from xml.etree import ElementTree


class TestConcatSVGMock:
    @pytest.fixture
    def concat_svgs(self):
        return ConcatSVG()

    @pytest.fixture
    def mock_svg_data(self):
        return ElementTree.Element('svg', {'width': '32', 'height': '28.4'})

    @pytest.fixture
    def mock_icon_data(self, tmp_path):
        icon_name = 'test_icon'
        icon_data = {
            'preferences': {'settings': {'icon': icon_name}},
            'name': 'Test Icon',
            'icons': ['test_icon-1'],
        }
        yaml_path = tmp_path / f'{icon_name}.yaml'
        with open(yaml_path, 'w') as f:
            f.write(f'{icon_data}')
        return yaml_path, icon_name

    def test_create_element_svg(self, concat_svgs):
        attributes = {'width': '100', 'height': '100', 'viewbox': '0 0 100 100'}
        svg_element = concat_svgs.create_element_svg(attributes)

        assert svg_element.tag == 'svg'
        assert svg_element.get('width') == '100'
        assert svg_element.get('height') == '100'
        assert svg_element.get('viewbox') == '0 0 100 100'

    def test_create_rounded_rect(self, concat_svgs, mock_svg_data):
        rect = concat_svgs.create_rounded_rect(mock_svg_data)
        assert rect.tag == 'g'
        assert rect.get('transform') == 'matrix(0.79,0,0,0.77,0,0)'

    def test_write_icon_name(self, concat_svgs, mock_svg_data):
        sticker_name = 'Test Icon'
        svgfile_name = 'icon_name.svg'
        text_element = concat_svgs.write_icon_name(
            mock_svg_data, sticker_name, svgfile_name
        )

        assert text_element.tag == 'g'
        assert len(text_element) == 1

    def test_edit_icon_svg(self, concat_svgs, mock_svg_data):
        patch('xml.etree.ElementTree.parse', return_value=mock_svg_data)
        icon_svg = concat_svgs.edit_icon_svg('tests/mocks/vitest.svg')

        assert icon_svg.get('width') == '32'
        assert icon_svg.get('height') == '28.4'
        assert icon_svg.get('viewbox') == '0 0 32 28.4'
        assert icon_svg.get('x') == '23'
        assert icon_svg.get('y') == '17'

    def test_create_icon_sticker(self, concat_svgs):
        sticker_svg = concat_svgs.create_icon_sticker(
            'tests/mocks/vitest.svg', str(12), str(8), 'Vitest', 'vitest.svg'
        )

        assert sticker_svg.get('width') == '79'
        assert sticker_svg.get('height') == '77'
        assert sticker_svg.get('viewbox') == '0 0 79 77'
        assert sticker_svg.get('x') == '12'
        assert sticker_svg.get('y') == '8'
        assert sticker_svg.tag == 'svg'
        assert len(sticker_svg) == 3

    def test_select_prefer_icon_light(self, concat_svgs):
        with patch.object(concat_svgs, 'add_to_list_svgs') as mock_add_to_list_svgs:
            prefer_icon = 'light'
            icon_name = 'test_icon'
            sticker_name = 'Test Icon'
            dir_origin = '/path/test'
            list_svgs = set()

            concat_svgs.select_prefer_icon(
                icon_name, sticker_name, dir_origin, list_svgs, prefer_icon
            )

            mock_add_to_list_svgs.assert_called_once_with(
                icon_name, sticker_name, dir_origin, list_svgs
            )

    def test_sorted_icons_list(self, concat_svgs):
        icon_name = 'vitest'
        result = concat_svgs.sorted_icons_list(DIR_DATA, DIR_ORIGIN)

        assert len(result) == 1
        assert (
            'Vitest',
            f'{DIR_DATA}/{icon_name}{SVG_EXTENSION}',
            f'{icon_name}{SVG_EXTENSION}',
        ) in result

    @pytest.fixture(autouse=True)
    def test_sorted_icons_list_directory_not_found(self, concat_svgs, caplog):
        caplog.clear()
        with patch('os.listdir', side_effect=FileNotFoundError):
            concat_svgs.sorted_icons_list(DIR_DATA, DIR_ORIGIN)
        assert caplog.record_tuples == [
            (
                'src.build.helpers.concat_svgs',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_sorted_icons_list_os_error(self, concat_svgs, caplog):
        caplog.clear()
        with patch('os.listdir', side_effect=OSError):
            concat_svgs.sorted_icons_list(DIR_DATA, DIR_ORIGIN)
        assert caplog.record_tuples == [
            (
                'src.build.helpers.concat_svgs',
                40,
                "[Errno 13] Permission denied: 'tests/mocks'",
            )
        ]

    def test_max_icons_per_file(self, concat_svgs):
        result = concat_svgs.max_icons_per_file(92, 8, 2000)

        assert result == 168

    def test_write_concat_svgs(self, tmp_path, concat_svgs, mock_icon_data):
        patch(
            'src.build.concat_svg.ConcatSVG.sorted_icons_list',
            return_value=[('test_icon', str(mock_icon_data[0]), 'test_icon.svg')],
        )

        output_svg = 'tests/mocks/output.svg'
        concat_svgs.write_concat_svgs(
            str(mock_icon_data[0].parent),
            str(mock_icon_data[0].parent),
            str(output_svg),
        )

        assert os.path.exists(output_svg)
        tree = ElementTree.parse(output_svg)
        root = tree.getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg'

    @pytest.fixture
    def mock_directory(self):
        mock_dir = os.path.join(os.path.dirname(__file__), 'mocks')
        if not os.path.exists(mock_dir):
            os.makedirs(mock_dir)
        yield mock_dir

        for file in os.listdir(mock_dir):
            file_path = os.path.join(mock_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_write_concat_svgs_all_icons(self, concat_svgs, mock_directory):
        with patch.object(
            concat_svgs, 'sorted_icons_list', return_value=['icon1', 'icon2', 'icon3']
        ) as mock_sorted_icons_list:
            with patch.object(
                concat_svgs,
                'create_icon_sticker',
                return_value=ElementTree.Element('icon'),
            ) as mock_create_icon_sticker:
                dir_icon_data = '/path/test/dir_icon_data'
                dir_origin = '/path/test/dir_origin'
                concat_svgfile = os.path.join(mock_directory, 'concat_svgfile.svg')
                prefer_icon = 'dark'
                is_sample = False
                sample_no = 30

                concat_svgs.write_concat_svgs(
                    dir_icon_data,
                    dir_origin,
                    concat_svgfile,
                    is_sample,
                    sample_no,
                    prefer_icon=prefer_icon,
                )

                mock_sorted_icons_list.assert_called_once_with(
                    dir_icon_data, dir_origin, prefer_icon
                )
                mock_create_icon_sticker.assert_called()
                assert isinstance(
                    mock_create_icon_sticker.return_value, ElementTree.Element
                )
                assert os.path.exists(concat_svgfile), (
                    f'File was not created at {concat_svgfile}'
                )

    def test_write_concat_svgs_sample_icons(self, concat_svgs, mock_directory):
        with patch.object(
            concat_svgs,
            'sorted_icons_list',
            return_value=['icon1', 'icon2', 'icon3', 'icon4', 'icon5'],
        ) as mock_sorted_icons_list, patch(
            'random.sample', return_value=['icon1', 'icon2', 'icon3']
        ) as mock_random_sample, patch.object(
            concat_svgs, 'create_icon_sticker', return_value=ElementTree.Element('icon')
        ) as mock_create_icon_sticker:
            dir_icon_data = '/path/test/dir_icon_data'
            dir_origin = '/path/test/dir_origin'
            concat_svgfile = os.path.join(mock_directory, 'concat_svgfile.svg')
            prefer_icon = 'dark'
            is_sample = True
            sample_no = 3

            concat_svgs.write_concat_svgs(
                dir_icon_data,
                dir_origin,
                concat_svgfile,
                is_sample,
                sample_no,
                prefer_icon=prefer_icon,
            )

            mock_sorted_icons_list.assert_called_once_with(
                dir_icon_data, dir_origin, prefer_icon
            )
            mock_random_sample.assert_called_once_with(
                ['icon1', 'icon2', 'icon3', 'icon4', 'icon5'], sample_no
            )
            mock_create_icon_sticker.assert_called()
            assert isinstance(
                mock_create_icon_sticker.return_value, ElementTree.Element
            )
            assert os.path.exists(concat_svgfile), (
                f'File was not created at {concat_svgfile}'
            )


class TestConcatSVG(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('tests/file-icons-concat.svg')

        cls.concat_svgs = ConcatSVG()

    def test_file_exist(self):
        self.concat_svgs.write_concat_svgs(
            'tests', 'tests', 'tests/file-icons-concat.svg'
        )
        self.assertTrue(os.path.exists('tests/file-icons-concat.svg'))

    # def test_params_write_concat_svgs(self):
    #     self.concat_svgs.write_concat_svgs('tests', 'tests', 'tests/file-icons-concat.svg')
    #     self.assertTrue(isinstance('tests', str))
    #     self.assertTrue(isinstance('tests/file-icons-concat.svg', str))
