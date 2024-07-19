import logging
import os
import shutil

from ..helpers.load_save_settings import get_settings
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
)
from ..utils.file_settings import (
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

    PNGs copies necessary if install using clone repo.
    """
    # Not checking if 'ignored_icon' is a list or 'change_icon' a dict, because they
    # are used after create syntaxes or preferences. Those are being check there.
    ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
    change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')

    for p in PRIMARY_ICONS:
        for s in ICONS_SUFFIX:
            if (
                TAG_PRIMARY in ignored_icon
                or p[0] in ignored_icon
                or p[1] in ignored_icon
                or (p[1] + SVG_EXTENSION) in ignored_icon
            ):
                if (
                    len(p) >= 3
                    and (p[0], p[1]) in change_icon.items()
                    and os.path.exists(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[2] + s + PNG_EXTENSION)
                    )
                ):
                    logger.debug(
                        '%s in change_icon, removing renamed PNGs %s', p[0], p[2]
                    )
                    os.remove(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[2] + s + PNG_EXTENSION)
                    )
                elif (
                    len(p) < 3
                    and p[0] not in change_icon.keys()
                    and os.path.exists(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                    )
                ):
                    logger.debug('%s not in change_icon, removing PNGs', p[0])
                    os.remove(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[1] + s + PNG_EXTENSION)
                    )
            elif (
                TAG_PRIMARY not in ignored_icon
                or p[0] not in ignored_icon
                or p[1] not in ignored_icon
                or (p[1] + SVG_EXTENSION) not in ignored_icon
            ):
                # Not checking if path exists, because if change icon path will exist
                # and will not replace icon unless delete icon first.
                if len(p) >= 3 and (p[0], p[1]) in change_icon.items():
                    # Currently, works for one icon option only.
                    logger.debug('%s in change_icon, renaming PNGs to %s', p[0], p[2])
                    shutil.copy2(
                        os.path.join(
                            ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                            p[1] + s + PNG_EXTENSION,
                        ),
                        os.path.join(ZUKAN_PKG_ICONS_PATH, p[2] + s + PNG_EXTENSION),
                    )
                elif len(p) < 3 and p[0] not in change_icon.keys():
                    logger.debug('%s not in change_icon, copying PNGs', p[0])
                    shutil.copy2(
                        os.path.join(
                            ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                            p[1] + s + PNG_EXTENSION,
                        ),
                        ZUKAN_PKG_ICONS_PATH,
                    )
