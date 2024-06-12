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
    DeletePreferences,  # noqa: F401
    DeleteSyntax,  # noqa: F401
    DeleteSyntaxes,  # noqa: F401
    DeleteTheme,  # noqa: F401
    DeleteThemes,  # noqa: F401
    InstallPreference,  # noqa: F401
    InstallSyntax,  # noqa: F401
    InstallTheme,  # noqa: F401
    InstallThemes,  # noqa: F401
    RebuildFiles,  # noqa: F401
    RebuildPreferences,  # noqa: F401
    RebuildSyntaxes,  # noqa: F401
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
from .src.zukan_icon_theme.utils.zukan_dir_paths import (  # noqa: E402
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)

# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules

logger = logging.getLogger(__name__)


def plugin_loaded():
    # New install from Package Control.
    # If installed using sublime-package, rebuild generate error the same as
    # on load. Even after restart and  all icons working fine.
    # Installing via clone, this does not happen. Only diff is move_folders,
    # they use same func.
    # If change for other themes, the icons are showing with no issues.
    if not os.path.exists(ZUKAN_PKG_ICONS_PATH) and not os.path.exists(
        ZUKAN_PKG_ICONS_SYNTAXES_PATH
    ):
        InstallEvent.new_install_pkg_control()

    # New install from repo clone. No icon themes, preferences or syntaxes.
    if (
        not any(
            preference.endswith(TMPREFERENCES_EXTENSION)
            for preference in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        )
        and not any(
            syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
            for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        )
        and not any(
            theme.endswith(SUBLIME_THEME_EXTENSION)
            for theme in os.listdir(ZUKAN_PKG_ICONS_PATH)
        )
    ):
        InstallEvent.new_install_manually()

    # Check user theme, if has or not icon theme created. Then delete or create
    # files if needed.
    SettingsEvent.get_user_theme()

    # Check if user theme changed.
    SettingsEvent.user_preferences_changed()

    # Check if package is upgraded.
    SettingsEvent.zukan_preferences_changed()


def plugin_unloaded():
    MoveFolder.remove_created_folder(ZUKAN_PKG_PATH)
