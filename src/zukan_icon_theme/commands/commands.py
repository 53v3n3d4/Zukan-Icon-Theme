import logging
import os
import sublime
import sublime_plugin

from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.move_folders import MoveFolder
from ..lib.themes import ThemeFile
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_syntaxes import compare_scopes
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.zukan_dir_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)

logger = logging.getLogger(__name__)


class DeleteSyntax(sublime_plugin.TextCommand):
    """
    Sublime command to delete syntax from a list of created syntaxes.
    """

    def run(self, edit, syntax_name: str):
        message = "Are you sure you want to delete '{s}'?".format(
            s=os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
        )
        if sublime.ok_cancel_dialog(message) is True:
            ZukanSyntax.delete_icon_syntax(syntax_name)

    def input(self, args: dict):
        # print(args)
        return DeleteSyntaxInputHandler()


class DeleteSyntaxInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created syntaxes and return syntax_name to DeleteSyntax.
    """

    def name(self) -> str:
        return 'syntax_name'

    def placeholder(self) -> str:
        return 'List of created syntaxes'

    def list_items(self) -> list:
        if ZukanSyntax.list_created_icons_syntaxes():
            return sorted(ZukanSyntax.list_created_icons_syntaxes())
        else:
            raise TypeError(
                logger.info('it does not exist any created syntax, list is empty')
            )


class DeleteSyntaxes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to delete all syntaxes in 'icons_syntaxes' folder.
    """

    def run(self):
        if ZukanSyntax.list_created_icons_syntaxes():
            message = "Are you sure you want to delete all syntaxes in '{f}'?".format(
                f=ZUKAN_PKG_ICONS_SYNTAXES_PATH
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanSyntax.delete_icons_syntaxes()
        else:
            raise TypeError(
                logger.info('it does not exist any created syntax, list is empty')
            )


class DeleteTheme(sublime_plugin.TextCommand):
    """
    Sublime command to delete theme from a list of created themes.
    """

    def run(self, edit, theme_name: str):
        # print(theme_name)
        message = "Are you sure you want to delete '{t}'?".format(
            t=os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
        )
        if sublime.ok_cancel_dialog(message) is True:
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
    Sublime command to delete all themes in 'icons' folder.
    """

    def run(self):
        if ThemeFile.list_created_themes_files():
            message = "Are you sure you want to delete all themes in '{f}'?".format(
                f=ZUKAN_PKG_ICONS_PATH
            )
            if sublime.ok_cancel_dialog(message) is True:
                ThemeFile.delete_created_themes_files()
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class InstallSyntax(sublime_plugin.TextCommand):
    """
    Sublime command to create syntax from zukan syntaxes list.
    """

    def run(self, edit, syntax_name: str):
        file_name, file_extension = os.path.splitext(syntax_name)
        ZukanSyntax.create_icon_syntax(file_name)

    def input(self, args: dict):
        return InstallSyntaxInputHandler()


class InstallSyntaxInputHandler(sublime_plugin.ListInputHandler):
    """
    Zukan syntaxes list, created syntaxes excluded, and return syntax_name
    to InstallSyntax.
    """

    def name(self) -> str:
        return 'syntax_name'

    def placeholder(self) -> str:
        return 'Zukan syntaxes list'

    def list_items(self) -> list:
        list_syntaxes_not_installed = []
        zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
        for s in zukan_icons_syntaxes:
            if s not in compare_scopes():
                list_syntaxes_not_installed.append(s['name'] + '.sublime-syntax')
        list_syntaxes_not_installed = list(
            set(list_syntaxes_not_installed).difference(
                ZukanSyntax.list_created_icons_syntaxes()
            )
        )
        if list_syntaxes_not_installed:
            return sorted(list_syntaxes_not_installed)
        else:
            raise TypeError(
                logger.info('all syntaxes are already created, list is empty.')
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
            ZukanSyntax.delete_icons_syntaxes()
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
                MoveFolder.move_folders()
        finally:
            ZukanSyntax.create_icons_syntaxes()
            ThemeFile.create_themes_files()


class RebuildSyntaxes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-syntaxes. First, try to remove all previous
    files.
    """

    def run(self):
        try:
            ZukanSyntax.delete_icons_syntaxes()
        finally:
            ZukanSyntax.create_icons_syntaxes()
            ZukanSyntax.edit_contexts_scopes()
