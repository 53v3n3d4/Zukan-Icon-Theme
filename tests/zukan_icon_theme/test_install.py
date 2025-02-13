import importlib

from unittest import TestCase
from unittest.mock import call, patch, MagicMock

install_event = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.install'
)

# Fixme: running test does not clear status message.


class TestInstallEvent(TestCase):
    def setUp(self):
        self.install_event = install_event.InstallEvent()

        self.mock_move_folder = MagicMock()
        self.mock_preference = MagicMock()
        self.mock_syntax = MagicMock()
        self.mock_theme = MagicMock()

        self.install_event.move_folder = self.mock_move_folder
        self.install_event.zukan_preference = self.mock_preference
        self.install_event.zukan_syntax = self.mock_syntax
        self.install_event.zukan_theme = self.mock_theme

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.install.is_zukan_restart_message'
    )
    def test_zukan_restart_message_setting(self, mock_restart_message):
        mock_restart_message.return_value = True
        self.assertTrue(self.install_event.zukan_restart_message_setting())

        mock_restart_message.return_value = False
        self.assertFalse(self.install_event.zukan_restart_message_setting())

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.core.install.get_upgraded_version_settings'
    )
    def test_pkg_version_setting(self, mock_version):
        mock_version.return_value = ('0.4.8', None)
        self.assertEqual(self.install_event.pkg_version_setting(), '0.4.8')

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.install.get_theme_settings')
    def test_install_batch(self, mock_theme_settings):
        # Test auto_install_theme is False
        mock_theme_settings.return_value = (None, False)

        self.install_event.install_batch()

        self.mock_theme.create_icons_themes.assert_called_once()
        self.mock_syntax.build_icons_syntaxes.assert_called_once()
        self.mock_preference.build_icons_preferences.assert_called_once()

        # Test auto_install_theme is True
        self.mock_theme.reset_mock()
        mock_theme_settings.return_value = (None, True)

        self.install_event.install_batch()

        self.mock_theme.create_icons_themes.assert_not_called()
        self.mock_syntax.build_icons_syntaxes.assert_called()
        self.mock_preference.build_icons_preferences.assert_called()

    def test_install_syntaxes_preferences(self):
        self.install_event.install_syntaxes_preferences()

        self.mock_syntax.build_icons_syntaxes.assert_called_once()
        self.mock_preference.build_icons_preferences.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.install.delete_unused_icons')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.install.threading.Thread')
    @patch('sublime.active_window')
    @patch('sublime.set_timeout')
    @patch('sublime.message_dialog')
    def test_install_upgrade_thread(
        self,
        mock_dialog,
        mock_set_timeout,
        mock_active_window,
        mock_thread,
        mock_delete_unused,
    ):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        mock_view = MagicMock()
        mock_window = MagicMock()
        mock_window.active_view.return_value = mock_view
        mock_active_window.return_value = mock_window

        with patch.object(
            self.install_event, 'pkg_version_setting', return_value='1.0.0'
        ), patch.object(
            self.install_event, 'zukan_restart_message_setting', return_value=True
        ):
            self.install_event.install_upgrade_thread()

            self.mock_move_folder.move_folders.assert_called_once()
            mock_thread.assert_called_once_with(
                target=self.install_event.install_syntaxes_preferences
            )
            mock_thread_instance.start.assert_called_once()
            mock_delete_unused.assert_has_calls(
                [
                    call(install_event.ZUKAN_PKG_ICONS_PATH),
                    call(install_event.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH),
                ]
            )

            mock_thread_instance.is_alive.return_value = False
            first_callback = mock_set_timeout.call_args_list[0][0][0]
            first_callback()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.install.threading.Thread')
    @patch('sublime.active_window')
    @patch('sublime.set_timeout')
    def test_rebuild_icon_files_thread(
        self, mock_set_timeout, mock_active_window, mock_thread
    ):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        mock_view = MagicMock()
        mock_window = MagicMock()
        mock_window.active_view.return_value = mock_view
        mock_active_window.return_value = mock_window

        self.install_event.rebuild_icon_files_thread()

        mock_thread.assert_called_once_with(
            target=self.install_event.install_syntaxes_preferences
        )
        mock_thread_instance.start.assert_called_once()

        mock_thread_instance.is_alive.return_value = False

        first_callback = mock_set_timeout.call_args_list[0][0][0]
        first_callback()

        cleanup_callback = mock_set_timeout.call_args_list[-1][0][0]
        cleanup_callback()

        mock_view.erase_status.assert_called_with('_zukan')

    @patch('Zukan Icon Theme.src.zukan_icon_theme.core.install.threading.Thread')
    @patch('sublime.active_window')
    @patch('sublime.set_timeout')
    @patch('sublime.message_dialog')
    def test_new_install(
        self, mock_dialog, mock_set_timeout, mock_active_window, mock_thread
    ):
        mock_view = MagicMock()
        mock_window = MagicMock()
        mock_window.active_view.return_value = mock_view
        mock_active_window.return_value = mock_window

        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        with patch.object(
            self.install_event, 'zukan_restart_message_setting', return_value=True
        ), patch.object(
            self.install_event, 'pkg_version_setting', return_value='0.4.8'
        ):
            self.install_event.new_install()
            mock_thread.assert_called_once_with(target=self.install_event.install_batch)
            mock_thread_instance.start.assert_called_once()

            mock_thread_instance.is_alive.return_value = False
            first_callback = mock_set_timeout.call_args_list[0][0][0]
            first_callback()

        mock_thread.reset_mock()
        mock_thread_instance.reset_mock()
        mock_set_timeout.reset_mock()
        mock_view.reset_mock()
        mock_dialog.reset_mock()

        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        with patch.object(
            self.install_event, 'zukan_restart_message_setting', return_value=False
        ):
            self.install_event.new_install()
            mock_thread.assert_called_once_with(target=self.install_event.install_batch)
            mock_thread_instance.start.assert_called_once()

            mock_thread_instance.is_alive.return_value = False
            first_callback = mock_set_timeout.call_args_list[0][0][0]
            first_callback()
