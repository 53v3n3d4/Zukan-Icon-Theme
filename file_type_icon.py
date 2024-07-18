import os
import sys

# From A File Icon https://github.com/SublimeText/AFileIcon/blob/master/plugin.py
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
    DeletePreference,  # noqa: F401
    DeleteSyntax,  # noqa: F401
    DeleteTheme,  # noqa: F401
    InstallPreference,  # noqa: F401
    InstallSyntax,  # noqa: F401
    InstallTheme,  # noqa: F401
    RebuildFiles,  # noqa: F401
)
from .src.zukan_icon_theme.commands.commands_settings import (  # noqa: E402
    ChangeFileExtension,  # noqa: F401
    ChangeIcon,  # noqa: F401
    CleanComments,  # noqa: F401
    DisableIcon,  # noqa: F401
    DisableTheme,  # noqa: F401
    EnableIcon,  # noqa: F401
    EnableTheme,  # noqa: F401
    ResetFileExtension,  # noqa: F401
    ResetIcon,  # noqa: F401
)
from .src.zukan_icon_theme.events.install import InstallEvent  # noqa: E402
from .src.zukan_icon_theme.events.settings import SettingsEvent  # noqa: E402
from .src.zukan_icon_theme.helpers.logger import logging  # noqa: E402
from .src.zukan_icon_theme.lib.move_folders import MoveFolder  # noqa: E402
from .src.zukan_icon_theme.utils.file_extensions import (  # noqa: E402
    SUBLIME_SYNTAX_EXTENSION,
    SUBLIME_THEME_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
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
    # Check user theme, if has or not icon theme created. Then delete or create
    # files if needed.
    if (
        os.path.exists(ZUKAN_PKG_ICONS_PATH)
        and os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        and os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        and (
            any(
                preference.endswith(TMPREFERENCES_EXTENSION)
                for preference in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            )
            or any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            )
            or any(
                theme.endswith(SUBLIME_THEME_EXTENSION)
                for theme in os.listdir(ZUKAN_PKG_ICONS_PATH)
            )
        )
    ):
        SettingsEvent.get_user_theme()

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

    # Check if user preferences changed.
    SettingsEvent.user_preferences_changed()

    # Check if zukan preferences changed.
    SettingsEvent.zukan_preferences_changed()

    # Print to console current Zukan settings if 'log_level' DEBUG
    SettingsEvent.get_user_zukan_preferences()


def plugin_unloaded():
    MoveFolder.remove_created_folder(ZUKAN_PKG_PATH)

    # Clear 'add_on_change'
    SettingsEvent.user_preferences_clear()
    SettingsEvent.zukan_preferences_clear()
