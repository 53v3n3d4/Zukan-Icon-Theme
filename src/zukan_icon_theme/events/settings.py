import logging
import os

from .install import InstallEvent, InstallEventE2
from ..commands.clean_comments import CleanComments
from ..lib.icons_preferences import ZukanPreference, ZukanPreferenceP2
from ..helpers.load_save_settings import (
    get_create_custom_icon_settings,
    get_change_icon_settings,
    get_ignored_icon_settings,
    get_prefer_icon_settings,
    get_settings,
    get_upgraded_version_settings,
    save_current_settings,
    read_current_settings,
)
from ..helpers.package_size import (
    bytes_to_readable_size,
    get_folder_size,
    get_file_size,
)
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

            folder_size = bytes_to_readable_size(get_folder_size(ZUKAN_PKG_PATH))
            print('Zukan folder size: {f}'.format(f=folder_size))

            zip_size = bytes_to_readable_size(get_file_size(ZUKAN_INSTALLED_PKG_PATH))
            print('sublime-package size: {z}'.format(z=zip_size))

            ruamel_size = bytes_to_readable_size(get_folder_size(LIB_RUAMEL_YAML_PATH))
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

            auto_prefer_icon, prefer_icon = get_prefer_icon_settings()
            change_icon, change_icon_file_extension = get_change_icon_settings()
            ignored_icon = get_ignored_icon_settings()

            create_custom_icon = get_create_custom_icon_settings()
            current_settings = read_current_settings()

            for d in data:
                # Currently, rebuilding all files, because of manually editing
                # sublime-settings, it is possible to have multiple entries.

                # When new settings added, need to include in zukan fike
                # before compare. Or it will raise key error.
                for k, v in current_settings.items():
                    if k not in d:
                        d.update({k: v})

                    save_current_settings()

                # Check if ignored_icon changed
                if sorted(d['ignored_icon']) != sorted(ignored_icon):
                    logger.info('"ignored_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                # Check if change_icon changed
                if sorted(d['change_icon']) != sorted(change_icon) or any(
                    [change_icon.get(k) != v for k, v in d['change_icon'].items()]
                ):
                    logger.info('"change_icon" changed, rebuilding files...')
                    ZukanPreference.build_icons_preferences()

                    # Command 'reset_icon' leaves entries commented in dict.
                    # It is working but still leaving the last reset one, because
                    # 'reloading settings Packages/User/Zukan Icon Theme.sublime-settings'
                    # happens after cleaning.
                    # It could left multiple commented entries if 'reset_icon > all' was
                    # used.
                    cleaner = CleanComments()
                    cleaner.clean_comments()
                    # self.clean_comments(self.file_path)

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

                # Check if create_custom_icon changed
                if any(
                    x != y for x, y in zip(d['create_custom_icon'], create_custom_icon)
                ) or len(d['create_custom_icon']) != len(create_custom_icon):
                    logger.info('"create_custom_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                    # 'create_custom_icon' also leaves commented entries when deleted
                    # using 'delete_custom_icon'. Same as 'reset_icon', but
                    # 'delete_custom_icon' leaves identation messed, and mix commented
                    # entries between othes entries.
                    cleaner = CleanComments()
                    cleaner.clean_comments()
                    # self.clean_comments(self.file_path)

                # Check if prefer_icon changed
                if sorted(d['prefer_icon']) != sorted(prefer_icon) or any(
                    [prefer_icon.get(k) != v for k, v in d['prefer_icon'].items()]
                ):
                    logger.info('"prefer_icon" changed, rebuilding files...')
                    ZukanPreference.build_icons_preferences()

                    cleaner = CleanComments()
                    cleaner.clean_comments()
                    # self.clean_comments(self.file_path)

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
        pkg_version, auto_upgraded = get_upgraded_version_settings()

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

        Also, call rebuild icons files when settings change.
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


class SettingsEventE2(CleanComments, InstallEventE2, ZukanPreferenceP2):
    def __init__(self):
        CleanComments.__init__(self)
        InstallEventE2.__init__(self)
        ZukanPreferenceP2.__init__(self)

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            self.data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)

        self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()
        self.change_icon, self.change_icon_file_extension = get_change_icon_settings()
        self.ignored_icon = get_ignored_icon_settings()

        self.create_custom_icon = get_create_custom_icon_settings()
        self.current_settings = read_current_settings()

        self.version_json_file = get_settings(ZUKAN_VERSION, 'version')

    def get_user_zukan_preferences(self):
        """
        Print to console, current Zukan settings options.
        """
        log_level = get_settings(ZUKAN_SETTINGS, 'log_level')

        if log_level == 'DEBUG':
            print('\n==== Zukan Icon Theme settings ====')

            folder_size = bytes_to_readable_size(get_folder_size(ZUKAN_PKG_PATH))
            print('Zukan folder size: {f}'.format(f=folder_size))

            zip_size = bytes_to_readable_size(get_file_size(ZUKAN_INSTALLED_PKG_PATH))
            print('sublime-package size: {z}'.format(z=zip_size))

            ruamel_size = bytes_to_readable_size(get_folder_size(LIB_RUAMEL_YAML_PATH))
            print('Ruamel size: {r}'.format(r=ruamel_size))

            for s in ZUKAN_SETTINGS_OPTIONS:
                setting_option = get_settings(ZUKAN_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('\n==== User ST settings ==============')

            for s in USER_SETTINGS_OPTIONS:
                setting_option = get_settings(USER_SETTINGS, s)
                print('{s}: {v}'.format(s=s, v=setting_option))

            print('------------------------------------')

    def rebuild_icons_files(self):
        """
        Rebuild icons files, when icons settings change in Zukan preferences.
        """
        logger.debug('if icons settings changed, begin rebuild...')
        auto_rebuild_icon = get_settings(ZUKAN_SETTINGS, 'auto_rebuild_icon')

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and auto_rebuild_icon is True:
            # data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)

            # auto_prefer_icon, prefer_icon = get_prefer_icon_settings()
            # change_icon, change_icon_file_extension = get_change_icon_settings()
            # ignored_icon = get_ignored_icon_settings()

            # create_custom_icon = get_create_custom_icon_settings()
            # current_settings = read_current_settings()

            for d in self.data:
                # Currently, rebuilding all files, because of manually editing
                # sublime-settings, it is possible to have multiple entries.

                # When new settings added, need to include in zukan fike
                # before compare. Or it will raise key error.
                for k, v in self.current_settings.items():
                    if k not in d:
                        d.update({k: v})

                    save_current_settings()

                # Check if ignored_icon changed
                if sorted(d['ignored_icon']) != sorted(self.ignored_icon):
                    logger.info('"ignored_icon" changed, rebuilding files...')
                    InstallEvent.rebuild_icon_files_thread()

                # Check if change_icon changed
                if sorted(d['change_icon']) != sorted(self.change_icon) or any(
                    [self.change_icon.get(k) != v for k, v in d['change_icon'].items()]
                ):
                    logger.info('"change_icon" changed, rebuilding files...')
                    self.build_icons_preferences()

                    # Command 'reset_icon' leaves entries commented in dict.
                    # It is working but still leaving the last reset one, because
                    # 'reloading settings Packages/User/Zukan Icon Theme.sublime-settings'
                    # happens after cleaning.
                    # It could left multiple commented entries if 'reset_icon > all' was
                    # used.
                    self.clean_comments()

                # Check if change_icon_file_extension changed
                if any(
                    x != y
                    for x, y in zip(
                        d['change_icon_file_extension'], self.change_icon_file_extension
                    )
                ) or len(d['change_icon_file_extension']) != len(
                    self.change_icon_file_extension
                ):
                    logger.info(
                        '"change_icon_file_extension" changed, rebuilding files...'
                    )
                    self.install_syntaxes()

                # Check if create_custom_icon changed
                if any(
                    x != y
                    for x, y in zip(d['create_custom_icon'], self.create_custom_icon)
                ) or len(d['create_custom_icon']) != len(self.create_custom_icon):
                    logger.info('"create_custom_icon" changed, rebuilding files...')
                    self.rebuild_icon_files_thread()

                    # 'create_custom_icon' also leaves commented entries when deleted
                    # using 'delete_custom_icon'. Same as 'reset_icon', but
                    # 'delete_custom_icon' leaves identation messed, and mix commented
                    # entries between othes entries.
                    self.clean_comments()

                # Check if prefer_icon changed
                if sorted(d['prefer_icon']) != sorted(self.prefer_icon) or any(
                    [self.prefer_icon.get(k) != v for k, v in d['prefer_icon'].items()]
                ):
                    logger.info('"prefer_icon" changed, rebuilding files...')
                    self.build_icons_preferences()

                    self.clean_comments()

        if auto_rebuild_icon is False:
            logger.debug('auto_rebuild_icon setting is False.')

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            save_current_settings()

    def upgrade_zukan_files(self):
        """
        Event for setting 'version' in 'Zukan Icon Theme.sublime-settings'.

        If option is True, will rebuild preferences and syntaxes files.

        It compares with 'version' value from 'zukan_current_settings.pkl'.
        """
        logger.debug('if package upgraded, begin rebuild...')
        # pkg_version, auto_upgraded = get_upgraded_version_settings()

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and self.auto_upgraded is True:
            # data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)
            installed_pkg_version = ''.join(
                [d['version'] for d in self.data if 'version' in d]
            )

            # Transform string to tuple to compare.
            tuple_installed_pkg_version = tuple(
                map(int, installed_pkg_version.split('.'))
            )
            tuple_pkg_version = tuple(map(int, self.pkg_version.split('.')))
            # print(tuple_installed_pkg_version)
            # print(tuple_pkg_version)
            # print((0, 1, 73) > (0, 1, 72))
            # print((0, 1, 72) == (0, 1, 72))
            if tuple_pkg_version == tuple_installed_pkg_version:
                logger.debug('no need to update')

            if tuple_pkg_version > tuple_installed_pkg_version:
                logger.info('updating package...')
                self.install_upgrade_thread()

                save_current_settings()

        if self.auto_upgraded is False:
            logger.debug('auto_upgraded setting is False.')

        # Setting file `zukan-version` depreceated in favor of `zukan_current_settings`
        # Need to upgrade from v0.3.0 to v0.3.1, where there is no
        # zukan_current_settings below v0.3.0.
        if os.path.exists(ZUKAN_VERSION_FILE) and self.auto_upgraded is True:
            # version_json_file = get_settings(ZUKAN_VERSION, 'version')
            tuple_version_json_file = tuple(map(int, self.version_json_file.split('.')))

            tuple_version_pkg = tuple(map(int, self.pkg_version.split('.')))

            if tuple_version_json_file <= (0, 3, 0) and tuple_version_pkg >= (0, 3, 1):
                logger.info('removing depreceated file "zukan-version"')
                os.remove(ZUKAN_VERSION_FILE)

                logger.info('updating package...')
                self.install_upgrade_thread()

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            save_current_settings()

    def zukan_options_settings(self):
        """
        Call upgrade zukan files function if 'rebuild_on_upgrade' is True.

        Also, call rebuild icons files when settings change.
        """
        # auto_upgraded setting
        self.upgrade_zukan_files()

        # auto_rebuild_icon setting
        # If not load in file_type_icons, log messages duplicated when changed
        # through commands_settings. It does not happen when manually changed
        # in sublime-settings file.
        # Having auto_rebuild_icon in load, helps in case where zukan current
        # settings file does not exist yet, and settings are modified.
        self.rebuild_icons_files()

    def zukan_preferences_clear(self):
        """
        Clear 'add_on_change' 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.clear_on_change('Zukan Icon Theme')

    def zukan_preferences_changed(self):
        """
        Listen to 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.add_on_change(
            'Zukan Icon Theme', SettingsEvent.zukan_options_settings
        )
