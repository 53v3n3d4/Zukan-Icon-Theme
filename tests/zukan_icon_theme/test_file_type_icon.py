import importlib
import os

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

file_type_icon = importlib.import_module('Zukan Icon Theme.file_type_icon')


class TestFileTypeIcon(TestCase):
    def setUp(self):
        self.original_path_exists = os.path.exists

    def tearDown(self):
        os.path.exists = self.original_path_exists

    def test_zukan_listener_enabled(self):
        with patch(
            'Zukan Icon Theme.file_type_icon.is_zukan_listener_enabled',
            return_value=True,
        ):
            mock_module = MagicMock()
            mock_listener = MagicMock()

            with patch.dict(
                'sys.modules',
                {
                    'zukan_icon_theme': mock_module,
                    'zukan_icon_theme.core': mock_module,
                    'zukan_icon_theme.core.listeners': mock_module,
                    'zukan_icon_theme.core.listeners.SchemeThemeListener': mock_listener,
                },
            ):
                try:
                    from zukan_icon_theme.core.listeners import SchemeThemeListener  # noqa 401

                    listener_imported = True
                except ImportError as e:
                    print(f'Import failed with error: {e}')
                    listener_imported = False

                self.assertTrue(listener_imported)

    @patch('os.path.exists')
    def test_zukan_listener_disabled(self, mock_exists):
        with patch(
            'Zukan Icon Theme.file_type_icon.is_zukan_listener_enabled',
            return_value=False,
        ):
            try:
                from .src.zukan_icon_theme.core.listeners import SchemeThemeListener  # noqa 401

                listener_imported = True
            except ImportError:
                listener_imported = False

            self.assertFalse(listener_imported)

    @patch('os.path.exists')
    def test_move_folders(self, mock_exists):
        mock_exists.return_value = False

        mock_move_folder = MagicMock()
        with patch(
            'Zukan Icon Theme.file_type_icon.MoveFolder', return_value=mock_move_folder
        ):
            if not os.path.exists(file_type_icon.ZUKAN_ICONS_DATA_FILE):
                mock_move_folder.move_folders()

            mock_move_folder.move_folders.assert_called_once()

    @patch('os.path.exists')
    def test_move_folders_when_data_file_exists(self, mock_exists):
        mock_exists.return_value = True

        mock_move_folder = MagicMock()
        with patch(
            'Zukan Icon Theme.file_type_icon.MoveFolder', return_value=mock_move_folder
        ):
            if not os.path.exists(file_type_icon.ZUKAN_ICONS_DATA_FILE):
                mock_move_folder.move_folders()

            mock_move_folder.move_folders.assert_not_called()

    def test_is_zukan_listener_enabled(self):
        result = file_type_icon.is_zukan_listener_enabled()
        self.assertIsInstance(result, bool)


class TestPluginLoaded(TestCase):
    def setUp(self):
        self.mock_event_bus = MagicMock()
        self.mock_sublime = MagicMock()

    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    @patch('Zukan Icon Theme.file_type_icon.get_sidebar_bgcolor')
    def test_get_sidebar_bgcolor(self, mock_get_bgcolor, mock_get_theme, mock_timeout):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        file_type_icon.plugin_loaded()
        mock_get_theme.assert_called_once()
        mock_timeout.assert_called_once()
        mock_timeout.call_args[0][0]()
        mock_get_bgcolor.assert_called_once_with('Treble Adaptive.sublime-theme')

    @patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info')
    def test_cached_theme_info_deleted(self, mock_delete_cache):
        file_type_icon.plugin_loaded()
        mock_delete_cache.assert_called_once()

    def test_zukan_listener_disabled(self):
        # fmt: off
        with patch('os.path.exists') as mock_exists, \
             patch(
                'Zukan Icon Theme.file_type_icon.zukan_listener_enabled', False
             ), \
             patch('Zukan Icon Theme.file_type_icon.get_theme_name'), \
             patch('sublime.set_timeout'), \
             patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info'):
             # fmt: on

            file_type_icon.plugin_loaded()
            calls = mock_exists.call_args_list
            self.assertTrue(
                all(
                    file_type_icon.ZUKAN_PKG_ICONS_PREFERENCES_PATH not in str(call)
                    and file_type_icon.ZUKAN_PKG_ICONS_SYNTAXES_PATH not in str(call)
                    for call in calls
                )
            )

    @patch('Zukan Icon Theme.file_type_icon.ZukanIconFiles')
    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    @patch('os.path.exists')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.InstallEvent')
    @patch('Zukan Icon Theme.file_type_icon.EventBus')
    @patch('Zukan Icon Theme.file_type_icon.UpgradePlugin')
    def test_new_install_when_icons_preferences_missing(
        self,
        mock_upgrade_plugin,
        mock_event_bus,
        mock_install_event,
        mock_exists,
        mock_get_theme,
        mock_delete_cache,
        mock_timeout,
        mock_zukan_files,
    ):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        mock_exists.side_effect = lambda path: {
            file_type_icon.ZUKAN_PKG_ICONS_PREFERENCES_PATH: False,
            file_type_icon.ZUKAN_PKG_ICONS_SYNTAXES_PATH: True,
        }.get(path, True)
        mock_install = MagicMock()
        mock_install_event.return_value = mock_install
        mock_upgrade = MagicMock()
        type(mock_upgrade).version_json_file = PropertyMock(return_value='1.0.0')
        mock_upgrade_plugin.return_value = mock_upgrade
        mock_zukan_files_instance = MagicMock()
        mock_zukan_files.return_value = mock_zukan_files_instance

        file_type_icon.plugin_loaded()

        mock_install.new_install.assert_called_once()

    @patch('Zukan Icon Theme.file_type_icon.ZukanIconFiles')
    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    @patch('os.path.exists')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.InstallEvent')
    @patch('Zukan Icon Theme.file_type_icon.EventBus')
    @patch('Zukan Icon Theme.file_type_icon.UpgradePlugin')
    def test_new_install_when_icons_syntaxes_missing(
        self,
        mock_upgrade_plugin,
        mock_event_bus,
        mock_install_event,
        mock_exists,
        mock_get_theme,
        mock_delete_cache,
        mock_timeout,
        mock_zukan_files,
    ):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        mock_exists.side_effect = lambda path: {
            file_type_icon.ZUKAN_PKG_ICONS_PREFERENCES_PATH: True,
            file_type_icon.ZUKAN_PKG_ICONS_SYNTAXES_PATH: False,
        }.get(path, True)

        mock_install = MagicMock()
        mock_install_event.return_value = mock_install

        mock_upgrade = MagicMock()
        type(mock_upgrade).version_json_file = PropertyMock(return_value='1.0.0')
        mock_upgrade_plugin.return_value = mock_upgrade

        file_type_icon.plugin_loaded()

        mock_install.new_install.assert_called_once()

    @patch('Zukan Icon Theme.file_type_icon.ZukanIconFiles')
    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    @patch('os.path.exists')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.EventBus')
    @patch('Zukan Icon Theme.file_type_icon.UpgradePlugin')
    def test_start_upgrade(
        self,
        mock_upgrade_plugin,
        mock_event_bus,
        mock_exists,
        mock_get_theme,
        mock_delete_cache,
        mock_timeout,
        mock_zukan_files,
    ):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        mock_exists.return_value = True
        mock_event_bus = MagicMock()
        mock_event_bus.return_value = mock_event_bus
        mock_upgrade = MagicMock()
        mock_upgrade_plugin.return_value = mock_upgrade
        mock_zukan_files = MagicMock()
        mock_zukan_files.return_value = mock_zukan_files

        file_type_icon.plugin_loaded()

        mock_upgrade.start_upgrade.assert_called_once()

    @patch('Zukan Icon Theme.file_type_icon.ZukanIconFiles')
    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.delete_cached_theme_info')
    @patch('os.path.exists')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.SettingsEvent')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    @patch('Zukan Icon Theme.file_type_icon.EventBus')
    @patch('Zukan Icon Theme.file_type_icon.UpgradePlugin')
    def test_settings_events(
        self,
        mock_upgrade_plugin,
        mock_event_bus,
        mock_get_theme,
        mock_settings_event,
        mock_exists,
        mock_delete_cache,
        mock_timeout,
        mock_zukan_files,
    ):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        mock_exists.return_value = True
        mock_event_bus = MagicMock()
        mock_event_bus.return_value = mock_event_bus
        mock_upgrade = MagicMock()
        mock_upgrade_plugin.return_value = mock_upgrade
        mock_zukan_files = MagicMock()
        mock_zukan_files.return_value = mock_zukan_files

        file_type_icon.plugin_loaded()

        mock_settings_event.zukan_preferences_changed.assert_called_once()
        mock_settings_event.output_to_console_zukan_pref_settings.assert_called_once()

    @patch('os.path.exists')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.EventBus')
    @patch('Zukan Icon Theme.file_type_icon.ZukanIconFiles')
    @patch('Zukan Icon Theme.file_type_icon.UpgradePlugin')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    def test_rebuild_icons_files(
        self,
        mock_get_theme,
        mock_upgrade_plugin,
        mock_zukan_icon_files,
        mock_event_bus,
        mock_exists,
    ):
        mock_get_theme.return_value = 'Treble Adaptive.sublime-theme'
        mock_exists.return_value = True
        mock_rebuild_icon_files = MagicMock()
        mock_zukan_icon_files.return_value = mock_rebuild_icon_files
        mock_event_bus_instance = MagicMock()
        mock_event_bus.return_value = mock_event_bus_instance

        mock_upgrade_instance = MagicMock()
        type(mock_upgrade_instance).version_json_file = PropertyMock(
            return_value='0.4.8'
        )
        mock_upgrade_plugin.return_value = mock_upgrade_instance

        file_type_icon.plugin_loaded()

        mock_rebuild_icon_files.rebuild_icons_files.assert_called_once_with(
            mock_event_bus_instance
        )

    @patch('sublime.set_timeout')
    @patch('Zukan Icon Theme.file_type_icon.get_theme_name')
    def test_get_theme_name_error_exception(self, mock_get_theme, mock_timeout):
        mock_get_theme.side_effect = Exception('Theme error')

        with self.assertRaises(Exception) as context:
            file_type_icon.plugin_loaded()

        self.assertEqual(str(context.exception), 'Theme error')


class TestPluginUnload(TestCase):
    def setUp(self):
        self.mock_move_folder = MagicMock()
        self.mock_settings_event = MagicMock()

    @patch('Zukan Icon Theme.file_type_icon.MoveFolder')
    def test_remove_created_folder(self, mock_move_folder_class):
        mock_move_folder = MagicMock()
        mock_move_folder_class.return_value = mock_move_folder

        file_type_icon.plugin_unloaded()

        mock_move_folder.remove_created_folder.assert_called_once_with(
            file_type_icon.ZUKAN_PKG_PATH
        )

    @patch('Zukan Icon Theme.file_type_icon.MoveFolder')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.SettingsEvent')
    def test_zukan_preferences_clear(self, mock_settings_event, mock_move_folder_class):
        file_type_icon.plugin_unloaded()

        mock_settings_event.zukan_preferences_clear.assert_called_once()

    @patch('Zukan Icon Theme.file_type_icon.MoveFolder')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', False)
    @patch('Zukan Icon Theme.file_type_icon.SettingsEvent')
    def test_zukan_preferences_clear_listener_disabled(
        self, mock_settings_event, mock_move_folder_class
    ):
        file_type_icon.plugin_unloaded()

        mock_settings_event.zukan_preferences_clear.assert_not_called()

    @patch('Zukan Icon Theme.file_type_icon.MoveFolder')
    def test_remove_created_folder_error_exception(self, mock_move_folder_class):
        mock_move_folder_instance = MagicMock()
        mock_move_folder_instance.remove_created_folder.side_effect = Exception(
            'Failed to remove folder'
        )
        mock_move_folder_class.return_value = mock_move_folder_instance

        with self.assertRaises(Exception) as context:
            file_type_icon.plugin_unloaded()

        self.assertEqual(str(context.exception), 'Failed to remove folder')

    @patch('Zukan Icon Theme.file_type_icon.MoveFolder')
    @patch('Zukan Icon Theme.file_type_icon.zukan_listener_enabled', True)
    @patch('Zukan Icon Theme.file_type_icon.SettingsEvent')
    def test_zukan_preferences_clear_error_exception(
        self, mock_settings_event, mock_move_folder_class
    ):
        mock_settings_event.zukan_preferences_clear.side_effect = Exception(
            'Failed to clear settings'
        )

        with self.assertRaises(Exception) as context:
            file_type_icon.plugin_unloaded()

        self.assertEqual(str(context.exception), 'Failed to clear settings')
