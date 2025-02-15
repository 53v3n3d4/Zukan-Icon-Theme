import errno
import logging
import os
import shutil

from .read_extract_zip import extract_folder
from ..utils.zukan_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
    ZUKAN_PKG_SRC_PATH,
)
from ..utils.zukan_pkg_folders import ZUKAN_PKG_FOLDERS

logger = logging.getLogger(__name__)


class MoveFolder:
    """
    Move folders and remove created folders. Used when installing and removing
    Zukan package.
    """

    def __init__(self):
        self.zukan_pkg_folders = ZUKAN_PKG_FOLDERS

    def move_folder(self, name: str):
        """
        Move folder if package is in folder Installed Packages.

        Parameters:
        name (str) -- folder name.
        """
        try:
            # check if is in Installed Packages, move
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
                logger.debug('Zukan exist in Installed folder.')
                if not os.path.exists(ZUKAN_PKG_PATH):
                    os.makedirs(ZUKAN_PKG_PATH)
                extract_folder(name, ZUKAN_PKG_PATH)
                logger.info('%s folder moved to Packages.', name)
                return name
            else:
                logger.debug('folder %s does not exist in Installed Packages.', name)
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), name
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), name
            )

    def move_folders(self):
        """
        Move icons and icons_data folders if project in folder Installed Packages.
        """
        try:
            # zukan_folders = ZUKAN_PKG_FOLDERS
            for folder in self.zukan_pkg_folders:
                self.move_folder(folder)
            return self.zukan_pkg_folders
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'icons and/or icons_syntaxes folder.',
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'icons and/or icons_syntaxes folder.',
            )

    def remove_created_folder(self, name: str):
        """
        Remove created folder from Zukan Icon Theme installation. Only
        if Zukan installed through Package Control.

        Parameters:
        name (str) -- folder name.
        """
        try:
            if (
                not os.path.exists(ZUKAN_PKG_SRC_PATH)
                and os.path.exists(ZUKAN_INSTALLED_PKG_PATH)
                and (
                    os.path.exists(ZUKAN_PKG_ICONS_PATH)
                    or os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
                )
            ):
                logger.debug('folder %s exists in Packages', name)
                shutil.rmtree(ZUKAN_PKG_PATH)
                logger.info('%s deleted.', ZUKAN_PKG_PATH)
                return name
            else:
                logger.info('Zukan folders does not exist in Installed Packages.')
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                name,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                name,
            )
