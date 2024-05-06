import pytest
import unittest

from build.helpers.clean_data import (
    clean_plist_tag,
    clean_yaml_tabs,
    _replace_line,
    _replace_tabs,
)
from unittest.mock import patch, mock_open


test_plist_file = 'foo/bar.plist'
test_plist_expected = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>scope</key>
    <string>binary.afdesign</string>
    <key>settings</key>
    <dict>
        <key>icon</key>
        <string>afdesign</string>
    </dict>
</dict>
</plist>
"""
test_yaml_file = 'foo/bar.yaml'
test_yaml_expected = """%YAML 1.2
---
name: Vitest
preferences:
scope: source.js.vitest, source.ts.vitest
settings:
icon: vitest
"""


class TestWriteFile(unittest.TestCase):
    def test_write_plist(self):
        with patch('builtins.open', mock_open()) as mocked_open:
            clean_plist_tag(test_plist_file)
            mocked_open.assert_called_with(test_plist_file, 'w')

    def test_write_yaml(self):
        with patch('builtins.open', mock_open()) as mocked_open:
            clean_yaml_tabs(test_yaml_file)
            mocked_open.assert_called_with(test_yaml_file, 'w')


class TestCleanPlistTag:
    @pytest.mark.parametrize('a, expected', [(test_plist_file, test_plist_expected)])
    def test_clean_plist_tag(self, a, expected):
        result = clean_plist_tag(a)
        return result
        assert result == test_plist_expected  # noqa: F821

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
    def test_write_plist_file_error(self, caplog):
        caplog.clear()
        with patch('build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = OSError
            clean_plist_tag('tests/build/files/plist.plist')
        assert caplog.record_tuples == [
            (
                'build.helpers.clean_data',
                40,
                "[Errno 13] Permission denied: 'tests/build/files/plist.plist'",
            )
        ]


class TestCleanYamlTabs:
    @pytest.mark.parametrize('a, expected', [(test_yaml_file, test_yaml_expected)])
    def test_clean_yaml_tabs(self, a, expected):
        result = clean_yaml_tabs(a)
        return result
        assert result == test_yaml_expected  # noqa: F821

    def test_replace_tabs(self):
        test_tab_file = '\tText foo bar'
        test_spc_file = '  Text foo bar'
        result = _replace_tabs(test_tab_file)
        assert result == test_spc_file

    @pytest.fixture(autouse=True)
    def test_write_yaml_file_error(self, caplog):
        caplog.clear()
        with patch('build.helpers.clean_data.open') as mock_open:
            mock_open.side_effect = OSError
            clean_yaml_tabs('tests/build/files/yaml.yaml')
        assert caplog.record_tuples == [
            (
                'build.helpers.clean_data',
                40,
                "[Errno 13] Permission denied: 'tests/build/files/yaml.yaml'",
            )
        ]
