import glob
import os

from src.zukan_icon_theme.utils.zukan_dir_paths import (
    INSTALLED_PACKAGES_PATH,
    PACKAGES_PATH,
    TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH,
)
from zipfile import ZipFile


# print(sublime.find_resources('*.sublime-theme'))

# Failing to find Default ST themes.


def search_installed_pkgs_themes():
    """
    Search for sublime-theme files in ST Installed Packages.

    It limit search to root directory.

    Returns:
    (list) -- list of themes in Installed Packages/*.sublime-package.
    """
    list_themes_installed_pkgs_folder = []
    # for files in glob.glob(sublime.installed_packages_path() + '/*.sublime-package'):
    for files in glob.glob(INSTALLED_PACKAGES_PATH + '/*.sublime-package'):
        with ZipFile(files, 'r') as zip:
            for info in zip.infolist():
                if info.filename.endswith('.sublime-theme'):
                    # print(info.filename)
                    list_themes_installed_pkgs_folder.append(info.filename)
    return list_themes_installed_pkgs_folder


# print(search_installed_pkgs_themes())


def search_pkgs_themes():
    """
    Search for sublime-theme files in ST Packages sub directories. Example:
    Packages/*/*.sublime-theme

    It limit search to one sub directory deep.

    Returns:
    (list) -- list of themes in Packages/*/*.sublime-theme.
    """
    list_themes_pkgs_folder = []
    # for files in glob.glob(sublime.packages_path() + '/*/*.sublime-theme'):
    for file in glob.glob(PACKAGES_PATH + '/*/*.sublime-theme'):
        list_themes_pkgs_folder.append(os.path.basename(file))
    return list_themes_pkgs_folder


# print(search_pkgs_themes())
