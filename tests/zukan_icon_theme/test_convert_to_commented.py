import importlib
import sublime

from unittest import TestCase

convert_to_commented = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.convert_to_commented'
)
constants_icons_syntaxes = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_icons_syntaxes'
)
constants_pickle = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_pickle'
)
constants_yaml = importlib.import_module('Zukan-Icon-Theme.tests.mocks.constants_yaml')


params_list = [
    (
        constants_icons_syntaxes.TEST_SUBLIME_SYNTAXES_DICT,
        constants_pickle.TEST_PICKLE_NESTED_ORDERED_DICT,
    ),
    (
        constants_icons_syntaxes.TEST_SUBLIME_SYNTAX_DICT,
        constants_pickle.TEST_PICKLE_ORDERED_DICT,
    ),
    (constants_yaml.TEST_YAML_ORDERED_DICT, constants_yaml.TEST_YAML_ORDERED_DICT),
    ('milk way', 'milk way'),
    (7, 7),
]


class TestConvertToCommented(TestCase):
    def test_convert_to_commented(self):
        for p1, p2 in params_list:
            with self.subTest(params_list):
                self.assertEqual(p1, p2)
                self.assertIsInstance(
                    constants_icons_syntaxes.TEST_SUBLIME_SYNTAXES_DICT, list
                )
                self.assertIsInstance(
                    constants_pickle.TEST_PICKLE_NESTED_ORDERED_DICT, list
                )
                self.assertIsInstance(
                    constants_icons_syntaxes.TEST_SUBLIME_SYNTAX_DICT, dict
                )
                self.assertIsInstance(constants_pickle.TEST_PICKLE_ORDERED_DICT, dict)
                self.assertIsInstance(constants_yaml.TEST_YAML_ORDERED_DICT, dict)
                self.assertIsInstance('milk way', str)
                self.assertIsInstance(7, int)
