import importlib
import json
import subprocess

from unittest import TestCase
from unittest.mock import patch, MagicMock


system_theme = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme'
)


class TestSystemTheme(TestCase):
    @patch('subprocess.check_output')
    def test_linux_theme_dark(self, mock_check_output):
        mock_check_output.return_value = json.dumps({'data': [{'data': 1}]})

        result = system_theme.linux_theme()
        self.assertTrue(result)

    @patch('subprocess.check_output')
    def test_linux_theme_light(self, mock_check_output):
        mock_check_output.return_value = json.dumps({'data': [{'data': 2}]})

        result = system_theme.linux_theme()
        self.assertFalse(result)

    @patch('subprocess.Popen')
    def test_macos_theme_dark(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('AppleInterfaceStyle', '')
        mock_popen.return_value = mock_process

        result = system_theme.macos_theme()
        self.assertTrue(result)

    @patch('subprocess.Popen')
    def test_macos_theme_light(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('', '')
        mock_popen.return_value = mock_process

        result = system_theme.macos_theme()
        self.assertFalse(result)

    @patch('platform.system', return_value='Linux')
    @patch('subprocess.check_output')
    def test_system_theme_linux(self, mock_check_output, mock_platform_system):
        mock_check_output.return_value = json.dumps({'data': [{'data': 1}]})

        result = system_theme.system_theme()
        self.assertTrue(result)

    @patch('platform.system', return_value='Darwin')
    @patch('subprocess.Popen')
    def test_system_theme_macos(self, mock_popen, mock_platform_system):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ('AppleInterfaceStyle', '')
        mock_popen.return_value = mock_process

        result = system_theme.system_theme()
        self.assertTrue(result)
