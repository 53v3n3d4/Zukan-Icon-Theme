import json
import logging
import os
import sublime

from zipfile import ZipFile
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
    ZUKAN_INSTALLED_PKG_PATH,
)

logger = logging.getLogger(__name__)


def get_settings(file_settings: str, option: str = None):
    """
    Load sublime-settings, and get options.

    Parameters:
    file_settings (str) -- sublime-settings file.
    option (str) -- get option value.
    """
    settings = sublime.load_settings(file_settings)
    if option is not None:
        return settings.get(option)
    return settings


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
    if theme_name == 'auto':
        theme_name = dark_theme_name if system_theme() else light_theme_name

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
    Get create custom icon setting.

    Returns:
    (tuple) -- tuple with create custom icon setting.
    """
    create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')

    if not is_valid_list(create_custom_icon):
        create_custom_icon = []

    return create_custom_icon


def get_change_icon_settings() -> tuple:
    """
    Get change icon setting.

    Returns:
    (tuple) -- tuple with change icon setting.
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
    Get ignore icon setting.

    Returns:
    (tuple) -- tuple with ignore icon setting.
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

    # ST4 Python 3.3 issue where settings are not loaded.
    # A similar issue occurs in `is_zukan_listener_enabled`.
    # This helps when `.sublime-package` file is enabled from `ignored_packages`,
    # e.g., after a Package Control upgrade. Upon reloading `file_type_icon`,
    # Sublime fails to load settings and returns None.
    # This works until the package is disabled and then re-enabled. After that,
    # Sublime cannot read settings and return them with value None instead of the
    # values from `Zukan Icon Theme.sublime-settings`.
    # current_settings = {
    #     'version': '0.4.5',
    #     'auto_install_theme': False,
    #     'log_level': 'INFO',
    #     'rebuild_on_upgrade': True,
    #     'zukan_restart_message': True,
    #     'ignored_icon': [],
    #     'create_custom_icon': [],
    #     'zukan_listener_enabled': True,
    #     'prefer_icon': {},
    #     'change_icon_file_extension': [],
    #     'ignored_theme': [],
    #     'auto_rebuild_icon': True,
    #     'auto_prefer_icon': True,
    #     'change_icon': {},
    # }
    if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
        current_settings = default_settings()

    for s in ZUKAN_SETTINGS_OPTIONS:
        setting_option = get_settings(ZUKAN_SETTINGS, s)
        # ST4 Python 3.3 issue not loading settings.
        # `set_timeout` for `load_settings`or for this methos at start `on_loaded`
        # did not work.
        if setting_option is not None:
            current_settings.update({s: setting_option})

    return current_settings


def remove_json_comments(json_data: str) -> str:
    """
    Removes comments from JSON.

    Parameters:
    json_data (str) -- string JSON.

    Returns:
    (str) -- string with out comments.
    """
    lines = json_data.splitlines()
    result = []

    for line in lines:
        if '//' in line:
            line = line.split('//', 1)[0]

        if line.strip():
            result.append(line)

    return '\n'.join(result)


def default_settings() -> dict:
    """
    Read default settings, `Zukan Icon Theme.sublime-settings`, in,
    `.sublime-package`, zip file.
    """
    installed_zukan_sublime_settings = os.path.join('sublime', ZUKAN_SETTINGS)

    with ZipFile(ZUKAN_INSTALLED_PKG_PATH, 'r') as zf:
        with zf.open(installed_zukan_sublime_settings) as f:
            content = f.read().decode('utf-8')

            content_no_comments = remove_json_comments(content)
            current_settings = json.loads(content_no_comments)

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
    current_system_theme: bool,
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
    current_ui_settings.update({'sidebar_bgcolor': sidebar_bgcolor})
    current_ui_settings.update({'system_theme': current_system_theme})
    current_ui_settings.update({'theme': current_theme})

    if os.path.exists(USER_UI_SETTINGS_FILE):
        # Delete previous pickle file
        os.remove(USER_UI_SETTINGS_FILE)

    dump_pickle_data(current_ui_settings, USER_UI_SETTINGS_FILE)


def is_zukan_listener_enabled() -> bool:
    """
    Check if zukan listener enabled setting is true or false.

    Returns:
    (bool) -- True or False for zukan listener enabled setting.
    """
    zukan_listener_enabled = get_settings(ZUKAN_SETTINGS, 'zukan_listener_enabled')

    # Help when `sublime-package` file is enabled from `ignored_packages`, e.g.
    # Package Control upgrade. After reload `file_type_icon`, Sublime seems to fail
    # to load settings and returns None, even though the default value is True.
    # Tested in ST4 and Python 3.3.
    # Same issue occur on `read_current_settings`.
    if zukan_listener_enabled is None:
        zukan_listener_enabled = True

    return zukan_listener_enabled


def is_zukan_restart_message() -> bool:
    """
    Check if zukan restart message setting is true or false.

    Returns:
    (bool) -- True or False for zukan restart message setting.
    """
    zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

    return zukan_restart_message


def is_cached_theme_info() -> (bool, None):
    """
    Check if cache theme info setting is true or false.

    Returns:
    (bool, None) -- True or False for valid cache, or None for cache invalid.
    """
    cached_theme_info = get_settings(ZUKAN_SETTINGS, 'cache_theme_info')

    return cached_theme_info


def get_cached_theme_info_lifespan() -> int:
    """
    Get cache theme info lifespan setting.

    Returns:
    (int) -- an integer representing the cache theme info lifespan in days.
    """
    cached_theme_info = get_settings(ZUKAN_SETTINGS, 'cache_theme_info_lifespan')

    return cached_theme_info
