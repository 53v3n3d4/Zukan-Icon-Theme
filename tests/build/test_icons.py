import errno
import logging
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
)
from unittest.mock import call, patch


class TestPNG:
    @pytest.fixture
    def icon_png(self):
        return IconPNG()

    @pytest.fixture(autouse=True)
    def test_generate_PNGs(self, icon_png, capfd):
        icon_png.svg_to_png(
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
    def test_generate_all_PNGs(self, icon_png, capfd):
        icon_png.svg_to_png_all(
            DIR_DATA, DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )

        out, err = capfd.readouterr()
        assert out == TEST_STDOUT_PNG

    @pytest.fixture(autouse=True)
    def test_png_file_not_found(self, icon_png, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            icon_png.svg_to_png(
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
    def test_png_os_error(self, icon_png, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = OSError
            icon_png.svg_to_png(
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
    def test_png_all_file_not_found(self, icon_png, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            icon_png.svg_to_png_all(
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
    def test_png_all_os_error(self, icon_png, caplog):
        caplog.clear()
        with patch('src.build.icons.open') as mock_open:
            mock_open.side_effect = OSError
            icon_png.svg_to_png_all(
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

        cls.icon_png = IconPNG()

    def test_file_exist(self):
        self.icon_png.svg_to_png(
            'data/file_type_ai.svg', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
        )
        self.assertTrue(os.path.exists('data/file_type_ai.svg'))


#     def test_file_not_found(self):
#         zukan_icon_png.svg_to_png(
#             'tests/file_type_babel.svg',
#             DIR_ORIGIN,
#             DIR_DESTINY,
#             DIR_DESTINY_PRIMARY_ICONS,
#         )
#         self.assertFalse(os.path.exists('tests/file_type_babel.svg'))

#     def test_params_svg_png(self):
#         icon_png.svg_to_png(
#             'data/file_type_ai.svg', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
#         )
#         self.assertTrue(isinstance('data/file_type_ai.svg', str))
#         self.assertFalse(isinstance('data/file_type_ai.svg', int))
#         self.assertFalse(isinstance('data/file_type_ai.svg', list))
#         self.assertFalse(isinstance('data/file_type_ai.svg', bool))
#         self.assertFalse(isinstance('data/file_type_ai.svg', set))
#         self.assertFalse(isinstance('data/file_type_ai.svg', tuple))
#         self.assertTrue(isinstance(DIR_ORIGIN, str))
#         self.assertFalse(isinstance(DIR_ORIGIN, int))
#         self.assertFalse(isinstance(DIR_ORIGIN, list))
#         self.assertFalse(isinstance(DIR_ORIGIN, bool))
#         self.assertTrue(isinstance(DIR_DESTINY, str))
#         self.assertFalse(isinstance(DIR_DESTINY, int))
#         self.assertFalse(isinstance(DIR_DESTINY, list))
#         self.assertFalse(isinstance(DIR_DESTINY, bool))
#         self.assertTrue(isinstance(DIR_DESTINY_PRIMARY_ICONS, str))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, int))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, list))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, bool))

#     def test_svg_png_all(self):
#         icon_png.svg_to_png_all(
#             'data/', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
#         )
#         self.assertTrue(os.path.exists('data/file_type_ai.svg'))

#     def test_params_svg_png_all(self):
#         icon_png.svg_to_png_all(
#             'data/', DIR_ORIGIN, DIR_DESTINY, DIR_DESTINY_PRIMARY_ICONS
#         )
#         self.assertTrue(os.path.exists('data/'))
#         self.assertTrue(isinstance('data/', str))
#         self.assertFalse(isinstance('data/', int))
#         self.assertFalse(isinstance('data/', list))
#         self.assertFalse(isinstance('data/', bool))
#         self.assertTrue(isinstance(DIR_ORIGIN, str))
#         self.assertFalse(isinstance(DIR_ORIGIN, int))
#         self.assertFalse(isinstance(DIR_ORIGIN, list))
#         self.assertFalse(isinstance(DIR_ORIGIN, bool))
#         self.assertTrue(isinstance(DIR_DESTINY, str))
#         self.assertFalse(isinstance(DIR_DESTINY, int))
#         self.assertFalse(isinstance(DIR_DESTINY, list))
#         self.assertFalse(isinstance(DIR_DESTINY, bool))
#         self.assertTrue(isinstance(DIR_DESTINY_PRIMARY_ICONS, str))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, int))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, list))
#         self.assertFalse(isinstance(DIR_DESTINY_PRIMARY_ICONS, bool))


class TestSVGtoPNG:
    @pytest.fixture
    def icon_png(self):
        return IconPNG()

    @pytest.fixture
    def sample_yaml(self):
        return {
            'name': 'Ada',
            'preferences': {'settings': {'icon': 'ada-dark'}},
        }

    @pytest.fixture
    def sample_yaml_primary_icon(self):
        return {
            'name': 'Image',
            'preferences': {'settings': {'icon': 'file_type_image-dark'}},
            'icons': ['file_type_image-light', 'file_type_image-1'],
        }

    def test_svg_to_png(self, icon_png, sample_yaml):
        with patch('src.build.icons.read_yaml_data') as mock_read_yaml:
            with patch.object(icon_png, 'generate_png') as mock_generate:
                mock_read_yaml.return_value = sample_yaml

                result = icon_png.svg_to_png(
                    'afdesign.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                )

                assert result == sample_yaml
                mock_generate.assert_called_once_with(
                    'Ada', 'ada-dark', 'afdesign.yaml', 'origin/dir', 'dest/dir'
                )

    def test_svg_to_png_primary_icon(self, icon_png, sample_yaml_primary_icon):
        with patch('src.build.icons.read_yaml_data') as mock_read_yaml:
            with patch.object(icon_png, 'generate_png') as mock_generate:
                with patch('src.build.icons.PRIMARY_ICONS', ['Image']):
                    mock_read_yaml.return_value = sample_yaml_primary_icon

                    result = icon_png.svg_to_png(
                        'file_type_image.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                    )

                    assert result == sample_yaml_primary_icon
                    assert mock_generate.call_count == 4

                    mock_generate.assert_has_calls(
                        [
                            call(
                                'Image',
                                'file_type_image-dark',
                                'file_type_image.yaml',
                                'origin/dir',
                                'dest/dir',
                            ),
                            call(
                                'Image',
                                'file_type_image-dark',
                                'file_type_image.yaml',
                                'origin/dir',
                                'primary/dir',
                            ),
                            call(
                                'Image',
                                'file_type_image-light',
                                'file_type_image.yaml',
                                'origin/dir',
                                'primary/dir',
                            ),
                            call(
                                'Image',
                                'file_type_image-1',
                                'file_type_image.yaml',
                                'origin/dir',
                                'primary/dir',
                            ),
                        ],
                        any_order=True,
                    )

    def test_svg_to_png_missing_icon(self, icon_png):
        invalid_data = {'preferences': {'settings': {}}}

        with patch('src.build.icons.read_yaml_data') as mock_read_yaml:
            with patch('src.build.icons.print_message') as mock_print:
                mock_read_yaml.return_value = invalid_data

                result = icon_png.svg_to_png(
                    'invalid.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                )

                mock_print.assert_called_once()
                assert result == invalid_data

    def test_svg_to_png_file_not_found(self, icon_png):
        with patch('src.build.icons.read_yaml_data') as mock_read:
            with patch('src.build.icons.logger.error') as mock_logger:
                mock_read.side_effect = FileNotFoundError()

                icon_png.svg_to_png(
                    'not_found.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                )

                mock_logger.assert_called_once()

    def test_svg_to_png_os_error(self, icon_png):
        with patch('src.build.icons.read_yaml_data') as mock_read:
            with patch('src.build.icons.logger.error') as mock_logger:
                mock_read.side_effect = OSError()

                icon_png.svg_to_png(
                    'os_error.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                )

                mock_logger.assert_called_once()

    def test_svg_to_png_not_yaml_file(self, icon_png):
        result = icon_png.svg_to_png(
            'afdesign.toml', 'origin/dir', 'dest/dir', 'primary/dir'
        )

        assert result == 'afdesign.toml'

    def test_svg_to_png_with_icon_options(self, icon_png):
        data_with_variants = {
            'name': 'Ada',
            'preferences': {'settings': {'icon': 'ada-dark'}},
            'icons': ['ada-light', 'ada1'],
        }

        with patch('src.build.icons.read_yaml_data') as mock_read_yaml:
            with patch.object(icon_png, 'generate_png') as mock_generate:
                mock_read_yaml.return_value = data_with_variants

                result = icon_png.svg_to_png(
                    'test.yaml', 'origin/dir', 'dest/dir', 'primary/dir'
                )

                assert result == data_with_variants
                assert mock_generate.call_count == 3


class TestSVGToPNGALL:
    @pytest.fixture
    def icon_png(self):
        return IconPNG()

    @pytest.fixture
    def mock_dirs(self):
        return {
            'data': '/path/test/icon/data',
            'origin': '/path/test/svgs',
            'destiny': '/path/test/pngs',
            'primary': '/path/test/primary/pngs',
        }

    def test_svg_to_png_all(self, icon_png, mock_dirs):
        mock_files = ['icon1.yaml', 'icon2.yaml', 'icon3.yaml']

        with patch('os.listdir', return_value=mock_files), patch.object(
            icon_png, 'svg_to_png'
        ) as mock_svg_to_png:
            result = icon_png.svg_to_png_all(
                mock_dirs['data'],
                mock_dirs['origin'],
                mock_dirs['destiny'],
                mock_dirs['primary'],
            )

            assert result == mock_files

            expected_calls = [
                call(
                    os.path.join(mock_dirs['data'], file),
                    mock_dirs['origin'],
                    mock_dirs['destiny'],
                    mock_dirs['primary'],
                )
                for file in mock_files
            ]
            assert mock_svg_to_png.call_count == len(mock_files)
            mock_svg_to_png.assert_has_calls(expected_calls, any_order=False)

    def test_svg_to_png_all_directory_not_found(self, icon_png, mock_dirs, caplog):
        with patch('os.listdir', side_effect=FileNotFoundError()), patch(
            'logging.getLogger', return_value=logging.getLogger()
        ):
            result = icon_png.svg_to_png_all(
                mock_dirs['data'],
                mock_dirs['origin'],
                mock_dirs['destiny'],
                mock_dirs['primary'],
            )

            assert result is None

            assert (
                f'[Errno {errno.ENOENT}] {os.strerror(errno.ENOENT)}: {mock_dirs["data"]!r}'
                in caplog.text
            )

    def test_svg_to_png_all_os_error(self, icon_png, mock_dirs, caplog):
        with patch(
            'os.listdir', side_effect=OSError(errno.EACCES, 'Permission denied')
        ), patch('logging.getLogger', return_value=logging.getLogger()):
            result = icon_png.svg_to_png_all(
                mock_dirs['data'],
                mock_dirs['origin'],
                mock_dirs['destiny'],
                mock_dirs['primary'],
            )

            assert result is None

            assert (
                f'[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: {mock_dirs["data"]!r}'
                in caplog.text
            )

    def test_svg_to_png_all_empty_directory(self, icon_png, mock_dirs):
        with patch('os.listdir', return_value=[]):
            result = icon_png.svg_to_png_all(
                mock_dirs['data'],
                mock_dirs['origin'],
                mock_dirs['destiny'],
                mock_dirs['primary'],
            )

            assert result == []

    @pytest.mark.parametrize(
        'dirs',
        [
            {
                'data': '',
                'origin': '/path/test',
                'destiny': '/path/test',
                'primary': '/path/test',
            },
            {
                'data': '/path/test',
                'origin': '',
                'destiny': '/path/test',
                'primary': '/path/test',
            },
            {
                'data': '/path/test',
                'origin': '/path/test',
                'destiny': '',
                'primary': '/path/test',
            },
            {
                'data': '/path/test',
                'origin': '/path/test',
                'destiny': '/path/test',
                'primary': '',
            },
        ],
    )
    def test_svg_to_png_all_invalid_directory(self, icon_png, dirs):
        with patch('os.listdir', return_value=['file.toml']):
            result = icon_png.svg_to_png_all(
                dirs['data'], dirs['origin'], dirs['destiny'], dirs['primary']
            )

            assert result == ['file.toml']
