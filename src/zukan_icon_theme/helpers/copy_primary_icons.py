import logging
import os
import shutil

from ..helpers.load_save_settings import get_settings
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
)
from ..utils.file_settings import (
    USER_SETTINGS,
    ZUKAN_SETTINGS,
)
from ..utils.primary_icons import (
    ICONS_SUFFIX,
    PRIMARY_ICONS,
    TAG_PRIMARY,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
)

logger = logging.getLogger(__name__)


def copy_primary_icons():
    """
    'primary' icons need to delete PNGs to work in 'ignore_icon' setting. They do
    not need preference file to show.

    While copying, if 'prefer_icon' setting is used, it will choose the icon, dark
    or light, to be copied.

    PNGs copies necessary if install using clone repo.
    """
    # Not checking if 'ignored_icon' is a list or 'change_icon' a dict, because they
    # are used after create syntaxes or preferences. Those are being check there.
    ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
    change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
    prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')

    # Get current user theme
    theme_name = get_settings(USER_SETTINGS, 'theme')

    for p in PRIMARY_ICONS:
        for s in ICONS_SUFFIX:
            for i in p[2]:
                if (
                    TAG_PRIMARY in ignored_icon
                    or p[0] in ignored_icon
                    or i in ignored_icon
                    or (i + SVG_EXTENSION) in ignored_icon
                ):
                    if (p[0], i) in change_icon.items() and os.path.exists(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                    ):
                        logger.debug(
                            '%s in change_icon, removing renamed %s%s',
                            p[0],
                            p[1],
                            s,
                        )
                        os.remove(
                            os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                        )
                    elif p[0] not in change_icon.keys() and os.path.exists(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                    ):
                        logger.debug(
                            '%s not in change_icon, removing %s%s', p[0], p[1], s
                        )
                        os.remove(
                            os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                        )
                elif (
                    TAG_PRIMARY not in ignored_icon
                    or p[0] not in ignored_icon
                    or i not in ignored_icon
                    or (i + SVG_EXTENSION) not in ignored_icon
                ):
                    # Not checking if path exists, because if change icon path will exist
                    # and will not replace icon unless delete icon first.
                    if (p[0], i) in change_icon.items():
                        logger.debug(
                            '%s in change_icon, renaming PNGs to %s%s',
                            p[0],
                            p[1],
                            s,
                        )
                        shutil.copy2(
                            os.path.join(
                                ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                                i + s + PNG_EXTENSION,
                            ),
                            os.path.join(
                                ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION
                            ),
                        )

                    elif p[0] not in change_icon.keys():
                        # Icon light or dark
                        if theme_name in prefer_icon and i.rsplit('-', 1)[
                            1
                        ] == prefer_icon.get(theme_name):
                            logger.debug(
                                '%s not in change_icon, copying prefer icon %s%s',
                                p[0],
                                i,
                                s,
                            )
                            shutil.copy2(
                                os.path.join(
                                    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                                    i + s + PNG_EXTENSION,
                                ),
                                os.path.join(
                                    ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION
                                ),
                            )

                        elif theme_name not in prefer_icon:
                            logger.debug(
                                '%s not in change_icon, copying default %s%s',
                                p[0],
                                i,
                                s,
                            )
                            shutil.copy2(
                                # Copy default icon, dark.
                                os.path.join(
                                    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                                    p[2][0] + s + PNG_EXTENSION,
                                ),
                                os.path.join(
                                    ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION
                                ),
                            )
