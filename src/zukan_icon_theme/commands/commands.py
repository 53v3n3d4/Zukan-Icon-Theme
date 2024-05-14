import os
import sublime_plugin

from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.move_folders import MoveFolder
from ..lib.themes import ThemeFile
from ..utils.zukan_dir_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
)


class InstallThemes(sublime_plugin.ApplicationCommand):
    def run(self):
        ThemeFile.create_themes_files()


class DeleteThemes(sublime_plugin.ApplicationCommand):
    def run(self):
        ThemeFile.delete_created_themes_files()


class RebuildFiles(sublime_plugin.ApplicationCommand):
    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
            MoveFolder.move_folders()
        ZukanSyntax.create_icons_syntaxes()
        ThemeFile.create_themes_files()
