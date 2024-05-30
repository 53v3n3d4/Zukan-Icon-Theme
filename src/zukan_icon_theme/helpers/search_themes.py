import logging
import re
import sublime

from ..utils.zukan_dir_paths import (
    ZUKAN_EXCLUDE_HIDDEN_THEME_PATH,
)

logger = logging.getLogger(__name__)


def filter_resources_themes(themes_list: list) -> list:
    """
    Filter sublime-themes on root. Use sublime package.

    Example: Packages/Zukan Icon Theme/icons/Treble Adaptive.sublime-theme
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
        if re.match(expression, name):
            filter_list.append(name)
    return filter_list


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
        # print(theme)
        # print(icon_file_type_list)
    elif 'rules' not in theme_content:
        icon_file_type_list = [
            k for k in theme_content if k['class'] == 'icon_file_type'
        ]
        # print('no rules: ' + theme)
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
    hidden_theme_name = sublime.find_resources(theme_content['extends'])
    # Exclude Zukan created themes, important for Rebuild Files command.
    hidden_theme_name = [
        h
        for h in hidden_theme_name
        if not h.startswith(ZUKAN_EXCLUDE_HIDDEN_THEME_PATH)
    ]
    logger.debug('list theme opa, theme content %s', hidden_theme_name)
    for t in hidden_theme_name:
        hidden_theme_content = sublime.decode_value(sublime.load_resource(t))
        # print('extends: ' + t)
        find_attributes(theme, hidden_theme_content, list_theme_has_attributes)
        if 'extends' in hidden_theme_content:
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
        find_attributes(theme, theme_content, list_theme_has_attributes)
        if 'extends' in theme_content:
            find_attributes_hidden_file(theme, theme_content, list_theme_has_attributes)
    # print(list_theme_has_attributes)
    return list_theme_has_attributes
