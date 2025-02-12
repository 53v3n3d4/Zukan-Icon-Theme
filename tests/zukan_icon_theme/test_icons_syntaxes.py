import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch

icons_syntaxes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes'
)


class TestZukanSyntax(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        self.sublime_mock.version.return_value = '4000'

        self.sublime_mock.reset_mock()

        self.sublime_patcher = patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.sublime',
            self.sublime_mock,
        )
        self.sublime_patcher.start()

        self.zukan = icons_syntaxes.ZukanSyntax()

    def tearDown(self):
        self.sublime_patcher.stop()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.read_pickle_data')
    def test_zukan_icons_data(self, mock_read_pickle):
        expected_data = ['icon1', 'icon2']
        mock_read_pickle.return_value = expected_data

        result = self.zukan.zukan_icons_data()

        self.assertEqual(result, expected_data)
        mock_read_pickle.assert_called_once_with(icons_syntaxes.ZUKAN_ICONS_DATA_FILE)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.get_change_icon_settings'
    )
    def test_change_icon_file_extension_setting(self, mock_get_settings):
        expected_extensions = ['.txt', '.md']
        mock_get_settings.return_value = (None, expected_extensions)

        result = self.zukan.change_icon_file_extension_setting()

        self.assertEqual(result, expected_extensions)
        mock_get_settings.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.get_ignored_icon_settings'
    )
    def test_ignored_icon_setting(self, mock_get_settings):
        expected_ignored = {'atest1', 'atest2'}
        mock_get_settings.return_value = list(expected_ignored)

        result = self.zukan.ignored_icon_setting()

        self.assertEqual(result, expected_ignored)
        mock_get_settings.assert_called_once()

    @patch('threading.Thread')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.ThreadProgress')
    def test_install_syntax(self, mock_thread_progress, mock_thread):
        file_name = 'ATest'
        syntax_name = 'Atest'
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        self.zukan.install_syntax(file_name, syntax_name)

        mock_thread.assert_called_once_with(
            target=self.zukan.build_icon_syntax, args=(file_name, syntax_name)
        )
        mock_thread_instance.start.assert_called_once()
        mock_thread_progress.assert_called_once_with(
            mock_thread_instance, 'Building zukan syntaxes', 'Build done'
        )

    def test_get_list_icons_syntaxes(self):
        zukan_icons = [{'syntax': 'Rust'}, {'other': 'value'}]
        custom_icons = [{'syntax': 'ATest-1'}]

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.generate_custom_icon'
        ) as mock_generate:
            mock_generate.return_value = custom_icons

            result = self.zukan.get_list_icons_syntaxes(zukan_icons)

            self.assertEqual(result, zukan_icons + custom_icons)
            mock_generate.assert_called_once_with(zukan_icons)

    def test_get_compare_scopes(self):
        zukan_icons = [
            {'scope': 'source.atest1'},
            {'scope': 'source.atest2'},
            {'other': 'value'},
        ]

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.compare_scopes'
        ) as mock_compare:
            mock_compare.return_value = [
                {'scope': 'source.atest1'},
                {'scope': 'source.atest2'},
            ]

            result = self.zukan.get_compare_scopes(zukan_icons)

            self.assertEqual(result, {'source.atest1', 'source.atest2'})
            mock_compare.assert_called_once_with(zukan_icons)

    def test_get_sublime_scope_set(self):
        # Setup
        contexts_scopes = [{'scope': 'source.atest1'}, {'scope': 'source.atest2'}]

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.CONTEXTS_SCOPES',
            contexts_scopes,
        ):
            # Passing all False since it has an inconsistency order if pass True and
            # False even sorting result. Test will pass sometimes and then fail.
            #
            # It can be some mock not being cleared. Or related to issue in method
            # `visible_syntaxes_only`, where API responds with all syntaxes being False
            # even icons syntaxes that are all marked hidden True.
            self.sublime_mock.find_syntax_by_scope.side_effect = [False, False]

            result = self.zukan.get_sublime_scope_set()

            expected = {'source.atest1': False, 'source.atest2': False}

            self.assertEqual(sorted(result.items()), sorted(expected.items()))
            self.assertEqual(
                self.sublime_mock.find_syntax_by_scope.call_count, len(contexts_scopes)
            )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_file_extension'
    )
    @patch('os.path.join')
    def test_create_icon_syntax(
        self, mock_path_join, mock_edit_extension, mock_save_syntax
    ):
        mock_path_join.return_value = '/test/path/ATest.sublime-syntax'
        mock_edit_extension.return_value = ['abc']

        self.zukan.zukan_icons_data = MagicMock(
            return_value=[
                {
                    'name': 'ATest-3',
                    'syntax': [
                        {
                            'name': 'ATest-3',
                            'scope': 'source.atest3',
                            'file_extensions': ['xyz'],
                        }
                    ],
                }
            ]
        )
        self.zukan.get_compare_scopes = MagicMock(return_value=set())
        self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
        self.zukan.ignored_icon_setting = MagicMock(return_value=set())
        self.zukan.get_list_icons_syntaxes = MagicMock(
            return_value=[
                {
                    'name': 'ATest-3',
                    'syntax': [
                        {
                            'name': 'ATest-3',
                            'scope': 'source.atest3',
                            'file_extensions': ['xyz'],
                        }
                    ],
                }
            ]
        )

        self.zukan.create_icon_syntax('ATest-3')

        expected_result = {'name': 'ATest-3', 'scope': 'source.atest3', 'file_extensions': ['abc']}
        expected_syntax = '/test/path/ATest.sublime-syntax'

        mock_save_syntax.assert_called_with(expected_result, expected_syntax)

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_icon_syntax(self, mock_remove, mock_exists):
        mock_exists.return_value = True
        syntax_name = 'Atest.sublime-syntax'

        result = self.zukan.delete_icon_syntax(syntax_name)

        mock_remove.assert_called_once()
        self.assertEqual(result, syntax_name)

    @patch('glob.iglob')
    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_icons_syntaxes(self, mock_remove, mock_exists, mock_glob):
        mock_glob.return_value = [
            '/test/path/ATest-1.sublime-syntax',
            '/test/path/ATest-2.sublime-syntax',
        ]
        mock_exists.return_value = True

        self.zukan.delete_icons_syntaxes()

        # 2 from glob + 1 from exists check
        self.assertEqual(mock_remove.call_count, 3)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_file_extension'
    )
    @patch('os.path.join')
    def test_create_icons_syntaxes(
        self, mock_path_join, mock_edit_extension, mock_save_syntax
    ):
        mock_path_join.return_value = '/test/path/ATest.sublime-syntax'
        mock_edit_extension.return_value = ['abc']

        self.zukan.zukan_icons_data = MagicMock(
            return_value=[
                {
                    'name': 'ATest-3',
                    'syntax': [
                        {
                            'name': 'ATest-3',
                            'scope': 'source.atest3',
                            'file_extensions': ['xyz'],
                        }
                    ],
                }
            ]
        )
        self.zukan.get_compare_scopes = MagicMock(return_value=set())
        self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
        self.zukan.ignored_icon_setting = MagicMock(return_value=set())
        self.zukan.get_list_icons_syntaxes = MagicMock(
            return_value=[
                {
                    'name': 'ATest-3',
                    'syntax': [
                        {
                            'name': 'ATest-3',
                            'scope': 'source.atest3',
                            'file_extensions': ['xyz'],
                        }
                    ],
                }
            ]
        )

        self.zukan.create_icons_syntaxes()

        mock_save_syntax.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.logger.info')
    def test_create_icon_syntax_ignored(self, mock_logger_info):
        self.zukan.zukan_icons_data = MagicMock(
            return_value=[
                {
                    'name': 'Ignored Icon',
                    'syntax': [
                        {'name': 'Ignored Icon', 'scope': 'source.ignored_icon'}
                    ],
                    'preferences': {'settings': {'icon': 'ignored_icon'}},
                }
            ]
        )
        self.zukan.get_compare_scopes = MagicMock(return_value=set())
        self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
        self.zukan.ignored_icon_setting = MagicMock(return_value={'ignored_icon'})
        self.zukan.get_list_icons_syntaxes = MagicMock(
            return_value=[
                {
                    'name': 'Ignored Icon',
                    'syntax': [
                        {'name': 'Ignored Icon', 'scope': 'source.ignored_icon'}
                    ],
                    'preferences': {'settings': {'icon': 'ignored_icon'}},
                }
            ]
        )

        self.zukan.create_icon_syntax('Ignored Icon')
        mock_logger_info.assert_called_once_with('ignored icon %s', 'Ignored Icon')

    @patch('os.path.exists')
    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'contexts:\n  main:\n    - include: scope:source.atest\n      '
            'apply_prototype: true\n'
        ),
    )
    def test_edit_context_scope_scope_exists(self, mock_file, mock_exists):
        mock_exists.return_value = True
        self.zukan.get_sublime_scope_set = MagicMock(
            return_value={'source.atest': True}
        )
        # Test old syntax ST3
        self.zukan.sublime_version = 4000

        mock_file_handle = mock_file()

        self.zukan.edit_context_scope('ATest.sublime-syntax')

        written_content = ''.join(
            call.args[0] for call in mock_file_handle.write.call_args_list
        )
        self.assertIn('contexts:\n  main:', written_content)
        self.assertIn('scope:source.atest', written_content)

    @patch('os.path.exists')
    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'contexts:\n  main:\n    - include: scope:source.atest\n      '
            'apply_prototype: true\n'
        ),
    )
    def test_edit_context_scope_scope_not_exists(self, mock_file, mock_exists):
        mock_exists.return_value = True
        self.zukan.get_sublime_scope_set = MagicMock(
            return_value={'source.atest': False}
        )

        mock_file_handle = mock_file()

        self.zukan.edit_context_scope('ATest.sublime-syntax')

        written_content = ''.join(
            call.args[0] for call in mock_file_handle.write.call_args_list
        )
        self.assertEqual(written_content, 'contexts:\n  main: []\n')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.logger.error')
    def test_edit_context_scope_file_not_found(
        self, mock_logger_error, mock_file, mock_exists
    ):
        mock_exists.return_value = True
        expected_path = os.path.join(
            icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH, 'ATest.sublime-syntax'
        )

        mock_file.side_effect = FileNotFoundError

        self.zukan.edit_context_scope('ATest.sublime-syntax')

        mock_logger_error.assert_called_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), expected_path
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_contexts_main'
    )
    def test_edit_contexts_scopes(self, mock_edit_contexts):
        self.zukan.list_created_icons_syntaxes = MagicMock(
            return_value=['ATest.sublime-syntax']
        )
        self.zukan.get_sublime_scope_set = MagicMock(
            return_value={'source.atest': True}
        )
        self.zukan.sublime_version = 4000

        test_contexts = [{'scope': 'source.atest', 'startsWith': 'ATest'}]
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.CONTEXTS_SCOPES',
            test_contexts,
        ):
            self.zukan.edit_contexts_scopes()

        mock_edit_contexts.assert_called_once()

    @patch('os.path.exists')
    @patch('glob.glob')
    def test_list_created_icons_syntaxes(self, mock_glob, mock_exists):
        mock_exists.return_value = True
        mock_glob.return_value = [
            '/path/test/ATest-1.sublime-syntax',
            '/path/test/ATest-2.sublime-syntax',
        ]

        result = self.zukan.list_created_icons_syntaxes()

        self.assertEqual(result, ['ATest-1.sublime-syntax', 'ATest-2.sublime-syntax'])

    @patch('os.path.exists')
    def test_list_created_icons_syntaxes_directory_not_found(self, mock_exists):
        mock_exists.return_value = False

        result = self.zukan.list_created_icons_syntaxes()

        self.assertIsNone(result)
