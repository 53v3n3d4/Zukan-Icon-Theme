import errno
import logging
import os
import sublime_plugin

from ..helpers.load_save_settings import (
    get_ignored_icon_settings,
    is_zukan_listener_enabled,
    set_save_settings,
)
from ..helpers.read_write_data import read_pickle_data
from ..lib.icons_syntaxes import ZukanSyntax
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.icons_tags import (
    ICONS_TAGS,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
)

logger = logging.getLogger(__name__)


class DisableEnableIcon:
    def __init__(self, zukan_syntax: ZukanSyntax):
        super().__init__()
        self.zukan_syntax = zukan_syntax

        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def zukan_icons_data(self):
        return read_pickle_data(ZUKAN_ICONS_DATA_FILE)

    def ignored_icon_setting(self):
        return get_ignored_icon_settings()

    def get_list_all_icons_syntaxes(self, zukan_icons: list):
        return self.zukan_syntax.get_list_icons_syntaxes(zukan_icons)

    def add_to_ignored_icon(self, ignored_icon: list, icon_name: str):
        ignored_icon.append(icon_name)

        self._save_ignored_icon_setting(ignored_icon)

    def _save_ignored_icon_setting(self, ignored_icon: list):
        sort_list = sorted(ignored_icon)

        set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', sort_list)

    def message_icon_tag(self, icon_name: str):
        if icon_name in ICONS_TAGS:
            logger.info('icons with %s tag ignored', icon_name)
        else:
            logger.info('%s icon ignored', icon_name)

    def enable_ignored_icon(self, ignored_icon: list, icon_name: str):
        # Remove icon_name
        ignored_icon = [i for i in ignored_icon if not i == icon_name]
        sort_list = sorted(ignored_icon)

        if self.zukan_listener_enabled:
            logger.info('enabling %s icon', icon_name)

        self._save_ignored_icon_setting(sort_list)

    def enable_all_ignored_icons(self, ignored_icon: list):
        ignored_icon = []

        if self.zukan_listener_enabled:
            logger.info('enabling all icons')

        self._save_ignored_icon_setting(ignored_icon)


class DisableIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to disable icon from a list of Zukan icons.
    """

    def __init__(self, view):
        super().__init__(view)
        self.zukan_syntax = ZukanSyntax()
        self.disable_enable_icon = DisableEnableIcon(self.zukan_syntax)

    def run(self, edit, icon_name: str):
        ignored_icon = self.disable_enable_icon.ignored_icon_setting()

        if icon_name not in ignored_icon:
            self.disable_enable_icon.add_to_ignored_icon(ignored_icon, icon_name)
            self.disable_enable_icon.message_icon_tag(icon_name)

            # Rebuild syntax and preference

    def input(self, args: dict):
        return DisableIconInputHandler(self.disable_enable_icon)


class DisableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of Zukan icons, and return icon_name to DisableIcon.
    """

    def __init__(self, disable_enable_icon: DisableEnableIcon):
        self.disable_enable_icon = disable_enable_icon

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of icons'

    def list_items(self) -> list:
        try:
            zukan_icons = self.disable_enable_icon.zukan_icons_data()
            ignored_icon = self.disable_enable_icon.ignored_icon_setting()

            ignored_icon_list = []

            list_all_icons_syntaxes = (
                self.disable_enable_icon.get_list_all_icons_syntaxes(zukan_icons)
            )

            for i in list_all_icons_syntaxes:
                if i.get('name') is not None and i.get('name') not in ignored_icon:
                    ignored_icon_list.append(i['name'])
            if ignored_icon_list:
                icon_list_with_tag = ICONS_TAGS + ignored_icon_list
                return sorted(icon_list_with_tag, key=lambda x: x.upper())

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


class EnableIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to enable icon from a list of ignored icons.
    """

    def __init__(self, view):
        super().__init__(view)
        self.zukan_syntax = ZukanSyntax()
        self.disable_enable_icon = DisableEnableIcon(self.zukan_syntax)

    def run(self, edit, icon_name: str):
        ignored_icon = self.disable_enable_icon.ignored_icon_setting()

        if ignored_icon:
            if icon_name == 'All':
                self.disable_enable_icon.enable_all_ignored_icons(ignored_icon)

            else:
                self.disable_enable_icon.enable_ignored_icon(ignored_icon, icon_name)

    def input(self, args: dict):
        return EnableIconInputHandler(self.disable_enable_icon)


class EnableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored icons, and return icon_name to EnableIcon.
    """

    def __init__(self, disable_enable_icon: DisableEnableIcon):
        self.disable_enable_icon = disable_enable_icon

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of ignored icons'

    def list_items(self) -> list:
        ignored_icon = self.disable_enable_icon.ignored_icon_setting()

        if ignored_icon:
            all_option = ['All']
            new_list = all_option + sorted(ignored_icon, key=lambda x: x.upper())
            return new_list
        else:
            raise TypeError(logger.info('no icons ignored, list is empty.'))
