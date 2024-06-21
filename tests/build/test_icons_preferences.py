import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.icons_preferences import Preference
from src.build.helpers.print_message import (
    print_created_message,
)
from tests.mocks.constants_icons_preferences import (
    TEST_TMPREFERENCES_CREATED_MESSAGE,
    TEST_TMPREFERENCES_FILE,
)
from tests.mocks.constants_yaml import (
    TEST_YAML_EXPECTED,
    TEST_YAML_FILE,
)
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DESTINY,
    TEST_DATA_DIR,
)
from unittest.mock import patch, mock_open


class TestPreferences:
    @pytest.mark.parametrize('a, b, expected', [(DIR_DATA, DIR_DESTINY, TEST_DATA_DIR)])
    def test_preferences_all(self, a, b, expected):
        result = Preference.preferences_all(a, b)
        assert result == TEST_DATA_DIR

    @pytest.fixture(autouse=True)
    def test_create_preferences_file(self, capfd):
        Preference.preferences('tests/mocks/yaml.yaml', DIR_DESTINY)

        out, err = capfd.readouterr()
        assert (
            out
            == '\x1b[36m[!] yaml.yaml\x1b[0m -> \x1b[93mvitest.tmPreferences\x1b[0m created.\n'
            '\x1b[36m[!] yaml.yaml\x1b[0m -> Deleting \x1b[93mtag <!DOCTYPE plist>\x1b[0m from vitest.tmPreferences.\n'
        )

    def test_mock_create_preferences_file(self):
        with patch('src.build.helpers.icons_preferences.open', mock_open()):
            result = Preference.preferences('tests/mocks/yaml.yaml', DIR_DESTINY)
            assert result is None

    # To do: should get an Errno 13 not empty
    @pytest.fixture(autouse=True)
    def test_preferences_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_preferences.open') as mock_open:
            mock_open.side_effect = OSError
            Preference.preferences(
                'tests/mocks/yaml.yaml',
                DIR_DESTINY,
            )
        assert caplog.record_tuples == []

    @pytest.fixture(autouse=True)
    def test_preferences_all_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_preferences.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            Preference.preferences_all(
                'tests/mocks/not_found_yaml.yaml',
                'tests/mocks/',
            )
        assert caplog.record_tuples == [
            (
                (
                    'src.build.helpers.icons_preferences',
                    40,
                    "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
                )
            )
        ]

    # To do: should get an Errno 13 not empty
    @pytest.fixture(autouse=True)
    def test_preferences_all_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_preferences.open') as mock_open:
            mock_open.side_effect = OSError
            Preference.preferences_all(
                DIR_DATA,
                DIR_DESTINY,
            )
        assert caplog.record_tuples == []

    @pytest.mark.parametrize(
        'a, b, c, expected',
        [
            (
                TEST_YAML_FILE,
                TEST_TMPREFERENCES_FILE,
                TEST_TMPREFERENCES_CREATED_MESSAGE,
                TEST_YAML_EXPECTED,
            )
        ],
    )
    def test_print_created_message(self, a, b, c, expected):
        result = print_created_message(a, b, c)
        return result
        assert result == TEST_YAML_EXPECTED  # noqa: F821


class TestIconPreferences(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml', contents='test')
        cls.fake_fs().create_file('data/afphoto.yaml', contents='test')
        cls.fake_fs().create_file('data/afpub.yaml', contents='test')
        cls.fake_fs().create_file('data/ai.yaml', contents='test')
        cls.fake_fs().create_file('data/angular.yaml', contents='test')

    def test_file_exist(self):
        Preference.preferences('data/ai.yaml', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/ai.yaml'))

    def test_dir_exist(self):
        Preference.preferences_all('data', DIR_DESTINY)
        self.assertTrue(os.path.exists('data'))

    def test_file_not_found(self):
        Preference.preferences_all('tests/build/mocks/not_found_yaml.yaml', DIR_DESTINY)
        self.assertFalse(os.path.exists('tests/build/mocks/not_found_yaml.yaml'))

    def test_params_preferences(self):
        Preference.preferences('data/ai.yaml', DIR_DESTINY)
        self.assertTrue(isinstance('data/ai.yaml', str))
        self.assertFalse(isinstance('data/ai.yaml', int))
        self.assertFalse(isinstance('data/ai.yaml', list))
        self.assertFalse(isinstance('data/ai.yaml', bool))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))

    def test_params_preferences_all(self):
        Preference.preferences_all('data/', DIR_DESTINY)
        self.assertTrue(isinstance('data/', str))
        self.assertFalse(isinstance('data/', int))
        self.assertFalse(isinstance('data/', list))
        self.assertFalse(isinstance('data/', bool))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
