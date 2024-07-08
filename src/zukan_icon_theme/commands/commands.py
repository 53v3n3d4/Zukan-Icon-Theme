import logging
import os
import sublime
import sublime_plugin

from ..events.install import InstallEvent
from ..events.settings import SettingsEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.get_settings import get_settings
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_syntaxes import compare_scopes
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
)

logger = logging.getLogger(__name__)


class DeletePreference(sublime_plugin.TextCommand):
    """
    Sublime command to delete preference from a list of created preferences.
    """

    def run(self, edit, preference_name: str):
        message = "Are you sure you want to delete '{p}'?".format(
            p=os.path.join(ZUKAN_PKG_ICONS_PREFERENCES_PATH, preference_name)
        )
        if sublime.ok_cancel_dialog(message) is True:
            ZukanPreference.delete_icons_preference(preference_name)

    def input(self, args: dict):
        return DeletePreferenceInputHandler()


class DeletePreferenceInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created preferences and return preference_name to DeletePreference.
    """

    def name(self) -> str:
        return 'preference_name'

    def placeholder(self) -> str:
        return 'List of created preferences'

    def list_items(self) -> list:
        if ZukanPreference.list_created_icons_preferences():
            return sorted(ZukanPreference.list_created_icons_preferences())
        else:
            raise TypeError(
                logger.info('it does not exist any created preference, list is empty')
            )


class DeletePreferences(sublime_plugin.ApplicationCommand):
    """
    Sublime command to delete all preferences in 'preferences' folder.
    """

    def run(self):
        if ZukanPreference.list_created_icons_preferences():
            message = (
                "Are you sure you want to delete all preferences in '{f}'?".format(
                    f=ZUKAN_PKG_ICONS_PREFERENCES_PATH
                )
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanPreference.delete_icons_preferences()
        else:
            raise TypeError(
                logger.info('it does not exist any created preference, list is empty')
            )


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
            return sorted(
                ZukanSyntax.list_created_icons_syntaxes(), key=lambda x: x.upper()
            )
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
        # 'zukan_restart_message' setting
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if zukan_restart_message is True:
            dialog_message = (
                'Are you sure you want to delete "{t}"?\n\n'
                'You may have to restart ST, for all icons do not show.'.format(
                    t=os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
                )
            )
        if zukan_restart_message is False:
            dialog_message = 'Are you sure you want to delete "{t}"?'.format(
                t=os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
            )

        if sublime.ok_cancel_dialog(dialog_message) is True:
            ZukanTheme.delete_icon_theme(theme_name)
            # Check if selected theme was deleted
            SettingsEvent.get_user_theme()

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
        if ZukanTheme.list_created_icons_themes():
            return sorted(ZukanTheme.list_created_icons_themes())
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class DeleteThemes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to delete all themes in 'icons' folder.
    """

    def run(self):
        if ZukanTheme.list_created_icons_themes():
            # 'zukan_restart_message' setting
            zukan_restart_message = get_settings(
                ZUKAN_SETTINGS, 'zukan_restart_message'
            )

            if zukan_restart_message is True:
                dialog_message = (
                    'Are you sure you want to delete all themes in "{f}"?\n\n'
                    'You may have to restart ST, for all icons do not show.'.format(
                        f=ZUKAN_PKG_ICONS_PATH
                    )
                )
            if zukan_restart_message is False:
                dialog_message = (
                    'Are you sure you want to delete all themes in "{f}"?'.format(
                        f=ZUKAN_PKG_ICONS_PATH
                    )
                )

            if sublime.ok_cancel_dialog(dialog_message) is True:
                ZukanTheme.delete_icons_themes()
                # Check if selected theme was deleted
                SettingsEvent.get_user_theme()
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class InstallPreference(sublime_plugin.TextCommand):
    """
    Sublime command to create preference from zukan preferences list.
    """

    def run(self, edit, preference_name: str):
        file_name, file_extension = os.path.splitext(preference_name)
        ZukanPreference.build_icon_preference(file_name, preference_name)

    def input(self, args: dict):
        return InstallPreferenceInputHandler()


class InstallPreferenceInputHandler(sublime_plugin.ListInputHandler):
    """
    Zukan preferences list, created preferences excluded, and return preference_name
    to InstallPreference.
    """

    def name(self) -> str:
        return 'preference_name'

    def placeholder(self) -> str:
        return 'Zukan preferences list'

    def list_items(self) -> list:
        list_preferences_not_installed = []
        zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
        for p in zukan_icons:
            if p['preferences'].get('scope') is not None:
                list_preferences_not_installed.append(
                    p['preferences']['settings']['icon'] + TMPREFERENCES_EXTENSION
                )
        list_preferences_not_installed = list(
            set(list_preferences_not_installed).difference(
                ZukanPreference.list_created_icons_preferences()
            )
        )
        if list_preferences_not_installed:
            return sorted(list_preferences_not_installed)
        else:
            raise TypeError(
                logger.info('all preferences are already created, list is empty.')
            )


class InstallSyntax(sublime_plugin.TextCommand):
    """
    Sublime command to create syntax from zukan syntaxes list.
    """

    def run(self, edit, syntax_name: str):
        file_name, file_extension = os.path.splitext(syntax_name)
        # ZukanSyntax.create_icon_syntax(file_name)
        # Edit icon syntax contexts main if syntax not installed or ST3.
        # ZukanSyntax.edit_context_scope(syntax_name)

        InstallEvent.install_syntax(file_name, syntax_name)

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
        zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
        for s in zukan_icons:
            if s.get('syntax') is not None:
                for k in s['syntax']:
                    if k not in compare_scopes():
                        list_syntaxes_not_installed.append(
                            k['name'] + SUBLIME_SYNTAX_EXTENSION
                        )
        list_syntaxes_not_installed = list(
            set(list_syntaxes_not_installed).difference(
                ZukanSyntax.list_created_icons_syntaxes()
            )
        )
        if list_syntaxes_not_installed:
            return sorted(list_syntaxes_not_installed, key=lambda x: x.upper())
        else:
            raise TypeError(
                logger.info('all syntaxes are already created, list is empty.')
            )


class InstallTheme(sublime_plugin.TextCommand):
    """
    Sublime command to create theme from a list of installed themes.
    """

    def run(self, edit, theme_name: str):
        # 'zukan_restart_message' setting
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if zukan_restart_message is True:
            dialog_message = (
                'You may have to restart ST, if all icons do not load in '
                'current theme.'
            )
            sublime.message_dialog(dialog_message)

        ZukanTheme.create_icon_theme(theme_name)
        # Check if selected theme was installed
        SettingsEvent.get_user_theme()

    def input(self, args: dict):
        return InstallThemeInputHandler()


class InstallThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding created themes, and return theme_name
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
            if file_name not in ZukanTheme.list_created_icons_themes():
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
        # 'zukan_restart_message' setting
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if zukan_restart_message is True:
            dialog_message = (
                'You may have to restart ST, if all icons do not load in current '
                'theme.'
            )
            sublime.message_dialog(dialog_message)

        ZukanTheme.create_icons_themes()
        # Check if selected theme was installed
        SettingsEvent.get_user_theme()


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
            ZukanPreference.delete_icons_preferences()
            ZukanTheme.delete_icons_themes()
            ZukanSyntax.delete_icons_syntaxes()
        finally:
            InstallEvent.new_install_manually()


class RebuildPreferences(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild tmPreferences. First, try to remove all previous
    files.
    """

    def run(self):
        try:
            ZukanPreference.delete_icons_preferences()
        finally:
            ZukanPreference.build_icons_preferences()


class RebuildSyntaxes(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-syntaxes. First, try to remove all previous
    files.
    """

    def run(self):
        try:
            ZukanSyntax.delete_icons_syntaxes()
        finally:
            InstallEvent.install_syntaxes()
