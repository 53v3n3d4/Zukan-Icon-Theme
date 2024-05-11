import pytest

from src.build.helpers.clean_data import (
    clean_plist_tag,
    clean_yaml_tabs,
    _replace_line,
    _replace_tabs,
)
from tests.mocks.constants_plist import (
    TEST_PLIST_EXPECTED,
    TEST_PLIST_FILE,
)
from tests.mocks.constants_yaml import (
    TEST_YAML_EXPECTED,
    TEST_YAML_FILE,
)
from unittest.mock import patch, mock_open


class TestWriteFile:
    def test_mock_write_plist(self):
        with patch('src.build.helpers.clean_data.open', mock_open()) as mocked_open:
            clean_plist_tag(TEST_PLIST_FILE)
            mocked_open.assert_called_with(TEST_PLIST_FILE, 'w')

    def test_write_yaml(self):
        with patch('src.build.helpers.clean_data.open', mock_open()) as mocked_open:
            clean_yaml_tabs(TEST_YAML_FILE)
            mocked_open.assert_called_with(TEST_YAML_FILE, 'w')


class TestCleanPlistTag:
    @pytest.mark.parametrize('a, expected', [(TEST_PLIST_FILE, TEST_PLIST_EXPECTED)])
    def test_clean_plist_tag(self, a, expected):
        result = clean_plist_tag(a)
        return result
        assert result == TEST_PLIST_EXPECTED  # noqa: F821

    def test_replace_line(self):
        test_line = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        test_removed = ''
        result = _replace_line(test_line)
        assert result == test_removed

    def test_replace_line_not_remove(self):
        test_line = 'Text not unused'
        test_removed = ''
        result = _replace_line(test_line)
        assert result != test_removed

    @pytest.fixture(autouse=True)
    def test_write_plist_file_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            clean_plist_tag('tests/mocks/not_found_plist.plist')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_plist.plist'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_plist_file_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = OSError
            clean_plist_tag('tests/mocks/plist.plist')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/plist.plist'",
            )
        ]


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
            clean_yaml_tabs('tests/mocks/not_found_yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_write_yaml_file_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = OSError
            clean_yaml_tabs('tests/mocks/yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.clean_data',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]
