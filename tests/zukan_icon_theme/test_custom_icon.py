import importlib

from unittest import TestCase
from unittest.mock import patch, MagicMock

custom_icon = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.custom_icon'
)


class TestGenerateCustomIcon(TestCase):
    @patch.object(custom_icon, 'get_create_custom_icon_settings')
    @patch.object(custom_icon, 'list_data_names')
    @patch.object(custom_icon, 'remove_empty_dict')
    @patch.object(custom_icon, 'logger')
    def test_generate_custom_icon(
        self,
        mock_logger,
        mock_remove_empty_dict,
        mock_list_data_names,
        mock_get_create_custom_icon_settings,
    ):
        create_custom_icon_data = [
            {
                'name': 'ATest-1',
                'scope': 'source.json.atest1',
                'contexts_scope': 'source.json',
                'file_extensions': ['atest1.config.json', 'atest11.config.json'],
                'syntax_name': 'JSON (ATest-1)',
            },
            {
                'name': 'ATest-2',
                'scope': 'source.atest2',
                'syntax_name': 'ATest-2',
                'icon': 'atest2',
                'file_extensions': ['xyz', 'pqr'],
            },
            {
                'name': 'ATest-3',
                'scope': 'source.atest3',
                'syntax_name': 'ATest-3',
                'icon': 'atest3',
                'file_extensions': ['abc', 'def'],
                'contexts_scope': 'source.atest2',
            },
            {
                'name': 'GitHub 2',
                'scope': 'source.yaml.github',
                'contexts_scope': 'source.yaml',
                'file_extensions': ['ci.yml'],
                'syntax_name': 'YAML (GitHub 2)',
                'icon': 'github',
            },
            # Test required name
            {
                'icon': 'required_name',
                'scope': 'source.required_name',
            },
            {
                'name': 'ATest',
                'scope': 'source.toml.atest, source.json.atest',
                'icon': 'atest',
            },
        ]

        mock_get_create_custom_icon_settings.return_value = create_custom_icon_data
        mock_list_data_names.return_value = ['ATest-2']
        mock_remove_empty_dict.side_effect = lambda x: x
        mock_warning = MagicMock()
        mock_logger.warning = mock_warning

        result = custom_icon.generate_custom_icon(['zukan_icon_1', 'zukan_icon_2'])

        self.assertEqual(len(result), 4)

        # Test name already exists
        mock_warning.assert_any_call(
            '%s key "name" already exists, it should be unique. Excluding from build.',
            'ATest-2',
        )

        # Test required name
        mock_warning.assert_any_call(
            '%s do not have key "name", it is required',
            {'scope': 'source.required_name', 'icon': 'required_name'},
        )

        # Syntax only
        self.assertEqual(result[0]['name'], 'ATest-1')
        self.assertNotIn('preferences', result[0])
        self.assertIn('syntax', result[0])

        # Syntax aad Preference
        self.assertEqual(result[1]['name'], 'ATest-3')
        self.assertIn('preferences', result[1])
        self.assertIn('syntax', result[1])

        # Syntax and Preference
        self.assertEqual(result[2]['name'], 'GitHub 2')
        self.assertIn('preferences', result[2])
        self.assertIn('syntax', result[2])

        # Preference only
        self.assertEqual(result[3]['name'], 'ATest')
        self.assertIn('preferences', result[3])
        self.assertNotIn('syntax', result[3])


class TestDataTemplate(TestCase):
    def test_data_with_preference(self):
        input_data = {
            'name': 'ATest',
            'scope': 'source.atest',
            'icon': 'atest',
        }
        expected_output = {
            'name': 'ATest',
            'preferences': {
                'scope': 'source.atest',
                'settings': {'icon': 'atest'},
            },
        }

        result = custom_icon.data(input_data)
        self.assertEqual(result, expected_output)

    def test_data_with_syntax(self):
        input_data = {
            'name': 'ATest-1',
            'scope': 'source.json.atest1',
            'syntax_name': 'ATest-1',
            'file_extensions': ['atest1.config.json', 'atest11.config.json'],
        }
        expected_output = {
            'name': 'ATest-1',
            'syntax': [
                {
                    'name': 'ATest-1',
                    'scope': 'source.json.atest1',
                    'hidden': True,
                    'file_extensions': ['atest1.config.json', 'atest11.config.json'],
                    'contexts': {'main': []},
                }
            ],
        }

        result = custom_icon.data(input_data)
        self.assertEqual(result, expected_output)

    def test_data_with_syntax_and_contexts(self):
        input_data = {
            'name': 'ATest-1',
            'scope': 'source.json.atest1',
            'syntax_name': 'ATest-1',
            'file_extensions': ['atest1.config.json', 'atest11.config.json'],
            'contexts_scope': 'source.json',
        }
        expected_output = {
            'name': 'ATest-1',
            'syntax': [
                {
                    'name': 'ATest-1',
                    'scope': 'source.json.atest1',
                    'hidden': True,
                    'file_extensions': ['atest1.config.json', 'atest11.config.json'],
                    'contexts': {
                        'main': [
                            {
                                'include': 'scope:source.json',
                                'apply_prototype': True,
                            }
                        ]
                    },
                }
            ],
        }

        result = custom_icon.data(input_data)
        self.assertEqual(result, expected_output)

    def test_data_with_syntax_and_preferences(self):
        input_data = {
            'name': 'ATest-2',
            'scope': 'source.atest2',
            'icon': 'atest2',
            'syntax_name': 'ATest-2',
            'file_extensions': ['xyz', 'pqr'],
        }
        expected_output = {
            'name': 'ATest-2',
            'preferences': {
                'scope': 'source.atest2',
                'settings': {'icon': 'atest2'},
            },
            'syntax': [
                {
                    'name': 'ATest-2',
                    'scope': 'source.atest2',
                    'hidden': True,
                    'file_extensions': ['xyz', 'pqr'],
                    'contexts': {'main': []},
                }
            ],
        }

        result = custom_icon.data(input_data)
        self.assertEqual(result, expected_output)

    def test_data_with_syntax_and_preference_and_contexts(self):
        input_data = {
            'name': 'ATest-3',
            'scope': 'source.atest3',
            'icon': 'atest3',
            'syntax_name': 'ATest-3',
            'file_extensions': ['abc', 'def'],
            'contexts_scope': 'source.atest2',
        }
        expected_output = {
            'name': 'ATest-3',
            'preferences': {
                'scope': 'source.atest3',
                'settings': {'icon': 'atest3'},
            },
            'syntax': [
                {
                    'name': 'ATest-3',
                    'scope': 'source.atest3',
                    'hidden': True,
                    'file_extensions': ['abc', 'def'],
                    'contexts': {
                        'main': [
                            {
                                'include': 'scope:source.atest2',
                                'apply_prototype': True,
                            }
                        ]
                    },
                }
            ],
        }

        result = custom_icon.data(input_data)
        self.assertEqual(result, expected_output)
