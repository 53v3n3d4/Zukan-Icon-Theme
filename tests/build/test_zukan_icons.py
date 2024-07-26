import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.zukan_icons import ZukanIcon
from tests.mocks.constants_pickle import (
    TEST_PICKLE_ZUKAN_FILE,
)
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DESTINY,
    TEST_DATA_DIR_EXCEPT_ZUKAN_FILE,
)
from unittest.mock import patch


class TestZukanIcon:
    @pytest.mark.parametrize(
        'a, b, c, expected',
        [
            (
                DIR_DATA,
                DIR_DESTINY,
                TEST_PICKLE_ZUKAN_FILE,
                TEST_DATA_DIR_EXCEPT_ZUKAN_FILE,
            )
        ],
    )
    def test_write_icon_data(self, a, b, c, expected):
        result = ZukanIcon.write_icon_data(a, b, c)
        assert result == TEST_DATA_DIR_EXCEPT_ZUKAN_FILE

    @pytest.fixture(autouse=True)
    def test_write_icon_data_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.zukan_icons.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            ZukanIcon.write_icon_data(
                'tests/mocks/not_found_yaml.yaml',
                DIR_DESTINY,
                TEST_PICKLE_ZUKAN_FILE,
            )
        assert caplog.record_tuples == [
            (
                'src.build.zukan_icons',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_icon_data_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.zukan_icons.open') as mock_open:
            mock_open.side_effect = OSError
            ZukanIcon.write_icon_data(
                'tests/mocks/yaml.yaml', DIR_DESTINY, TEST_PICKLE_ZUKAN_FILE
            )
        assert caplog.record_tuples == [
            (
                'src.build.zukan_icons',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]


class TestIconZukanIcon(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml')
        cls.fake_fs().create_file('data/afphoto.yaml')
        cls.fake_fs().create_file('data/afpub.yaml')
        cls.fake_fs().create_file('data/ai.yaml')
        cls.fake_fs().create_file('data/angular.yaml')

    def test_dir_exist(self):
        ZukanIcon.write_icon_data('data', DIR_DESTINY, TEST_PICKLE_ZUKAN_FILE)
        self.assertTrue(os.path.exists('data'))

    def test_params_write_icon_data(self):
        ZukanIcon.write_icon_data('data', DIR_DESTINY, TEST_PICKLE_ZUKAN_FILE)
        self.assertTrue(isinstance('data', str))
        self.assertFalse(isinstance('data', int))
        self.assertFalse(isinstance('data', list))
        self.assertFalse(isinstance('data', bool))
        self.assertFalse(isinstance('data', dict))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertFalse(isinstance(DIR_DESTINY, dict))
        self.assertTrue(isinstance(TEST_PICKLE_ZUKAN_FILE, str))
        self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, int))
        self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, list))
        self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, bool))
        self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, dict))
