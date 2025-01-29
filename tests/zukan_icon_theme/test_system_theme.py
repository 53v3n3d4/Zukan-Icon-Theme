import importlib
import json
import platform

from unittest import TestCase
from unittest.mock import patch, MagicMock


system_theme = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme'
)


class TestSystemTheme(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.check_output'
    )
    def test_linux_theme_dark(self, mock_check_output):
        mock_check_output.return_value = json.dumps({'data': [{'data': 1}]})

        result = system_theme.linux_theme()
        self.assertTrue(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.check_output'
    )
    def test_linux_theme_light(self, mock_check_output):
        mock_check_output.return_value = json.dumps({'data': [{'data': 2}]})

        result = system_theme.linux_theme()
        self.assertFalse(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.Popen'
    )
    def test_macos_theme_dark(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('AppleInterfaceStyle', '')
        mock_popen.return_value = mock_process

        result = system_theme.macos_theme()
        self.assertTrue(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.Popen'
    )
    def test_macos_theme_light(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('', '')
        mock_popen.return_value = mock_process

        result = system_theme.macos_theme()
        self.assertFalse(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.platform.system',
        return_value='Linux',
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.check_output'
    )
    def test_system_theme_linux(self, mock_check_output, mock_platform_system):
        mock_check_output.return_value = json.dumps({'data': [{'data': 1}]})

        result = system_theme.system_theme()
        self.assertTrue(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.platform.system',
        return_value='Darwin',
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.Popen'
    )
    def test_system_theme_macos(self, mock_popen, mock_platform_system):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('AppleInterfaceStyle', '')
        mock_popen.return_value = mock_process

        result = system_theme.system_theme()
        self.assertTrue(result)

    if platform.system() == 'Windows':
        import winreg

        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.OpenKey'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.EnumValue'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.ConnectRegistry'
        )
        def test_windows_theme_dark(
            self, mock_connect_registry, mock_enum_value, mock_open_key
        ):
            mock_connect_registry.return_value = MagicMock()
            mock_open_key.return_value = MagicMock()
            mock_enum_value.return_value = ('AppsUseLightTheme', 0, None)

            result = system_theme.windows_theme()
            self.assertTrue(result)

        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.OpenKey'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.EnumValue'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.ConnectRegistry'
        )
        def test_windows_theme_light(
            self, mock_connect_registry, mock_enum_value, mock_open_key
        ):
            mock_connect_registry.return_value = MagicMock()
            mock_open_key.return_value = MagicMock()
            mock_enum_value.return_value = ('AppsUseLightTheme', 1, None)

            result = system_theme.windows_theme()
            self.assertFalse(result)

        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.platform.system',
            return_value='Windows',
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg',
            MagicMock(),
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.ConnectRegistry'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.OpenKey'
        )
        @patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.winreg.EnumValue'
        )
        def test_system_theme_windows(
            self,
            mock_enum_value,
            mock_open_key,
            mock_connect_registry,
            mock_platform_system,
            mock_winreg,
        ):
            mock_connect_registry.return_value = MagicMock()
            mock_open_key.return_value = MagicMock()
            mock_enum_value.return_value = ('AppsUseLightTheme', 0, None)

            result = system_theme.system_theme()
            self.assertTrue(result)
