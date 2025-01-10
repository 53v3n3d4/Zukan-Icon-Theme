import os
import sys

# Copied from A File Icon
# https://github.com/SublimeText/AFileIcon/blob/master/plugin.py
# Clear module cache to force reloading all modules of this package.
prefix = __package__ + '.'  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
del prefix

# fmt: off
from .src.zukan_icon_theme.core.change_file_extension import ChangeFileExtensionCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.change_file_extension import ResetFileExtensionCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.change_icon import ChangeIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.change_icon import ResetIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.create_custom_icon import CreateCustomIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.create_custom_icon import DeleteCustomIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.disable_icon import DisableIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.disable_icon import EnableIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.disable_theme import DisableThemeCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.disable_theme import EnableThemeCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.install import InstallEvent  # noqa: E402
from .src.zukan_icon_theme.core.preferences import DeletePreferenceCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.preferences import InstallPreferenceCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.rebuild_files import RebuildFilesCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.select_prefer_icon import RemovePreferIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.select_prefer_icon import SelectPreferIconCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.syntaxes import DeleteSyntaxCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.syntaxes import InstallSyntaxCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.themes import DeleteThemeCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.themes import InstallThemeCommand  # noqa: E402 F401
from .src.zukan_icon_theme.core.zukan_pref_settings import SettingsEvent  # noqa: E402
from .src.zukan_icon_theme.core.zukan_pref_settings import ZukanIconFiles  # noqa: E402
from .src.zukan_icon_theme.helpers.clean_comments import CleanCommentsCommand  # noqa: E402 F401
from .src.zukan_icon_theme.helpers.load_save_settings import is_zukan_listener_enabled  # noqa: E402
from .src.zukan_icon_theme.helpers.logger import logging  # noqa: E402
from .src.zukan_icon_theme.helpers.move_folders import MoveFolder  # noqa: E402
from .src.zukan_icon_theme.helpers.zukan_reporter import ZukanReporterCommand  # noqa: E402 F401
from .src.zukan_icon_theme.utils.zukan_paths import (  # noqa: E402
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

# Extract and move folder if installed using Package Controal.
if not os.path.exists(ZUKAN_ICONS_DATA_FILE):
    MoveFolder().move_folders()


def plugin_loaded():
    if zukan_listener_enabled:
        # New install or when preferences or syntaxes folders do not exist.
        if not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH) or not os.path.exists(
            ZUKAN_PKG_ICONS_SYNTAXES_PATH
        ):
            InstallEvent().new_install()

        zukan_icon_files = ZukanIconFiles()

        # Package auto upgraded setting.
        zukan_icon_files.upgrade_zukan_files()

        # Check if zukan preferences changed.
        SettingsEvent.zukan_preferences_changed()

        # Print to console current Zukan settings if 'log_level' DEBUG
        SettingsEvent.output_to_console_zukan_pref_settings()

        # Build icons files if changed in Zukan settings
        zukan_icon_files.rebuild_icons_files()


def plugin_unloaded():
    MoveFolder().remove_created_folder(ZUKAN_PKG_PATH)

    if zukan_listener_enabled:
        # Clear 'add_on_change'
        SettingsEvent.zukan_preferences_clear()
