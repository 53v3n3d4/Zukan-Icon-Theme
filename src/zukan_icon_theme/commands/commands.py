import logging
import os
import sublime
import sublime_plugin

from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.move_folders import MoveFolder
from ..lib.themes import ThemeFile
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.zukan_dir_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_ICONS_PATH,
)

logger = logging.getLogger(__name__)


class DeleteTheme(sublime_plugin.TextCommand):
    """
    Sublime command to delete theme from a list of created themes.
    """

    def run(self, edit, theme_name: str):
        # print(theme_name)
        message = 'Are you sure you want to delete {t}?'.format(
            t=os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
        )
        if sublime.yes_no_cancel_dialog(message) == sublime.DIALOG_YES:
            ThemeFile.delete_created_theme_file(theme_name)

    def input(self, args: dict):
        # print(args)
        return DeleteThemeInputHandler()


class DeleteThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created themes and return theme_name to DeleteTheme.
    """

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of created themes'

    def list_items(self) -> list:
        if ThemeFile.list_created_themes_files():
            return sorted(ThemeFile.list_created_themes_files())
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class DeleteThemes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to delete all themes from a list of created themes.
    """

    def run(self):
        if ThemeFile.list_created_themes_files():
            message = 'Are you sure you want to delete all themes in {f}?'.format(
                f=ZUKAN_PKG_ICONS_PATH
            )
            if sublime.yes_no_cancel_dialog(message) == sublime.DIALOG_YES:
                ThemeFile.delete_created_themes_files()
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class InstallTheme(sublime_plugin.TextCommand):
    """
    Sublime command to create theme from a list of installed themes.
    """

    def run(self, edit, theme_name: str):
        ThemeFile.create_theme_file(theme_name)

    def input(self, args: dict):
        return InstallThemeInputHandler()


class InstallThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, created themes excluded, and return theme_name
    to InstallTheme.
    """

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        list_themes_not_installed = []
        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in ThemeFile.list_created_themes_files():
                list_themes_not_installed.append(name)
        if list_themes_not_installed:
            return sorted(list_themes_not_installed)
        else:
            raise TypeError(
                logger.info('all themes are already created, list is empty.')
            )


class InstallThemes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to create all themes from a list of installed themes.

    It will save over already existing file.
    """

    def run(self):
        ThemeFile.create_themes_files()


class RebuildFiles(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-themes and sublime-syntaxes.
    """

    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            ZukanSyntax.remove_icons_syntaxes()
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
                MoveFolder.move_folders()
        finally:
            ZukanSyntax.create_icons_syntaxes()
            ThemeFile.create_themes_files()
