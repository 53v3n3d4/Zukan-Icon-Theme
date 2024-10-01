import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.icons import IconPNG
from tests.mocks.constants_icons import (
    TEST_STDOUT_PNG,
)
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DATA_NOT_FOUND,
    DIR_DESTINY,
    DIR_DESTINY_PRIMARY_ICONS,
    DIR_ORIGIN,
    # TEST_DATA_DIR,
    # TEST_DATA_DIR_EMPTY_YAML_FILE,
)
from unittest.mock import patch


class TestPNG:
    @pytest.fixture(autouse=True)
    def test_generate_PNGs(self, capfd):
        IconPNG.svg_to_png(
            'tests/mocks/yaml.yaml', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )

        out, err = capfd.readouterr()
        assert (
            out
            == '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest.png\x1b[0m done.\n'
            '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@2x.png\x1b[0m done.\n'
            '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@3x.png\x1b[0m done.\n'
        )

    @pytest.fixture(autouse=True)
    def test_generate_all_PNGs(self, capfd):
        IconPNG.svg_to_png_all(
            DIR_DATA, DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )

        out, err = capfd.readouterr()
        assert out == TEST_STDOUT_PNG

    @pytest.fixture(autouse=True)
    def test_png_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            IconPNG.svg_to_png(
                'tests/mocks/not_found_yaml.yaml',
                DIR_ORIGIN,
                DIR_DESTINY,
                DIR_DESTINY_PRIMARY_ICONS,
            )
        assert caplog.record_tuples == [
            (
                'src.build.icons',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_png_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = OSError
            IconPNG.svg_to_png(
                'tests/mocks/not_found_yaml.yaml',
                DIR_ORIGIN,
                DIR_DESTINY,
                DIR_DESTINY_PRIMARY_ICONS,
            )
        assert caplog.record_tuples == [
            (
                'src.build.icons',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_png_all_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            IconPNG.svg_to_png_all(
                DIR_DATA_NOT_FOUND,
                DIR_ORIGIN,
                DIR_DESTINY,
                DIR_DESTINY_PRIMARY_ICONS,
            )
        assert caplog.record_tuples == [
            (
                'src.build.icons',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/icons_not_found/'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_png_all_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = OSError
            IconPNG.svg_to_png_all(
                DIR_DATA,
                DIR_ORIGIN,
                DIR_DESTINY,
                DIR_DESTINY_PRIMARY_ICONS,
            )
        assert caplog.record_tuples == [
            (
                'src.build.icons',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]


class TestIconPNG(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/file_type_afdesign.svg')
        cls.fake_fs().create_file('data/file_type_afphoto.svg')
        cls.fake_fs().create_file('data/file_type_afpub.svg')
        cls.fake_fs().create_file('data/file_type_ai.svg')
        cls.fake_fs().create_file('data/file_type_angular.svg')

    def test_file_exist(self):
        IconPNG.svg_to_png(
            'data/file_type_ai.svg', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )
        self.assertTrue(os.path.exists('data/file_type_ai.svg'))

    def test_file_not_found(self):
        IconPNG.svg_to_png(
            'tests/file_type_babel.svg',
            DIR_ORIGIN,
            DIR_DESTINY,
            DIR_DESTINY_PRIMARY_ICONS,
        )
        self.assertFalse(os.path.exists('tests/file_type_babel.svg'))

    def test_params_svg_png(self):
        IconPNG.svg_to_png(
            'data/file_type_ai.svg', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )
        self.assertTrue(isinstance('data/file_type_ai.svg', str))
        self.assertFalse(isinstance('data/file_type_ai.svg', int))
        self.assertFalse(isinstance('data/file_type_ai.svg', list))
        self.assertFalse(isinstance('data/file_type_ai.svg', bool))
        self.assertFalse(isinstance('data/file_type_ai.svg', set))
        self.assertFalse(isinstance('data/file_type_ai.svg', tuple))
        self.assertTrue(isinstance(DIR_ORIGIN, str))
        self.assertFalse(isinstance(DIR_ORIGIN, int))
        self.assertFalse(isinstance(DIR_ORIGIN, list))
        self.assertFalse(isinstance(DIR_ORIGIN, bool))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertTrue(isinstance(DIR_DESTINY_PRIMARY_ICONS, str))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, int))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, list))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, bool))

    def test_svg_png_all(self):
        IconPNG.svg_to_png_all(
            'data/', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )
        self.assertTrue(os.path.exists('data/file_type_ai.svg'))

    def test_params_svg_png_all(self):
        IconPNG.svg_to_png_all(
            'data/', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )
        self.assertTrue(os.path.exists('data/'))
        self.assertTrue(isinstance('data/', str))
        self.assertFalse(isinstance('data/', int))
        self.assertFalse(isinstance('data/', list))
        self.assertFalse(isinstance('data/', bool))
        self.assertTrue(isinstance(DIR_ORIGIN, str))
        self.assertFalse(isinstance(DIR_ORIGIN, int))
        self.assertFalse(isinstance(DIR_ORIGIN, list))
        self.assertFalse(isinstance(DIR_ORIGIN, bool))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertTrue(isinstance(DIR_DESTINY_PRIMARY_ICONS, str))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, int))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, list))
        self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, bool))
