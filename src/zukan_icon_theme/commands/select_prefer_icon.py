import logging
import sublime
import sublime_plugin

from ..lib.icons_themes import ZukanThemeT2
from ..helpers.load_save_settings import (
    get_prefer_icon_settings,
    set_save_settings,
    is_zukan_listener_enabled,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)

logger = logging.getLogger(__name__)


class SelectRemovePreferIcon(ZukanThemeT2):
    def __init__(self, zukan_preferences_file: str):
        super().__init__()
        self.zukan_preferences_file = zukan_preferences_file

        self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()
        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def update_prefer_icon(self, prefer_icon: dict, selected_prefer_icon: dict):
        prefer_icon.update(selected_prefer_icon)
        self._save_prefer_icon_setting(prefer_icon)

    def _save_prefer_icon_setting(self, prefer_icon: dict):
        set_save_settings(self.zukan_preferences_file, 'prefer_icon', prefer_icon)

    def get_list_created_icons_themes(self):
        return self.list_created_icons_themes()

    def remove_prefer_icon(self, prefer_icon: dict, select_prefer_icon_theme: str):
        # self.prefer_icon = {
        #     k: v
        #     for k, v in self.prefer_icon.items()
        #     if k != select_prefer_icon_theme
        # }
        del prefer_icon[select_prefer_icon_theme]

        # print(self.prefer_icon)
        if self.zukan_listener_enabled:
            logger.info('reseting icon %s', select_prefer_icon_theme)

        self._save_prefer_icon_setting(prefer_icon)

    def remove_all_prefer_icons(self, prefer_icon: dict):
        prefer_icon.clear()

        if self.zukan_listener_enabled:
            logger.info('removing all prefer icons')

        self._save_prefer_icon_setting(prefer_icon)


class SelectPreferIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to select a preferred icon theme and version.
    """

    def __init__(self, view):
        super().__init__(view)
        self.select_remove_prefer_icon = SelectRemovePreferIcon(
            ZUKAN_SETTINGS,
        )

    def run(self, edit, select_prefer_icon_theme: str, select_prefer_icon_version: str):
        _, prefer_icon = get_prefer_icon_settings()

        selected_prefer_icon = {select_prefer_icon_theme: select_prefer_icon_version}

        if select_prefer_icon_theme and select_prefer_icon_version:
            self.select_remove_prefer_icon.update_prefer_icon(
                prefer_icon, selected_prefer_icon
            )

    def input(self, args: dict):
        if not args.get('select_prefer_icon_theme'):
            return SelectPreferIconThemeInputHandler(self.select_remove_prefer_icon)

        if not args.get('select_prefer_icon_version'):
            return SelectPreferIconVersionInputHandler()


class SelectPreferIconThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    Return select_prefer_icon_theme to SelectPreferIcon.
    """

    def __init__(self, select_remove_prefer_icon):
        self.select_remove_prefer_icon = select_remove_prefer_icon

    def name(self) -> str:
        return 'select_prefer_icon_theme'

    def placeholder(self) -> str:
        sublime.status_message('Select theme to prefer icon.')
        return 'List of created themes'

    def list_items(self) -> list:
        auto_prefer_icon, prefer_icon = get_prefer_icon_settings()

        installed_icon_themes = (
            self.select_remove_prefer_icon.get_list_created_icons_themes()
        )

        if installed_icon_themes:
            # Create a dict with prefer icon value, empty string.
            # Then update with prefer icon to show 'dark' or 'light'
            empty_str = ''
            created_themes_with_prefer_icon = dict.fromkeys(
                installed_icon_themes, empty_str
            )
            created_themes_with_prefer_icon.update(prefer_icon)

            installed_themes_list = [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(text=k[0], value=k[0], annotation=k[1])
                for k in sorted(created_themes_with_prefer_icon.items())
            ]

            return installed_themes_list
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )

    def next_input(self, args):
        if 'select_prefer_icon_theme' not in args:
            return SelectPreferIconVersionInputHandler()


class SelectPreferIconVersionInputHandler(sublime_plugin.ListInputHandler):
    """
    Return select_prefer_icon_version to SelectPreferIcon.
    """

    def name(self) -> str:
        return 'select_prefer_icon_version'

    def placeholder(self) -> str:
        sublime.status_message('Select prefer icon version.')
        return 'Icon options: dark and light'

    def list_items(self) -> list:
        version_opts = ['dark', 'light']
        return version_opts


class RemovePreferIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to remove a preferred icon theme.
    """

    def __init__(self, view):
        super().__init__(view)
        self.select_remove_prefer_icon = SelectRemovePreferIcon(
            ZUKAN_SETTINGS,
        )

    def run(self, edit, select_prefer_icon_theme: str):
        _, prefer_icon = get_prefer_icon_settings()

        if prefer_icon:
            if select_prefer_icon_theme == 'All':
                self.select_remove_prefer_icon.remove_all_prefer_icons(prefer_icon)

                # icon_dict_updated = {}

                # if zukan_listener_enabled:
                #     logger.info('removing all prefer icons')

            else:
                if select_prefer_icon_theme in prefer_icon.keys():
                    self.select_remove_prefer_icon.remove_prefer_icon(
                        prefer_icon, select_prefer_icon_theme
                    )
                    # icon_dict_updated = {
                    #     k: v
                    #     for k, v in prefer_icon.items()
                    #     if k != select_prefer_icon_theme
                    # }

                    # if zukan_listener_enabled:
                    #     logger.info('reseting icon %s', select_prefer_icon_theme)

            # set_save_settings(ZUKAN_SETTINGS, 'prefer_icon', icon_dict_updated)

    def input(self, args: dict):
        return RemovePreferIconInputHandler()


class RemovePreferIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of prefered icons, and return select_prefer_icon_theme to RemovePreferIcon.
    """

    def name(self) -> str:
        return 'select_prefer_icon_theme'

    def placeholder(self) -> str:
        return 'List of preferred icons'

    def list_items(self) -> list:
        auto_prefer_icon, prefer_icon = get_prefer_icon_settings()

        if prefer_icon:
            all_option = ['All']

            new_list = all_option + [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(text=i[0], value=i[0], annotation=i[1])
                for i in prefer_icon.items()
            ]

            return new_list

        else:
            raise TypeError(logger.info('no prefer icons to remove, list is empty.'))


# class SelectPreferIcon:
#     def __init__(self, select_prefer_icon_theme: str, select_prefer_icon_version: str):
#         self.select_prefer_icon_theme = select_prefer_icon_theme
#         self.select_prefer_icon_version = select_prefer_icon_version
#         self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()

#     def update_prefer_icon(self):
#         selected_prefer_icon = {
#             self.select_prefer_icon_theme: self.select_prefer_icon_version
#         }

#         if self.select_prefer_icon_theme and self.select_prefer_icon_version:
#             self.prefer_icon.update(selected_prefer_icon)
#             self._save_prefer_icon_settings()

#     def _save_prefer_icon_settings(self):
#         set_save_settings(ZUKAN_SETTINGS, 'prefer_icon', self.prefer_icon)


# class SelectPreferIconCommand(sublime_plugin.TextCommand):
#     """
#     Sublime command to select a preferred icon theme and version.
#     """

#     def run(self, edit, select_prefer_icon_theme: str, select_prefer_icon_version: str):
#         prefer_icon = SelectPreferIcon(
#             select_prefer_icon_theme, select_prefer_icon_version
#         )
#         prefer_icon.update_prefer_icon()

#     def input(self, args: dict):
#         if not args.get('select_prefer_icon_theme'):
#             return SelectPreferIconThemeInputHandler()

#         if not args.get('select_prefer_icon_version'):
#             return SelectPreferIconVersionInputHandler()


# class SelectPreferIconThemeInputHandler(sublime_plugin.ListInputHandler):
#     """
#     Return select_prefer_icon_theme to SelectPreferIcon.
#     """

#     def name(self) -> str:
#         return 'select_prefer_icon_theme'

#     def placeholder(self) -> str:
#         sublime.status_message('Select theme to prefer icon.')
#         return 'List of created themes'

#     def list_items(self) -> list:
#         auto_prefer_icon, prefer_icon = get_prefer_icon_settings()

#         if ZukanTheme.list_created_icons_themes():
#             # Create a dict with prefer icon value, empty string.
#             # Then update with prefer icon to show 'dark' or 'light'
#             empty_str = ''
#             created_themes_with_prefer_icon = dict.fromkeys(
#                 ZukanTheme.list_created_icons_themes(), empty_str
#             )
#             created_themes_with_prefer_icon.update(prefer_icon)

#             installed_themes_list = [
#                 # 'sublime.ListInputItem' since ST 4095
#                 sublime.ListInputItem(text=k[0], value=k[0], annotation=k[1])
#                 for k in sorted(created_themes_with_prefer_icon.items())
#             ]

#             return installed_themes_list
#         else:
#             raise TypeError(
#                 logger.info('it does not exist any created theme, list is empty')
#             )

#     def next_input(self, args):
#         if 'select_prefer_icon_theme' not in args:
#             return SelectPreferIconVersionInputHandler()


# class SelectPreferIconVersionInputHandler(sublime_plugin.ListInputHandler):
#     """
#     Return select_prefer_icon_version to SelectPreferIcon.
#     """

#     def name(self) -> str:
#         return 'select_prefer_icon_version'

#     def placeholder(self) -> str:
#         sublime.status_message('Select prefer icon version.')
#         return 'Icon options: dark and light'

#     def list_items(self) -> list:
#         version_opts = ['dark', 'light']
#         return version_opts


# class RemovePreferIcon:
#     def __init__(self, select_prefer_icon_theme: str):
#         self.select_prefer_icon_theme = select_prefer_icon_theme
#         self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()
#         self.zukan_listener_enabled = is_zukan_listener_enabled()

#     def remove_preferred_icon(self):
#         if self.prefer_icon:
#             if self.select_prefer_icon_theme == 'All':
#                 self._remove_all_prefer_icons()
#             else:
#                 self._remove_prefer_icon()

#             self._save_prefer_icon()

#     def _remove_prefer_icon(self):
#         if self.select_prefer_icon_theme in self.prefer_icon.keys():
#             # self.prefer_icon = {
#             #     k: v
#             #     for k, v in self.prefer_icon.items()
#             #     if k != self.select_prefer_icon_theme
#             # }
#             del self.prefer_icon[self.select_prefer_icon_theme]

#             if self.zukan_listener_enabled:
#                 logger.info('reseting icon %s', self.select_prefer_icon_theme)

#     def _remove_all_prefer_icons(self):
#         self.prefer_icon.clear()

#         if self.zukan_listener_enabled:
#             logger.info('removing all prefer icons')

#     def _save_prefer_icon(self):
#         set_save_settings(ZUKAN_SETTINGS, 'prefer_icon', self.prefer_icon)


# class RemovePreferIconCommand(sublime_plugin.TextCommand):
#     """
#     Sublime command to remove a preferred icon theme.
#     """

#     def run(self, edit, select_prefer_icon_theme: str):
#         remove_icon = RemovePreferIcon(select_prefer_icon_theme)
#         remove_icon.remove_preferred_icon()

#     def input(self, args: dict):
#         return RemovePreferIconInputHandler()


# class RemovePreferIconInputHandler(sublime_plugin.ListInputHandler):
#     """
#     List of prefered icons, and return select_prefer_icon_theme to RemovePreferIcon.
#     """

#     def name(self) -> str:
#         return 'select_prefer_icon_theme'

#     def placeholder(self) -> str:
#         return 'Select a preferred icon to remove'

#     def list_items(self) -> list:
#         auto_prefer_icon, prefer_icon = get_prefer_icon_settings()

#         if prefer_icon:
#             all_option = ['All']

#             new_list = all_option + [
#                 # 'sublime.ListInputItem' since ST 4095
#                 sublime.ListInputItem(text=i[0], value=i[0], annotation=i[1])
#                 for i in prefer_icon.items()
#             ]

#             return new_list

#         else:
#             raise TypeError(logger.info('no prefer icons to remove, list is empty.'))
