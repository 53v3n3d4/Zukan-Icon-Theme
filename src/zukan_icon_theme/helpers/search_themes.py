import glob
import os
import re
import sublime

from ..utils.zukan_dir_paths import (
    INSTALLED_PACKAGES_PATH,
    PACKAGES_PATH,
    TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH,
)
from zipfile import ZipFile


def filter_resources_themes(themes_list: list) -> list:
    """
    Filter sublime-themes on root. Use sublime package.

    Paramenters:
    themes_list (list) -- list of sublime-themes.

    Returns:
    filter_list (list) -- list of themes names except themes in packages
    sub dir. Example: Zukan Icon Theme/icons/Treble Adaptive.sublime-theme
    is excluded.
    """
    filter_list = []
    # Regex for 2 subdir, when use sublime find_resources.
    expression = re.compile(r'^([^\/]+/[^\/]+/)(?!.*/)(.*sublime-theme)', re.I)
    for name in themes_list:
        # print(name)
        if re.match(expression, name):
            file_path, file_name = name.rsplit('/', 1)
            # print(file_name)
            filter_list.append(file_name)
    return filter_list


# print(filter_resources_themes(resources_list))


def search_resources_sublime_themes() -> list:
    """
    Search for sublime-themes then filter results. Use sublime package.

    Retunrs:
    (list) -- Filtered list of sublime-themes.
    """
    themes_list = sublime.find_resources('*.sublime-theme')
    return filter_resources_themes(themes_list)


def filter_themes(themes_list: list) -> list:
    """
    Filter sublime-themes on root. Not use sublime api.

    Paramenters:
    themes_list (list) -- filter to exclude sublime-themes files if located in
    sub folders.

    Returns:
    (list) -- list of themes in Installed Packages/*.sublime-package.
    """
    filter_list = []
    # Regex to filter only sublime-theme on root level, using in
    # search_installed_pkgs_themes.
    expression = re.compile(r'^(?!.*/)(.*sublime-theme)', re.I)
    for name in themes_list:
        # print(name)
        if re.match(expression, name):
            filter_list.append(name)
    return filter_list


def search_installed_pkgs_themes() -> list:
    """
    Search for sublime-theme files in ST Installed Packages.

    It limit search to root directory.

    Returns:
    (list) -- list of themes in Installed Packages/*.sublime-package, only on
    package root.
    """
    list_themes_installed_pkgs_folder = []
    for files in glob.glob(INSTALLED_PACKAGES_PATH + '/*.sublime-package'):
        with ZipFile(files, 'r') as zf:
            for info in zf.infolist():
                if info.filename.endswith('.sublime-theme'):
                    # print(info.filename)
                    list_themes_installed_pkgs_folder.append(info.filename)
    return filter_themes(list_themes_installed_pkgs_folder)
    # return list_themes_installed_pkgs_folder


# print(search_installed_pkgs_themes())


def search_pkgs_themes() -> list:
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


# # print(search_pkgs_themes())
