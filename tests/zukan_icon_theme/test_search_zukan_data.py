import importlib

from unittest import TestCase

search_zukan_data = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_zukan_data'
)


class TestListDataNames(TestCase):
    def test_list_create_custom_icons_names(self):
        zukan_icons_data = [
            {'name': 'ATest-1'},
            {'name': 'ATest-2'},
            {'name': 'ATest-3'},
        ]

        result = search_zukan_data.list_data_names(zukan_icons_data)

        self.assertEqual(result, ['ATest-1', 'ATest-2', 'ATest-3'])
        self.assertIsInstance(zukan_icons_data, list)
        self.assertIsInstance(zukan_icons_data[0], dict)
        self.assertIsInstance(zukan_icons_data[0]['name'], str)
        self.assertIsInstance(zukan_icons_data[1]['name'], str)
        self.assertIsInstance(zukan_icons_data[2]['name'], str)

        self.assertIsInstance(result, list)
        for name in result:
            self.assertIsInstance(name, str)

    def test_list_create_custom_icons_names_empty(self):
        zukan_icons_data = []

        result = search_zukan_data.list_data_names(zukan_icons_data)

        self.assertEqual(result, [])
        self.assertIsInstance(zukan_icons_data, list)

    def test_error_zukan_icons_data(self):
        zukan_icons_data = None

        with self.assertRaises(TypeError):
            search_zukan_data.list_data_names(zukan_icons_data)
