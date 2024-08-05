import logging
import os
import sublime
import threading

from .install import InstallEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.clean_settings import clean_comments_settings
from ..helpers.load_save_settings import get_settings
from ..helpers.read_write_data import dump_pickle_data, read_pickle_data
from ..helpers.search_themes import (
    filter_resources_themes,
    search_resources_sublime_themes,
)
from ..helpers.thread_progress import ThreadProgress
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    USER_SETTINGS,
    USER_SETTINGS_OPTIONS,
    ZUKAN_SETTINGS,
    ZUKAN_SETTINGS_OPTIONS,
    ZUKAN_VERSION,
)
from ..utils.zukan_paths import (
    ZUKAN_CURRENT_SETTINGS_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
    ZUKAN_USER_SUBLIME_SETTINGS,
    ZUKAN_VERSION_FILE,
)

logger = logging.getLogger(__name__)


class SettingsEvent:
    def get_user_theme():
        """
        Using sublime function 'add_on_change' to know when 'Preferences' settings
        is activated.

        This also activate when syntax is created or deleted, Seems when ST write to
        console 'generating syntax summary' trigger 'Preferences'.

        This function will check if theme changed then create or delete syntaxes
        and preferences for a icon theme.

        It creates themes if setting 'auto_install_theme' is set to True. And
        do not create theme if theme name in 'ignored_theme' setting.
        """
        logger.debug('Preferences.sublime-settings changed')
        theme_name = get_settings(USER_SETTINGS, 'theme')
        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')

        if (
            theme_name not in ZukanTheme.list_created_icons_themes()
            and auto_install_theme is False
        ) or theme_name in ignored_theme:
            # Delete preferences to avoid error unable to decode 'icon_file_type'
            # Example of extensions that this errors show: HAML, LICENSE, README,
            # Makefile
            if any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ZukanSyntax.delete_icons_syntaxes()
            if any(
                preferences.endswith(TMPREFERENCES_EXTENSION)
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                ZukanPreference.delete_icons_preferences()

        # 'auto_install_theme' setting
        # Commands 'Delete Syntax', 'Delete Syntaxes', 'Install Syntax' and
        # 'Rebuild Syntaxes' are triggered here and build themes.
        #
        # Creating icon theme if does not exist.
        if auto_install_theme is True and not os.path.exists(icon_theme_file):
            theme_st_path = sublime.find_resources(theme_name)
            # Excluding themes in Packages sub directories.
            filter_list = filter_resources_themes(theme_st_path)
            list_all_themes = search_resources_sublime_themes()
            # Check if installed theme file exist.
            for t in filter_list:
                if t in list_all_themes and os.path.basename(t) not in ignored_theme:
                    if zukan_restart_message is True:
                        dialog_message = (
                            'You may have to restart ST, if all icons do not load in '
                            'current theme.'
                        )
                        sublime.message_dialog(dialog_message)
                    ZukanTheme.create_icon_theme(t)

        if (
            theme_name in ZukanTheme.list_created_icons_themes()
            and theme_name not in ignored_theme
        ):
            if not any(
                preferences.endswith(TMPREFERENCES_EXTENSION)
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                threading.Thread(target=ZukanPreference.build_icons_preferences).start()

            if not any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ts = threading.Thread(target=ZukanSyntax.build_icons_syntaxes)
                ts.start()
                ThreadProgress(ts, 'Building zukan files', 'Build done')

        # Deleting ignored theme in case it already exists before ignoring.
        if theme_name in ignored_theme and os.path.exists(icon_theme_file):
            if zukan_restart_message is True:
                dialog_message = (
                    'You may have to restart ST, for all icons do not show.'
                )
                sublime.message_dialog(dialog_message)
            ZukanTheme.delete_icon_theme(theme_name)

    def get_user_zukan_preferences():
        """
        Print to console, current Zukan settings options.
        """
        log_level = get_settings(ZUKAN_SETTINGS, 'log_level')

        if log_level == 'DEBUG':
            print('\n==== Zukan Icon Theme settings ====')

            for s in ZUKAN_SETTINGS_OPTIONS:
                setting_option = get_settings(ZUKAN_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('\n==== User ST settings ==============')

            for s in USER_SETTINGS_OPTIONS:
                setting_option = get_settings(USER_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('------------------------------------')

    def save_current_settings():
        """
        Save current settings in pkl file to compare when Zukan settings options
        get modified.
        """
        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            # Delete previous pickle file
            os.remove(ZUKAN_CURRENT_SETTINGS_FILE)

        current_settings = {}

        for s in ZUKAN_SETTINGS_OPTIONS:
            setting_option = get_settings(ZUKAN_SETTINGS, s)
            current_settings.update({s: setting_option})
        dump_pickle_data(current_settings, ZUKAN_CURRENT_SETTINGS_FILE)

    def rebuild_icons_files():
        """
        Rebuild icons files, when icons settings change in Zukan preferences.
        """
        logger.debug('if icons settings changed, begin rebuild...')
        auto_rebuild_icon = get_settings(ZUKAN_SETTINGS, 'auto_rebuild_icon')

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and auto_rebuild_icon is True:
            data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)
            # print(data)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
            change_icon_file_extension = get_settings(
                ZUKAN_SETTINGS, 'change_icon_file_extension'
            )
            create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')

            for d in data:
                # Currently, rebuilding all files, because of manually editing
                # sublime-settings, it is possible to have multiple entries.

                # Check if ignored_icon changed
                if sorted(d['ignored_icon']) != sorted(ignored_icon):
                    logger.info('"ignored_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                    SettingsEvent.save_current_settings()

                # Check if change_icon changed
                if sorted(d['change_icon']) != sorted(change_icon) or any(
                    [change_icon.get(k) != v for k, v in d['change_icon'].items()]
                ):
                    logger.info('"change_icon" changed, rebuilding files...')
                    ZukanPreference.build_icons_preferences()

                    SettingsEvent.save_current_settings()

                    # Command 'reset_icon' leaves entries commented in dict.
                    # It is working but still leaving the last reset one, because
                    # 'reloading settings Packages/User/Zukan Icon Theme.sublime-settings'
                    # happens after cleaning.
                    # It could left multiple commented entries if 'reset_icon > all' was
                    # used.
                    clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)

                # Check if change_icon_file_extension changed
                if any(
                    x != y
                    for x, y in zip(
                        d['change_icon_file_extension'], change_icon_file_extension
                    )
                ) or len(d['change_icon_file_extension']) != len(
                    change_icon_file_extension
                ):
                    logger.info(
                        '"change_icon_file_extension" changed, rebuilding files...'
                    )
                    InstallEvent.install_syntaxes()

                    SettingsEvent.save_current_settings()

                # Check if create_custom_icon changed
                if any(
                    x != y for x, y in zip(d['create_custom_icon'], create_custom_icon)
                ) or len(d['create_custom_icon']) != len(create_custom_icon):
                    logger.info('"create_custom_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                    SettingsEvent.save_current_settings()

                    # 'create_custom_icon' also leaves commented entries when deleted
                    # using 'delete_custom_icon'. Same as 'reset_icon', but
                    # 'delete_custom_icon' leaves identation messed, and mix commented
                    # entries between othes entries.
                    clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)

        if auto_rebuild_icon is False:
            logger.debug('auto_rebuild_icon setting is False.')

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            SettingsEvent.save_current_settings()

    def upgrade_zukan_files():
        """
        Event for setting 'version' in 'Zukan Icon Theme.sublime-settings'.

        If option is True, will rebuild preferences and syntaxes files.

        It compares with 'version' value from 'zukan_current_settings.pkl'.
        """
        logger.debug('if package upgraded, begin rebuild...')
        pkg_version = get_settings(ZUKAN_SETTINGS, 'version')
        auto_upgraded = get_settings(ZUKAN_SETTINGS, 'rebuild_on_upgrade')

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and auto_upgraded is True:
            # installed_pkg_version = get_settings(ZUKAN_VERSION, 'version')
            data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)
            installed_pkg_version = ''.join(
                [d['version'] for d in data if 'version' in d]
            )
            # print(installed_pkg_version)

            # Transform string to tuple to compare.
            tuple_installed_pkg_version = tuple(
                map(int, installed_pkg_version.split('.'))
            )
            tuple_pkg_version = tuple(map(int, pkg_version.split('.')))
            # print(tuple_installed_pkg_version)
            # print(tuple_pkg_version)
            # print((0, 1, 73) > (0, 1, 72))
            # print((0, 1, 72) == (0, 1, 72))
            if tuple_pkg_version == tuple_installed_pkg_version:
                logger.debug('no need to update')

            if tuple_pkg_version > tuple_installed_pkg_version:
                logger.info('updating package...')
                InstallEvent.install_upgrade_thread()

                # content = {'version': pkg_version}
                # dump_json_data(content, ZUKAN_VERSION_FILE)
                SettingsEvent.save_current_settings()

        if auto_upgraded is False:
            logger.debug('auto_upgraded setting is False.')

        # Setting file `zukan-version` depreceated in favor of `zukan_current_settings`
        # Need to upgrade from v0.3.0 to v0.3.1, where there is no
        # zukan_current_settings below v0.3.0.
        if os.path.exists(ZUKAN_VERSION_FILE) and auto_upgraded is True:
            version_json_file = get_settings(ZUKAN_VERSION, 'version')
            tuple_version_json_file = tuple(map(int, version_json_file.split('.')))

            tuple_version_pkg = tuple(map(int, pkg_version.split('.')))

            if tuple_version_json_file <= (0, 3, 0) and tuple_version_pkg >= (0, 3, 1):
                logger.info('removing depreceated file "zukan-version"')
                os.remove(ZUKAN_VERSION_FILE)

                logger.info('updating package...')
                InstallEvent.install_upgrade_thread()

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        # if not os.path.exists(ZUKAN_VERSION_FILE):
        #     content = {'version': pkg_version}
        #     dump_json_data(content, ZUKAN_VERSION_FILE)
        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            SettingsEvent.save_current_settings()

    def zukan_options_settings():
        """
        Call upgrade zukan files function if 'rebuild_on_upgrade' is True.
        """
        # auto_upgraded setting
        SettingsEvent.upgrade_zukan_files()

        # auto_rebuild_icon setting
        # If not load in file_type_icons, log messages duplicated when changed
        # through commands_settings. It does not happen when manually changed
        # in sublime-settings file.
        # Having auto_rebuild_icon in load, helps in case where zukan current
        # settings file does not exist yet, and settings are modified.
        SettingsEvent.rebuild_icons_files()

    def user_preferences_clear():
        """
        Clear 'add_on_change' 'Preferences.sublime-settings'.
        """
        user_preferences = get_settings(USER_SETTINGS)
        user_preferences.clear_on_change('Preferences')

    def user_preferences_changed():
        """
        Listen to 'Preferences.sublime-settings'.
        """
        user_preferences = get_settings(USER_SETTINGS)
        user_preferences.add_on_change('Preferences', SettingsEvent.get_user_theme)

    def zukan_preferences_clear():
        """
        Clear 'add_on_change' 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.clear_on_change('Zukan Icon Theme')

    def zukan_preferences_changed():
        """
        Listen to 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.add_on_change(
            'Zukan Icon Theme', SettingsEvent.zukan_options_settings
        )
