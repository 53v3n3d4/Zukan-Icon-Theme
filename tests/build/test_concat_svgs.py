import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.concat_svgs import ConcatSVG
from src.build.utils.file_extensions import SVG_EXTENSION
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_ORIGIN,
)
from unittest import mock
from xml.etree import ElementTree

zukan_concat_svgs = ConcatSVG()


class TestConcatSVGMock:
    @pytest.fixture
    def mock_svg_data(self):
        # Sample mock data for an SVG
        return ElementTree.Element('svg', {'width': '32', 'height': '28.4'})

    @pytest.fixture
    def mock_icon_data(self, tmp_path):
        # Mock icon data and YAML file
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

    def test_create_element_svg(self):
        attributes = {'width': '100', 'height': '100', 'viewbox': '0 0 100 100'}
        svg_element = zukan_concat_svgs.create_element_svg(attributes)

        assert svg_element.tag == 'svg'
        assert svg_element.get('width') == '100'
        assert svg_element.get('height') == '100'
        assert svg_element.get('viewbox') == '0 0 100 100'

    def test_create_rounded_rect(self, mock_svg_data):
        rect = zukan_concat_svgs.create_rounded_rect(mock_svg_data)
        assert rect.tag == 'g'
        assert rect.get('transform') == 'matrix(0.79,0,0,0.77,0,0)'

    def test_write_icon_name(self, mock_svg_data):
        sticker_name = 'Test Icon'
        svgfile_name = 'icon_name.svg'
        text_element = zukan_concat_svgs.write_icon_name(
            mock_svg_data, sticker_name, svgfile_name
        )

        assert text_element.tag == 'g'
        assert len(text_element) == 1

    def test_edit_icon_svg(self, mock_svg_data):
        mock.patch('xml.etree.ElementTree.parse', return_value=mock_svg_data)
        icon_svg = zukan_concat_svgs.edit_icon_svg('tests/mocks/vitest.svg')

        assert icon_svg.get('width') == '32'
        assert icon_svg.get('height') == '28.4'
        assert icon_svg.get('viewbox') == '0 0 32 28.4'
        assert icon_svg.get('x') == '23'
        assert icon_svg.get('y') == '17'

    def test_create_icon_sticker(self):
        sticker_svg = zukan_concat_svgs.create_icon_sticker(
            'tests/mocks/vitest.svg', str(12), str(8), 'Vitest', 'vitest.svg'
        )

        assert sticker_svg.get('width') == '79'
        assert sticker_svg.get('height') == '77'
        assert sticker_svg.get('viewbox') == '0 0 79 77'
        assert sticker_svg.get('x') == '12'
        assert sticker_svg.get('y') == '8'
        assert sticker_svg.tag == 'svg'
        assert len(sticker_svg) == 3

    def test_sorted_icons_list(self):
        icon_name = 'vitest'
        result = zukan_concat_svgs.sorted_icons_list(DIR_DATA, DIR_ORIGIN)

        assert len(result) == 1
        assert (
            'Vitest',
            f'{DIR_DATA}/{icon_name}{SVG_EXTENSION}',
            f'{icon_name}{SVG_EXTENSION}',
        ) in result

    def test_max_icons_per_file(self):
        result = zukan_concat_svgs.max_icons_per_file(92, 8, 2000)

        assert result == 168

    def test_write_concat_svgs(self, tmp_path, mock_icon_data):
        mock.patch(
            'src.build.concat_svg.ConcatSVG.sorted_icons_list',
            return_value=[('test_icon', str(mock_icon_data[0]), 'test_icon.svg')],
        )

        output_svg = 'tests/mocks/output.svg'
        zukan_concat_svgs.write_concat_svgs(
            str(mock_icon_data[0].parent),
            str(mock_icon_data[0].parent),
            str(output_svg),
        )

        assert os.path.exists(output_svg)
        tree = ElementTree.parse(output_svg)
        root = tree.getroot()
        assert (
            root.tag == '{http://www.w3.org/2000/svg}svg'
        )  # Check if the root is an SVG element


# class TestConcatSVG(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.setUpClassPyfakefs()
#         cls.fake_fs().create_file('tests/file-icons-concat.svg')

#     def test_file_exist(self):
#         ConcatSVG.write_concat_svgs('tests', 'tests', 'tests/file-icons-concat.svg')
#         self.assertTrue(os.path.exists('tests/file-icons-concat.svg'))

#     def test_params_write_concat_svgs(self):
#         ConcatSVG.write_concat_svgs('tests', 'tests', 'tests/file-icons-concat.svg')
#         self.assertTrue(isinstance('tests', str))
#         self.assertTrue(isinstance('tests/file-icons-concat.svg', str))
