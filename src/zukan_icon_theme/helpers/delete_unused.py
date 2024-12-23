import logging
import os

from ..lib.icons_themes import ZukanTheme
from ..helpers.search_themes import (
    search_resources_sublime_themes,
)
from ..utils.file_extensions import (
    PNG_EXTENSION,
)
from ..utils.icons_suffix import (
    ICONS_SUFFIX,
)

logger = logging.getLogger(__name__)


def delete_unused_icon_theme():
    """
    Delete unused icon theme file.

    When uninstall a theme package, it leaves an icon-theme file.
    """
    list_all_themes = search_resources_sublime_themes()
    list_icon_themes = ZukanTheme.list_created_icons_themes()

    list_themes = []

    for t in list_all_themes:
        n = os.path.basename(t)
        list_themes.append(n)

    list_unused_icon_themes = list(set(list_icon_themes) - set(list_themes))

    for o in list_unused_icon_themes:
        logger.info('removing unused zukan icon theme, %s', o)
        ZukanTheme.delete_icon_theme(o)


def delete_unused_icons(folder: str):
    """
    Delete unused icons that has dark and light versions.

    Scan over 'icons' and 'primary_icons' folder and delete unused icons.
    Icons that has a dark or light version, previous icons are not used.

    Example:
    - ada.png
    - ada-dark.png
    - ada-light.png

    Parameters:
    folder (str) -- path to folder.
    """
    icon_has_dark = []
    icon_has_light = []
    icon_no_version = []

    for i in os.listdir(folder):
        if i.endswith('-dark.png'):
            i = i[:-9]
            icon_has_dark.append(i)

        if i.endswith('-light.png'):
            i = i[:-10]
            icon_has_light.append(i)

        if not i.endswith('-dark.png') and not i.endswith('-light.png'):
            i = i[:-4]
            icon_no_version.append(i)

    remove_unused = [
        i for i in icon_no_version if i in icon_has_dark and i in icon_has_light
    ]

    if remove_unused:
        logger.debug('removing unused PNGs.')

        # Add suffix and extension
        for i in remove_unused:
            for s in ICONS_SUFFIX:
                icon_path = os.path.join(folder, i + s + PNG_EXTENSION)

                if os.path.exists(icon_path):
                    os.remove(icon_path)
                    logger.debug('unused icon %s%s%s deleted.', i, s, PNG_EXTENSION)
                    # print('{}{}{} removed'.format(i, s, PNG_EXTENSION))

    if not remove_unused:
        logger.debug('folder has no unused icon to remove.')
