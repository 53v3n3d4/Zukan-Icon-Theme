import importlib
import sublime_plugin

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

change_file_extension = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension'
)


class TestChangeResetFileExtension(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        self.logger_mock = MagicMock()

        patcher = patch.multiple(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension',
            sublime=self.sublime_mock,
            logger=self.logger_mock,
            is_zukan_listener_enabled=MagicMock(return_value=True),
            get_change_icon_settings=MagicMock(return_value=(None, [])),
            set_save_settings=MagicMock(),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.change_reset_file_extension = (
            change_file_extension.ChangeResetFileExtension()
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension.is_zukan_listener_enabled'
    )
    def test_change_reset_file_extension_init(self, mock_listener):
        mock_listener.return_value = True
        file_extension = change_file_extension.ChangeResetFileExtension()
        self.assertTrue(file_extension.zukan_listener_enabled)
        mock_listener.assert_called_once()

    def test_change_icon_file_extension_setting(self):
        expected = ['test.txt']
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension.get_change_icon_settings',
            return_value=(None, expected),
        ):
            result = (
                self.change_reset_file_extension.change_icon_file_extension_setting()
            )
            self.assertEqual(result, expected)

    def test_message_required_change_file_scope_extension(self):
        self.change_reset_file_extension.message_required_change_file_scope_extension(
            '', 'txt'
        )
        self.sublime_mock.error_message.assert_called_with(
            'Scope and file extension inputs are required'
        )

        self.change_reset_file_extension.message_required_change_file_scope_extension(
            'source.python', ''
        )
        self.sublime_mock.error_message.assert_called_with(
            'Scope and file extension inputs are required'
        )

    def test_convert_to_list(self):
        test_cases = [
            ('txt,py,js', ['txt', 'py', 'js']),
            ('txt', ['txt']),
            ('txt, py , js', ['txt', 'py', 'js']),
            ('', ['']),
        ]

        for input_str, expected in test_cases:
            result = self.change_reset_file_extension.convert_to_list(input_str)
            self.assertEqual(result, expected)

    def test_scope_not_exists(self):
        change_icon_file_extension = [
            {'scope': 'source.python', 'file_extensions': ['py']}
        ]
        new_scopes_list = []
        test_scope = 'source.js'
        inserted_scope = {'scope': test_scope, 'file_extensions': ['js']}

        self.change_reset_file_extension.scope_not_exists(
            change_icon_file_extension[0],
            test_scope,
            change_icon_file_extension,
            new_scopes_list,
            inserted_scope,
        )

        self.assertEqual(new_scopes_list, [inserted_scope])

    def test_scope_exists(self):
        d = {'scope': 'source.python', 'file_extensions': ['py']}
        change_icon_file_extension = [d]

        self.change_reset_file_extension.scope_exists(
            d, 'source.python', 'py,pyw', change_icon_file_extension, ['pyw']
        )
        self.assertEqual(d['file_extensions'], ['py', 'pyw'])

        self.change_reset_file_extension.scope_exists(
            d, 'source.python', 'py', change_icon_file_extension, []
        )
        self.sublime_mock.error_message.assert_called()

    def test_file_extension_exists(self):
        d = {'scope': 'source.python', 'file_extensions': ['py']}
        result = self.change_reset_file_extension.file_extension_exists(
            d, 'source.javascript', ['py']
        )
        self.assertIsNone(result)
        self.sublime_mock.error_message.assert_called_with(
            'File extension present in different scope'
        )

    def test_cleaning_duplicated(self):
        test_cases = [
            (
                [
                    {'scope': 'source.atest1'},
                    {'scope': 'source.atest1'},
                    {'scope': 'source.atest2'},
                ],
                [{'scope': 'source.atest1'}, {'scope': 'source.atest2'}],
            ),
            ([{'scope': 'source.atest1'}], [{'scope': 'source.atest1'}]),
            ([], []),
        ]

        for input_list, expected in test_cases:
            result = self.change_reset_file_extension.cleaning_duplicated(input_list)
            self.assertEqual(result, expected)

    def test_reset_file_extension(self):
        change_icon_file_extension = [
            {'scope': 'source.python', 'file_extensions': ['py']},
            {'scope': 'source.js', 'file_extensions': ['js']},
        ]

        self.change_reset_file_extension.reset_file_extension(
            change_icon_file_extension, 'source.python'
        )

        self.logger_mock.info.assert_called_with(
            'reseting file extensions for %s', 'source.python'
        )

    def test_reset_all_file_extensions(self):
        change_icon_file_extension = [
            {'scope': 'source.python', 'file_extensions': ['py']},
            {'scope': 'source.js', 'file_extensions': ['js']},
        ]

        self.change_reset_file_extension.reset_all_file_extensions(
            change_icon_file_extension
        )

        self.logger_mock.info.assert_called_with(
            'reseting file extensions for all scopes'
        )


class TestChangeFileExtensionCommand(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        self.sublime_plugin_mock = MagicMock()
        self.logger_mock = MagicMock()
        self.view_mock = MagicMock()
        self.change_reset_mock = MagicMock()

        patcher = patch.multiple(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension',
            sublime=self.sublime_mock,
            sublime_plugin=self.sublime_plugin_mock,
            logger=self.logger_mock,
            ChangeResetFileExtension=MagicMock(return_value=self.change_reset_mock),
            set_save_settings=MagicMock(),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.command = change_file_extension.ChangeFileExtensionCommand(self.view_mock)

    def test_change_file_extension_command_init(self):
        self.assertIsNotNone(self.command.change_reset_file_extension)
        self.assertEqual(self.command.view, self.view_mock)

    def test_change_file_extension_command_run_empty(self):
        self.command.run(MagicMock(), '', '')
        self.change_reset_mock.message_required_change_file_scope_extension.assert_called_with(
            '', ''
        )

    def test_change_file_extension_command_run(self):
        self.change_reset_mock.change_icon_file_extension_setting.return_value = []

        self.command.run(MagicMock(), 'source.python', 'py,pyw')

        self.change_reset_mock.convert_to_list.assert_called_with('py,pyw')
        self.logger_mock.debug.assert_called_with('change_icon_file_extension is empty')

    def test_change_file_extension_command_run_existing_scope(self):
        existing_settings = [{'scope': 'source.python', 'file_extensions': ['py']}]
        self.change_reset_mock.change_icon_file_extension_setting.return_value = (
            existing_settings
        )
        self.change_reset_mock.convert_to_list.return_value = ['py', 'pyw']

        self.command.run(MagicMock(), 'source.python', 'py,pyw')

        self.change_reset_mock.scope_exists.assert_called()

    def test_change_file_extension_command_input(self):
        args = {}
        result = self.command.input(args)
        self.assertIsInstance(
            result, change_file_extension.ChangeFileExtensionScopeInputHandler
        )

        args = {'change_file_extension_scope': 'source.python'}
        result = self.command.input(args)
        self.assertIsInstance(
            result, change_file_extension.ChangeFileExtensionExtsInputHandler
        )

        args = {
            'change_file_extension_scope': 'source.python',
            'change_file_extension_exts': 'py,pyw',
        }
        result = self.command.input(args)
        self.assertIsNone(result)


class TestChangeFileExtensionScopeInputHandler(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        patcher = patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension.sublime',
            self.sublime_mock,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.handler = change_file_extension.ChangeFileExtensionScopeInputHandler()

    def test_change_file_extension_scope_input_handler_placeholder(self):
        result = self.handler.placeholder()
        self.assertEqual(result, 'Type scope. E.g. source.js')
        self.sublime_mock.status_message.assert_called_with('Scope name to be used')

    def test_change_file_extension_scope_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, change_file_extension.ChangeFileExtensionExtsInputHandler
        )


class TestChangeFileExtensionExtsInputHandler(TestCase):
    def setUp(self):
        self.change_icon_file_extension = Mock(
            spec=change_file_extension.ChangeResetFileExtension
        )
        self.handler = change_file_extension.ChangeFileExtensionExtsInputHandler()

    def test_change_file_extension_exts_input_handler_placeholder(self):
        self.assertEqual(
            self.handler.placeholder(),
            'Type file extensions, separated by commma. E.g. js, cjs, mjs',
        )

    def test_change_file_extension_exts_input_handler_confirm(self):
        self.handler.confirm('test')
        self.assertEqual(self.handler.text, 'test')

    def test_change_file_extension_exts_input_handler_next_input_back(self):
        self.handler.text = 'back'
        result = self.handler.next_input({})
        self.assertIsInstance(result, sublime_plugin.BackInputHandler)


class TestResetFileExtensionCommand(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        self.sublime_plugin_mock = MagicMock()
        self.logger_mock = MagicMock()
        self.view_mock = MagicMock()
        self.change_reset_mock = MagicMock()

        patcher = patch.multiple(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension',
            sublime=self.sublime_mock,
            sublime_plugin=self.sublime_plugin_mock,
            logger=self.logger_mock,
            ChangeResetFileExtension=MagicMock(return_value=self.change_reset_mock),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.command = change_file_extension.ResetFileExtensionCommand(self.view_mock)

    def test_reset_file_extension_command_init(self):
        self.assertIsNotNone(self.command.change_reset_file_extension)
        self.assertEqual(self.command.view, self.view_mock)

    def test_reset_file_extension_command_run_all(self):
        mock_settings = [
            {'scope': 'source.python', 'file_extensions': ['py']},
            {'scope': 'source.js', 'file_extensions': ['js']},
        ]
        self.change_reset_mock.change_icon_file_extension_setting.return_value = (
            mock_settings
        )

        self.command.run(MagicMock(), 'All')

        self.change_reset_mock.reset_all_file_extensions.assert_called_with(
            mock_settings
        )
        self.change_reset_mock.reset_file_extension.assert_not_called()

    def test_reset_file_extension_command_run(self):
        mock_settings = [
            {'scope': 'source.python', 'file_extensions': ['py']},
            {'scope': 'source.js', 'file_extensions': ['js']},
        ]
        self.change_reset_mock.change_icon_file_extension_setting.return_value = (
            mock_settings
        )

        self.command.run(MagicMock(), 'source.python')

        self.change_reset_mock.reset_file_extension.assert_called_with(
            mock_settings, 'source.python'
        )
        self.change_reset_mock.reset_all_file_extensions.assert_not_called()

    def test_reset_file_extension_command_is_enabled(self):
        self.change_reset_mock.change_icon_file_extension_setting.return_value = [
            {'scope': 'source.python', 'file_extensions': ['py']}
        ]
        self.assertTrue(self.command.is_enabled())

    def test_reset_file_extension_command_is_enabled_none(self):
        self.change_reset_mock.change_icon_file_extension_setting.return_value = []
        self.assertFalse(self.command.is_enabled())

        self.change_reset_mock.change_icon_file_extension_setting.return_value = None
        self.assertFalse(self.command.is_enabled())

    def test_reset_file_extension_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(
            result, change_file_extension.ResetFileExtensionInputHandler
        )


class TestResetFileExtensionInputHandler(TestCase):
    def setUp(self):
        self.sublime_mock = MagicMock()
        self.logger_mock = MagicMock()
        self.view_mock = MagicMock()
        self.change_reset_mock = MagicMock()
        self.handler = change_file_extension.ResetFileExtensionInputHandler(
            self.change_reset_mock
        )

        class MockListInputItem:
            def __init__(self, text, value, annotation):
                self.text = text
                self.value = value
                self.annotation = annotation

        self.sublime_mock.ListInputItem = MockListInputItem

        patcher = patch.multiple(
            'Zukan Icon Theme.src.zukan_icon_theme.core.change_file_extension',
            sublime=self.sublime_mock,
            logger=self.logger_mock,
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.command = change_file_extension.ResetFileExtensionCommand(self.view_mock)

    def test_reset_file_extension_input_handler_init(self):
        self.assertIsNotNone(self.command.change_reset_file_extension)
        self.assertEqual(self.command.view, self.view_mock)

    def test_reset_file_extension_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'scope_name')

    def test_reset_file_extension_input_handler_placeholder(self):
        self.assertEqual(
            self.handler.placeholder(), 'List of changed icons file extensions'
        )

    def test_reset_file_extension_input_handler_list_items(self):
        mock_settings = [
            {'scope': 'source.python', 'file_extensions': ['py', 'pyw']},
            {'scope': 'source.js', 'file_extensions': ['js', 'jsx']},
        ]
        self.change_reset_mock.change_icon_file_extension_setting.return_value = (
            mock_settings
        )

        items = self.handler.list_items()

        # Assert sorting
        self.assertEqual(items[0], 'All')
        self.assertEqual(len(items), 3)

        self.assertEqual(items[1].text, 'source.js')
        self.assertEqual(items[1].value, 'source.js')
        self.assertEqual(items[1].annotation, 'js, jsx')

        self.assertEqual(items[2].text, 'source.python')
        self.assertEqual(items[2].value, 'source.python')
        self.assertEqual(items[2].annotation, 'py, pyw')

    def test_reset_file_extension_input_handler_list_items_none(self):
        self.change_reset_mock.change_icon_file_extension_setting.return_value = []

        with self.assertRaises(TypeError):
            self.handler.list_items()
