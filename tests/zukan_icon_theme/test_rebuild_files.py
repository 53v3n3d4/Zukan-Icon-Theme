import importlib

from unittest import TestCase
from unittest.mock import Mock

rebuild_files = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.rebuild_files'
)


class TestRebuildFilesCommand(TestCase):
    def setUp(self):
        self.mock_install_event = Mock(spec=rebuild_files.InstallEvent)
        self.mock_zukan_theme = Mock(spec=rebuild_files.ZukanTheme)
        self.command = rebuild_files.RebuildFilesCommand(
            install_event=self.mock_install_event, zukan_theme=self.mock_zukan_theme
        )

    def test_rebuild_files_command_init(self):
        self.assertIs(self.command.install_event, self.mock_install_event)
        self.assertIs(self.command.zukan_theme, self.mock_zukan_theme)

    def test_rebuild_files_command_init_no_dependencies(self):
        command = rebuild_files.RebuildFilesCommand()
        self.assertIsInstance(command.install_event, rebuild_files.InstallEvent)
        self.assertIsInstance(command.zukan_theme, rebuild_files.ZukanTheme)

    def test_rebuild_files_command_run(self):
        self.command.run()

        self.mock_zukan_theme.delete_icons_themes.assert_called_once()
        self.mock_install_event.new_install.assert_called_once()
