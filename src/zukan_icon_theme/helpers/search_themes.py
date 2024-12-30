import logging
import re
import sublime

from ..helpers.theme_dark_light import (
    convert_to_rgb,
    rgb_dark_light,
    st_colors_to_hex,
)
from ..helpers.read_write_data import read_pickle_data
from ..utils.st_color_palette import (
    ST_COLOR_PALETTE,
)
from ..utils.zukan_paths import (
    PKG_ZUKAN_ICON_THEME_FOLDER,
    USER_UI_SETTINGS_FILE,
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


def find_variables(
    var_value: str, theme_content: str, target_list: list, theme: str
) -> list:
    """
    Recursively find variable value. Filter for HSL, RGB, Hex, background and
    ST colors to return dark/light, depending on color HSP.

    Paramenters:
    var_value (str) -- variable name.
    theme_content (dict) -- parsed json file, sublime-theme.
    target_list (list) -- list if theme and its hidden themes have
    attributes or value.
    theme (str) -- path theme name.

    Returns:
    target_list (list) -- 'dark' or 'light' depending on color HSP.
    """
    regex_hsl = (
        # r'hsla?\((\d{1,3}),\s*(\d+)(?:%)?\s*,\s*(\d+)(?:%)?\s*(?:,'
        # '\s*([01]?\d(\.\d+)?|1(\.0+)?))?\)'
        r'hsla?\((\d+),\s*(-?\d*\.?\d+)%?,\s*(-?\d*\.?\d+)%?(?:,\s*(\d+(\.\d+)?))?\)'
    )
    regex_rgb = (
        r'rgba?\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})(?:,'
        '\s*([01]?\d(\.\d+)?|1(\.0+)?))?\)'
    )
    regex_hex = r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})'

    # Both Default and Default Dark give HSP = 124.12283073381384.
    # So it chooses icon light for both themes.
    # HSP 127,5 is the formula limit to select dark or light.
    #
    # Ensuring here until find a better solution
    if theme == 'Packages/Theme - Default/Default.sublime-theme':
        dark_light = 'light'

        target_list.append(dark_light)

    # HSL and HSLA
    elif re.match(regex_hsl, var_value):
        result = re.findall(regex_hsl, var_value)
        # print(isinstance(result, str))
        # print(result[0])

        if result:
            for r in result:
                hue, sat, lum, alpha = r[0], r[1], r[2], r[3]

                hsl_color = 'hsl({h}, {s}%, {l}%)'.format(h=hue, s=sat, l=lum)

                if alpha:
                    hsl_color = 'hsla({h}, {s}%, {l}%, {a})'.format(
                        h=hue, s=sat, l=lum, a=alpha
                    )

        dark_light = rgb_dark_light(convert_to_rgb(hsl_color))

        target_list.append(dark_light)

    # RGB and RGBA
    elif re.match(regex_rgb, var_value):
        result = re.findall(regex_rgb, var_value)

        if result:
            for r in result:
                red, green, blue, alpha = r[0], r[1], r[2], r[3]

                rgb_color = 'rgb({r}, {g}, {b})'.format(r=red, g=green, b=blue)

                if alpha:
                    rgb_color = 'rgba({r}, {g}, {b}, {a})'.format(
                        r=red, g=green, b=blue, a=alpha
                    )

        dark_light = rgb_dark_light(convert_to_rgb(rgb_color))

        target_list.append(dark_light)

    # Hex and Hexa
    elif re.match(regex_hex, var_value):
        hex_color = re.findall(regex_hex, var_value)
        # print(hex_color[0])

        dark_light = rgb_dark_light(convert_to_rgb(hex_color[0]))

        target_list.append(dark_light)

    # Background
    elif 'var(--background)' in var_value:
        # Get color scheme background and append
        user_ui_settings = read_pickle_data(USER_UI_SETTINGS_FILE)
        bgcolor = [d.get('background') for d in user_ui_settings]

        dark_light = rgb_dark_light(convert_to_rgb(bgcolor[0]))

        target_list.append(dark_light)

    # ST color palette
    # E.g. aliceblue
    elif any(var_value in d for d in ST_COLOR_PALETTE):
        st_color = var_value

        dark_light = rgb_dark_light(convert_to_rgb(st_colors_to_hex(st_color)))

        target_list.append(dark_light)

    elif 'var' in var_value:
        logger.debug('searching in variables.')

        if 'variables' in theme_content:
            for k, v in theme_content['variables'].items():
                var_name = re.findall(r'var\(([^)]+)\)', var_value)

                if k == var_name[0]:
                    logger.debug('recursive find variables.')
                    # print(v)

                    find_variables(v, theme_content, target_list, theme)

    else:
        logger.debug('failed to find sidebar background.')


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

    elif 'rules' not in theme_content:
        class_name_list = [k for k in theme_content if k['class'] == class_name]

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
        if not class_parent and i.get(target_key):
            logger.debug('%s sidebar layer0.tint is %s', theme, i.get(target_key))

            find_variables(i.get(target_key), theme_content, target_list, theme)


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


def theme_with_opacity(theme_st_path: str) -> bool:
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
    theme_st_path (str) -- path to theme.

    Returns:
    (bool) -- True or False for theme or its hidden-theme(s) has attributes.
    """
    class_name = 'icon_file_type'
    class_parent = 'parents'
    target_key = 'tree_row'
    target_values = ['hover', 'selected']
    target_list = []
    theme_content = sublime.decode_value(sublime.load_resource(theme_st_path))

    find_attributes(
        theme_st_path,
        theme_content,
        class_name,
        target_key,
        target_list,
        target_values,
        class_parent,
    )
    if 'extends' in theme_content:
        find_attributes_hidden_file(
            theme_st_path,
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


def find_sidebar_background(theme_st_path: str) -> list:
    """
    Find sidebar background color and return 'dark' or 'light', depending on
    color HSP.

    It search in sublime theme files for class 'sidebar_container' and key
    'layer0.tint'.

    Parameters:
    theme_st_path (str) -- path to theme.

    Returns:
    target_list (list) -- 'dark' or 'light' depending on color HSP.
    """
    class_name = 'sidebar_container'
    target_key = 'layer0.tint'
    target_list = []
    theme_content = sublime.decode_value(sublime.load_resource(theme_st_path))
    find_attributes(
        theme_st_path,
        theme_content,
        class_name,
        target_key,
        target_list,
    )
    if 'extends' in theme_content:
        find_attributes_hidden_file(
            theme_st_path,
            theme_content,
            class_name,
            target_key,
            target_list,
        )

    # print(target_list)
    return target_list


def get_sidebar_bgcolor(theme_name: str) -> str:
    """
    Get sidebar background color.

    Parameters:
    theme_name (str) -- theme name. E.g.: Default.sublime-theme

    Returns:
    (str) -- returns value 'dark' or 'light'
    """
    bgcolor = None
    theme_st_path = sublime.find_resources(theme_name)

    if theme_st_path:
        bgcolor = find_sidebar_background(theme_st_path[0])

    return bgcolor[0]
