import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.create_test_icon_theme import TestIconTheme
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DESTINY,
    OS_FILE_MOCKS_PATH,
    TEST_DATA_DIR,
)
from unittest.mock import patch

test_icon_theme = TestIconTheme()


class TestCreateIconTheme:
    @pytest.mark.parametrize('a, b, expected', [(DIR_DATA, DIR_DESTINY, TEST_DATA_DIR)])
    def test_create_test_icon_theme(self, a, b, expected):
        data_dir_list = test_icon_theme.create_icons_files(a, b)

        # Delete '.DS_Store' and 'Thumbs.db'file that get created when
        # running tests
        result = [i for i in data_dir_list if i not in OS_FILE_MOCKS_PATH]

        assert result == TEST_DATA_DIR

    @pytest.fixture(autouse=True)
    def test_create_icons_files_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.create_test_icon_theme.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            test_icon_theme.create_icons_files(
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
            test_icon_theme.create_icons_files('tests/mocks/yaml.yaml', DIR_DESTINY)
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
        test_icon_theme.create_icon_file('data/afdesign.yaml', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/afdesign.yaml'))

    # def test_create_icons_files_exist(self):
    #     test_icon_theme.create_icons_files('data', DIR_DESTINY)
    #     self.assertTrue(os.path.exists('data/afdesign.yaml'))

#     def test_params_create_icon_file(self):
#         test_icon_theme.create_icon_file('data/afdesign.yaml', DIR_DESTINY)
#         self.assertTrue(isinstance('data/afdesign.yaml', str))
#         self.assertFalse(isinstance('data/afdesign.yaml', int))
#         self.assertFalse(isinstance('data/afdesign.yaml', list))
#         self.assertFalse(isinstance('data/afdesign.yaml', bool))
#         self.assertFalse(isinstance('data/afdesign.yaml', dict))
#         self.assertTrue(isinstance(DIR_DESTINY, str))
#         self.assertFalse(isinstance(DIR_DESTINY, int))
#         self.assertFalse(isinstance(DIR_DESTINY, list))
#         self.assertFalse(isinstance(DIR_DESTINY, bool))
#         self.assertFalse(isinstance(DIR_DESTINY, dict))

#     def test_params_create_icons_files(self):
#         test_icon_theme.create_icons_files('data/', DIR_DESTINY)
#         self.assertTrue(isinstance('data/', str))
#         self.assertFalse(isinstance('data/', int))
#         self.assertFalse(isinstance('data/', list))
#         self.assertFalse(isinstance('data/', bool))
#         self.assertFalse(isinstance('data/', dict))
#         self.assertTrue(isinstance(DIR_DESTINY, str))
#         self.assertFalse(isinstance(DIR_DESTINY, int))
#         self.assertFalse(isinstance(DIR_DESTINY, list))
#         self.assertFalse(isinstance(DIR_DESTINY, bool))
#         self.assertFalse(isinstance(DIR_DESTINY, dict))
