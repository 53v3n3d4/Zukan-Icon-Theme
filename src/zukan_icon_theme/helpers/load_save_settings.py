import logging
import os
import sublime

from ..helpers.read_write_data import dump_pickle_data
from ..helpers.system_theme import system_theme
from ..utils.file_settings import (
    USER_SETTINGS,
    ZUKAN_SETTINGS,
    ZUKAN_SETTINGS_OPTIONS,
)
from ..utils.zukan_paths import (
    USER_UI_SETTINGS_FILE,
    ZUKAN_CURRENT_SETTINGS_FILE,
)

logger = logging.getLogger(__name__)


def get_settings(file_settings: str, option: str = None):
    """
    Load sublime-settings, and get options.

    Parameters:
    file_settings (str) -- sublime-settings file.
    option (str) -- get option value.
    """
    if option is not None:
        return sublime.load_settings(file_settings).get(option)
    if option is None:
        return sublime.load_settings(file_settings)


def set_save_settings(file_settings: str, option: str, option_value: list):
    """
    Modify and save settings options.

    Parameters:
    file_settings (str) -- sublime-settings file.
    option (str) -- set option key.
    option_value (list) --  option vslue.
    """
    sublime.load_settings(file_settings).set(option, option_value)
    sublime.save_settings(file_settings)


def is_valid_dict(setting_option: dict) -> bool:
    """
    Check if the setting_option is a dictionary.
    """
    if not isinstance(setting_option, dict):
        logger.warning('%s option malformed, needs to be a dict')
        return False
    return True


def is_valid_list(setting_option: list) -> bool:
    """
    Check if the setting_option is a list.
    """
    if not isinstance(setting_option, list):
        logger.warning('%s option malformed, needs to be a list')
        return False
    return True


def get_theme_name() -> str:
    """
    Get theme name.

    Returns:
    (str) -- theme name.
    """
    dark_theme_name = get_settings(USER_SETTINGS, 'dark_theme')
    light_theme_name = get_settings(USER_SETTINGS, 'light_theme')
    theme_name = get_settings(USER_SETTINGS, 'theme')

    # Get system theme
    if theme_name == 'auto' and not system_theme():
        theme_name = light_theme_name

    if theme_name == 'auto' and system_theme():
        theme_name = dark_theme_name

    return theme_name


def get_theme_settings() -> tuple:
    """
    Get theme settings.

    Returns:
    (tuple) -- tuple with zukan theme settings.
    """
    auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
    ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')

    if not is_valid_list(ignored_theme):
        ignored_theme = []

    return ignored_theme, auto_install_theme


def get_create_custom_icon_settings() -> tuple:
    """
    Get create custom icon settings.

    Returns:
    (tuple) -- tuple with create custom icon settings.
    """
    create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')

    if not is_valid_list(create_custom_icon):
        create_custom_icon = []

    return create_custom_icon


def get_change_icon_settings() -> tuple:
    """
    Get change icon settings.

    Returns:
    (tuple) -- tuple with change icon settings.
    """
    change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
    change_icon_file_extension = get_settings(
        ZUKAN_SETTINGS, 'change_icon_file_extension'
    )

    if not is_valid_dict(change_icon):
        change_icon = {}

    return change_icon, change_icon_file_extension


def get_prefer_icon_settings() -> tuple:
    """
    Get prefer icon settings.

    Returns:
    (tuple) -- tuple with prefer icon settings.
    """
    auto_prefer_icon = get_settings(ZUKAN_SETTINGS, 'auto_prefer_icon')
    prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')

    if not is_valid_dict(prefer_icon):
        prefer_icon = {}

    return auto_prefer_icon, prefer_icon


def get_ignored_icon_settings() -> tuple:
    """
    Get ignore icon settings.

    Returns:
    (tuple) -- tuple with ignore icon settings.
    """
    ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

    if not is_valid_list(ignored_icon):
        ignored_icon = []

    return ignored_icon


def get_upgraded_version_settings() -> tuple:
    """
    Get upgrade and version plugin settings.

    Returns:
    (tuple) -- tuple with upgrade and version plugin settings.
    """
    pkg_version = get_settings(ZUKAN_SETTINGS, 'version')
    auto_upgraded = get_settings(ZUKAN_SETTINGS, 'rebuild_on_upgrade')

    return pkg_version, auto_upgraded


def read_current_settings() -> dict:
    """
    Read current settings from zukan options list.
    """
    current_settings = {}

    for s in ZUKAN_SETTINGS_OPTIONS:
        setting_option = get_settings(ZUKAN_SETTINGS, s)
        current_settings.update({s: setting_option})

    return current_settings


def save_current_settings():
    """
    Save current settings in pkl file to compare when Zukan settings options
    get modified.
    """
    if os.path.exists(ZUKAN_CURRENT_SETTINGS_FILE):
        # Delete previous pickle file
        os.remove(ZUKAN_CURRENT_SETTINGS_FILE)

    current_settings = read_current_settings()
    dump_pickle_data(current_settings, ZUKAN_CURRENT_SETTINGS_FILE)


def save_current_ui_settings(
    color_scheme_background: str,
    current_color_scheme: str,
    current_dark_theme: str,
    current_light_theme: str,
    current_theme: str,
    sidebar_bgcolor: str = 'light',
):
    """
    Save current user UI theme and color-scheme.

    Parameters:
    color_scheme_background (str) - color scheme background.
    current_theme (str) -- user theme in Preferences.
    current_color_scheme (str) -- user color-scheme in Preferences.
    """
    current_ui_settings = {}
    current_ui_settings.update({'background': color_scheme_background})
    current_ui_settings.update({'color_scheme': current_color_scheme})
    current_ui_settings.update({'dark_theme': current_dark_theme})
    current_ui_settings.update({'light_theme': current_light_theme})
    current_ui_settings.update({'theme': current_theme})
    current_ui_settings.update({'sidebar_bgcolor': sidebar_bgcolor})

    if os.path.exists(USER_UI_SETTINGS_FILE):
        # Delete previous pickle file
        os.remove(USER_UI_SETTINGS_FILE)

    dump_pickle_data(current_ui_settings, USER_UI_SETTINGS_FILE)
