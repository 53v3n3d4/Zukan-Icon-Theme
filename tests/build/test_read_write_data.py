import os
import pytest
import unittest


from build.helpers.read_write_data import (
    read_yaml_data,
    dump_yaml_data,
    dump_plist_data,
)
from build.utils.build_dir_paths import DATA_PATH, ICONS_TEST_PATH
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch, mock_open

# YAML
test_yaml_file = 'foo/bar.yaml'
test_yaml_expected = """%YAML 1.2
---
name: Vitest
preferences:
scope: source.js.vitest, source.ts.vitest
settings:
icon: vitest
syntax:
- name: JavaScript (Vitest)
scope: source.js.vitest
hidden: true
file_extensions:
  - vitest.config.js
  - vitest.config.cjs
  - vitest.config.mjs
  - vitest.workspace
contexts:
  main:
    - include: scope:source.js
      apply_prototype: true
- name: TypeScript (Vitest)
scope: source.ts.vitest
hidden: true
file_extensions:
  - vitest.config.ts
  - vitest.config.cts
  - vitest.config.mts
contexts:
  main:
    - include: scope:source.ts
      apply_prototype: true
"""
test_yaml_content = """%YAML 1.2
---
name: Vitest
preferences:
scope: source.js.vitest, source.ts.vitest
settings:
icon: vitest
syntax:
- name: JavaScript (Vitest)
scope: source.js.vitest
hidden: true
file_extensions:
  - vitest.config.js
  - vitest.config.cjs
  - vitest.config.mjs
  - vitest.workspace
contexts:
  main:
    - include: scope:source.js
      apply_prototype: true
- name: TypeScript (Vitest)
scope: source.ts.vitest
hidden: true
file_extensions:
  - vitest.config.ts
  - vitest.config.cts
  - vitest.config.mts
contexts:
  main:
    - include: scope:source.ts
      apply_prototype: true
"""
test_yaml_dict = {
    'name': 'Binary (Affinity Designer)',
    'scope': 'binary.afdesign',
    'hidden': True,
    'file_extensions': ['afdesign'],
    'contexts': {'main': []},
}
test_empty_yaml_file = ''
test_toml_file = 'foo/bar.toml'

# PLIST
test_plist_file = 'foo/bar.plist'
test_plist_expected = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
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
test_plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
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
test_plist_dict = {
    'name': 'Affinity Designer',
    'preferences': {'scope': 'binary.afdesign', 'settings': {'icon': 'afdesign'}},
    'syntax': [
        {
            'name': 'Binary (Affinity Designer)',
            'scope': 'binary.afdesign',
            'hidden': True,
            'file_extensions': ['afdesign'],
            'contexts': {'main': []},
        }
    ],
}


class TestDumpFile(unittest.TestCase):
    def test_dump_plist(self):
        with patch('builtins.open', mock_open()) as mocked_open:
            dump_plist_data(test_plist_content, test_plist_file)
            mocked_open.assert_called_with(test_plist_file, 'wb')

    def test_dump_yaml(self):
        with patch('builtins.open', mock_open()) as mocked_open:
            dump_yaml_data(test_yaml_content, test_yaml_file)
            mocked_open.assert_called_with(test_yaml_file, 'w')


class TestLoadYaml(unittest.TestCase):
    def test_empty_file(self):
        with patch('builtins.open', mock_open()):
            file_data = read_yaml_data(test_empty_yaml_file)
            self.assertEqual(file_data, '')


class TestYamlData:
    @pytest.mark.parametrize('a, expected', [(test_yaml_content, test_yaml_expected)])
    def test_load_yaml(self, a, expected):
        result = read_yaml_data(a)
        assert result == test_yaml_expected

    @pytest.mark.parametrize(
        'a, b, expected', [(test_yaml_content, test_yaml_file, test_yaml_expected)]
    )
    def test_dump_yaml(self, a, b, expected):
        result = dump_yaml_data(a, b)
        return result
        assert result == test_yaml_expected


class TestPlistData:
    @pytest.mark.parametrize(
        'a, b, expected', [(test_plist_file, test_plist_content, test_plist_expected)]
    )
    def test_dump_plist(self, a, b, expected):
        result = dump_plist_data(a, b)
        return result
        assert result == test_plist_expected


file_yaml_test = os.path.join(DATA_PATH, 'afpub.yaml')
file_plist_test = os.path.join(DATA_PATH, 'afpub.plist')


class TestReadWriteYamlData(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml', contents='test')
        cls.fake_fs().create_file('data/afphoto.yaml', contents='test')
        cls.fake_fs().create_file('data/afpub.yaml', contents='test')
        cls.fake_fs().create_file('data/ai.yaml', contents='test')
        cls.fake_fs().create_file('data/angular.yaml', contents='test')

    def test_file_exist(self):
        read_yaml_data('data/afpub.yaml')
        dump_yaml_data(file_yaml_test, ICONS_TEST_PATH)
        self.assertFalse(os.path.exists('afpub.yaml'))

    def test_load_dump(self):
        read_yaml_data('data/afdesign.yaml')
        dump_yaml_data(file_yaml_test, ICONS_TEST_PATH)
        self.assertFalse(os.path.exists('afpub.yaml'))
        # self.assertTrue('data/afdesign.yaml')

    def test_file_not_found(self):
        read_yaml_data('./yaml.yaml')
        self.assertFalse(os.path.exists('./yaml.yaml'))

    def test_load_params(self):
        read_yaml_data('data/afdesign.yaml')
        self.assertTrue(isinstance('data/afdesign.yaml', str))
        self.assertFalse(isinstance('data/afdesign.yaml', int))
        self.assertFalse(isinstance('data/afdesign.yaml', list))
        self.assertFalse(isinstance('data/afdesign.yaml', bool))
        self.assertFalse(isinstance('data/afdesign.yaml', dict))

    def test_dump_params(self):
        dump_yaml_data(test_yaml_dict, 'data/afdesign.yaml')
        self.assertTrue(isinstance('data/afdesign.yaml', str))
        self.assertFalse(isinstance('data/afdesign.yaml', int))
        self.assertFalse(isinstance('data/afdesign.yaml', list))
        self.assertFalse(isinstance('data/afdesign.yaml', bool))
        self.assertFalse(isinstance('data/afdesign.yaml', dict))
        self.assertTrue(isinstance(test_yaml_dict, dict))
        self.assertFalse(isinstance(test_yaml_dict, int))
        self.assertFalse(isinstance(test_yaml_dict, list))
        self.assertFalse(isinstance(test_yaml_dict, bool))
        self.assertFalse(isinstance(test_yaml_dict, str))


class TestWritePlistData(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.plist', contents='test')
        cls.fake_fs().create_file('data/afphoto.plist', contents='test')
        cls.fake_fs().create_file('data/afpub.plist', contents='test')
        cls.fake_fs().create_file('data/ai.plist', contents='test')
        cls.fake_fs().create_file('data/angular.plist', contents='test')

    def test_file_exist(self):
        dump_plist_data(file_plist_test, ICONS_TEST_PATH)
        self.assertFalse(os.path.exists('afpub.plist'))

    def test_dump_params(self):
        dump_plist_data(test_plist_dict, 'data/afdesign.plist')
        self.assertTrue(isinstance('data/afdesign.plist', str))
        self.assertFalse(isinstance('data/afdesign.plist', int))
        self.assertFalse(isinstance('data/afdesign.plist', list))
        self.assertFalse(isinstance('data/afdesign.plist', bool))
        self.assertFalse(isinstance('data/afdesign.plist', dict))
        self.assertTrue(isinstance(test_plist_dict, dict))
        self.assertFalse(isinstance(test_plist_dict, int))
        self.assertFalse(isinstance(test_plist_dict, list))
        self.assertFalse(isinstance(test_plist_dict, bool))
        self.assertFalse(isinstance(test_plist_dict, str))
