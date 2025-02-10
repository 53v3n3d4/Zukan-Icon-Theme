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
    OS_FILE_MOCKS_PATH,
    TEST_DATA_DIR_EXCEPT_ZUKAN_FILE,
)
from unittest.mock import MagicMock, patch


class TestZukanIconParams:
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
        data_dir_list = ZukanIcon.write_icon_data(a, b, c)

        # Delete '.DS_Store' and 'Thumbs.db'file that get created when
        # running tests
        result = [i for i in data_dir_list if i not in OS_FILE_MOCKS_PATH]

        assert sorted(result) == sorted(TEST_DATA_DIR_EXCEPT_ZUKAN_FILE)


class TestZukanIcon:
    # Ensure os.remove is patched globally for this class scope
    @pytest.fixture(autouse=True)
    def mock_os(self):
        with patch('os.path.exists', return_value=False), patch(
            'os.makedirs'
        ) as mock_makedirs, patch('os.remove') as mock_remove, patch(
            'builtins.open', MagicMock()
        ):
            yield mock_makedirs, mock_remove

    # Fixture to handle FileNotFoundError
    @pytest.fixture(autouse=True)
    def test_write_icon_data_file_not_found(self, caplog):
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

    # Fixture to handle OSError
    @pytest.fixture(autouse=True)
    def test_write_icon_data_os_error(self, caplog):
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

    # If put below and same class with parametrize tests, `zukan_icon_data.pkl` in
    # `tests/mocks` get deleted when run tests.
    def test_make_directory(self, mock_os):
        mock_makedirs, mock_remove = mock_os

        # Call the method to test
        ZukanIcon.make_directory('mock_dir')

        # Assertions to verify the correct behavior
        assert mock_makedirs.call_count == 1
        mock_makedirs.assert_any_call('mock_dir')

        # Ensure os.remove was never called
        mock_remove.assert_not_called()


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


#     def test_params_write_icon_data(self):
#         ZukanIcon.write_icon_data('data', DIR_DESTINY, TEST_PICKLE_ZUKAN_FILE)
#         self.assertTrue(isinstance('data', str))
#         self.assertFalse(isinstance('data', int))
#         self.assertFalse(isinstance('data', list))
#         self.assertFalse(isinstance('data', bool))
#         self.assertFalse(isinstance('data', dict))
#         self.assertTrue(isinstance(DIR_DESTINY, str))
#         self.assertFalse(isinstance(DIR_DESTINY, int))
#         self.assertFalse(isinstance(DIR_DESTINY, list))
#         self.assertFalse(isinstance(DIR_DESTINY, bool))
#         self.assertFalse(isinstance(DIR_DESTINY, dict))
#         self.assertTrue(isinstance(TEST_PICKLE_ZUKAN_FILE, str))
#         self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, int))
#         self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, list))
#         self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, bool))
#         self.assertFalse(isinstance(TEST_PICKLE_ZUKAN_FILE, dict))
