import os
import sublime

from .file_extensions import PICKLE_EXTENSION, SUBLIME_PACKAGE_EXTENSION


# Zukan-Icon-Theme.src.zukan_icon_theme.utils
PACKAGE_NAME = __package__.split('.', 1)[0]

PKG_ZUKAN_ICON_THEME_FOLDER = os.path.join('Packages', PACKAGE_NAME)

# Zukan dir paths

ZUKAN_PKG_ICONS_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'icons')

ZUKAN_PKG_ICONS_PREFERENCES_PATH = os.path.join(
    sublime.packages_path(), PACKAGE_NAME, 'icons_preferences'
)

ZUKAN_PKG_ICONS_SYNTAXES_PATH = os.path.join(
    sublime.packages_path(), PACKAGE_NAME, 'icons_syntaxes'
)

ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME)

ZUKAN_PKG_SRC_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'src')

ZUKAN_PKG_SUBLIME_PATH = os.path.join(sublime.packages_path(), PACKAGE_NAME, 'sublime')

# Zukan file paths

ZUKAN_INSTALLED_PKG_PATH = os.path.join(
    sublime.installed_packages_path(), PACKAGE_NAME + SUBLIME_PACKAGE_EXTENSION
)

ZUKAN_PREFERENCES_DATA_FILE = os.path.join(
    sublime.packages_path(),
    PACKAGE_NAME,
    'icons_preferences',
    'zukan_preferences_data' + PICKLE_EXTENSION,
)

ZUKAN_SYNTAXES_DATA_FILE = os.path.join(
    sublime.packages_path(),
    PACKAGE_NAME,
    'icons_syntaxes',
    'zukan_syntaxes_data' + PICKLE_EXTENSION,
)

ZUKAN_VERSION_FILE = os.path.join(
    sublime.packages_path(), PACKAGE_NAME, 'sublime', 'zukan-version.sublime-settings'
)
