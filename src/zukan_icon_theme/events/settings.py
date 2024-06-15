import logging
import os
import sublime
import threading

from .install import InstallEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.read_write_data import dump_json_data
from ..helpers.thread_progress import ThreadProgress
from ..utils.zukan_dir_paths import (  # noqa: E402
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
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
        theme_name = sublime.load_settings('Preferences.sublime-settings').get('theme')

        auto_install_theme = sublime.load_settings(
            'Zukan Icon Theme.sublime-settings'
        ).get('auto_install_theme')

        if (
            theme_name not in ZukanTheme.list_created_icons_themes()
            and auto_install_theme is False
        ):
            # Delete preferences to avoid error unable to decode 'icon_file_type'
            # Example of extensions that this errors show: HAML, LICENSE, README, Makefile
            if any(
                syntax.endswith('.sublime-syntax')
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ZukanSyntax.delete_icons_syntaxes()
            if any(
                preferences.endswith('.tmPreferences')
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
                preferences.endswith('.tmPreferences')
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                threading.Thread(target=ZukanPreference.build_icons_preferences).start()

            if not any(
                syntax.endswith('.sublime-syntax')
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ts = threading.Thread(target=ZukanSyntax.build_icons_syntaxes)
                ts.start()
                ThreadProgress(ts, 'Building zukan files', 'Build done')

    def upgrade_zukan_files():
        """
        Event for setting 'version' in 'Zukan Icon Theme.sublime-settings'.

        If option is True, will rebuild preferences and syntaxes files.

        It compare with 'version' value from 'zukan-version.sublime-settings'.
        """
        logger.debug('If package upgraded, begin rebuild...')
        pkg_version = sublime.load_settings('Zukan Icon Theme.sublime-settings').get(
            'version'
        )

        auto_upgraded = sublime.load_settings('Zukan Icon Theme.sublime-settings').get(
            'rebuild_on_upgrade'
        )

        if os.path.exists(ZUKAN_VERSION_FILE) and auto_upgraded is True:
            installed_pkg_version = sublime.load_settings(
                'zukan-version.sublime-settings'
            ).get('version')

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

        if not os.path.exists(ZUKAN_VERSION_FILE):
            content = {'version': pkg_version}
            dump_json_data(content, ZUKAN_VERSION_FILE)

    def zukan_options_settings():
        """
        Call upgrade zukan files function if 'rebuild_on_upgrade' is True.
        """
        # auto_upgraded setting
        SettingsEvent.upgrade_zukan_files()

    def user_preferences_changed():
        """
        Listen to 'Preferences.sublime-settings'.
        """
        user_preferences = sublime.load_settings('Preferences.sublime-settings')

        user_preferences.add_on_change('Preferences', SettingsEvent.get_user_theme)

    def zukan_preferences_changed():
        """
        Listen to 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = sublime.load_settings('Zukan Icon Theme.sublime-settings')

        zukan_preferences.add_on_change(
            'Zukan Icon Theme', SettingsEvent.zukan_options_settings
        )
