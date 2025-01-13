import logging
import os
import sublime
import sublime_plugin

from ..helpers.load_save_settings import get_ignored_icon_settings
from ..lib.icons_preferences import ZukanPreference
from ..utils.file_extensions import (
    TMPREFERENCES_EXTENSION,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
)

logger = logging.getLogger(__name__)


class Preferences(ZukanPreference):
    """
    Preferences list, install and delete.
    """

    def __init__(self, preferences_path: str):
        super().__init__()
        self.preferences_path = preferences_path

    def ignored_icon_setting(self):
        return get_ignored_icon_settings()

    def delete_icon_preference(self, preference_name: str):
        self.delete_icons_preference(preference_name)

    def delete_all_icons_preferences(self):
        self.delete_icons_preferences()

    def get_installed_preferences(self):
        installed_preferences_list = self.list_created_icons_preferences()
        return sorted(installed_preferences_list)

    def get_not_installed_preferences(self):
        list_preferences_not_installed = []

        list_all_icons_preferences = self.get_list_icons_preferences()

        for p in list_all_icons_preferences:
            if p['preferences'].get('scope') is not None:
                # Default icon
                icon_name = p['preferences']['settings']['icon']
                if icon_name.endswith('-dark'):
                    icon_name = icon_name[:-5]
                if icon_name.endswith('-light'):
                    icon_name = icon_name[:-6]

                list_preferences_not_installed.append(
                    icon_name + TMPREFERENCES_EXTENSION
                )
        list_preferences_not_installed = list(
            set(list_preferences_not_installed).difference(
                self.list_created_icons_preferences()
            )
        )

        return list_preferences_not_installed

    def install_icon_preference(self, preference_name: str):
        file_name, _ = os.path.splitext(preference_name)

        list_all_icons_preferences = self.get_list_icons_preferences()

        for p in list_all_icons_preferences:
            if (
                p['preferences']['settings']['icon'] == file_name
                or p['preferences']['settings']['icon'][:-5] == file_name
                or p['preferences']['settings']['icon'][:-6] == file_name
            ):
                if p['name'] in self.ignored_icon_setting():
                    dialog_message = (
                        '{i} icon is disabled. Need to enable first.'.format(
                            i=p['name']
                        )
                    )
                    # sublime.message_dialog(dialog_message)
                    sublime.error_message(dialog_message)

                else:
                    # Default icon
                    # Need to add '-dark' or 'light' that was removed to mount list
                    if p['preferences']['settings']['icon'][:-5] == file_name:
                        file_name = p['preferences']['settings']['icon']

                    if p['preferences']['settings']['icon'][:-6] == file_name:
                        file_name = p['preferences']['settings']['icon']

                    # print(file_name)
                    self.build_icon_preference(file_name, preference_name)

    def install_all_icons_preferences(self):
        self.build_icons_preferences()

    def confirm_delete(self, message: str):
        return sublime.ok_cancel_dialog(message)


class DeletePreferenceCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete preference from a list of created preferences.
    """

    def __init__(self, view):
        super().__init__(view)
        self.preferences = Preferences(ZUKAN_PKG_ICONS_PREFERENCES_PATH)

    def run(self, edit, preference_name: str):
        if preference_name == 'All':
            dialog_message = (
                "Are you sure you want to delete all preferences in '{f}'?".format(
                    f=self.preferences.preferences_path
                )
            )
            if self.preferences.confirm_delete(dialog_message):
                self.preferences.delete_all_icons_preferences()
        else:
            dialog_message = "Are you sure you want to delete '{p}'?".format(
                p=os.path.join(self.preferences.preferences_path, preference_name)
            )
            if self.preferences.confirm_delete(dialog_message):
                self.preferences.delete_icon_preference(preference_name)

    def input(self, args: dict):
        return DeletePreferenceInputHandler(self.preferences)


class DeletePreferenceInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created preferences and return preference_name to DeletePreference.
    """

    def __init__(self, preferences):
        self.preferences = preferences

    def name(self) -> str:
        return 'preference_name'

    def placeholder(self) -> str:
        return 'List of created preferences'

    def list_items(self) -> list:
        installed_preferences_list = self.preferences.get_installed_preferences()

        if installed_preferences_list:
            all_option = ['All']
            new_list = all_option + installed_preferences_list
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created preference, list is empty')
            )


class InstallPreferenceCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create preference from zukan preferences list.
    """

    def __init__(self, view):
        super().__init__(view)
        self.preferences = Preferences(ZUKAN_PKG_ICONS_PREFERENCES_PATH)

    def run(self, edit, preference_name: str):
        if preference_name == 'All':
            self.preferences.install_all_icons_preferences()
        else:
            self.preferences.install_icon_preference(preference_name)

    def input(self, args: dict):
        return InstallPreferenceInputHandler(self.preferences)


class InstallPreferenceInputHandler(sublime_plugin.ListInputHandler):
    """
    Zukan preferences list, created preferences excluded, and return preference_name
    to InstallPreference.
    """

    def __init__(self, preferences):
        self.preferences = preferences

    def name(self) -> str:
        return 'preference_name'

    def placeholder(self) -> str:
        return 'Zukan preferences list'

    def list_items(self) -> list:
        list_preferences_not_installed = (
            self.preferences.get_not_installed_preferences()
        )

        if list_preferences_not_installed:
            all_option = ['All']
            preferences_list = sorted(list_preferences_not_installed)
            new_list = all_option + preferences_list
            return new_list
        else:
            raise TypeError(
                logger.info('all preferences are already created, list is empty.')
            )
