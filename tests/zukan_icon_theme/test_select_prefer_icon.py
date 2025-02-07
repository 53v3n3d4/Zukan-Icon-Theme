import importlib

from unittest import TestCase
from unittest.mock import Mock, patch

select_prefer_icon = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon'
)


class TestSelectRemovePreferIcon(TestCase):
    def setUp(self):
        self.zukan_theme = Mock(spec=select_prefer_icon.ZukanTheme)
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.is_zukan_listener_enabled'
        ) as mock_enabled:
            mock_enabled.return_value = True
            self.select_remove_prefer_icon = select_prefer_icon.SelectRemovePreferIcon(
                self.zukan_theme
            )

        self.sample_prefer_icon = {
            'theme1': {'icon': 'path1'},
            'theme2': {'icon': 'path2'},
            'theme3': {'icon': 'path3'},
        }

    def test_select_remove_prefer_icon_init(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.is_zukan_listener_enabled'
        ) as mock_enabled:
            mock_enabled.return_value = True
            icon_manager = select_prefer_icon.SelectRemovePreferIcon(self.zukan_theme)
            self.assertEqual(icon_manager.zukan_theme, self.zukan_theme)
            self.assertTrue(icon_manager.zukan_listener_enabled)

    def test_prefer_icon_setting(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.get_prefer_icon_settings'
        ) as mock_get:
            expected = {'theme1': {'icon': 'path1'}}
            mock_get.return_value = (None, expected)

            result = self.select_remove_prefer_icon.prefer_icon_setting()
            self.assertEqual(result, expected)

    def test_update_prefer_icon(self):
        with patch.object(
            self.select_remove_prefer_icon, '_save_prefer_icon_setting'
        ) as mock_save:
            new_prefer_icon = {'theme4': {'icon': 'path4'}}
            self.select_remove_prefer_icon.update_prefer_icon(
                self.sample_prefer_icon, new_prefer_icon
            )

            expected = {**self.sample_prefer_icon, **new_prefer_icon}
            mock_save.assert_called_once_with(expected)

    def test_save_prefer_icon_setting(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.set_save_settings'
        ) as mock_save:
            prefer_icon = {'theme1': {'icon': 'path1'}}
            self.select_remove_prefer_icon._save_prefer_icon_setting(prefer_icon)

            mock_save.assert_called_once_with(
                select_prefer_icon.ZUKAN_SETTINGS, 'prefer_icon', prefer_icon
            )

    def test_get_list_created_icons_themes(self):
        expected = ['theme1', 'theme2']
        self.zukan_theme.list_created_icons_themes.return_value = expected

        result = self.select_remove_prefer_icon.get_list_created_icons_themes()
        self.assertEqual(result, expected)
        self.zukan_theme.list_created_icons_themes.assert_called_once()

    def test_remove_prefer_icon(self):
        with patch.object(
            self.select_remove_prefer_icon, '_save_prefer_icon_setting'
        ) as mock_save:
            test_data = self.sample_prefer_icon.copy()
            self.select_remove_prefer_icon.remove_prefer_icon(test_data, 'theme2')

            expected = {'theme1': {'icon': 'path1'}, 'theme3': {'icon': 'path3'}}
            self.assertEqual(test_data, expected)
            mock_save.assert_called_once_with(expected)

    def test_remove_prefer_icon_logging(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.logger'
        ) as mock_logger:
            with patch.object(
                self.select_remove_prefer_icon, '_save_prefer_icon_setting'
            ):
                self.select_remove_prefer_icon.remove_prefer_icon(
                    self.sample_prefer_icon, 'theme2'
                )
                mock_logger.info.assert_called_once_with('reseting icon %s', 'theme2')

    def test_remove_all_prefer_icons(self):
        with patch.object(
            self.select_remove_prefer_icon, '_save_prefer_icon_setting'
        ) as mock_save:
            test_data = self.sample_prefer_icon.copy()
            self.select_remove_prefer_icon.remove_all_prefer_icons(test_data)

            self.assertEqual(test_data, {})
            mock_save.assert_called_once_with({})

    def test_remove_all_prefer_icons_logging(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.logger'
        ) as mock_logger:
            with patch.object(
                self.select_remove_prefer_icon, '_save_prefer_icon_setting'
            ):
                self.select_remove_prefer_icon.remove_all_prefer_icons(
                    self.sample_prefer_icon
                )
                mock_logger.info.assert_called_once_with('removing all prefer icons')


class TestSelectPreferIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.zukan_theme = Mock(spec=select_prefer_icon.ZukanTheme)
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.ZukanTheme'
        ) as mock_zukan:
            mock_zukan.return_value = self.zukan_theme
            self.command = select_prefer_icon.SelectPreferIconCommand(self.view)

        self.mock_select_remove_prefer_icon = Mock(
            spec=select_prefer_icon.SelectRemovePreferIcon
        )
        self.command.select_remove_prefer_icon = self.mock_select_remove_prefer_icon

        self.sample_prefer_icon = {
            'theme1': 'dark',
            'theme2': 'light',
            'theme3': 'dark',
        }

    def test_select_prefer_icon_command_init(self):
        self.assertIsNotNone(self.command.select_remove_prefer_icon)
        self.assertEqual(self.command.view, self.view)

    def test_select_prefer_icon_command_run(self):
        mock_prefer_icon = {'existing_theme': 'dark'}
        self.command.select_remove_prefer_icon.prefer_icon_setting.return_value = (
            mock_prefer_icon
        )

        self.command.run(
            edit=Mock(),
            select_prefer_icon_theme='test_theme',
            select_prefer_icon_version='dark',
        )

        self.command.select_remove_prefer_icon.update_prefer_icon.assert_called_once_with(
            mock_prefer_icon, {'test_theme': 'dark'}
        )

    def test_select_prefer_icon_command_run_empty(self):
        mock_prefer_icon = {'existing_theme': 'dark'}
        self.command.select_remove_prefer_icon.prefer_icon_setting.return_value = (
            mock_prefer_icon
        )

        self.command.run(
            edit=Mock(), select_prefer_icon_theme='', select_prefer_icon_version=''
        )

        self.command.select_remove_prefer_icon.update_prefer_icon.assert_not_called()

    def test_select_prefer_icon_command_is_enabled(self):
        self.command.select_remove_prefer_icon.get_list_created_icons_themes.return_value = [
            'theme1',
            'theme2',
        ]
        self.assertTrue(self.command.is_enabled())

    def test_select_prefer_icon_command_is_enabled_empty(self):
        self.command.select_remove_prefer_icon.get_list_created_icons_themes.return_value = []
        self.assertFalse(self.command.is_enabled())

    def test_select_prefer_icon_command_is_enabled_none(self):
        self.command.select_remove_prefer_icon.get_list_created_icons_themes.return_value = None
        self.assertFalse(self.command.is_enabled())

    def test_select_prefer_icon_command_input_theme(self):
        result = self.command.input({})
        self.assertIsInstance(
            result, select_prefer_icon.SelectPreferIconThemeInputHandler
        )

    def test_select_prefer_icon_command_input_version(self):
        result = self.command.input({'select_prefer_icon_theme': 'test_theme'})
        self.assertIsInstance(
            result, select_prefer_icon.SelectPreferIconVersionInputHandler
        )

    def test_select_prefer_icon_command_input_none(self):
        result = self.command.input(
            {
                'select_prefer_icon_theme': 'test_theme',
                'select_prefer_icon_version': 'dark',
            }
        )
        self.assertIsNone(result)


class TestSelectPreferIconThemeInputHandler(TestCase):
    def setUp(self):
        self.select_remove_prefer_icon = Mock(
            spec=select_prefer_icon.SelectRemovePreferIcon
        )
        self.handler = select_prefer_icon.SelectPreferIconThemeInputHandler(
            self.select_remove_prefer_icon
        )

    def test_select_prefer_icon_theme_input_handler_init(self):
        self.assertEqual(
            self.handler.select_remove_prefer_icon, self.select_remove_prefer_icon
        )

    def test_select_prefer_icon_theme_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'select_prefer_icon_theme')

    def test_select_prefer_icon_theme_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(placeholder, 'List of created themes')
            mock_status.assert_called_once_with('Select theme to prefer icon.')

    def test_select_prefer_icon_theme_input_handler_list_items(self):
        self.select_remove_prefer_icon.prefer_icon_setting.return_value = {
            'theme1': 'dark'
        }
        self.select_remove_prefer_icon.get_list_created_icons_themes.return_value = [
            'theme1',
            'theme2',
        ]

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.sublime.ListInputItem'
        ) as mock_item:
            mock_item.side_effect = lambda text, value, annotation: (
                text,
                value,
                annotation,
            )
            items = self.handler.list_items()

        self.assertEqual(len(items), 2)
        self.assertIn(('theme1', 'theme1', 'dark'), items)
        self.assertIn(('theme2', 'theme2', ''), items)

    def test_select_prefer_icon_theme_input_handler_list_items_none(self):
        self.select_remove_prefer_icon.get_list_created_icons_themes.return_value = None
        with self.assertRaises(TypeError):
            self.handler.list_items()

    def test_select_prefer_icon_theme_input_handler_next_input(self):
        result = self.handler.next_input({})
        self.assertIsInstance(
            result, select_prefer_icon.SelectPreferIconVersionInputHandler
        )


class TestSelectPreferIconVersionInputHandler(TestCase):
    def setUp(self):
        self.handler = select_prefer_icon.SelectPreferIconVersionInputHandler()

    def test_select_prefer_icon_version_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'select_prefer_icon_version')

    def test_select_prefer_icon_version_input_handler_placeholder(self):
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.sublime.status_message'
        ) as mock_status:
            placeholder = self.handler.placeholder()
            self.assertEqual(placeholder, 'Icon options: dark and light')
            mock_status.assert_called_once_with('Select prefer icon version.')

    def test_select_prefer_icon_version_input_handler_list_items(self):
        items = self.handler.list_items()
        self.assertEqual(items, ['dark', 'light'])


class TestRemovePreferIconCommand(TestCase):
    def setUp(self):
        self.view = Mock()
        self.zukan_theme = Mock(spec=select_prefer_icon.ZukanTheme)
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.core.select_prefer_icon.ZukanTheme'
        ) as mock_zukan:
            mock_zukan.return_value = self.zukan_theme
            self.command = select_prefer_icon.RemovePreferIconCommand(self.view)

        self.mock_select_remove_prefer_icon = Mock(
            spec=select_prefer_icon.SelectRemovePreferIcon
        )
        self.command.select_remove_prefer_icon = self.mock_select_remove_prefer_icon

        self.sample_prefer_icon = {
            'theme1': 'dark',
            'theme2': 'light',
            'theme3': 'dark',
        }

    def test_remove_prefer_icon_command_init(self):
        self.assertIsNotNone(self.command.select_remove_prefer_icon)
        self.assertEqual(self.command.view, self.view)

    def test_remove_prefer_icon_command_run(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = (
            self.sample_prefer_icon.copy()
        )

        self.command.run(edit=Mock(), select_prefer_icon_theme='theme2')

        self.mock_select_remove_prefer_icon.remove_prefer_icon.assert_called_once_with(
            self.sample_prefer_icon, 'theme2'
        )
        self.mock_select_remove_prefer_icon.remove_all_prefer_icons.assert_not_called()

    def test_remove_prefer_icon_command_run_all(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = (
            self.sample_prefer_icon.copy()
        )

        self.command.run(edit=Mock(), select_prefer_icon_theme='All')

        self.mock_select_remove_prefer_icon.remove_all_prefer_icons.assert_called_once_with(
            self.sample_prefer_icon
        )
        self.mock_select_remove_prefer_icon.remove_prefer_icon.assert_not_called()

    def test_remove_prefer_icon_command_run_theme_not_in_prefer_icon(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = (
            self.sample_prefer_icon.copy()
        )

        self.command.run(edit=Mock(), select_prefer_icon_theme='non_existent_theme')

        self.mock_select_remove_prefer_icon.remove_prefer_icon.assert_not_called()
        self.mock_select_remove_prefer_icon.remove_all_prefer_icons.assert_not_called()

    def test_remove_prefer_icon_command_run_empty(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = {}

        self.command.run(edit=Mock(), select_prefer_icon_theme='theme1')

        self.mock_select_remove_prefer_icon.remove_prefer_icon.assert_not_called()
        self.mock_select_remove_prefer_icon.remove_all_prefer_icons.assert_not_called()

    def test_remove_prefer_icon_command_is_enabled(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = (
            self.sample_prefer_icon
        )
        self.assertTrue(self.command.is_enabled())

    def test_remove_prefer_icon_command_is_enabled_empty(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = {}
        self.assertFalse(self.command.is_enabled())

    def test_remove_prefer_icon_command_is_enabled_none(self):
        self.mock_select_remove_prefer_icon.prefer_icon_setting.return_value = None
        self.assertFalse(self.command.is_enabled())

    def test_remove_prefer_icon_command_input(self):
        result = self.command.input({})
        self.assertIsInstance(result, select_prefer_icon.RemovePreferIconInputHandler)


class TestRemovePreferIconInputHandler(TestCase):
    def setUp(self):
        self.select_remove_prefer_icon = Mock(
            spec=select_prefer_icon.SelectRemovePreferIcon
        )
        self.handler = select_prefer_icon.RemovePreferIconInputHandler(
            self.select_remove_prefer_icon
        )

        self.sample_prefer_icon = {
            'theme1': 'dark',
            'theme2': 'light',
            'theme3': 'dark',
        }

    def test_remove_prefer_icon_theme_input_handler_init(self):
        self.assertEqual(
            self.handler.select_remove_prefer_icon, self.select_remove_prefer_icon
        )

    def test_remove_prefer_icon_input_handler_name(self):
        self.assertEqual(self.handler.name(), 'select_prefer_icon_theme')

    def test_remove_prefer_icon_input_handler_placeholder(self):
        self.assertEqual(self.handler.placeholder(), 'List of preferred icons')

    def test_remove_prefer_icon_input_handler_list_items(self):
        self.select_remove_prefer_icon.prefer_icon_setting.return_value = (
            self.sample_prefer_icon
        )

        with patch('sublime.ListInputItem') as mock_item:
            mock_item.side_effect = lambda text, value, annotation: (
                text,
                value,
                annotation,
            )
            items = self.handler.list_items()

        self.assertEqual(len(items), 4)
        self.assertEqual(items[0], 'All')
        self.assertIn(('theme1', 'theme1', 'dark'), items)
        self.assertIn(('theme2', 'theme2', 'light'), items)
        self.assertIn(('theme3', 'theme3', 'dark'), items)

    def test_remove_prefer_icon_input_handler_list_items_empty(self):
        self.select_remove_prefer_icon.prefer_icon_setting.return_value = {}

        with self.assertRaises(TypeError):
            self.handler.list_items()

    def test_remove_prefer_icon_input_handler_list_items_none(self):
        self.select_remove_prefer_icon.prefer_icon_setting.return_value = None

        with self.assertRaises(TypeError):
            self.handler.list_items()
