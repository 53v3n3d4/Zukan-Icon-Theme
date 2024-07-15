import errno
import logging
import os
import sublime_plugin

from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.load_save_settings import get_settings, set_save_settings
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
)

logger = logging.getLogger(__name__)


class DisableIcon(sublime_plugin.TextCommand):
    """
    Sublime command to disable icon from a list of Zukan icons.
    """

    def run(self, edit, icon_name: str):
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

        if icon_name not in ignored_icon:
            ignored_icon.append(icon_name)
            sort_list = sorted(ignored_icon)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', sort_list)
            logger.info('%s icon ignored', icon_name)

            # Rebuild syntax and preference

    def input(self, args: dict):
        return DisableIconInputHandler()


class DisableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of Zukan icons, and return icon_name to DisableIcon.
    """

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of icons'

    def list_items(self) -> list:
        try:
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            ignored_icon_list = []

            # 'create_custom_icon' setting
            custom_list = [s for s in create_custom_icon() if 'syntax' in s]
            new_list = zukan_icons + custom_list

            for i in new_list:
                if i.get('name') is not None and i.get('name') not in ignored_icon:
                    ignored_icon_list.append(i['name'])
            if ignored_icon_list:
                return sorted(ignored_icon_list)
            else:
                raise TypeError(
                    logger.info('all icons are already disabled, list is empty.')
                )
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), i
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), i
            )


class DisableTheme(sublime_plugin.TextCommand):
    """
    Sublime command to disable theme from a list of installed themes.
    """

    def run(self, edit, theme_st_path: str):
        theme_name = os.path.basename(theme_st_path)
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')

        if theme_name not in ignored_theme:
            ignored_theme.append(theme_name)
            sort_list = sorted(ignored_theme)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_theme', sort_list)
            logger.info('%s ignored', theme_name)

    def input(self, args: dict):
        return DisableThemeInputHandler()


class DisableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding ignored themes, and return theme_st_path
    to DisableTheme.
    """

    def name(self) -> str:
        return 'theme_st_path'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')
        ignored_theme_list = []

        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in ignored_theme:
                ignored_theme_list.append(name)
        if ignored_theme_list:
            return sorted(ignored_theme_list)
        else:
            raise TypeError(
                logger.info('all themes are already disabled, list is empty.')
            )


class EnableIcon(sublime_plugin.TextCommand):
    """
    Sublime command to enable icon from a list of ignored icons.
    """

    def run(self, edit, icon_name: str):
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

        if ignored_icon:
            # Remove icon_name
            ignored_icon = [i for i in ignored_icon if not i == icon_name]
            sort_list = sorted(ignored_icon)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', sort_list)
            logger.info('%s icon enabled', icon_name)

            # Rebuild syntax and preference

    def input(self, args: dict):
        return EnableIconInputHandler()


class EnableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored icons, and return icon_name to EnableTheme.
    """

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of ignored icons'

    def list_items(self) -> list:
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
        if not isinstance(ignored_icon, list):
            logger.warning('ignored_icon option malformed, need to be a string list')

        if ignored_icon:
            return sorted(ignored_icon)
        else:
            raise TypeError(logger.info('no icons ignored, list is empty.'))


class EnableTheme(sublime_plugin.TextCommand):
    """
    Sublime command to enable theme from a list of ignored themes.
    """

    def run(self, edit, theme_name: str):
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')

        if ignored_theme:
            # Remove theme_name
            ignored_theme = [t for t in ignored_theme if not t == theme_name]
            sort_list = sorted(ignored_theme)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_theme', sort_list)
            logger.info('%s enabled', theme_name)

    def input(self, args: dict):
        return EnableThemeInputHandler()


class EnableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored themes, and return theme_name to EnableTheme.
    """

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of ignored themes'

    def list_items(self) -> list:
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')

        if ignored_theme:
            return sorted(ignored_theme)
        else:
            raise TypeError(logger.info('no themes ignored, list is empty.'))
