import os
import sublime

from .file_extensions import PICKLE_EXTENSION, SUBLIME_PACKAGE_EXTENSION


def filepath(url: str) -> str:
    """
    Get the relative path to script directory.
    Paths are relative to the working directory.
    Script diretory is
        .../Sublime Text/Packages/Zukan-Icon-Theme/src/zukan_icon_theme/utils
    If installed trough packagecontrol.io, instead of Packages, folder is
    Installed Packages.

    Parameters:
    url (str) -- destination path.

    Returns:
    fp (str) -- script directory + url path.
    """
    if isinstance(url, str):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        return fp
    else:
        raise ValueError('Url need to be string.')


# Zukan-Icon-Theme.src.zukan_icon_theme.utils
PACKAGE_NAME = __package__.split('.', 1)[0]

PKG_ZUKAN_ICON_THEME_FOLDER = os.path.join('Packages', PACKAGE_NAME)

# ZUKAN_INSTALLED_PKG_PATH = filepath(
#     '../../../../../Installed Packages/Zukan Icon Theme.sublime-package'
# )
ZUKAN_INSTALLED_PKG_PATH = os.path.join(
    sublime.installed_packages_path(), PACKAGE_NAME + SUBLIME_PACKAGE_EXTENSION
)

# ZUKAN_PKG_ICONS_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme/icons')
ZUKAN_PKG_ICONS_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'icons')

ZUKAN_PKG_ICONS_PREFERENCES_PATH = os.path.join(
    sublime.packages_path(), PACKAGE_NAME, 'icons_preferences'
)

# ZUKAN_PKG_ICONS_SYNTAXES_PATH = filepath(
#     '../../../../../Packages/Zukan-Icon-Theme/icons_syntaxes'
# )
ZUKAN_PKG_ICONS_SYNTAXES_PATH = os.path.join(
    sublime.packages_path(), PACKAGE_NAME, 'icons_syntaxes'
)

ZUKAN_PKG_SRC_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'src')

# ZUKAN_PKG_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme')
ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME)

ZUKAN_PREFERENCES_DATA_FILE = os.path.join(
    sublime.packages_path(),
    PACKAGE_NAME,
    'icons_preferences',
    'zukan_preferences_data' + PICKLE_EXTENSION,
)

# ZUKAN_SYNTAXES_DATA_FILE = filepath('../../../icons_syntaxes/zukan_syntaxes_data.pkl')
ZUKAN_SYNTAXES_DATA_FILE = os.path.join(
    sublime.packages_path(),
    PACKAGE_NAME,
    'icons_syntaxes',
    'zukan_syntaxes_data' + PICKLE_EXTENSION,
)

# Testing only

# TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH = filepath('../../../not/icons')
