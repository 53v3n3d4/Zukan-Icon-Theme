import logging
import os
import sublime
import sublime_plugin

from ..helpers.load_save_settings import (
    get_theme_settings,
    is_zukan_restart_message,
)
from ..helpers.search_themes import search_resources_sublime_themes
from ..lib.icons_themes import ZukanTheme
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
)

logger = logging.getLogger(__name__)


class Themes(ZukanTheme):
    """
    Themes list, install and delete.
    """

    def __init__(self, zukan_pkg_icons_path: str):
        super().__init__()
        self.zukan_pkg_icons_path = zukan_pkg_icons_path

    def ignored_theme_setting(self) -> list:
        ignored_theme, _ = get_theme_settings()
        return ignored_theme

    def zukan_restart_message_setting(self) -> bool:
        return is_zukan_restart_message()

    def delete_single_icon_theme(self, theme_name: str):
        self.delete_icon_theme(theme_name)

    def delete_all_icons_themes(self):
        self.delete_icons_themes()

    def get_installed_themes(self) -> list:
        installed_themes_list = self.list_created_icons_themes()
        return sorted(installed_themes_list)

    def get_not_installed_themes(self) -> list:
        list_themes_not_installed = []

        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in self.list_created_icons_themes():
                list_themes_not_installed.append(name)

        return list_themes_not_installed

    def install_icon_theme(self, theme_st_path: str):
        # 'ignored_theme' setting
        ignored_theme = self.ignored_theme_setting()

        theme_name = os.path.basename(theme_st_path)

        if theme_name in ignored_theme:
            dialog_message = '{t} is disabled. Need to enable first.'.format(
                t=theme_name
            )
            # sublime.message_dialog(dialog_message)
            sublime.error_message(dialog_message)

        else:
            self.create_icon_theme(theme_st_path)

    def install_all_icons_themes(self):
        self.create_icons_themes()

    def confirm_delete(self, message: str):
        return sublime.ok_cancel_dialog(message)


class DeleteThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete theme from a list of created themes.
    """

    def __init__(self, view):
        super().__init__(view)
        self.themes = Themes(ZUKAN_PKG_ICONS_PATH)

    def run(self, edit, theme_name: str):
        # 'zukan_restart_message' setting
        zukan_restart_message = self.themes.zukan_restart_message_setting()

        if theme_name == 'All':
            if zukan_restart_message:
                dialog_message = (
                    'Are you sure you want to delete all themes in "{f}"?\n\n'
                    'You may have to restart ST, for all icons do not show.'.format(
                        f=self.themes.zukan_pkg_icons_path
                    )
                )
            else:
                dialog_message = (
                    'Are you sure you want to delete all themes in "{f}"?'.format(
                        f=self.themes.zukan_pkg_icons_path
                    )
                )

            if self.themes.confirm_delete(dialog_message):
                self.themes.delete_all_icons_themes()

        else:
            if zukan_restart_message:
                dialog_message = (
                    'Are you sure you want to delete "{t}"?\n\n'
                    'You may have to restart ST, for all icons do not show.'.format(
                        t=os.path.join(self.themes.zukan_pkg_icons_path, theme_name)
                    )
                )
            else:
                dialog_message = 'Are you sure you want to delete "{t}"?'.format(
                    t=os.path.join(self.themes.zukan_pkg_icons_path, theme_name)
                )

            if self.themes.confirm_delete(dialog_message):
                self.themes.delete_single_icon_theme(theme_name)

        # Comment because change 'add_on_change' to ViewListener
        # Check if selected theme was deleted
        # get_user_theme()

    def is_enabled(self):
        list_installed_themes = self.themes.get_installed_themes()

        return list_installed_themes is not None and len(list_installed_themes) > 0

    def input(self, args: dict):
        return DeleteThemeInputHandler(self.themes)


class DeleteThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created themes and return theme_name to DeleteTheme.
    """

    def __init__(self, themes: Themes):
        self.themes = themes

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of created themes'

    def list_items(self) -> list:
        list_installed_themes = self.themes.get_installed_themes()

        if list_installed_themes:
            all_option = ['All']
            new_list = all_option + list_installed_themes
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class InstallThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create theme from a list of installed themes.
    """

    def __init__(self, view):
        super().__init__(view)
        self.themes = Themes(ZUKAN_PKG_ICONS_PATH)

    def run(self, edit, theme_st_path: str):
        # 'zukan_restart_message' setting
        zukan_restart_message = self.themes.zukan_restart_message_setting()

        if theme_st_path == 'All':
            if zukan_restart_message:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in current '
                    'theme.'
                )
                sublime.message_dialog(dialog_message)

            self.themes.install_all_icons_themes()

        else:
            # 'ignored_theme' setting
            ignored_theme = self.themes.ignored_theme_setting()
            theme_name = os.path.basename(theme_st_path)

            if zukan_restart_message and theme_name not in ignored_theme:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in '
                    'current theme.'
                )
                sublime.message_dialog(dialog_message)

            self.themes.install_icon_theme(theme_st_path)

    def is_enabled(self):
        list_themes_not_installed = self.themes.get_not_installed_themes()
        return (
            list_themes_not_installed is not None and len(list_themes_not_installed) > 0
        )

    def input(self, args: dict):
        return InstallThemeInputHandler(self.themes)


class InstallThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding created themes, and return theme_st_path
    to InstallTheme.
    """

    def __init__(self, themes: Themes):
        self.themes = themes

    def name(self) -> str:
        return 'theme_st_path'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        list_themes_not_installed = self.themes.get_not_installed_themes()

        if list_themes_not_installed:
            all_option = ['All']
            themes_list = sorted(list_themes_not_installed)
            new_list = all_option + themes_list
            return new_list

        else:
            raise TypeError(
                logger.info('all themes are already created, list is empty.')
            )
