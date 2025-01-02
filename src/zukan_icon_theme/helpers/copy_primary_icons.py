import logging
import os
import shutil

from ..helpers.load_save_settings import (
    get_change_icon_settings,
    get_ignored_icon_settings,
    get_prefer_icon_settings,
    get_theme_name,
)
from ..helpers.search_themes import get_sidebar_bgcolor
from ..helpers.color_dark_light import get_icon_dark_light
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
)
from ..utils.icons_suffix import (
    ICONS_SUFFIX,
)
from ..utils.primary_icons import (
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

    While copying, if 'prefer_icon' or 'auto_prefer_icon' setting is used, it
    will choose the icon, dark or light, to be copied.

    PNGs copies necessary if install using clone repo.
    """
    auto_prefer_icon, prefer_icon = get_prefer_icon_settings()
    change_icon, _ = get_change_icon_settings()
    ignored_icon = get_ignored_icon_settings()

    theme_name = get_theme_name()
    bgcolor = get_sidebar_bgcolor(theme_name)
    icon_dark_light = get_icon_dark_light(bgcolor)

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
                    # Not checking if path exists, because change icon path will exist
                    # and will not replace icon unless delete icon first.
                    if (p[0], i) in change_icon.items():
                        logger.debug(
                            '%s in change_icon, renaming PNGs to %s%s',
                            p[0],
                            p[1],
                            s,
                        )
                        # Icon has dark/light option
                        if i.endswith('-dark') or i.endswith('-light'):
                            if bgcolor == 'dark':
                                icon_name = i.rsplit('-', 1)[0] + '-light'
                            else:
                                icon_name = i.rsplit('-', 1)[0] + '-dark'

                            shutil.copy2(
                                os.path.join(
                                    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                                    icon_name + s + PNG_EXTENSION,
                                ),
                                os.path.join(
                                    ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION
                                ),
                            )
                        # Icon does not have icon dark/light option
                        # E.g. file_type_image-1
                        else:
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
                        if (
                            theme_name in prefer_icon
                            and i.rsplit('-', 1)[1] == prefer_icon.get(theme_name)
                        ) or (
                            bgcolor
                            and theme_name not in prefer_icon
                            and i.rsplit('-', 1)[1] == icon_dark_light
                            and auto_prefer_icon
                        ):
                            logger.debug(
                                '%s not in change_icon, copying prefer icon %s%s',
                                p[0],
                                i,
                                s,
                            )
                            if bgcolor == 'dark':
                                icon_name = p[2][1]
                            else:
                                icon_name = p[2][0]

                            shutil.copy2(
                                os.path.join(
                                    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                                    icon_name + s + PNG_EXTENSION,
                                ),
                                os.path.join(
                                    ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION
                                ),
                            )

                        elif (
                            theme_name not in prefer_icon and not auto_prefer_icon
                        ) or not bgcolor:
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
