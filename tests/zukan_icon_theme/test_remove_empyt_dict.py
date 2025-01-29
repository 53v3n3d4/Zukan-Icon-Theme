import importlib

from unittest import TestCase

remove_empty_dict = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.remove_empty_dict'
)


class TestRemoveEmptyDict(TestCase):
    def test_empty_dict(self):
        self.assertEqual(remove_empty_dict.remove_empty_dict({}), {})

    def test_dict_with_empty_values_1(self):
        input_dict = {
            'name': 'ATest',
            'icon': 'atest',
            'syntax_name': '',
            'scope': 'source.toml.atest, source.js.atest',
            'file_extensions': [],
        }
        expected = {
            'name': 'ATest',
            'icon': 'atest',
            'scope': 'source.toml.atest, source.js.atest',
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), expected)

    def test_dict_with_empty_values_2(self):
        input_dict = {
            'name': 'ATest-1',
            'icon': None,
            'syntax_name': 'JSON (ATest-1)',
            'scope': 'source.json.atest1',
            'file_extensions': ['atest1.config.json'],
            'contexts_scope': 'source.json',
        }
        expected = {
            'name': 'ATest-1',
            'syntax_name': 'JSON (ATest-1)',
            'scope': 'source.json.atest1',
            'file_extensions': ['atest1.config.json'],
            'contexts_scope': 'source.json',
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), expected)

    def test_dict_with_empty_values_3(self):
        input_dict = {
            'name': 'ATest-2',
            'icon': 'atest2',
            'syntax_name': 'ATest-2',
            'scope': 'source.atest2',
            'file_extensions': ['xyz'],
            'contexts_scope': '',
        }
        expected = {
            'name': 'ATest-2',
            'icon': 'atest2',
            'syntax_name': 'ATest-2',
            'scope': 'source.atest2',
            'file_extensions': ['xyz'],
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), expected)

    def test_no_empty_dict_1(self):
        input_dict = {
            'name': 'ATest-2',
            'icon': 'atest2',
            'syntax_name': 'ATest-2',
            'scope': 'source.atest2',
            'file_extensions': ['xyz'],
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), input_dict)

    def test_no_empty_dict_2(self):
        input_dict = {
            'name': 'ATest-3',
            'icon': 'atest3',
            'syntax_name': 'ATest-3',
            'scope': 'source.atest3',
            'file_extensions': ['abc', 'def'],
            'contexts_scope': 'source.atest2',
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), input_dict)

    def test_no_empty_dict_3(self):
        input_dict = {
            'name': 'GitHub 2',
            'icon': 'github',
            'syntax_name': 'YAML (GitHub 2)',
            'scope': 'source.yaml.github',
            'file_extensions': ['ci.yml'],
            'contexts_scope': 'source.yaml',
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), input_dict)

    def test_no_empty_dict_4(self):
        input_dict = {
            'name': 'ATest',
            'icon': 'atest',
            'scope': 'source.toml.atest, source.js.atest',
        }
        self.assertEqual(remove_empty_dict.remove_empty_dict(input_dict), input_dict)
