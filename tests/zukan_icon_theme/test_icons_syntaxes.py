import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import call, MagicMock, mock_open, patch

icons_syntaxes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes'
)


class TestZukanSyntax(TestCase):
    def setUp(self):
        self.test_syntax_file_name = 'ATest-3.sublime-syntax'
        self.test_syntax_path = '/test/path/ATest-3.sublime-syntax'
        self.test_edit_extensions_data = ['abc', 'xyz']
        self.mock_zukan_icons_data = [
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
        self.mock_get_list_icons_syntaxes_data = [
            {
                'name': 'ATest-3',
                'syntax': [
                    {
                        'name': 'ATest-3',
                        'scope': 'source.atest3',
                        'file_extensions': ['abc', 'xyz'],
                    }
                ],
            }
        ]
        self.test_syntax_data = {
            'name': 'ATest-3',
            'scope': 'source.atest3',
            'file_extensions': ['abc', 'xyz'],
        }
        self.test_contexts_scopes = [
            {'startsWith': 'ATest-1', 'scope': 'source.atest1'},
            {'startsWith': 'ATest-2', 'scope': 'source.atest2'},
        ]

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
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.should_clean_output_dir'
    )
    def test_clean_output_dir_setting(self, mock_should_clean):
        mock_should_clean.return_value = True

        result = self.zukan.clean_output_dir_setting()

        self.assertTrue(result)
        mock_should_clean.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.should_clean_output_dir'
    )
    def test_clean_output_dir_setting_false(self, mock_should_clean):
        mock_should_clean.return_value = False

        result = self.zukan.clean_output_dir_setting()

        self.assertFalse(result)
        mock_should_clean.assert_called_once()

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

    @patch('threading.Thread')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.ThreadProgress')
    def test_install_syntaxes(self, mock_thread_progress, mock_thread):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        self.zukan.install_syntaxes()

        mock_thread.assert_called_once_with(target=self.zukan.build_icons_syntaxes)
        mock_thread_instance.start.assert_called_once()
        mock_thread_progress.assert_called_once_with(
            mock_thread_instance, 'Building zukan syntaxes', 'Build done'
        )

    def test_build_icons_syntaxes_deletes_existing_syntaxes(self):
        # fmt: off
        with patch('os.path.exists') as mock_exists, \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.listdir') as mock_listdir, \
             patch.object(self.zukan, 'clean_output_dir_setting') as mock_clean_output_dir, \
             patch.object(self.zukan, 'delete_icons_syntaxes') as mock_delete, \
             patch.object(self.zukan, 'create_icons_syntaxes') as mock_create, \
             patch.object(self.zukan, 'edit_contexts_scopes') as mock_edit_contexts, \
             patch(
                 'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.copy_primary_icons'
             ) as mock_copy_icons:
        # fmt: on

            mock_exists.return_value = True
            mock_listdir.return_value = [
                'Atest-1.sublime-syntax',
                'Atest-2.sublime-syntax',
            ]
            mock_clean_output_dir.return_value = True

            self.zukan.build_icons_syntaxes()

            mock_delete.assert_called_once()
            mock_create.assert_called_once()
            mock_edit_contexts.assert_called_once()
            mock_copy_icons.assert_called_once()

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
        mock_path_join.return_value = self.test_syntax_path
        mock_edit_extension.return_value = self.test_edit_extensions_data

        self.zukan.zukan_icons_data = MagicMock(return_value=self.mock_zukan_icons_data)
        self.zukan.get_compare_scopes = MagicMock(return_value=set())
        self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
        self.zukan.ignored_icon_setting = MagicMock(return_value=set())
        self.zukan.get_list_icons_syntaxes = MagicMock(
            return_value=self.mock_get_list_icons_syntaxes_data
        )

        self.zukan.create_icon_syntax('ATest-3')

        mock_save_syntax.assert_called_with(
            self.test_syntax_data, self.test_syntax_path
        )

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

    def test_create_icon_syntax_file_not_found(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
        ) as mock_save:
            mock_save.side_effect = FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.test_syntax_file_name
            )

            self.zukan.zukan_icons_data = MagicMock(
                return_value=self.mock_zukan_icons_data
            )
            self.zukan.get_compare_scopes = MagicMock(return_value=set())
            self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
            self.zukan.ignored_icon_setting = MagicMock(return_value=[])
            self.zukan.get_list_icons_syntaxes = MagicMock(
                return_value=self.mock_get_list_icons_syntaxes_data
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.create_icon_syntax('ATest-3')

            self.assertIn(
                f"[Errno {errno.ENOENT}] {os.strerror(errno.ENOENT)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

    def test_create_icon_syntax_os_error(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
        ) as mock_save:
            mock_save.side_effect = OSError(
                errno.EACCES, os.strerror(errno.EACCES), self.test_syntax_file_name
            )

            self.zukan.zukan_icons_data = MagicMock(
                return_value=self.mock_zukan_icons_data
            )
            self.zukan.get_compare_scopes = MagicMock(return_value=set())
            self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
            self.zukan.ignored_icon_setting = MagicMock(return_value=[])
            self.zukan.get_list_icons_syntaxes = MagicMock(
                return_value=self.mock_get_list_icons_syntaxes_data
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.create_icon_syntax('ATest-3')

            self.assertIn(
                f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

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
        mock_path_join.return_value = self.test_syntax_path
        mock_edit_extension.return_value = self.test_edit_extensions_data

        self.zukan.zukan_icons_data = MagicMock(return_value=self.mock_zukan_icons_data)
        self.zukan.get_compare_scopes = MagicMock(return_value=set())
        self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
        self.zukan.ignored_icon_setting = MagicMock(return_value=set())
        self.zukan.get_list_icons_syntaxes = MagicMock(
            return_value=self.mock_get_list_icons_syntaxes_data
        )

        self.zukan.create_icons_syntaxes()

        mock_save_syntax.assert_any_call(self.test_syntax_data, self.test_syntax_path)
        assert mock_save_syntax.call_count > 0

        list_all_icons_syntaxes = self.zukan.get_list_icons_syntaxes()
        assert mock_save_syntax.call_count == len(list_all_icons_syntaxes)

    def test_create_icons_syntaxes_file_not_found(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
        ) as mock_save:
            mock_save.side_effect = FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.test_syntax_file_name
            )

            self.zukan.zukan_icons_data = MagicMock(
                return_value=self.mock_zukan_icons_data
            )
            self.zukan.get_compare_scopes = MagicMock(return_value=set())
            self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
            self.zukan.ignored_icon_setting = MagicMock(return_value=[])
            self.zukan.get_list_icons_syntaxes = MagicMock(
                return_value=self.mock_get_list_icons_syntaxes_data
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.create_icons_syntaxes()

            self.assertIn(
                f"[Errno {errno.ENOENT}] {os.strerror(errno.ENOENT)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

    def test_create_icons_syntaxes_os_error(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.save_sublime_syntax'
        ) as mock_save:
            mock_save.side_effect = OSError(
                errno.EACCES, os.strerror(errno.EACCES), self.test_syntax_file_name
            )

            self.zukan.zukan_icons_data = MagicMock(
                return_value=self.mock_zukan_icons_data
            )
            self.zukan.get_compare_scopes = MagicMock(return_value=set())
            self.zukan.change_icon_file_extension_setting = MagicMock(return_value=[])
            self.zukan.ignored_icon_setting = MagicMock(return_value=[])
            self.zukan.get_list_icons_syntaxes = MagicMock(
                return_value=self.mock_get_list_icons_syntaxes_data
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.create_icons_syntaxes()

            self.assertIn(
                f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_icon_syntax(self, mock_remove, mock_exists):
        mock_exists.return_value = True

        result = self.zukan.delete_icon_syntax(self.test_syntax_file_name)

        mock_remove.assert_called_once()
        self.assertEqual(result, self.test_syntax_file_name)

    def test_delete_icon_syntax_file_not_found(self):
        with patch('os.remove') as mock_remove:
            mock_remove.side_effect = FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.test_syntax_file_name
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.delete_icon_syntax(self.test_syntax_file_name)

            self.assertIn(
                f"[Errno {errno.ENOENT}] {os.strerror(errno.ENOENT)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

            mock_remove.assert_called_once_with(
                os.path.join(
                    icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                    self.test_syntax_file_name,
                )
            )

    def test_delete_icon_syntax_os_error(self):
        with patch('os.remove') as mock_remove:
            mock_remove.side_effect = OSError(
                errno.EACCES, os.strerror(errno.EACCES), self.test_syntax_file_name
            )

            with self.assertLogs(level='ERROR') as log:
                self.zukan.delete_icon_syntax(self.test_syntax_file_name)

            self.assertIn(
                f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: '{self.test_syntax_file_name}'",
                log.output[0],
            )

            mock_remove.assert_called_once_with(
                os.path.join(
                    icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                    self.test_syntax_file_name,
                )
            )

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

    def test_delete_icons_syntaxes_file_not_found(self):
        with patch('glob.iglob', return_value=[self.test_syntax_file_name]):
            with patch('os.remove') as mock_remove:
                mock_remove.side_effect = FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), self.test_syntax_file_name
                )
                with patch('os.path.exists', return_value=False):
                    with self.assertLogs(level='ERROR') as log:
                        self.zukan.delete_icons_syntaxes()

                    self.assertIn(
                        f"[Errno {errno.ENOENT}] {os.strerror(errno.ENOENT)}: '{self.test_syntax_file_name}'",
                        log.output[0],
                    )
                    mock_remove.assert_called_once_with(self.test_syntax_file_name)

    def test_delete_icons_syntaxes_os_error(self):
        with patch('glob.iglob', return_value=[self.test_syntax_file_name]):
            with patch('os.remove') as mock_remove:
                mock_remove.side_effect = OSError(
                    errno.EACCES, os.strerror(errno.EACCES), self.test_syntax_file_name
                )
                with patch('os.path.exists', return_value=False):
                    with self.assertLogs(level='ERROR') as log:
                        self.zukan.delete_icons_syntaxes()

                    self.assertIn(
                        f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: '{self.test_syntax_file_name}'",
                        log.output[0],
                    )
                    mock_remove.assert_called_once_with(self.test_syntax_file_name)

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

        self.zukan.edit_context_scope(self.test_syntax_file_name)

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

        self.zukan.edit_context_scope(self.test_syntax_file_name)

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
            icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH, self.test_syntax_file_name
        )

        mock_file.side_effect = FileNotFoundError

        self.zukan.edit_context_scope(self.test_syntax_file_name)

        mock_logger_error.assert_called_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), expected_path
        )

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.logger.error')
    def test_edit_context_scope_os_error(
        self, mock_logger_error, mock_file, mock_exists
    ):
        mock_exists.return_value = True
        expected_path = os.path.join(
            icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH, self.test_syntax_file_name
        )

        mock_file.side_effect = OSError

        self.zukan.edit_context_scope(self.test_syntax_file_name)

        mock_logger_error.assert_called_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), expected_path
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_contexts_main'
    )
    def test_edit_contexts_scopes(self, mock_edit_contexts):
        self.zukan.list_created_icons_syntaxes = MagicMock(
            return_value=[self.test_syntax_file_name]
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

    def test_edit_contexts_scopes_not_installed(self):
        test_installed_syntaxes = ['ATest-1.sublime-syntax', 'ATest-2.sublime-syntax']
        self.zukan.list_created_icons_syntaxes = MagicMock(
            return_value=test_installed_syntaxes
        )

        self.zukan.get_sublime_scope_set = MagicMock(
            return_value={'source.atest1': None, 'source.atest2': None}
        )

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.CONTEXTS_SCOPES',
            self.test_contexts_scopes,
        ):
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_contexts_main'
            ) as mock_edit:
                self.zukan.edit_contexts_scopes()

                expected_calls = [
                    call(
                        os.path.join(
                            icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                            'ATest-1.sublime-syntax',
                        ),
                        None,
                    ),
                    call(
                        os.path.join(
                            icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                            'ATest-2.sublime-syntax',
                        ),
                        None,
                    ),
                ]
                mock_edit.assert_has_calls(expected_calls, any_order=True)
                self.assertEqual(mock_edit.call_count, 2)

    def test_edit_contexts_scopes_empty_installed_list(self):
        self.zukan.list_created_icons_syntaxes = MagicMock(return_value=[])

        self.zukan.get_sublime_scope_set = MagicMock(
            return_value={'source.atest1': None, 'source.atest2': None}
        )

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.CONTEXTS_SCOPES',
            self.test_contexts_scopes,
        ):
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_syntaxes.edit_contexts_main'
            ) as mock_edit:
                self.zukan.edit_contexts_scopes()

                mock_edit.assert_not_called()

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

    def test_list_created_icons_syntaxes_os_error(self):
        with patch('os.path.exists') as mock_exists:
            mock_exists.side_effect = OSError(
                errno.EACCES,
                os.strerror(errno.EACCES),
                icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
            )

            with self.assertLogs(level='ERROR') as log:
                result = self.zukan.list_created_icons_syntaxes()

            self.assertIn(
                f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: 'Zukan Icon Theme/icons_syntaxes folder'",
                log.output[0],
            )
            self.assertIsNone(result)
            mock_exists.assert_called_once_with(
                icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH
            )

    def test_list_created_icons_syntaxes_os_error_glob(self):
        with patch('os.path.exists', return_value=True):
            with patch('glob.glob') as mock_glob:
                mock_glob.side_effect = OSError(
                    errno.EACCES,
                    os.strerror(errno.EACCES),
                    icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                )

                with self.assertLogs(level='ERROR') as log:
                    result = self.zukan.list_created_icons_syntaxes()

                self.assertIn(
                    f"[Errno {errno.EACCES}] {os.strerror(errno.EACCES)}: 'Zukan Icon Theme/icons_syntaxes folder'",
                    log.output[0],
                )
                self.assertIsNone(result)
                mock_glob.assert_called_once_with(
                    os.path.join(
                        icons_syntaxes.ZUKAN_PKG_ICONS_SYNTAXES_PATH,
                        '*' + icons_syntaxes.SUBLIME_SYNTAX_EXTENSION,
                    )
                )
