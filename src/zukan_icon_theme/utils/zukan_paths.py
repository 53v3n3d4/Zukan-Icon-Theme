import os
# import sublime

from .file_extensions import (
    PICKLE_EXTENSION,
    SUBLIME_PACKAGE_EXTENSION,
    SUBLIME_SETTINGS_EXTENSION,
)


def filepath(url: str) -> str:
    """
    Get the relative path to script directory.
    Paths are relative to the working directory.
    Script diretory is
        .../Sublime Text/Packages/Zukan Icon Theme/src/build/utils
    If installed trough packagecontrol.io, instead of Packages, folder is
    Installed Packages.

    Parameters:
    url (str) -- destination path.

    Returns:
    fp (str) -- script directory + url path.
    """
    if isinstance(url, str):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        # print(os.path.relpath(fp, start='../../../'))
        return fp
    else:
        raise ValueError('Url need to be string.')


# Zukan-Icon-Theme.src.zukan_icon_theme.utils
PACKAGE_NAME = __package__.split('.', 1)[0]

PKG_ZUKAN_ICON_THEME_FOLDER = os.path.join('Packages', PACKAGE_NAME)

# Zukan dir paths

PACKAGES_PATH = filepath('../../../../../Packages')
INSTALLED_PACKAGES_PATH = filepath('../../../../../Installed Packages')

# ZUKAN_PKG_ICONS_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'icons')
ZUKAN_PKG_ICONS_PATH = os.path.join(PACKAGES_PATH, PACKAGE_NAME, 'icons')

# ZUKAN_PKG_ICONS_DATA_PATH = os.path.join(
#     sublime.packages_path(), PACKAGE_NAME, 'icons_data'
# )
ZUKAN_PKG_ICONS_DATA_PATH = os.path.join(PACKAGES_PATH, PACKAGE_NAME, 'icons_data')

# ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH = os.path.join(
#     sublime.packages_path(), PACKAGE_NAME, 'icons_data', 'primary_icons'
# )
ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH = os.path.join(
    PACKAGES_PATH, PACKAGE_NAME, 'icons_data', 'primary_icons'
)

# ZUKAN_PKG_ICONS_PREFERENCES_PATH = os.path.join(
#     sublime.packages_path(), PACKAGE_NAME, 'icons_preferences'
# )
ZUKAN_PKG_ICONS_PREFERENCES_PATH = os.path.join(
    PACKAGES_PATH, PACKAGE_NAME, 'icons_preferences'
)

# ZUKAN_PKG_ICONS_SYNTAXES_PATH = os.path.join(
#     sublime.packages_path(), PACKAGE_NAME, 'icons_syntaxes'
# )
ZUKAN_PKG_ICONS_SYNTAXES_PATH = os.path.join(
    PACKAGES_PATH, PACKAGE_NAME, 'icons_syntaxes'
)

# ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME)
ZUKAN_PKG_PATH = os.path.join(PACKAGES_PATH, PACKAGE_NAME)

# ZUKAN_PKG_SRC_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'src')
ZUKAN_PKG_SRC_PATH = os.path.join(PACKAGES_PATH, PACKAGE_NAME, 'src')

# ZUKAN_PKG_SUBLIME_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'sublime')
ZUKAN_PKG_SUBLIME_PATH = os.path.join(PACKAGES_PATH, PACKAGE_NAME, 'sublime')

# Zukan file paths

# ZUKAN_INSTALLED_PKG_PATH = os.path.join(
#     sublime.installed_packages_path(), PACKAGE_NAME + SUBLIME_PACKAGE_EXTENSION
# )
ZUKAN_INSTALLED_PKG_PATH = os.path.join(
    INSTALLED_PACKAGES_PATH, PACKAGE_NAME + SUBLIME_PACKAGE_EXTENSION
)

# ZUKAN_ICONS_DATA_FILE = os.path.join(
#     sublime.packages_path(),
#     PACKAGE_NAME,
#     'icons_data',
#     'zukan_icons_data' + PICKLE_EXTENSION,
# )
ZUKAN_ICONS_DATA_FILE = os.path.join(
    PACKAGES_PATH,
    PACKAGE_NAME,
    'icons_data',
    'zukan_icons_data' + PICKLE_EXTENSION,
)

# ZUKAN_USER_SUBLIME_SETTINGS = os.path.join(
#     sublime.packages_path(),
#     'User',
#     'Zukan Icon Theme' + SUBLIME_SETTINGS_EXTENSION,
# )
ZUKAN_USER_SUBLIME_SETTINGS = os.path.join(
    PACKAGES_PATH,
    'User',
    'Zukan Icon Theme' + SUBLIME_SETTINGS_EXTENSION,
)

# ZUKAN_VERSION_FILE = os.path.join(
#     sublime.packages_path(), PACKAGE_NAME, 'sublime', 'zukan-version.sublime-settings'
# )
ZUKAN_VERSION_FILE = os.path.join(
    PACKAGES_PATH, PACKAGE_NAME, 'sublime', 'zukan-version' + SUBLIME_SETTINGS_EXTENSION
)
