import importlib
import sublime_plugin

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

create_custom_icon = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon'
)


class TestCreateDeleteCustomIcon(TestCase):
    def setUp(self):
        self.preferences_file = 'test_preferences.sublime-settings'
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.is_zukan_listener_enabled'
        ) as mock_listener:
            mock_listener.return_value = True
            self.icon_handler = create_custom_icon.CreateDeleteCustomIcon(
                self.preferences_file
            )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.is_zukan_listener_enabled'
    )
    def test_change_reset_file_extension_init(self, mock_listener):
        self.assertEqual(
            self.icon_handler.zukan_preferences_file, self.preferences_file
        )
        self.assertEqual(
            self.icon_handler.zukan_pkg_icons_path,
            create_custom_icon.ZUKAN_PKG_ICONS_PATH,
        )
        self.assertIsInstance(self.icon_handler.zukan_listener_enabled, bool)

    def test_convert_to_list(self):
        extensions = 'py, js, html'
        expected = ['py', 'js', 'html']
        result = self.icon_handler.convert_to_list(extensions)
        self.assertEqual(result, expected)

        self.assertEqual(self.icon_handler.convert_to_list(''), [''])

        self.assertEqual(self.icon_handler.convert_to_list('py'), ['py'])

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.error_message'
    )
    def test_message_required_name(self, mock_error):
        self.icon_handler.message_required_name('')
        mock_error.assert_called_once_with('Name input is required')

        mock_error.reset_mock()
        self.icon_handler.message_required_name('valid_name')
        mock_error.assert_not_called()

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.error_message'
    )
    def test_png_exists(self, mock_error, mock_exists):
        mock_exists.return_value = False
        custom_icon = 'atest'
        self.icon_handler.png_exists(custom_icon)
        expected_message = (
            f'{custom_icon} icon PNGs not found.\n\n'
            f'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {self.icon_handler.zukan_pkg_icons_path}'
        )
        mock_error.assert_called_once_with(expected_message)

        mock_error.reset_mock()
        mock_exists.return_value = True
        self.icon_handler.png_exists(custom_icon)
        mock_error.assert_not_called()

    def test_remove_empty_keys(self):
        test_data = [
            {'name': 'ATest-1', 'icon': 'atest1', 'syntax_name': '', 'scope': None},
            {
                'name': 'ATest-2',
                'icon': 'atest2',
                'syntax_name': 'ATest-2',
                'scope': 'source.atest2',
            },
        ]
        expected = [
            {'name': 'ATest-1', 'icon': 'atest1'},
            {
                'name': 'ATest-2',
                'icon': 'atest2',
                'syntax_name': 'ATest-2',
                'scope': 'source.atest2',
            },
        ]
        result = self.icon_handler.remove_empty_keys(test_data)
        self.assertEqual(result, expected)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.set_save_settings'
    )
    def test_delete_custom_icon(self, mock_save):
        test_data = [
            {'name': 'ATest-1', 'icon': 'atest1'},
            {'name': 'ATest-2', 'icon': 'atest2'},
        ]

        self.icon_handler.delete_custom_icon(test_data, 'ATest-1')
        mock_save.assert_called_once_with(
            self.preferences_file,
            'create_custom_icon',
            [{'name': 'ATest-2', 'icon': 'atest2'}],
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.set_save_settings'
    )
    def test_delete_all_customs_icons(self, mock_save):
        test_data = [
            {'name': 'ATest-1', 'icon': 'atest1'},
            {'name': 'ATest-2', 'icon': 'atest2'},
        ]

        self.icon_handler.delete_all_customs_icons(test_data)
        mock_save.assert_called_once_with(
            self.preferences_file, 'create_custom_icon', []
        )

    def test_custom_icon_name_exists(self):
        existing_data = {
            'name': 'ATest',
            'icon': 'previous_icon',
            'syntax_name': 'previous_syntax',
            'scope': 'previous_scope',
            'contexts_scope': 'previous_context',
            'file_extensions': ['txt', 'md'],
        }

        custom_icon_data = {
            'name': 'ATest',
            'icon': 'new_icon',
            'syntax_name': 'new_syntax',
            'scope': 'new_scope',
            'contexts_scope': 'new_context',
        }

        self.icon_handler.custom_icon_name_exists(
            existing_data,
            custom_icon_data,
            'new_icon',
            'new_syntax',
            'new_scope',
            'new_context',
            ['json', 'yaml'],
        )

        self.assertEqual(existing_data['icon'], 'new_icon')
        self.assertEqual(existing_data['syntax_name'], 'new_syntax')
        self.assertEqual(existing_data['scope'], 'new_scope')
        self.assertEqual(existing_data['contexts_scope'], 'new_context')
        self.assertEqual(
            sorted(existing_data['file_extensions']),
            sorted(['txt', 'md', 'json', 'yaml']),
        )


class TestCreateCustomIconCommand(TestCase):
    def setUp(self):
        self.view = MagicMock()
        mock_creator = MagicMock()

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.CreateDeleteCustomIcon',
            return_value=mock_creator,
        ):
            self.command = create_custom_icon.CreateCustomIconCommand(self.view)
            self.mock_creator = mock_creator

    def test_create_custom_icon_command_init(self):
        command = create_custom_icon.CreateCustomIconCommand(self.view)
        self.assertIsInstance(
            command.create_delete_custom_icon, create_custom_icon.CreateDeleteCustomIcon
        )
        self.assertEqual(command.view, self.view)

    def test_create_custom_icon_command_run_empty(self):
        self.mock_creator.create_custom_icon_setting.return_value = []
        self.mock_creator.convert_to_list.return_value = ['pip.conf']

        test_data = {
            'create_custom_icon_name': 'Pip',
            'create_custom_icon_file': 'pip',
            'create_custom_icon_syntax': 'INI (Pip)',
            'create_custom_icon_scope': 'source.ini.pip',
            'create_custom_icon_extensions': 'pip.conf',
            'create_custom_icon_contexts': 'source.ini',
        }

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.set_save_settings'
        ) as mock_save:
            self.command.run(MagicMock(), **test_data)

            self.mock_creator.message_required_name.assert_called_once_with('Pip')
            self.mock_creator.png_exists.assert_called_once_with('pip')
            self.mock_creator.remove_empty_keys.assert_called_once()
            mock_save.assert_called_once()

    def test_create_custom_icon_command_run(self):
        existing_data = [
            {
                'name': 'ATest',
                'icon': 'atest',
                'syntax_name': 'ATest',
                'scope': 'source.atest',
                'file_extensions': ['abc'],
                'contexts_scope': 'source.yaml',
            }
        ]

        self.mock_creator.create_custom_icon_setting.return_value = existing_data
        self.mock_creator.convert_to_list.return_value = ['pip.conf']

        test_data = {
            'create_custom_icon_name': 'Pip',
            'create_custom_icon_file': 'pip',
            'create_custom_icon_syntax': 'INI (Pip)',
            'create_custom_icon_scope': 'source.ini.pip',
            'create_custom_icon_extensions': 'pip.conf',
            'create_custom_icon_contexts': 'source.ini',
        }

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.set_save_settings'
        ):
            self.command.run(MagicMock(), **test_data)

            self.mock_creator.custom_icon_name_exists.assert_called_once()
            self.mock_creator.custom_icon_name_not_exists.assert_called_once()

    def test_create_custom_icon_run_empty_name(self):
        test_data = {
            'create_custom_icon_name': '',
            'create_custom_icon_file': 'pip',
            'create_custom_icon_syntax': 'INI (Pip)',
            'create_custom_icon_scope': 'source.ini.pip',
            'create_custom_icon_extensions': 'pip.conf',
            'create_custom_icon_contexts': 'source.ini',
        }

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.set_save_settings'
        ) as mock_save:
            self.command.run(MagicMock(), **test_data)

            self.mock_creator.message_required_name.assert_called_once_with('')
            mock_save.assert_not_called()

    def test_create_custom_icon_command_input(self):
        self.assertIsInstance(
            self.command.input({}), create_custom_icon.CreateCustomIconNameInputHandler
        )

        self.assertIsInstance(
            self.command.input({'create_custom_icon_name': 'ATest'}),
            create_custom_icon.CreateCustomIconFileInputHandler,
        )

        self.assertIsInstance(
            self.command.input(
                {'create_custom_icon_name': 'ATest', 'create_custom_icon_file': 'atest'}
            ),
            create_custom_icon.CreateCustomIconSyntaxInputHandler,
        )

        self.assertIsInstance(
            self.command.input(
                {
                    'create_custom_icon_name': 'ATest',
                    'create_custom_icon_file': 'atest',
                    'create_custom_icon_syntax': 'ATest',
                }
            ),
            create_custom_icon.CreateCustomIconScopeInputHandler,
        )

        self.assertIsInstance(
            self.command.input(
                {
                    'create_custom_icon_name': 'ATest',
                    'create_custom_icon_file': 'atest',
                    'create_custom_icon_syntax': 'ATest',
                    'create_custom_icon_scope': 'source.atest',
                }
            ),
            create_custom_icon.CreateCustomIconExtensionsInputHandler,
        )

        self.assertIsInstance(
            self.command.input(
                {
                    'create_custom_icon_name': 'ATest',
                    'create_custom_icon_file': 'atest',
                    'create_custom_icon_syntax': 'ATest',
                    'create_custom_icon_scope': 'source.atest',
                    'create_custom_icon_extensions': 'abc',
                }
            ),
            create_custom_icon.CreateCustomIconContextsInputHandler,
        )

    def test_create_custom_icon_command_input_none(self):
        result = self.command.input(
            {
                'create_custom_icon_name': 'ATest',
                'create_custom_icon_file': 'atest',
                'create_custom_icon_syntax': 'ATest',
                'create_custom_icon_scope': 'source.atest',
                'create_custom_icon_extensions': 'abc',
                'create_custom_icon_contexts': 'source.yaml',
            }
        )
        self.assertIsNone(result)


class TestCreateCustomIconNameInputHandler(TestCase):
    def setUp(self):
        self.view = MagicMock()

        self.handler = create_custom_icon.CreateCustomIconNameInputHandler()

    def test_create_custom_icon_name_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(placeholder, 'Type a Name. E.g. Pip')
            mock_status.assert_called_once_with('Name is required field.')

    def test_create_custom_icon_name_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, create_custom_icon.CreateCustomIconFileInputHandler
        )


class TestCreateCustomIconFileInputHandler(TestCase):
    def setUp(self):
        self.view = MagicMock()

        self.handler = create_custom_icon.CreateCustomIconFileInputHandler()

    def test_create_custom_icon_file_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(
                placeholder, 'Type icon file name, without extension. E.g. pip'
            )
            mock_status.assert_called_once_with('Hit enter if field not needed')

    def test_create_custom_icon_file_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, create_custom_icon.CreateCustomIconSyntaxInputHandler
        )


class TestCreateCustomIconSyntaxInputHandler(TestCase):
    def setUp(self):
        self.view = MagicMock()

        self.handler = create_custom_icon.CreateCustomIconSyntaxInputHandler()

    def test_create_custom_icon_syntax_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(placeholder, 'Type syntax name. E.g. INI (Pip)')
            mock_status.assert_called_once_with('Type syntax name. E.g. INI (Pip)')

    def test_create_custom_icon_syntax_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, create_custom_icon.CreateCustomIconScopeInputHandler
        )


class TestCreateCustomIconScopeInputHandler(TestCase):
    def setUp(self):
        self.view = MagicMock()

        self.handler = create_custom_icon.CreateCustomIconScopeInputHandler()

    def test_create_custom_icon_scope_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(placeholder, 'Type scope. E.g. source.ini.pip')
            mock_status.assert_called_once_with('Type scope. E.g. source.ini.pip')

    def test_create_custom_icon_scope_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, create_custom_icon.CreateCustomIconExtensionsInputHandler
        )


class TestCreateCustomIconExtensionsInputHandler(TestCase):
    def setUp(self):
        self.view = MagicMock()

        self.handler = create_custom_icon.CreateCustomIconExtensionsInputHandler()

    def test_create_custom_icon_extensions_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(
                placeholder, 'Type file extensions, separated by commas. E.g. pip.conf'
            )
            mock_status.assert_called_once_with(
                'Type file extensions, separated by commas. E.g. pip.conf'
            )

    def test_create_custom_icon_extensions_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, create_custom_icon.CreateCustomIconContextsInputHandler
        )


class TestCreateCustomIconContextsInputHandler(TestCase):
    def setUp(self):
        self.create_custom_icon = Mock(spec=create_custom_icon.CreateDeleteCustomIcon)
        self.handler = create_custom_icon.CreateCustomIconContextsInputHandler()

    def test_create_custom_icon_contexts_input_handler_placeholder(self):
        self.assertEqual(
            self.handler.placeholder(),
            'Type contexts main. E.g. source.ini',
        )

    def test_create_custom_icon_contexts_input_handler_confirm(self):
        self.handler.confirm('test')
        self.assertEqual(self.handler.text, 'test')

    def test_create_custom_icon_contexts_input_handler_next_input_back(self):
        self.handler.text = 'back'
        result = self.handler.next_input({})
        self.assertIsInstance(result, sublime_plugin.BackInputHandler)


class TestDeleteCustomIconCommand(TestCase):
    def setUp(self):
        self.view = MagicMock()
        mock_creator = MagicMock()

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.CreateDeleteCustomIcon',
            return_value=mock_creator,
        ):
            self.command = create_custom_icon.DeleteCustomIconCommand(self.view)
            self.mock_creator = mock_creator

    def test_delete_custom_icon_command_init(self):
        command = create_custom_icon.DeleteCustomIconCommand(self.view)
        self.assertIsInstance(
            command.create_delete_custom_icon, create_custom_icon.CreateDeleteCustomIcon
        )
        self.assertEqual(command.view, self.view)

    def test_delete_custom_icon_command_run(self):
        test_icons = [{'name': 'ATest-1'}, {'name': 'ATest-2'}]
        self.mock_creator.create_custom_icon_setting.return_value = test_icons

        self.command.run(MagicMock(), name='ATest-1')

        self.mock_creator.delete_custom_icon.assert_called_once_with(
            test_icons, 'ATest-1'
        )
        self.mock_creator.delete_all_customs_icons.assert_not_called()

    def test_delete_custom_icon_command_run_all(self):
        test_icons = [{'name': 'ATest-1'}, {'name': 'ATest-2'}]
        self.mock_creator.create_custom_icon_setting.return_value = test_icons

        self.command.run(MagicMock(), name='All')

        self.mock_creator.delete_all_customs_icons.assert_called_once_with(test_icons)
        self.mock_creator.delete_custom_icon.assert_not_called()

    def test_delete_custom_icon_command_is_enabled(self):
        self.mock_creator.create_custom_icon_setting.return_value = [
            {'name': 'ATest-1'}
        ]

        self.assertTrue(self.command.is_enabled())

    def test_delete_custom_icon_command_is_enabled_empty(self):
        self.mock_creator.create_custom_icon_setting.return_value = []

        self.assertFalse(self.command.is_enabled())

    def test_delete_custom_icon_command_is_enabled_none(self):
        self.mock_creator.create_custom_icon_setting.return_value = None

        self.assertFalse(self.command.is_enabled())

    def test_delete_custom_icon_command_input(self):
        input_handler = self.command.input({})
        self.assertIsInstance(
            input_handler, create_custom_icon.DeleteCustomIconInputHandler
        )


class TestDeleteCustomIconInputHandler(TestCase):
    def setUp(self):
        self.mock_creator = MagicMock()
        self.handler = create_custom_icon.DeleteCustomIconInputHandler(
            self.mock_creator
        )

    def test_delete_custom_icon_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'name')

    def test_delete_custom_icon_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of customized icons')

    def test_delete_custom_icon_input_handler_list_items(self):
        test_icons = [
            {'name': 'ATest-2'},
            {'name': 'ATest-1'},
            {'name': 'ATest-3'},
        ]
        self.mock_creator.create_custom_icon_setting.return_value = test_icons

        expected_list = ['All', 'ATest-1', 'ATest-2', 'ATest-3']

        result = self.handler.list_items()
        self.assertEqual(result, expected_list)

    def test_delete_custom_icon_input_handler_list_items_none(self):
        self.mock_creator.create_custom_icon_setting.return_value = []

        with self.assertRaises(TypeError):
            self.handler.list_items()

    def test_delete_custom_icon_input_handler_list_items_missing_names(self):
        test_icons = [
            {'name': 'ATest-1'},
            {'icon': 'atest2'},  # Missing name
            {'name': 'ATest-3'},
        ]
        self.mock_creator.create_custom_icon_setting.return_value = test_icons

        expected_list = ['All', 'ATest-1', 'ATest-3']

        result = self.handler.list_items()
        self.assertEqual(result, expected_list)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.create_custom_icon.logger')
    def test_delete_custom_icon_input_handler_list_items_logging(self, mock_logger):
        self.mock_creator.create_custom_icon_setting.return_value = []

        with self.assertRaises(TypeError):
            self.handler.list_items()

        mock_logger.info.assert_called_once_with(
            'customized icon not found, list is empty.'
        )
