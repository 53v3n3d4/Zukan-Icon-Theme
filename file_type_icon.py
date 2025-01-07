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


from .src.zukan_icon_theme.commands.change_file_extension import (  # noqa: E402
    ChangeFileExtensionCommand,  # noqa: F401
    ResetFileExtensionCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.change_icon import (  # noqa: E402
    ChangeIconCommand,  # noqa: F401
    ResetIconCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.clean_comments import (  # noqa: E402
    CleanCommentsCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.commands_settings import (  # noqa: E402
    CreateCustomIconCommand,  # noqa: F401
    DeleteCustomIconCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.disable_icon import (  # noqa: E402
    DisableIconCommand,  # noqa: F401
    EnableIconCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.disable_theme import (  # noqa: E402
    DisableThemeCommand,  # noqa: F401
    EnableThemeCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.preferences import (  # noqa: E402
    DeletePreferenceCommand,  # noqa: F401
    InstallPreferenceCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.rebuild_files import (  # noqa: E402
    RebuildFilesCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.select_prefer_icon import (  # noqa: E402
    RemovePreferIconCommand,  # noqa: F401
    SelectPreferIconCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.syntaxes import (  # noqa: E402
    DeleteSyntaxCommand,  # noqa: F401
    InstallSyntaxCommand,  # noqa: F401
)
from .src.zukan_icon_theme.commands.themes import (  # noqa: E402
    DeleteThemeCommand,  # noqa: F401
    InstallThemeCommand,  # noqa: F401
)
from .src.zukan_icon_theme.events.install import InstallEventE2  # noqa: E402
from .src.zukan_icon_theme.events.settings import SettingsEventE2  # noqa: E402
from .src.zukan_icon_theme.helpers.load_save_settings import is_zukan_listener_enabled  # noqa: E402
from .src.zukan_icon_theme.helpers.logger import logging  # noqa: E402
from .src.zukan_icon_theme.lib.move_folders import MoveFolderF2  # noqa: E402
from .src.zukan_icon_theme.utils.zukan_paths import (  # noqa: E402
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)

# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules

logger = logging.getLogger(__name__)

zukan_listener_enabled = is_zukan_listener_enabled()

if zukan_listener_enabled:
    from .src.zukan_icon_theme.events.listeners import (  # noqa: E402
        SchemeThemeListener,  # noqa: F401
    )


def plugin_loaded():
    if zukan_listener_enabled:
        install_event = InstallEventE2()

        # New install from repo clone, or when preferences or syntaxes folders do
        # not exist.
        if os.path.exists(ZUKAN_PKG_ICONS_PATH) and (
            not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            or not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        ):
            install_event.new_install_manually()

        # New install from Package Control, a sublime-package file.
        if (
            not os.path.exists(ZUKAN_PKG_ICONS_PATH)
            and not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            and not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        ):
            install_event.new_install_pkg_control()

        settings_event = SettingsEventE2()
        # Package auto upgraded setting.
        settings_event.upgrade_zukan_files()

        # Check if zukan preferences changed.
        settings_event.zukan_preferences_changed()

        # Print to console current Zukan settings if 'log_level' DEBUG
        settings_event.get_user_zukan_preferences()

        # Build icons files if changed in Zukan settings
        settings_event.rebuild_icons_files()


def plugin_unloaded():
    MoveFolderF2().remove_created_folder(ZUKAN_PKG_PATH)

    if zukan_listener_enabled:
        # Clear 'add_on_change'
        SettingsEventE2().zukan_preferences_clear()
