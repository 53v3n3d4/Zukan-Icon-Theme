import logging
import os
import sublime_plugin

from ..helpers.load_save_settings import (
    get_theme_settings,
    set_save_settings,
    is_zukan_listener_enabled,
)
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)

logger = logging.getLogger(__name__)


class DisableEnableTheme:
    def __init__(self):
        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def ignored_theme_setting(self):
        ignored_theme, _ = get_theme_settings()
        return ignored_theme

    def add_to_ignored_themes(self, theme_name: str, ignored_theme: list):
        ignored_theme.append(theme_name)

        self._save_ignored_theme_setting(ignored_theme)

    def get_ignored_theme_list(self, ignored_theme: list):
        ignored_theme_list = []

        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in ignored_theme:
                ignored_theme_list.append(name)

        return ignored_theme_list

    def enable_icon_theme(self, theme_name: str, ignored_theme: list):
        # Remove theme_name
        ignored_theme = [t for t in ignored_theme if not t == theme_name]

        self._save_ignored_theme_setting(ignored_theme)

        if self.zukan_listener_enabled:
            logger.info('enabling %s', theme_name)

    def enable_all_icons_themes(self, ignored_theme: list):
        ignored_theme = []

        self._save_ignored_theme_setting(ignored_theme)

        if self.zukan_listener_enabled:
            logger.info('enabling all themes')

    def _save_ignored_theme_setting(self, ignored_theme: list):
        sort_list = sorted(ignored_theme)
        set_save_settings(ZUKAN_SETTINGS, 'ignored_theme', sort_list)


class DisableThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to disable a theme from the list of installed themes.
    """

    def __init__(self, view):
        super().__init__(view)
        self.disable_enable_theme = DisableEnableTheme()

    def run(self, edit, theme_st_path: str):
        theme_name = os.path.basename(theme_st_path)
        ignored_theme = self.disable_enable_theme.ignored_theme_setting()

        if theme_name not in ignored_theme:
            self.disable_enable_theme.add_to_ignored_themes(theme_name, ignored_theme)

            logger.info('%s ignored', theme_name)

    def input(self, args: dict):
        return DisableThemeInputHandler(self.disable_enable_theme)


class DisableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding ignored themes, and return theme_st_path
    to DisableTheme.
    """

    def __init__(self, disable_enable_theme: DisableEnableTheme):
        self.disable_enable_theme = disable_enable_theme

    def name(self) -> str:
        return 'theme_st_path'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        ignored_theme = self.disable_enable_theme.ignored_theme_setting()

        ignored_theme_list = self.disable_enable_theme.get_ignored_theme_list(
            ignored_theme
        )

        if ignored_theme_list:
            return sorted(ignored_theme_list)
        else:
            raise TypeError(
                logger.info('all themes are already disabled, list is empty.')
            )


class EnableThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to enable a theme from the list of ignored themes.
    """

    def __init__(self, view):
        super().__init__(view)
        self.disable_enable_theme = DisableEnableTheme()

    def run(self, edit, theme_name: str):
        ignored_theme = self.disable_enable_theme.ignored_theme_setting()

        if ignored_theme:
            if theme_name == 'All':
                self.disable_enable_theme.enable_all_icons_themes(ignored_theme)
            else:
                self.disable_enable_theme.enable_icon_theme(theme_name, ignored_theme)

    def input(self, args: dict):
        return EnableThemeInputHandler(self.disable_enable_theme)


class EnableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored themes, and return theme_name to EnableTheme.
    """

    def __init__(self, disable_enable_theme: DisableEnableTheme):
        self.disable_enable_theme = disable_enable_theme

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of ignored themes'

    def list_items(self) -> list:
        ignored_theme = self.disable_enable_theme.ignored_theme_setting()

        if ignored_theme:
            all_option = ['All']
            new_list = all_option + sorted(ignored_theme)
            return new_list
        else:
            raise TypeError(logger.info('no themes ignored, list is empty.'))
