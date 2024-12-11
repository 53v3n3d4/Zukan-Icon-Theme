import logging
import re
import sublime

from ..utils.zukan_paths import (
    PKG_ZUKAN_ICON_THEME_FOLDER,
)

logger = logging.getLogger(__name__)


def filter_resources_themes(themes_list: list) -> list:
    """
    Filter sublime-themes on root.

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
    Search for sublime-themes then filter results.

    Retunrs:
    (list) -- Filtered list of sublime-themes.
    """
    themes_list = sublime.find_resources('*.sublime-theme')
    return filter_resources_themes(themes_list)


def package_theme_exists(theme_name: str) -> bool:
    """
    Check if a Package Theme is installed

    Paramenters:
    theme_name (str) -- theme name.

    Returns:
    (bool) -- True or False for Package Theme
    """
    theme_st_path = sublime.find_resources(theme_name)
    # Excluding themes in Packages sub directories.
    filter_list = filter_resources_themes(theme_st_path)
    list_all_themes = search_resources_sublime_themes()

    # Check if installed theme file exist.
    for t in filter_list:
        if t in list_all_themes:
            return True
        if t not in list_all_themes:
            return False


def find_attributes(
    theme: str,
    theme_content: dict,
    class_name: str,
    target_key: str,
    target_list: list,
    target_values: list = None,
    class_parent: str = None,
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
    target_list (list) -- list if theme and its hidden themes have
    attributes or value.
    """
    if 'rules' in theme_content:
        class_name_list = [
            k for k in theme_content['rules'] if k['class'] == class_name
        ]
        # print(theme)
        # print(class_name_list)
    elif 'rules' not in theme_content:
        class_name_list = [k for k in theme_content if k['class'] == class_name]
        # print('no rules: ' + theme)
    for i in class_name_list:
        # Theme opacity
        if class_parent:
            if i.get(class_parent) is not None:
                for p in i.get(class_parent):
                    if p['class'] == target_key and all(
                        a in p['attributes'] for a in target_values
                    ):
                        logger.debug('%s has attributes', theme)
                        target_list.append(True)

        # Find sidebar background
        if not class_parent:
            logger.debug('%s sidebar layer0.tint is ', theme)
            target_list.append(i.get(target_key))


def find_attributes_hidden_file(
    theme: str,
    theme_content: dict,
    class_name: str,
    target_key: str,
    target_list: list,
    target_values: list = None,
    class_parent: str = None,
) -> list:
    """
    Recursively search for attributes, in hidden-theme files.

    Paramenters:
    theme (str) -- path theme name.
    theme_content (dict) -- parsed json file, hidden-theme.
    target_list (list) -- list if theme and its hidden themes have
    attributes or value.
    """
    hidden_theme_list = sublime.find_resources(theme_content['extends'])
    # Exclude Zukan created themes, important for Rebuild Files command.
    hidden_theme_name = [
        h for h in hidden_theme_list if not h.startswith(PKG_ZUKAN_ICON_THEME_FOLDER)
    ]
    for t in hidden_theme_name:
        hidden_theme_content = sublime.decode_value(sublime.load_resource(t))
        logger.debug('extends %s', t)
        find_attributes(
            theme,
            hidden_theme_content,
            class_name,
            target_key,
            target_list,
            target_values,
            class_parent,
        )
        logger.debug('%s target_list is %s', t, target_list)
        if 'extends' in hidden_theme_content:
            find_attributes_hidden_file(
                theme,
                hidden_theme_content,
                class_name,
                target_key,
                target_list,
                target_values,
                class_parent,
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
    class_name = 'icon_file_type'
    class_parent = 'parents'
    target_key = 'tree_row'
    target_values = ['hover', 'selected']
    target_list = []
    theme_content = sublime.decode_value(sublime.load_resource(theme_name))

    find_attributes(
        theme_name,
        theme_content,
        class_name,
        target_key,
        target_list,
        target_values,
        class_parent,
    )
    if 'extends' in theme_content:
        find_attributes_hidden_file(
            theme_name,
            theme_content,
            class_name,
            target_key,
            target_list,
            target_values,
            class_parent,
        )

    if True in target_list:
        return True
    else:
        return False
