import importlib

from unittest import TestCase
from unittest.mock import Mock, patch

disable_icon = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.disable_icon'
)


class TestDisableEnableIcon(TestCase):
    def setUp(self):
        self.zukan_syntax = Mock(spec=disable_icon.ZukanSyntax)
        self.disable_enable_icon = disable_icon.DisableEnableIcon(self.zukan_syntax)

    @patch.object(disable_icon, 'read_pickle_data')
    def test_zukan_icons_data(self, mock_read):
        mock_data = [{'name': 'ATest'}, {'name': 'ATest-1'}]
        mock_read.return_value = mock_data
        result = self.disable_enable_icon.zukan_icons_data()
        self.assertEqual(result, mock_data)

    @patch.object(disable_icon, 'get_ignored_icon_settings')
    def test_ignored_icon_setting(self, mock_get):
        mock_ignored = ['atest', 'atest1']
        mock_get.return_value = mock_ignored
        result = self.disable_enable_icon.ignored_icon_setting()
        self.assertEqual(result, mock_ignored)

    def test_get_list_all_icons_syntaxes(self):
        mock_icons = [{'name': 'ATest'}, {'name': 'ATest-1'}]
        mock_syntaxes = [
            {'name': 'ATest', 'syntax': 'ATest'},
            {'name': 'ATest-1', 'syntax': 'ATest-1'},
        ]
        self.zukan_syntax.get_list_icons_syntaxes.return_value = mock_syntaxes
        result = self.disable_enable_icon.get_list_all_icons_syntaxes(mock_icons)
        self.assertEqual(result, mock_syntaxes)

    @patch.object(disable_icon, 'read_pickle_data')
    @patch.object(disable_icon, 'get_ignored_icon_settings')
    def test_get_list_not_ignored_icons(self, mock_ignored, mock_read):
        mock_icons = [{'name': 'ATest-1'}, {'name': 'ATest-2'}]
        mock_read.return_value = mock_icons
        mock_ignored.return_value = ['ATest-2']
        mock_syntaxes = [
            {'name': 'ATest-1', 'syntax': 'ATest-1'},
            {'name': 'ATest-2', 'syntax': 'ATest-2'},
        ]
        self.zukan_syntax.get_list_icons_syntaxes.return_value = mock_syntaxes

        result = self.disable_enable_icon.get_list_not_ignored_icons()
        self.assertEqual(result, ['ATest-1'])

    @patch.object(disable_icon, 'set_save_settings')
    def test_add_to_ignored_icon(self, mock_save):
        ignored_list = ['atest']
        self.disable_enable_icon.add_to_ignored_icon(ignored_list, 'atest1')
        mock_save.assert_called_once()
        self.assertEqual(ignored_list, ['atest', 'atest1'])

    @patch.object(disable_icon, 'set_save_settings')
    def test_save_ignored_icon_setting(self, mock_save):
        ignored_list = ['atest2', 'atest1']
        self.disable_enable_icon._save_ignored_icon_setting(ignored_list)
        mock_save.assert_called_once_with(
            disable_icon.ZUKAN_SETTINGS, 'ignored_icon', ['atest1', 'atest2']
        )

    @patch.object(disable_icon, 'logger')
    def test_message_icon_tag_with_tag(self, mock_logger):
        with patch.object(
            disable_icon,
            'ICONS_TAGS',
            ['test_tag'],
        ):
            self.disable_enable_icon.message_icon_tag('test_tag')
            mock_logger.info.assert_called_with('icons with %s tag ignored', 'test_tag')

    @patch.object(disable_icon, 'logger')
    def test_message_icon_tag_without_tag(self, mock_logger):
        with patch.object(
            disable_icon,
            'ICONS_TAGS',
            [],
        ):
            self.disable_enable_icon.message_icon_tag('test_icon')
            mock_logger.info.assert_called_with('%s icon ignored', 'test_icon')

    @patch.object(disable_icon, 'set_save_settings')
    @patch.object(disable_icon, 'logger')
    def test_enable_ignored_icon(self, mock_logger, mock_save):
        ignored_list = ['atest1', 'atest2']
        self.disable_enable_icon.enable_ignored_icon(ignored_list, 'atest1')
        mock_save.assert_called_once()
        mock_logger.info.assert_called_with('enabling %s icon', 'atest1')

    @patch.object(disable_icon, 'set_save_settings')
    @patch.object(disable_icon, 'logger')
    def test_enable_all_ignored_icons(self, mock_logger, mock_save):
        ignored_list = ['atest1', 'atest2']
        self.disable_enable_icon.enable_all_ignored_icons(ignored_list)
        mock_save.assert_called_once_with(
            disable_icon.ZUKAN_SETTINGS, 'ignored_icon', []
        )
        mock_logger.info.assert_called_with('enabling all icons')


class TestDisableIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = disable_icon.DisableIconCommand(self.view)

    def test_disbale_icon_command_init(self):
        self.assertIsInstance(self.command.zukan_syntax, disable_icon.ZukanSyntax)
        self.assertIsInstance(
            self.command.disable_enable_icon, disable_icon.DisableEnableIcon
        )

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    @patch.object(disable_icon.DisableEnableIcon, 'add_to_ignored_icon')
    @patch.object(disable_icon.DisableEnableIcon, 'message_icon_tag')
    def test_disbale_icon_command_run(self, mock_message, mock_add, mock_ignored):
        mock_ignored.return_value = ['atest1']
        self.command.run(None, icon_name='atest2')
        mock_add.assert_called_once_with(['atest1'], 'atest2')
        mock_message.assert_called_once_with('atest2')

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    @patch.object(disable_icon.DisableEnableIcon, 'add_to_ignored_icon')
    def test_disbale_icon_command_run_ignored(self, mock_add, mock_ignored):
        mock_ignored.return_value = ['atest1']
        self.command.run(None, icon_name='atest1')
        mock_add.assert_not_called()

    @patch.object(disable_icon.DisableEnableIcon, 'get_list_not_ignored_icons')
    def test_disbale_icon_command_is_enabled(self, mock_list):
        mock_list.return_value = ['atest1', 'atest2']
        self.assertTrue(self.command.is_enabled())

    @patch.object(disable_icon.DisableEnableIcon, 'get_list_not_ignored_icons')
    def test_disbale_icon_command_is_enabled_none(self, mock_list):
        mock_list.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_disbale_icon_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, disable_icon.DisableIconInputHandler)


class TestDisableIconInputHandler(TestCase):
    def setUp(self):
        self.disable_enable_icon = Mock()
        self.handler = disable_icon.DisableIconInputHandler(self.disable_enable_icon)

    def test_disbale_icon_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'icon_name')

    def test_disbale_icon_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of icons')

    @patch.object(
        disable_icon,
        'ICONS_TAGS',
        ['tag1', 'tag2'],
    )
    def test_disbale_icon_input_handler_list_items(self):
        self.disable_enable_icon.get_list_not_ignored_icons.return_value = [
            'atest3',
            'atest4',
        ]
        expected = sorted(['tag1', 'tag2', 'atest3', 'atest4'], key=lambda x: x.upper())
        self.assertEqual(self.handler.list_items(), expected)

    def test_disbale_icon_input_handler_list_items_none(self):
        self.disable_enable_icon.get_list_not_ignored_icons.return_value = None
        with self.assertRaises(TypeError):
            self.handler.list_items()


class TestEnableIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.command = disable_icon.EnableIconCommand(self.view)

    def test_enable_icon_command_init(self):
        self.assertIsInstance(self.command.zukan_syntax, disable_icon.ZukanSyntax)
        self.assertIsInstance(
            self.command.disable_enable_icon, disable_icon.DisableEnableIcon
        )

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    @patch.object(disable_icon.DisableEnableIcon, 'enable_all_ignored_icons')
    def test_enable_icon_command_run_all(self, mock_enable_all, mock_ignored):
        mock_ignored.return_value = ['atest1', 'atest2']
        self.command.run(None, icon_name='All')
        mock_enable_all.assert_called_once_with(['atest1', 'atest2'])

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    @patch.object(disable_icon.DisableEnableIcon, 'enable_ignored_icon')
    def test_enable_icon_command_run(self, mock_enable, mock_ignored):
        mock_ignored.return_value = ['atest3', 'atest4']
        self.command.run(None, icon_name='atest3')
        mock_enable.assert_called_once_with(['atest3', 'atest4'], 'atest3')

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    def test_enable_icon_command_run_no_ignored_icons(self, mock_ignored):
        mock_ignored.return_value = []
        self.command.run(None, icon_name='atest')

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    def test_enable_icon_command_is_enabled(self, mock_ignored):
        mock_ignored.return_value = ['atest1']
        self.assertTrue(self.command.is_enabled())

    @patch.object(disable_icon.DisableEnableIcon, 'ignored_icon_setting')
    def test_enable_icon_command_is_enabled_none(self, mock_ignored):
        mock_ignored.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_enable_icon_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, disable_icon.EnableIconInputHandler)


class TestEnableIconInputHandler(TestCase):
    def setUp(self):
        self.disable_enable_icon = Mock()
        self.handler = disable_icon.EnableIconInputHandler(self.disable_enable_icon)

    def test_enable_icon_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'icon_name')

    def test_enable_icon_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of ignored icons')

    def test_enable_icon_input_handler_list_items(self):
        self.disable_enable_icon.ignored_icon_setting.return_value = [
            'atest2',
            'atest1',
        ]
        expected = ['All', 'atest1', 'atest2']
        self.assertEqual(self.handler.list_items(), expected)

    def test_enable_icon_input_handler_list_items_none(self):
        self.disable_enable_icon.ignored_icon_setting.return_value = []
        with self.assertRaises(TypeError):
            self.handler.list_items()
