import importlib

from unittest import TestCase
from unittest.mock import patch, MagicMock

search_syntaxes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_syntaxes'
)
zukan_paths = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.zukan_paths'
)


class TestZukanSyntaxFunctions(TestCase):
    @patch.object(search_syntaxes.sublime, 'list_syntaxes')
    def test_visible_syntaxes_only(self, mock_list_syntaxes):
        mock_syntax1 = MagicMock(
            name='ATest-1',
            hidden=False,
            path='Packages/ATest-1/ATest-1.sublime-syntax',
            scope='source.atest1',
        )
        mock_syntax2 = MagicMock(
            name='ATest-2',
            hidden=False,
            path='Packages/ATest-2/ATest-2.sublime-syntax',
            scope='source.atest2',
        )
        mock_syntax3 = MagicMock(
            name='HTML (ATest)',
            hidden=True,
            path='Packages/ATest/HTML (ATest).sublime-syntax',
            scope='text.html.js-atest',
        )
        mock_syntax4 = MagicMock(
            name='ATest-3',
            hidden=False,
            path='Packages/ATest-3/ATest-3.sublime-syntax',
            scope='embedding.atest3',
        )

        mock_list_syntaxes.return_value = [
            mock_syntax1,
            mock_syntax2,
            mock_syntax3,
            mock_syntax4,
        ]

        result = search_syntaxes.visible_syntaxes_only()
        self.assertEqual(len(result), 3)
        self.assertIn(mock_syntax1, result)
        self.assertIn(mock_syntax2, result)
        self.assertIn(mock_syntax4, result)
        self.assertNotIn(mock_syntax3, result)

    @patch.object(search_syntaxes.sublime, 'list_syntaxes')
    def test_compare_scopes(self, mock_list_syntaxes):
        zukan_icons_data = [
            {'syntax': [{'scope': 'source.atest1'}, {'scope': 'source.atest2'}]},
            {'syntax': [{'scope': 'embedding.atest3'}, {'scope': 'text.atest4'}]},
        ]

        mock_syntax1 = MagicMock(
            name='ATest-1',
            hidden=False,
            path='Packages/ATest-1/ATest-1.sublime-syntax',
            scope='source.atest1',
        )
        mock_syntax2 = MagicMock(
            name='ATest-2',
            hidden=True,
            path='Packages/ATest-2/ATest-2.sublime-syntax',
            scope='source.atest2',
        )
        mock_syntax3 = MagicMock(
            name='ATest-3',
            hidden=False,
            path='Packages/ATest-3/ATest-3.sublime-syntax',
            scope='embedding.atest3',
        )

        mock_list_syntaxes.return_value = [mock_syntax1, mock_syntax2, mock_syntax3]

        result = search_syntaxes.compare_scopes(zukan_icons_data)
        self.assertEqual(
            result, [{'scope': 'source.atest1'}, {'scope': 'embedding.atest3'}]
        )

    @patch.object(search_syntaxes.sublime, 'list_syntaxes')
    @patch.object(zukan_paths, 'ICONS_SYNTAXES_PARTIAL_PATH', 'path/to/icons_syntaxe')
    def test_compare_scopes_no_match(self, mock_list_syntaxes):
        zukan_icons_data = [
            {'syntax': [{'scope': 'source.atest11'}, {'scope': 'source.atest12'}]},
            {'syntax': [{'scope': 'embedding.atest3'}, {'scope': 'text.atest4'}]},
        ]

        mock_syntax1 = MagicMock(
            name='ATest-1',
            hidden=False,
            path='Packages/ATest-1/ATest-1.sublime-syntax',
            scope='source.atest1',
        )
        mock_syntax2 = MagicMock(
            name='ATest-2',
            hidden=True,
            path='Packages/ATest-2/ATest-2.sublime-syntax',
            scope='source.atest2',
        )

        mock_list_syntaxes.return_value = [mock_syntax1, mock_syntax2]

        result = search_syntaxes.compare_scopes(zukan_icons_data)
        self.assertEqual(result, [])

    @patch.object(search_syntaxes.sublime, 'list_syntaxes')
    def test_compare_scopes_empty_input(self, mock_list_syntaxes):
        zukan_icons_data = []

        mock_list_syntaxes.return_value = []

        result = search_syntaxes.compare_scopes(zukan_icons_data)
        self.assertEqual(result, [])

    @patch.object(search_syntaxes.sublime, 'list_syntaxes')
    def test_compare_scopes_no_syntax(self, mock_list_syntaxes):
        zukan_icons_data = [
            {'name': 'ATest-22'},
            {'name': 'ATest-33', 'syntax': []},
            {
                'name': 'ATest-44',
                'syntax': [{'scope': 'source.atest1'}, {'scope': 'embedding.atest3'}],
            },
        ]

        mock_syntax1 = MagicMock(
            name='ATest-1',
            hidden=False,
            path='Packages/ATest-1/ATest-1.sublime-syntax',
            scope='source.atest1',
        )
        mock_syntax2 = MagicMock(
            name='ATest-2',
            hidden=False,
            path='Packages/ATest-2/ATest-2.sublime-syntax',
            scope='embedding.atest3',
        )
        mock_syntax3 = MagicMock(
            name='ATest-3',
            hidden=True,
            path='Packages/ATest-3/ATest-3.sublime-syntax',
            scope='source.atest2',
        )

        mock_list_syntaxes.return_value = [mock_syntax1, mock_syntax2, mock_syntax3]

        result = search_syntaxes.compare_scopes(zukan_icons_data)
        self.assertEqual(
            result, [{'scope': 'source.atest1'}, {'scope': 'embedding.atest3'}]
        )
