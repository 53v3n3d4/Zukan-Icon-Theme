import errno
import logging
import os
import shutil

# from ..helpers.print_message import print_filenotfounderror, print_oserror
from ..helpers.read_extract_zip import extract_folder
from ..utils.zukan_dir_paths import (
    # INSTALLED_PACKAGES_PATH,
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)
from ..utils.zukan_pkg_folders import ZUKAN_PKG_FOLDERS

logger = logging.getLogger(__name__)

# Testing path
zukan_pkg_assets = os.path.join(ZUKAN_PKG_PATH + '/assets')
# test_path = os.path.join(zukan_pkg_assets, 'Zukan Icon Theme')


class MoveFolder:
    """
    Move folders and remove created folders. Used when installing and removing
    Zukan package.
    """

    def move_folder(name: str):
        """
        Move icons and icons_syntaxes folder if project in folder Installed Packages.

        Parameters:
        name (str) -- folder name.
        """
        try:
            # check if is in Installed Packages, move
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
                # print('Zukan Icon Theme exist in Installed folder.')
                logger.debug('Zukan exist in Installed folder.')
                extract_folder(name, zukan_pkg_assets)
                logger.info('%s folder moved to Packages.', name)
                return name
            else:
                logger.debug('folder %s does not exist in Installed Packages.', name)
        except FileNotFoundError:
            # print_filenotfounderror(name)
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), name
            )
        except OSError:
            # print_oserror(name)
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), name
            )

    def move_folders():
        """
        Move icons and icons_syntaxes folder if project in folder Installed Packages.

        Parameters:
        zukan_folders (str) -- list of folders.
        """
        try:
            zukan_folders = ZUKAN_PKG_FOLDERS
            for folder in zukan_folders:
                MoveFolder.move_folder(folder)
            return zukan_folders
        except FileNotFoundError:
            # print_filenotfounderror('Zukan Icon Theme: icons and/or icons_syntaxes folder.')
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'icons and/or icons_syntaxes folder.',
            )
        except OSError:
            # print_oserror('Zukan Icon Theme: icons and/or icons_syntaxes folder.')
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'icons and/or icons_syntaxes folder.',
            )

    def remove_created_folder(name: str):
        """
        Remove created folder from Zukan Icon Theme installation. Only
        if Zukan installed through Package Control.

        Parameters:
        name (str) -- folder name.
        """
        try:
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH) and (
                os.path.exists(ZUKAN_PKG_ICONS_PATH)
                or os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                # print('Zukan Icon Theme: folder %s exists in Packages' % name)
                logger.debug('folder %s exists in Packages', name)
                # After testing, change to Packages/Zukan Icon Theme
                shutil.rmtree(os.path.join(zukan_pkg_assets, name))
                # print('[!] Zukan Icon Theme: %s deleted.' % os.path.join(zukan_pkg_assets, name))
                logger.info('%s deleted.', os.path.join(zukan_pkg_assets, name))
                return name
            else:
                # print('Zukan Icon Theme: folder does not exist in Packages.')
                logger.info('Zukan folders does not exist in Installed Packages.')
        except FileNotFoundError:
            # print_filenotfounderror('icons and/or icons_syntaxes folder.')
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                name,
            )
        except OSError:
            # print_oserror('icons and/or icons_syntaxes folder.')
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                name,
            )
