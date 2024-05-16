# import glob
# import os
import re
import sublime

# from ..utils.zukan_dir_paths import (
#     INSTALLED_PACKAGES_PATH,
#     PACKAGES_PATH,
#     TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH,
# )
# from zipfile import ZipFile


def filter_resources_themes(themes_list: list) -> list:
    """
    Filter sublime-themes on root. Use sublime package.

    Example: Zukan Icon Theme/icons/Treble Adaptive.sublime-theme
    is excluded.

    Paramenters:
    themes_list (list) -- list of sublime-themes.

    Returns:
    filter_list (list) -- list of themes names except themes in packages
    sub dir.
    """
    filter_list = []
    # Regex for 2 subdir, when use sublime find_resources.
    expression = re.compile(r'^([^\/]+/[^\/]+/)(?!.*/)(.*sublime-theme)', re.I)
    for name in themes_list:
        # print(name)
        if re.match(expression, name):
            filter_list.append(name)
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


def find_attributes(
    theme: str, theme_content: dict, list_theme_has_attributes: list
) -> list:
    """
    Search in sublime-theme files if they use icon_file_type. And, if
    icon_file_type has attributes 'hover' and 'selected'.

    Example:
    {
        "class": "icon_file_type",
        "parents": [{"class": "tree_row", "attributes": ["selected"]}],
        "layer0.opacity": 1.0
    }

    Paramenters:
    theme (str) -- path theme name.
    theme_content (dict) -- parsed json file, sublime-theme.
    list_theme_has_attributes (list) -- list of path theme that has attributes.
    """
    if 'rules' in theme_content:
        icon_file_type_list = [
            k for k in theme_content['rules'] if k['class'] == 'icon_file_type'
        ]
    elif 'rules' not in theme_content:
        icon_file_type_list = [
            k for k in theme_content if k['class'] == 'icon_file_type'
        ]
        # print('no rules' + theme)
    for i in icon_file_type_list:
        if i.get('parents') is not None:
            for p in i.get('parents'):
                if p['class'] == 'tree_row' and all(
                    a in p['attributes'] for a in ['hover', 'selected']
                ):
                    # print(theme)
                    list_theme_has_attributes.append(theme)


def find_attributes_hidden_file(
    theme: str, theme_content: dict, list_theme_has_attributes: list
) -> list:
    """
    Recursively search for attributes, in hidden-theme files.

    Paramenters:
    theme (str) -- path theme name.
    theme_content (dict) -- parsed json file, hidden-theme.
    list_theme_has_attributes (list) -- list of path theme that has attributes.
    """
    if 'extends' in theme_content:
        hidden_theme_name = sublime.find_resources(theme_content['extends'])
        for t in hidden_theme_name:
            hidden_theme_content = sublime.decode_value(sublime.load_resource(t))
            # print(t)
            if (
                'rules' in hidden_theme_content
                and 'extends' not in hidden_theme_content
            ):
                find_attributes(theme, hidden_theme_content, list_theme_has_attributes)
            else:
                find_attributes_hidden_file(
                    theme, hidden_theme_content, list_theme_has_attributes
                )


def list_theme_with_opacity() -> list:
    """
    Create a themes list that use icon_file_type, with attributes 'hover' and
    'selected'.

    Example:
    {
        "class": "icon_file_type",
        "parents": [{"class": "tree_row", "attributes": ["hover"]}],
        "layer0.opacity": 1.0
    }

    Returns:
    list_theme_has_attributes (list) -- list of installed theme with attributes hover
    and selected.
    """
    all_themes = search_resources_sublime_themes()
    list_theme_has_attributes = []
    for theme in all_themes:
        theme_content = sublime.decode_value(sublime.load_resource(theme))
        # print(theme_content)
        # print(theme)
        if 'extends' not in theme_content:
            find_attributes(theme, theme_content, list_theme_has_attributes)
        elif 'extends' in theme_content:
            find_attributes_hidden_file(theme, theme_content, list_theme_has_attributes)
    # print(list_theme_has_attributes)
    return list_theme_has_attributes


# def filter_themes(themes_list: list) -> list:
#     """
#     Filter sublime-themes on root. Not use sublime api.

#     Paramenters:
#     themes_list (list) -- filter to exclude sublime-themes files if located in
#     sub folders.

#     Returns:
#     (list) -- list of themes in Installed Packages/*.sublime-package.
#     """
#     filter_list = []
#     # Regex to filter only sublime-theme on root level, using in
#     # search_installed_pkgs_themes.
#     expression = re.compile(r'^(?!.*/)(.*sublime-theme)', re.I)
#     for name in themes_list:
#         # print(name)
#         if re.match(expression, name):
#             filter_list.append(name)
#     return filter_list


# def search_installed_pkgs_themes() -> list:
#     """
#     Search for sublime-theme files in ST Installed Packages.

#     It limit search to root directory.

#     Returns:
#     (list) -- list of themes in Installed Packages/*.sublime-package, only on
#     package root.
#     """
#     list_themes_installed_pkgs_folder = []
#     for files in glob.glob(INSTALLED_PACKAGES_PATH + '/*.sublime-package'):
#         with ZipFile(files, 'r') as zf:
#             for info in zf.infolist():
#                 if info.filename.endswith('.sublime-theme'):
#                     # print(info.filename)
#                     list_themes_installed_pkgs_folder.append(info.filename)
#     return filter_themes(list_themes_installed_pkgs_folder)
#     # return list_themes_installed_pkgs_folder


# print(search_installed_pkgs_themes())


# def search_pkgs_themes() -> list:
#     """
#     Search for sublime-theme files in ST Packages sub directories. Example:
#     Packages/*/*.sublime-theme

#     It limit search to one sub directory deep.

#     Returns:
#     (list) -- list of themes in Packages/*/*.sublime-theme.
#     """
#     list_themes_pkgs_folder = []
#     # for files in glob.glob(sublime.packages_path() + '/*/*.sublime-theme'):
#     for file in glob.glob(PACKAGES_PATH + '/*/*.sublime-theme'):
#         list_themes_pkgs_folder.append(os.path.basename(file))
#     return list_themes_pkgs_folder


# # print(search_pkgs_themes())
