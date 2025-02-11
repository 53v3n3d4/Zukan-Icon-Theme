import json
import os
import sublime

from datetime import datetime, timedelta
from ..helpers.load_save_settings import get_cached_theme_info_lifespan
from ..utils.file_extensions import (
    SUBLIME_PACKAGE_EXTENSION,
)
from ..utils.st_default_themes import (
    ST_DEFAULT_THEMES,
)
from ..utils.zukan_paths import (
    INSTALLED_PACKAGES_PATH,
    THEME_INFO_FILE,
)


def get_modified_time(file_path: str) -> int:
    """
    Get file last modified time.

    Parameters:
    file_path (str) -- file path.

    Returns:
    (int) -- file lastest modified timestamp
    """
    installed_package_name = os.path.basename(os.path.dirname(file_path))
    # print(installed_package_name)

    if not installed_package_name:
        current_time = datetime.now(tz=timezone.utc)
        dt_rounded = current_time.replace(microsecond=0)

    else:
        modified_time = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(modified_time, tz=timezone.utc)
        dt_rounded = dt.replace(microsecond=0)

    # print(dt_rounded)
    return dt_rounded.timestamp()


def get_file_path(file_path: str) -> str:
    """
    Try define the file path for a theme. Theme can be from four different source:
    - Installed Packages
    - Packages
    - User
    - Default Theme

    Parameters:
    file_path (str) -- API returns themes with partial paths, e.g. Packages/
    Treble Adaptive.sublime-theme

    Returns:
    (str) -- return a string representing theme path.
    """
    installed_package_name = os.path.basename(os.path.dirname(file_path))

    if os.path.exists(file_path):
        return file_path

    elif installed_package_name == 'Theme - Default':
        return 'Theme - Default'

    elif os.path.exists(
        os.path.join(
            INSTALLED_PACKAGES_PATH, installed_package_name + SUBLIME_PACKAGE_EXTENSION
        )
    ):
        return os.path.join(
            INSTALLED_PACKAGES_PATH, installed_package_name + SUBLIME_PACKAGE_EXTENSION
        )


def is_theme_info_valid(file_path: str) -> bool:
    """

    Parameters:
    file_path (str) -- API returns themes with partial paths, e.g. Packages/
    Treble Adaptive.sublime-theme

    Returns:
    (Optional[bool) -- returns True or False for theme opacity value, or None
    if path does not exist.
    """
    if os.path.exists(THEME_INFO_FILE):
        theme_path = get_file_path(file_path)
        source_date = get_modified_time(theme_path)
        theme_name = os.path.basename(file_path)
        st_version = sublime.version()

        with open(THEME_INFO_FILE, 'r') as f:
            cache = json.load(f)

            for t in cache['themes']:
                # print(t)
                if (
                    theme_name == t['name']
                    and theme_name in ST_DEFAULT_THEMES
                    and st_version == t['st_version']
                ):
                    # print('ST Theme')
                    return t['opacity']['value']
                    break
                elif (
                    theme_name == t['name']
                    and theme_path == t['source']
                    and source_date == t['opacity']['last_updated']
                ):
                    # print('is true')
                    return t['opacity']['value']
                    break
    return None


def save_theme_info(file_path: str, opacity: bool):
    """
    Save theme info in a JSON file.

    Parameters:
    file_path (str) -- file path.
    opacity (bool) -- True or False for theme opacity value.
    """
    theme_path = get_file_path(file_path)
    # print(theme_path)
    last_updated = get_modified_time(theme_path)
    theme_name = os.path.basename(file_path)
    st_version = sublime.version()

    if not os.path.exists(THEME_INFO_FILE):
        cache = {'themes': []}
    else:
        with open(THEME_INFO_FILE, 'r') as f:
            cache = json.load(f)

    theme_found = False

    for t in cache['themes']:
        if (
            theme_name == t['name']
            and theme_name in ST_DEFAULT_THEMES
            and st_version == t['st_version']
        ):
            if last_updated == t['opacity']['last_updated']:
                theme_found = True
                return
            else:
                t['opacity']['value'] = opacity
                t['opacity']['last_updated'] = last_updated
                theme_found = True
                break

        elif theme_name == t['name'] and theme_path == t['source']:
            if last_updated == t['opacity']['last_updated']:
                theme_found = True
                return
            else:
                t['opacity']['value'] = opacity
                t['opacity']['last_updated'] = last_updated
                theme_found = True
                break

    if not theme_found:
        cache['themes'].append(
            {
                'name': theme_name,
                'source': theme_path,
                'st_version': st_version,
                'opacity': {
                    'value': opacity,
                    'last_updated': last_updated,
                },
            }
        )

    with open(THEME_INFO_FILE, 'w') as f:
        json.dump(cache, f, indent=4)


def cache_theme_info_lifespan() -> bool:
    """
    `theme_info.json` cache lifespan. Default is 180 days.

    Returns:
    (bool) -- True or False for expired cache.
    """
    if not os.path.exists(THEME_INFO_FILE):
        return False

    cache_theme_info_lifespan = get_cached_theme_info_lifespan()
    cache_created_time = datetime.fromtimestamp(os.path.getctime(THEME_INFO_FILE))
    expiration_time = cache_created_time + timedelta(days=cache_theme_info_lifespan)

    # print(expiration_time)
    return datetime.now() > expiration_time


def delete_cached_theme_info():
    """
    Delete cache file `theme_info.json` if cache expired.
    """
    if cache_theme_info_lifespan():
        os.remove(THEME_INFO_FILE)
