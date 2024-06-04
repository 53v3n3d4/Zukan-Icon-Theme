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

# from .src.zukan_icon_theme.commands.listeners import (  # noqa: E402
#     ThemeSettingListener,  # noqa: F401
# )
from .src.zukan_icon_theme.helpers.logger import logging  # noqa: E402
from .src.zukan_icon_theme.lib.icons_preferences import ZukanPreference  # noqa: E402
from .src.zukan_icon_theme.lib.icons_syntaxes import ZukanSyntax  # noqa: E402
from .src.zukan_icon_theme.lib.icons_themes import ThemeFile  # noqa: E402
from .src.zukan_icon_theme.lib.move_folders import MoveFolder  # noqa: E402
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
    """
    Try move folders if installed trough Package Control. Then install
    sublime-theme and sublime-syntax files.
    """
    try:
        if not os.path.exists(ZUKAN_PKG_ICONS_PATH) and not os.path.exists(
            ZUKAN_PKG_ICONS_SYNTAXES_PATH
        ):
            MoveFolder.move_folders()
    finally:
        if not any(
            syntax.endswith('.sublime-syntax')
            for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        ):
            ZukanSyntax.create_icons_syntaxes()
            # Edit icons syntaxes contexts main if syntax not installed or ST3
            ZukanSyntax.edit_contexts_scopes()
        if not any(
            theme.endswith('.sublime-theme')
            for theme in os.listdir(ZUKAN_PKG_ICONS_PATH)
        ):
            ThemeFile.create_themes_files()
        if not any(
            preferences.endswith('.tmPreferences')
            for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        ):
            ZukanPreference.create_icons_preferences()
            # Remove plist tag <!DOCTYPE plist>
            ZukanPreference.delete_plist_tags()


def plugin_unloaded():
    MoveFolder.remove_created_folder(ZUKAN_PKG_PATH)
