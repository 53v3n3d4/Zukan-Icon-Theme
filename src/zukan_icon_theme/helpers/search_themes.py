import logging
import re
import sublime

from ..utils.zukan_paths import (
    PKG_ZUKAN_ICON_THEME_FOLDER,
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
    theme: str, theme_content: dict, theme_has_attributes: list
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
    theme_has_attributes (list) -- list if theme and its hidden themes have
    attributes hover and selected.
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
                    logger.debug('%s has attributes', theme)
                    theme_has_attributes.append(True)


def find_attributes_hidden_file(
    theme: str, theme_content: dict, theme_has_attributes: list
) -> list:
    """
    Recursively search for attributes, in hidden-theme files.

    Paramenters:
    theme (str) -- path theme name.
    theme_content (dict) -- parsed json file, hidden-theme.
    theme_has_attributes (list) -- list if theme and its hidden themes have
    attributes hover and selected.
    """
    hidden_theme_list = sublime.find_resources(theme_content['extends'])
    # Exclude Zukan created themes, important for Rebuild Files command.
    hidden_theme_name = [
        h for h in hidden_theme_list if not h.startswith(PKG_ZUKAN_ICON_THEME_FOLDER)
    ]
    for t in hidden_theme_name:
        hidden_theme_content = sublime.decode_value(sublime.load_resource(t))
        logger.debug('extends %s', t)
        find_attributes(theme, hidden_theme_content, theme_has_attributes)
        logger.debug('%s theme_has_attributes is %s', t, theme_has_attributes)
        if 'extends' in hidden_theme_content:
            find_attributes_hidden_file(
                theme, hidden_theme_content, theme_has_attributes
            )


def theme_with_opacity(theme_name: str) -> bool:
    """
    Search if theme or hidden theme use icon_file_type, with attributes 'hover' and
    'selected'.

    Example:
    {
        "class": "icon_file_type",
        "parents": [{"class": "tree_row", "attributes": ["hover"]}],
        "layer0.opacity": 1.0
    }

    Parameters:
    theme_name (str) -- theme name.

    Returns:
    (bool) -- True or False for theme or its hidden-theme(s) has attributes.
    """
    theme_has_attributes = []
    theme_content = sublime.decode_value(sublime.load_resource(theme_name))
    find_attributes(theme_name, theme_content, theme_has_attributes)
    if 'extends' in theme_content:
        find_attributes_hidden_file(theme_name, theme_content, theme_has_attributes)

    if True in theme_has_attributes:
        return True
    else:
        return False
