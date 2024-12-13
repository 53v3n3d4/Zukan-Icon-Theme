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


from .src.zukan_icon_theme.commands.commands import (  # noqa: E402
    DeletePreferenceCommand,  # noqa: F401
    DeleteSyntaxCommand,  # noqa: F401
    DeleteThemeCommand,  # noqa: F401
    InstallPreferenceCommand,  # noqa: F401
    InstallSyntaxCommand,  # noqa: F401
    InstallThemeCommand,  # noqa: F401
    RebuildFilesCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.commands_settings import (  # noqa: E402
    ChangeFileExtensionCommand,  # noqa: F401
    ChangeIconCommand,  # noqa: F401
    CleanCommentsCommand,  # noqa: F401
    CreateCustomIconCommand,  # noqa: F401
    DeleteCustomIconCommand,  # noqa: F401
    DisableIconCommand,  # noqa: F401
    DisableThemeCommand,  # noqa: F401
    EnableIconCommand,  # noqa: F401
    EnableThemeCommand,  # noqa: F401
    RemovePreferIconCommand,  # noqa: F401
    ResetFileExtensionCommand,  # noqa: F401
    ResetIconCommand,  # noqa: F401
    SelectPreferIconCommand,  # noqa: F401
)
from .src.zukan_icon_theme.events.install import InstallEvent  # noqa: E402
from .src.zukan_icon_theme.events.listeners import (  # noqa: E402
    SchemeThemeListener,  # noqa: F401
)
from .src.zukan_icon_theme.events.settings import SettingsEvent  # noqa: E402
from .src.zukan_icon_theme.helpers.logger import logging  # noqa: E402
from .src.zukan_icon_theme.lib.move_folders import MoveFolder  # noqa: E402
from .src.zukan_icon_theme.utils.zukan_paths import (  # noqa: E402
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)

# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules

logger = logging.getLogger(__name__)


def plugin_loaded():
    # New install from repo clone, or when preferences or syntaxes folders do
    # not exist.
    if os.path.exists(ZUKAN_PKG_ICONS_PATH) and (
        not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        or not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
    ):
        InstallEvent.new_install_manually()

    # New install from Package Control, a sublime-package file.
    if (
        not os.path.exists(ZUKAN_PKG_ICONS_PATH)
        and not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        and not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
    ):
        InstallEvent.new_install_pkg_control()

    # Package auto upgraded setting.
    SettingsEvent.upgrade_zukan_files()

    # Check if zukan preferences changed.
    SettingsEvent.zukan_preferences_changed()

    # Print to console current Zukan settings if 'log_level' DEBUG
    SettingsEvent.get_user_zukan_preferences()

    # Build icons files if changed in Zukan settings
    SettingsEvent.rebuild_icons_files()


def plugin_unloaded():
    MoveFolder.remove_created_folder(ZUKAN_PKG_PATH)

    # Clear 'add_on_change'
    SettingsEvent.zukan_preferences_clear()
