import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.create_test_icon_theme import TestIconTheme
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DESTINY,
    DS_STORE_MOCKS_PATH,
    TEST_DATA_DIR,
)
from unittest.mock import patch


class TestCreateIconTheme:
    @pytest.mark.parametrize('a, b, expected', [(DIR_DATA, DIR_DESTINY, TEST_DATA_DIR)])
    def test_create_test_icon_theme(self, a, b, expected):
        # Delete '.DS_Store' file that get created when running tests
        if '.DS_Store' in os.listdir(DIR_DESTINY):
            os.remove(DS_STORE_MOCKS_PATH)

        result = TestIconTheme.create_icons_files(a, b)
        assert result == TEST_DATA_DIR

    @pytest.fixture(autouse=True)
    def test_create_icons_files_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.create_test_icon_theme.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            TestIconTheme.create_icons_files(
                'tests/mocks/not_found_yaml.yaml', DIR_DESTINY
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.create_test_icon_theme',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_create_icons_files_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.create_test_icon_theme.open') as mock_open:
            mock_open.side_effect = OSError
            TestIconTheme.create_icons_files('tests/mocks/yaml.yaml', DIR_DESTINY)
        assert caplog.record_tuples == [
            (
                'src.build.helpers.create_test_icon_theme',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]


class TestCreateIconThemeFile(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml')
        cls.fake_fs().create_file('data/afphoto.yaml')
        cls.fake_fs().create_file('data/afpub.yaml')
        cls.fake_fs().create_file('data/ai.yaml')
        cls.fake_fs().create_file('data/angular.yaml')

    def test_create_icon_file_exist(self):
        TestIconTheme.create_icon_file('data/afdesign.yaml', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/afdesign.yaml'))

    def test_create_icons_files_exist(self):
        TestIconTheme.create_icons_files('data', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/afdesign.yaml'))

    def test_params_create_icon_file(self):
        TestIconTheme.create_icon_file('data/afdesign.yaml', DIR_DESTINY)
        self.assertTrue(isinstance('data/afdesign.yaml', str))
        self.assertFalse(isinstance('data/afdesign.yaml', int))
        self.assertFalse(isinstance('data/afdesign.yaml', list))
        self.assertFalse(isinstance('data/afdesign.yaml', bool))
        self.assertFalse(isinstance('data/afdesign.yaml', dict))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertFalse(isinstance(DIR_DESTINY, dict))

    def test_params_create_icons_files(self):
        TestIconTheme.create_icons_files('data/', DIR_DESTINY)
        self.assertTrue(isinstance('data/', str))
        self.assertFalse(isinstance('data/', int))
        self.assertFalse(isinstance('data/', list))
        self.assertFalse(isinstance('data/', bool))
        self.assertFalse(isinstance('data/', dict))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertFalse(isinstance(DIR_DESTINY, dict))
