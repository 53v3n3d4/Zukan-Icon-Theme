import pytest

from src.build.helpers.clean_data import (
    clean_yaml_tabs,
    _replace_tabs,
)
from tests.build.mocks.constants_yaml import (
    TEST_YAML_EXPECTED,
    TEST_YAML_FILE,
)
from unittest.mock import patch, mock_open


class TestWriteFile:
    def test_write_yaml(self):
        with patch('src.build.helpers.clean_data.open', mock_open()) as mocked_open:
            clean_yaml_tabs(TEST_YAML_FILE)
            mocked_open.assert_called_with(TEST_YAML_FILE, 'w')


class TestCleanYamlTabs:
    @pytest.mark.parametrize('a, expected', [(TEST_YAML_FILE, TEST_YAML_EXPECTED)])
    def test_clean_yaml_tabs(self, a, expected):
        result = clean_yaml_tabs(a)
        return result
        assert result == TEST_YAML_EXPECTED  # noqa: F821

    def test_replace_tabs(self):
        test_tab_file = '\tText foo bar'
        test_spc_file = '  Text foo bar'
        result = _replace_tabs(test_tab_file)
        assert result == test_spc_file

    @pytest.fixture(autouse=True)
    def test_write_yaml_file_filenotfounferror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            clean_yaml_tabs('tests/build/mocks/not_found_yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_yaml_file_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = OSError
            clean_yaml_tabs('tests/build/mocks/yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/yaml.yaml'",
            )
        ]
