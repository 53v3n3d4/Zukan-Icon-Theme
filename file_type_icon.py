import os
import sublime

# fmt: off
from .src.zukan_icon_theme.core.change_file_extension import ChangeFileExtensionCommand  # noqa F401
from .src.zukan_icon_theme.core.change_file_extension import ResetFileExtensionCommand  # noqa F401
from .src.zukan_icon_theme.core.change_icon import ChangeIconCommand  # noqa F401
from .src.zukan_icon_theme.core.change_icon import ResetIconCommand  # noqa F401
from .src.zukan_icon_theme.core.create_custom_icon import CreateCustomIconCommand  # noqa F401
from .src.zukan_icon_theme.core.create_custom_icon import DeleteCustomIconCommand  # noqa F401
from .src.zukan_icon_theme.core.disable_icon import DisableIconCommand  # noqa F401
from .src.zukan_icon_theme.core.disable_icon import EnableIconCommand  # noqa F401
from .src.zukan_icon_theme.core.disable_theme import DisableThemeCommand  # noqa F401
from .src.zukan_icon_theme.core.disable_theme import EnableThemeCommand  # noqa F401
from .src.zukan_icon_theme.core.install import InstallEvent
from .src.zukan_icon_theme.core.preferences import DeletePreferenceCommand  # noqa F401
from .src.zukan_icon_theme.core.preferences import InstallPreferenceCommand  # noqa F401
from .src.zukan_icon_theme.core.rebuild_files import RebuildFilesCommand  # noqa F401
from .src.zukan_icon_theme.core.select_prefer_icon import RemovePreferIconCommand  # noqa F401
from .src.zukan_icon_theme.core.select_prefer_icon import SelectPreferIconCommand  # noqa F401
from .src.zukan_icon_theme.core.syntaxes import DeleteSyntaxCommand  # noqa F401
from .src.zukan_icon_theme.core.syntaxes import InstallSyntaxCommand  # noqa F401
from .src.zukan_icon_theme.core.themes import DeleteThemeCommand  # noqa F401
from .src.zukan_icon_theme.core.themes import InstallThemeCommand  # noqa F401
from .src.zukan_icon_theme.core.zukan_pref_settings import EventBus
from .src.zukan_icon_theme.core.zukan_pref_settings import SettingsEvent
from .src.zukan_icon_theme.core.zukan_pref_settings import UpgradePlugin
from .src.zukan_icon_theme.core.zukan_pref_settings import ZukanIconFiles
from .src.zukan_icon_theme.helpers.cache_theme_info import delete_cached_theme_info
from .src.zukan_icon_theme.helpers.clean_comments import CleanCommentsCommand  # noqa F401
from .src.zukan_icon_theme.helpers.search_themes import get_sidebar_bgcolor
from .src.zukan_icon_theme.helpers.load_save_settings import get_theme_name
from .src.zukan_icon_theme.helpers.load_save_settings import is_zukan_listener_enabled
from .src.zukan_icon_theme.helpers.logger import logging
from .src.zukan_icon_theme.helpers.move_folders import MoveFolder
from .src.zukan_icon_theme.helpers.zukan_reporter import ZukanReporterCommand  # noqa F401
from .src.zukan_icon_theme.utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)
# fmt: on

# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules

logger = logging.getLogger(__name__)

zukan_listener_enabled = is_zukan_listener_enabled()

if zukan_listener_enabled:
    from .src.zukan_icon_theme.core.listeners import SchemeThemeListener  # noqa: F401

# Extract and move folder if installed using Package Control.
if not os.path.exists(ZUKAN_ICONS_DATA_FILE):
    MoveFolder().move_folders()


def plugin_loaded():
    # IndexError when testing in ST4 Python 3.3, using sublime-package file.
    # get_sidebar_bgcolor use sublime find_resources
    theme_name = get_theme_name()
    sublime.set_timeout(lambda: get_sidebar_bgcolor(theme_name))

    # `cache_theme_info` setting. Cache default is false.
    delete_cached_theme_info()

    if zukan_listener_enabled:
        # New install or when preferences or syntaxes folders do not exist.
        if not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH) or not os.path.exists(
            ZUKAN_PKG_ICONS_SYNTAXES_PATH
        ):
            InstallEvent().new_install()

        event_bus = EventBus()

        # Package auto upgraded setting.
        upgrade_zukan = UpgradePlugin(event_bus)
        upgrade_zukan.start_upgrade()

        # Check if zukan preferences changed.
        SettingsEvent.zukan_preferences_changed()

        # Print to console current Zukan settings if `log_level` DEBUG
        SettingsEvent.output_to_console_zukan_pref_settings()

        # Build icons files if changed in Zukan settings
        zukan_icon_files = ZukanIconFiles(event_bus)
        zukan_icon_files.rebuild_icons_files(event_bus)


def plugin_unloaded():
    MoveFolder().remove_created_folder(ZUKAN_PKG_PATH)

    if zukan_listener_enabled:
        # Clear `add_on_change`
        SettingsEvent.zukan_preferences_clear()
