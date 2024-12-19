import logging
import os

from .install import InstallEvent
from ..lib.icons_preferences import ZukanPreference
from ..helpers.clean_settings import clean_comments_settings
from ..helpers.load_save_settings import (
    get_settings,
    save_current_settings,
    read_current_settings,
)
from ..helpers.package_size import file_size, get_size
from ..helpers.read_write_data import read_pickle_data
from ..utils.file_settings import (
    USER_SETTINGS,
    USER_SETTINGS_OPTIONS,
    ZUKAN_SETTINGS,
    ZUKAN_SETTINGS_OPTIONS,
    ZUKAN_VERSION,
)
from ..utils.zukan_paths import (
    LIB_RUAMEL_YAML_PATH,
    ZUKAN_CURRENT_SETTINGS_FILE,
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
    ZUKAN_USER_SUBLIME_SETTINGS,
    ZUKAN_VERSION_FILE,
)

logger = logging.getLogger(__name__)


class SettingsEvent:
    def get_user_zukan_preferences():
        """
        Print to console, current Zukan settings options.
        """
        log_level = get_settings(ZUKAN_SETTINGS, 'log_level')

        if log_level == 'DEBUG':
            print('\n==== Zukan Icon Theme settings ====')

            installation_size = file_size(
                get_size([ZUKAN_PKG_PATH, ZUKAN_INSTALLED_PKG_PATH])
            )
            print('Install size: {i}'.format(i=installation_size))

            ruamel_size = file_size(get_size([LIB_RUAMEL_YAML_PATH]))
            print('Ruamel size: {r}'.format(r=ruamel_size))

            for s in ZUKAN_SETTINGS_OPTIONS:
                setting_option = get_settings(ZUKAN_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('\n==== User ST settings ==============')

            for s in USER_SETTINGS_OPTIONS:
                setting_option = get_settings(USER_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('------------------------------------')

    def rebuild_icons_files():
        """
        Rebuild icons files, when icons settings change in Zukan preferences.
        """
        logger.debug('if icons settings changed, begin rebuild...')
        auto_rebuild_icon = get_settings(ZUKAN_SETTINGS, 'auto_rebuild_icon')

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and auto_rebuild_icon is True:
            data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)

            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
            change_icon_file_extension = get_settings(
                ZUKAN_SETTINGS, 'change_icon_file_extension'
            )
            create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')
            prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')
            current_settings = read_current_settings()

            for d in data:
                # Currently, rebuilding all files, because of manually editing
                # sublime-settings, it is possible to have multiple entries.

                # When new option settings added, need to include in zukan fike
                # before compare. Or it will raise key error.
                for k, v in current_settings.items():
                    if k not in d:
                        d.update({k: v})

                    save_current_settings()

                # Check if ignored_icon changed
                if sorted(d['ignored_icon']) != sorted(ignored_icon):
                    logger.info('"ignored_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                    save_current_settings()

                # Check if change_icon changed
                if sorted(d['change_icon']) != sorted(change_icon) or any(
                    [change_icon.get(k) != v for k, v in d['change_icon'].items()]
                ):
                    logger.info('"change_icon" changed, rebuilding files...')
                    ZukanPreference.build_icons_preferences()

                    save_current_settings()

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

                    save_current_settings()

                # Check if create_custom_icon changed
                if any(
                    x != y for x, y in zip(d['create_custom_icon'], create_custom_icon)
                ) or len(d['create_custom_icon']) != len(create_custom_icon):
                    logger.info('"create_custom_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                    save_current_settings()

                    # 'create_custom_icon' also leaves commented entries when deleted
                    # using 'delete_custom_icon'. Same as 'reset_icon', but
                    # 'delete_custom_icon' leaves identation messed, and mix commented
                    # entries between othes entries.
                    clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)

                # Check if prefer_icon changed
                if sorted(d['prefer_icon']) != sorted(prefer_icon) or any(
                    [prefer_icon.get(k) != v for k, v in d['prefer_icon'].items()]
                ):
                    logger.info('"prefer_icon" changed, rebuilding files...')
                    ZukanPreference.build_icons_preferences()

                    save_current_settings()

                    clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)

        if auto_rebuild_icon is False:
            logger.debug('auto_rebuild_icon setting is False.')

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            save_current_settings()

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
            data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)
            installed_pkg_version = ''.join(
                [d['version'] for d in data if 'version' in d]
            )

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

                save_current_settings()

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

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            save_current_settings()

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
