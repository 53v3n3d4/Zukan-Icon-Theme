import logging
import os

from collections.abc import Callable
from .install import InstallEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..helpers.clean_comments import CleanComments
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
    ZUKAN_CURRENT_SETTINGS_FILE,
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
    ZUKAN_VERSION_FILE,
)

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event bus to allow communication between UpgradePlugin and ZukanIconFiles.
    """

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name: str, listener: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def publish(self, event_name: str):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener()


class ZukanIconFiles:
    """
    Modify icons, if need, when Zukan Preferences settings change.
    """

    def __init__(
        self,
        event_bus: EventBus,
        clean_comments: CleanComments = None,
        install_event: InstallEvent = None,
        zukan_preference: ZukanPreference = None,
        zukan_syntax: ZukanSyntax = None,
    ):
        self.event_bus = event_bus
        self.clean_comments = clean_comments if clean_comments else CleanComments()
        self.install_event = install_event if install_event else InstallEvent()
        self.zukan_preference = (
            zukan_preference if zukan_preference else ZukanPreference()
        )
        self.zukan_syntax = zukan_syntax if zukan_syntax else ZukanSyntax()

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            self.data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)
        else:
            self.data = []

        self.auto_rebuild_icon = get_settings(ZUKAN_SETTINGS, 'auto_rebuild_icon')
        self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()
        self.change_icon, self.change_icon_file_extension = get_change_icon_settings()
        self.ignored_icon = get_ignored_icon_settings()

        self.create_custom_icon = get_create_custom_icon_settings()
        self.current_settings = read_current_settings()

        self.is_upgrading = False
        self.event_bus.subscribe('upgrade_started', self.on_upgrade_started)
        self.event_bus.subscribe('upgrade_finished', self.on_upgrade_finished)

        # Tracks rebuild functions
        self.rebuild_functions = {
            'rebuild_icon_files_thread': False,
            'build_icons_preferences': False,
            'install_syntaxes': False,
        }

    def on_upgrade_started(self):
        self.is_upgrading = True
        logger.debug('upgrade started, skipping rebuild.')

    def on_upgrade_finished(self):
        self.is_upgrading = False
        logger.debug('upgrade finished, rebuild can proceed.')

    def rebuild_icons_files(self, event_bus: EventBus):
        """
        Rebuild icons files, when icons settings change in Zukan preferences.
        """
        logger.debug('if icons settings changed, begin rebuild...')

        auto_rebuild_icon = self.auto_rebuild_icon

        if not self.is_upgrading:
            if (
                os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE)
                and auto_rebuild_icon is True
            ):
                # data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)

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
                        self.rebuild_functions['rebuild_icon_files_thread'] = True

                    # Check if change_icon changed
                    if sorted(d['change_icon']) != sorted(self.change_icon) or any(
                        [
                            self.change_icon.get(k) != v
                            for k, v in d['change_icon'].items()
                        ]
                    ):
                        logger.info('"change_icon" changed, rebuilding files...')
                        self.rebuild_functions['build_icons_preferences'] = True

                    # Check if change_icon_file_extension changed
                    if any(
                        x != y
                        for x, y in zip(
                            d['change_icon_file_extension'],
                            self.change_icon_file_extension,
                        )
                    ) or len(d['change_icon_file_extension']) != len(
                        self.change_icon_file_extension
                    ):
                        logger.info(
                            '"change_icon_file_extension" changed, rebuilding files...'
                        )
                        self.rebuild_functions['install_syntaxes'] = True

                    # Check if create_custom_icon changed
                    if any(
                        x != y
                        for x, y in zip(
                            d['create_custom_icon'], self.create_custom_icon
                        )
                    ) or len(d['create_custom_icon']) != len(self.create_custom_icon):
                        logger.info('"create_custom_icon" changed, rebuilding files...')
                        self.rebuild_functions['rebuild_icon_files_thread'] = True

                    # Check if prefer_icon changed
                    if sorted(d['prefer_icon']) != sorted(self.prefer_icon) or any(
                        [
                            self.prefer_icon.get(k) != v
                            for k, v in d['prefer_icon'].items()
                        ]
                    ):
                        logger.info('"prefer_icon" changed, rebuilding files...')
                        self.rebuild_functions['build_icons_preferences'] = True

                    self.execute_rebuilds()

            if auto_rebuild_icon is False:
                logger.debug('auto_rebuild_icon setting is False.')

            if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
                os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

            if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
                save_current_settings()

        else:
            logger.debug('upgrade in progress, delay rebuild.')

    def execute_rebuilds(self):
        """
        Rebuild functions that have been changed.
        """
        # Rebuild icons preferences
        if (
            self.rebuild_functions['build_icons_preferences']
            and not self.rebuild_functions['rebuild_icon_files_thread']
        ):
            self.zukan_preference.build_icons_preferences()
            self.rebuild_functions['build_icons_preferences'] = False

            # Command 'reset_icon' leaves entries commented in dict.
            # It is working but still leaving the last reset one, because
            # 'reloading settings Packages/User/Zukan Icon Theme.sublime-settings'
            # happens after cleaning.
            # It could left multiple commented entries if 'reset_icon > all' was
            # used.
            #
            # 'select_prefer_icon' also leaves entries commented.
            #
            self.clean_comments.clean_comments()

        # Rebuild icons syntaxes
        if (
            self.rebuild_functions['install_syntaxes']
            and not self.rebuild_functions['rebuild_icon_files_thread']
        ):
            self.zukan_syntax.install_syntaxes()
            self.rebuild_functions['install_syntaxes'] = False

        # Rebuild icons preferences and syntaxes
        if self.rebuild_functions['rebuild_icon_files_thread']:
            self.install_event.rebuild_icon_files_thread()
            self.rebuild_functions['rebuild_icon_files_thread'] = False

            # 'create_custom_icon' also leaves commented entries when deleted
            # using 'delete_custom_icon'. Same as 'reset_icon', but
            # 'delete_custom_icon' leaves identation messed, and mix commented
            # entries between othes entries.
            self.clean_comments.clean_comments()


class SettingsEvent:
    """
    Watch Zukan Preferences settings.
    """

    @staticmethod
    def get_user_zukan_preferences() -> str:
        folder_size = bytes_to_readable_size(get_folder_size(ZUKAN_PKG_PATH))
        zip_size = bytes_to_readable_size(get_file_size(ZUKAN_INSTALLED_PKG_PATH))

        zukan_opts_list = []
        for s in ZUKAN_SETTINGS_OPTIONS:
            setting_option = get_settings(ZUKAN_SETTINGS, s)
            line = '\t{s}: {v}\n'.format(s=s, v=setting_option)
            zukan_opts_list.append(line)

        user_pref_list = []
        for s in USER_SETTINGS_OPTIONS:
            setting_option = get_settings(USER_SETTINGS, s)
            line = '\t{s}: {v}\n'.format(s=s, v=setting_option)
            user_pref_list.append(line)

        # lines
        header_zukan = '==== Zukan Icon Theme settings ===='
        zukan_pkg_folder = 'Zukan folder size: {f}'.format(f=folder_size)
        zukan_installed_zip_file = 'sublime-package size: {z}'.format(z=zip_size)
        zukan_opts_to_str = ''.join(zukan_opts_list)
        header_st = '==== User ST settings =============='
        user_pref_to_str = ''.join(user_pref_list)
        end_line = '------------------------------------'

        new_line = '\n'
        tab_indent = '\t'

        data = (
            new_line
            + tab_indent
            + header_zukan
            + new_line
            + tab_indent
            + zukan_pkg_folder
            + new_line
            + tab_indent
            + zukan_installed_zip_file
            + new_line
            + new_line
            + zukan_opts_to_str
            + new_line
            + tab_indent
            + header_st
            + new_line
            + user_pref_to_str
            + new_line
            + tab_indent
            + end_line
        )

        return data

    @staticmethod
    def output_to_console_zukan_pref_settings():
        """
        Print to console, current Zukan settings options.
        """
        log_level = get_settings(ZUKAN_SETTINGS, 'log_level')

        if log_level == 'DEBUG':
            print(SettingsEvent.get_user_zukan_preferences())

    def zukan_options_settings():
        """
        Call upgrade zukan files function if 'rebuild_on_upgrade' is True.

        Also, call rebuild icons files when settings change.
        """

        event_bus = EventBus()

        # auto_upgraded setting
        upgrade_zukan = UpgradePlugin(event_bus)
        upgrade_zukan.start_upgrade()

        # auto_rebuild_icon setting
        # If not load in file_type_icons, log messages duplicated when changed
        # through commands_settings. It does not happen when manually changed
        # in sublime-settings file.
        # Having auto_rebuild_icon in load, helps in case where zukan current
        # settings file does not exist yet, and settings are modified.
        zukan_icon_files = ZukanIconFiles(event_bus)
        zukan_icon_files.rebuild_icons_files(event_bus)

    @staticmethod
    def zukan_preferences_clear():
        """
        Clear 'add_on_change' 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.clear_on_change('Zukan Icon Theme')

    @staticmethod
    def zukan_preferences_changed():
        """
        Listen to 'Zukan Icon Theme.sublime-settings'.
        """
        zukan_preferences = get_settings(ZUKAN_SETTINGS)
        zukan_preferences.add_on_change(
            'Zukan Icon Theme', SettingsEvent.zukan_options_settings
        )


class UpgradePlugin:
    """
    Watch when package is upgraded and rebuild files.
    """

    def __init__(
        self,
        event_bus: EventBus,
        install_event: InstallEvent = None,
    ):
        self.event_bus = event_bus
        self.is_upgrading = False
        self.install_event = install_event if install_event else InstallEvent()

        self.pkg_version, self.auto_upgraded = get_upgraded_version_settings()
        self.version_json_file = get_settings(ZUKAN_VERSION, 'version')

    def start_upgrade(self):
        """
        Allow upgrade zukan files and delay rebuild icon files.
        """
        self.is_upgrading = True
        self.event_bus.publish('upgrade_started')

        self.upgrade_zukan_files()

        self.is_upgrading = False
        self.event_bus.publish('upgrade_finished')

    def upgrade_zukan_files(self):
        """
        Event for setting 'version' in 'Zukan Icon Theme.sublime-settings'.

        If option is True, will rebuild preferences and syntaxes files.

        It compares with 'version' value from 'zukan_current_settings.pkl'.
        """
        logger.debug('if package upgraded, begin rebuild...')

        if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE) and self.auto_upgraded is True:
            data = read_pickle_data(ZUKAN_CURRENT_SETTINGS_FILE)

            installed_pkg_version = ''.join(
                [d['version'] for d in data if 'version' in d]
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
                self.install_event.install_upgrade_thread()

                save_current_settings()

        # Setting file `zukan-version` depreceated in favor of `zukan_current_settings`
        # Need to upgrade from v0.3.0 to v0.3.1, where there is no
        # zukan_current_settings below v0.3.0.
        if os.path.exists(ZUKAN_VERSION_FILE) and self.auto_upgraded is True:
            tuple_version_json_file = tuple(map(int, self.version_json_file.split('.')))

            tuple_version_pkg = tuple(map(int, self.pkg_version.split('.')))

            if tuple_version_json_file <= (0, 3, 0) and tuple_version_pkg >= (0, 3, 1):
                logger.info('removing depreceated file "zukan-version"')
                os.remove(ZUKAN_VERSION_FILE)

                logger.info('updating package...')
                self.install_event.install_upgrade_thread()

        if self.auto_upgraded is False:
            logger.debug('auto_upgraded setting is False.')

        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
            save_current_settings()
