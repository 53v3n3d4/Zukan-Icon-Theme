import logging
import os
import sublime
import sublime_plugin

from ..events.install import InstallEvent
from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.edit_file_extension import edit_file_extension
from ..helpers.load_save_settings import (
    get_ignored_icon_settings,
    get_theme_settings,
    is_zukan_restart_message,
)
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_syntaxes import compare_scopes
from ..helpers.search_themes import search_resources_sublime_themes
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
)

logger = logging.getLogger(__name__)


class DeletePreferenceCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete preference from a list of created preferences.
    """

    def run(self, edit, preference_name: str):
        if not preference_name == 'All':
            message = "Are you sure you want to delete '{p}'?".format(
                p=os.path.join(ZUKAN_PKG_ICONS_PREFERENCES_PATH, preference_name)
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanPreference.delete_icons_preference(preference_name)
        if preference_name == 'All':
            message = (
                "Are you sure you want to delete all preferences in '{f}'?".format(
                    f=ZUKAN_PKG_ICONS_PREFERENCES_PATH
                )
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanPreference.delete_icons_preferences()

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
            all_option = ['All']
            installed_preferences_list = sorted(
                ZukanPreference.list_created_icons_preferences()
            )
            new_list = all_option + installed_preferences_list
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created preference, list is empty')
            )


class DeleteSyntaxCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete syntax from a list of created syntaxes.
    """

    def run(self, edit, syntax_name: str):
        if not syntax_name == 'All':
            message = "Are you sure you want to delete '{s}'?".format(
                s=os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanSyntax.delete_icon_syntax(syntax_name)

        if syntax_name == 'All':
            message = "Are you sure you want to delete all syntaxes in '{f}'?".format(
                f=ZUKAN_PKG_ICONS_SYNTAXES_PATH
            )
            if sublime.ok_cancel_dialog(message) is True:
                ZukanSyntax.delete_icons_syntaxes()

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
            all_option = ['All']
            syntaxes_list = sorted(
                ZukanSyntax.list_created_icons_syntaxes(), key=lambda x: x.upper()
            )
            new_list = all_option + syntaxes_list
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created syntax, list is empty')
            )


class DeleteThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete theme from a list of created themes.
    """

    def run(self, edit, theme_name: str):
        # 'zukan_restart_message' setting
        zukan_restart_message = is_zukan_restart_message()

        if not theme_name == 'All':
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

        if theme_name == 'All':
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

        # Comment because change 'add_on_change' to event listener
        # Check if selected theme was deleted
        # ThemeListener.get_user_theme()

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
            all_option = ['All']
            installed_themes_list = sorted(ZukanTheme.list_created_icons_themes())
            new_list = all_option + installed_themes_list
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )


class InstallPreferenceCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create preference from zukan preferences list.
    """

    def run(self, edit, preference_name: str):
        file_name, file_extension = os.path.splitext(preference_name)

        if not preference_name == 'All':
            # 'ignored_icon' setting
            ignored_icon = get_ignored_icon_settings()

            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

            # 'create_custom_icon' setting
            custom_list = [p for p in create_custom_icon() if 'preferences' in p]
            new_list = zukan_icons + custom_list

            for p in new_list:
                if (
                    p['preferences']['settings']['icon'] == file_name
                    and p['name'] in ignored_icon
                ):
                    dialog_message = (
                        '{i} icon is disabled. Need to enable first.'.format(
                            i=p['name']
                        )
                    )
                    sublime.message_dialog(dialog_message)

                # Default icon
                # Need to add '-dark' or 'light' that was removed to mount list
                if p['preferences']['settings']['icon'][:-5] == file_name:
                    file_name = p['preferences']['settings']['icon']

                if p['preferences']['settings']['icon'][:-6] == file_name:
                    file_name = p['preferences']['settings']['icon']

            ZukanPreference.build_icon_preference(file_name, preference_name)

        if preference_name == 'All':
            ZukanPreference.build_icons_preferences()

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

        # 'create_custom_icon' setting
        custom_list = [p for p in create_custom_icon() if 'preferences' in p]
        new_list = zukan_icons + custom_list

        for p in new_list:
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
                ZukanPreference.list_created_icons_preferences()
            )
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


class InstallSyntaxCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create syntax from zukan syntaxes list.
    """

    def run(self, edit, syntax_name: str):
        file_name, file_extension = os.path.splitext(syntax_name)
        # ZukanSyntax.create_icon_syntax(file_name)
        # Edit icon syntax contexts main if syntax not installed or ST3.
        # ZukanSyntax.edit_context_scope(syntax_name)

        if not syntax_name == 'All':
            # 'ignored_icon' setting
            ignored_icon = get_ignored_icon_settings()

            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

            # 'create_custom_icon' setting
            custom_list = [s for s in create_custom_icon() if 'syntax' in s]
            new_list = zukan_icons + custom_list

            for d in new_list:
                if 'syntax' in d:
                    for s in d['syntax']:
                        if s['name'] == file_name and d['name'] in ignored_icon:
                            dialog_message = (
                                '{i} icon is disabled. Need to enable first.'.format(
                                    i=d['name']
                                )
                            )
                            sublime.message_dialog(dialog_message)

            InstallEvent.install_syntax(file_name, syntax_name)

        if syntax_name == 'All':
            InstallEvent.install_syntaxes()

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

        # 'create_custom_icon' setting
        custom_list = [s for s in create_custom_icon() if 'syntax' in s]
        new_list = zukan_icons + custom_list

        for s in new_list:
            if s.get('syntax') is not None:
                for k in s['syntax']:
                    if k not in compare_scopes():
                        # 'change_scope_file_extension' setting
                        k['file_extensions'] = edit_file_extension(
                            k['file_extensions'], k['scope']
                        )
                        # file_extensions list can be empty
                        if k['file_extensions']:
                            list_syntaxes_not_installed.append(
                                k['name'] + SUBLIME_SYNTAX_EXTENSION
                            )
        list_syntaxes_not_installed = list(
            set(list_syntaxes_not_installed).difference(
                ZukanSyntax.list_created_icons_syntaxes()
            )
        )
        if list_syntaxes_not_installed:
            all_option = ['All']
            syntaxes_list = sorted(list_syntaxes_not_installed, key=lambda x: x.upper())
            new_list = all_option + syntaxes_list
            return new_list
        else:
            raise TypeError(
                logger.info('all syntaxes are already created, list is empty.')
            )


class InstallThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create theme from a list of installed themes.
    """

    def run(self, edit, theme_st_path: str):
        # 'zukan_restart_message' setting
        zukan_restart_message = is_zukan_restart_message()

        if not theme_st_path == 'All':
            # 'ignored_theme' setting
            ignored_theme, _ = get_theme_settings()

            theme_name = os.path.basename(theme_st_path)

            if theme_name in ignored_theme:
                dialog_message = '{t} is disabled. Need to enable first.'.format(
                    t=theme_name
                )
                sublime.message_dialog(dialog_message)

            if zukan_restart_message is True and theme_name not in ignored_theme:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in '
                    'current theme.'
                )
                sublime.message_dialog(dialog_message)

            ZukanTheme.create_icon_theme(theme_st_path)

        if theme_st_path == 'All':
            if zukan_restart_message is True:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in current '
                    'theme.'
                )
                sublime.message_dialog(dialog_message)

            ZukanTheme.create_icons_themes()

        # Comment because change 'add_on_change' to event listener
        # Check if selected theme was installed
        # ThemeListener.get_user_theme()

    def input(self, args: dict):
        return InstallThemeInputHandler()


class InstallThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding created themes, and return theme_st_path
    to InstallTheme.
    """

    def name(self) -> str:
        return 'theme_st_path'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        list_themes_not_installed = []
        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in ZukanTheme.list_created_icons_themes():
                list_themes_not_installed.append(name)
        if list_themes_not_installed:
            all_option = ['All']
            themes_list = sorted(list_themes_not_installed)
            new_list = all_option + themes_list
            return new_list
            # return sorted(list_themes_not_installed)

        else:
            raise TypeError(
                logger.info('all themes are already created, list is empty.')
            )


class RebuildFilesCommand(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-themes and sublime-syntaxes.
    """

    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            # Syntax getting deleted in 'build_icons_preferences' which
            # is used by 'new_install_manually'
            # ZukanPreference.delete_icons_preferences()
            ZukanTheme.delete_icons_themes()
            # Syntax getting deleted in 'build_icons_syntaxes' which
            # is used by 'new_install_manually'
            # ZukanSyntax.delete_icons_syntaxes()
        finally:
            InstallEvent.new_install_manually()
