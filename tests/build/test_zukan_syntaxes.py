import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.zukan_syntaxes import ZukanSyntax
from tests.build.mocks.tests_paths import (
    DIR_DATA,
    TEST_DATA_DIR,
)
from unittest.mock import patch


class TestZukanSyntax:
    @pytest.mark.parametrize('a, expected', [(DIR_DATA, TEST_DATA_DIR)])
    def test_write_zukan_data(self, a, expected):
        result = ZukanSyntax.write_zukan_data(a)
        assert result == TEST_DATA_DIR

    @pytest.fixture(autouse=True)
    def test_write_zukan_data_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.zukan_syntaxes.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            ZukanSyntax.write_zukan_data('tests/build/mocks/not_found_yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.zukan_syntaxes',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_zukan_data_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.zukan_syntaxes.open') as mock_open:
            mock_open.side_effect = OSError
            ZukanSyntax.write_zukan_data('tests/build/mocks/yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.zukan_syntaxes',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/yaml.yaml'",
            )
        ]


class TestIconZukanSyntax(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml')
        cls.fake_fs().create_file('data/afphoto.yaml')
        cls.fake_fs().create_file('data/afpub.yaml')
        cls.fake_fs().create_file('data/ai.yaml')
        cls.fake_fs().create_file('data/angular.yaml')

    def test_dir_exist(self):
        ZukanSyntax.write_zukan_data('data')
        self.assertTrue(os.path.exists('data'))

    def test_params_write_zukan_data(self):
        ZukanSyntax.write_zukan_data('data')
        self.assertTrue(isinstance('data', str))
        self.assertFalse(isinstance('data', int))
        self.assertFalse(isinstance('data', list))
        self.assertFalse(isinstance('data', bool))
        self.assertFalse(isinstance('data', dict))
