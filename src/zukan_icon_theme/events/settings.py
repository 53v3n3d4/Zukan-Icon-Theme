import logging
import os
import threading

from .install import InstallEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.get_settings import load_settings
from ..helpers.read_write_data import dump_json_data
from ..helpers.thread_progress import ThreadProgress
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    USER_SETTINGS,
    ZUKAN_SETTINGS,
    ZUKAN_SETTINGS_OPTIONS,
    ZUKAN_VERSION,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
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

        It also create themes if setting 'auto_install_theme' is set to True.
        """
        logger.debug('Preferences.sublime-settings changed')
        theme_name = load_settings(USER_SETTINGS, 'theme')
        auto_install_theme = load_settings(ZUKAN_SETTINGS, 'auto_install_theme')

        if (
            theme_name not in ZukanTheme.list_created_icons_themes()
            and auto_install_theme is False
        ):
            # Delete preferences to avoid error unable to decode 'icon_file_type'
            # Example of extensions that this errors show: HAML, LICENSE, README, Makefile
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
        # 'Rebuild Syntaxes' is triggered here and build themes.
        if auto_install_theme is True:
            # ZukanTheme.create_icon_theme(theme_name)
            ZukanTheme.create_icons_themes()

        if theme_name in ZukanTheme.list_created_icons_themes():
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

    def get_user_zukan_preferences():
        """
        Print to console, current Zukan settings options.
        """
        log_level = load_settings(ZUKAN_SETTINGS, 'log_level')

        if log_level == 'DEBUG':
            print('==== Zukan Icon Theme settings ====')

            for s in ZUKAN_SETTINGS_OPTIONS:
                setting_option = load_settings(ZUKAN_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('------------------------------------')

    def upgrade_zukan_files():
        """
        Event for setting 'version' in 'Zukan Icon Theme.sublime-settings'.

        If option is True, will rebuild preferences and syntaxes files.

        It compare with 'version' value from 'zukan-version.sublime-settings'.
        """
        logger.debug('If package upgraded, begin rebuild...')
        pkg_version = load_settings(ZUKAN_SETTINGS, 'version')
        auto_upgraded = load_settings(ZUKAN_SETTINGS, 'rebuild_on_upgrade')

        if os.path.exists(ZUKAN_VERSION_FILE) and auto_upgraded is True:
            installed_pkg_version = load_settings(ZUKAN_VERSION, 'version')

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
                logger.debug('no need to update.')

            if tuple_pkg_version > tuple_installed_pkg_version:
                logger.info('updating package...')
                InstallEvent.install_upgrade_thread()

                content = {'version': pkg_version}
                dump_json_data(content, ZUKAN_VERSION_FILE)

        if auto_upgraded is False:
            logger.debug('auto_upgraded setting is False.')

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_VERSION_FILE):
            content = {'version': pkg_version}
            dump_json_data(content, ZUKAN_VERSION_FILE)

    def zukan_options_settings():
        """
        Call upgrade zukan files function if 'rebuild_on_upgrade' is True.
        """
        # auto_upgraded setting
        SettingsEvent.upgrade_zukan_files()

    def user_preferences_clear():
        """
        Clear 'add_on_change' 'Preferences.sublime-settings'.
        """
        user_preferences = load_settings(USER_SETTINGS)
        user_preferences.clear_on_change('Preferences')

    def user_preferences_changed():
        """
        Listen to 'Preferences.sublime-settings'.
        """
        user_preferences = load_settings(USER_SETTINGS)
        user_preferences.add_on_change('Preferences', SettingsEvent.get_user_theme)

    def zukan_preferences_clear():
        """
        Clear 'add_on_change' 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = load_settings(ZUKAN_SETTINGS)
        zukan_preferences.clear_on_change('Zukan Icon Theme')

    def zukan_preferences_changed():
        """
        Listen to 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = load_settings(ZUKAN_SETTINGS)
        zukan_preferences.add_on_change(
            'Zukan Icon Theme', SettingsEvent.zukan_options_settings
        )
