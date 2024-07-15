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
    ZUKAN_PKG_ICONS_DATA_PATH,
)


def copy_primary_icons():
    """
    'primary' icons need to delete PNGs to work in 'ignore_icon' setting. They do
    not need preference file to show.
    """
    # Not checking if 'ignored_icon' is a list because it is used after create
    # syntaxes or preferences. It is being check there.
    ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
    for i in PRIMARY_ICONS:
        for s in ICONS_SUFFIX:
            if (
                TAG_PRIMARY in ignored_icon
                or i[0] in ignored_icon
                or i[1] in ignored_icon
                or (i[1] + SVG_EXTENSION) in ignored_icon
            ):
                if os.path.exists(
                    os.path.join(ZUKAN_PKG_ICONS_PATH, i[1] + s + PNG_EXTENSION)
                ):
                    os.remove(
                        os.path.join(ZUKAN_PKG_ICONS_PATH, i[1] + s + PNG_EXTENSION)
                    )
            elif (
                TAG_PRIMARY not in ignored_icon
                or i[0] not in ignored_icon
                or i[1] not in ignored_icon
                or (i[1] + SVG_EXTENSION) not in ignored_icon
            ):
                if not os.path.exists(
                    os.path.join(ZUKAN_PKG_ICONS_PATH, i[1] + s + PNG_EXTENSION)
                ):
                    shutil.copy2(
                        os.path.join(
                            ZUKAN_PKG_ICONS_DATA_PATH, i[1] + s + PNG_EXTENSION
                        ),
                        ZUKAN_PKG_ICONS_PATH,
                    )
