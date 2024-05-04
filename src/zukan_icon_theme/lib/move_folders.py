import os
import shutil

from ..helpers.print_message import print_filenotfounderror, print_oserror
from ..utils.zukan_dir_paths import (
    # INSTALLED_PACKAGES_PATH,
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_PATH,
)
from ..utils.zukan_pkg_folders import zukan_pkg_folders
from zipfile import ZipFile


# Testing path
zukan_pkg_assets = os.path.join(ZUKAN_PKG_PATH + '/assets')


# icons_folder = 'icons/'
icons_folder = 'Zukan Icon Theme/icons/'
icons_syntaxes_folder = 'Zukan Icon Theme/icons_syntaxes/'

test_path = os.path.join(zukan_pkg_assets, 'Zukan Icon Theme')


def dir_exist(z, name):
    return any(
        file_in_zip.startswith('{n}'.format(n=name.rstrip('/')))
        for file_in_zip in z.namelist()
    )


def extract_folder(name):
    # with ZipFile(package_control_installed_pkg, 'r') as zf:
    with ZipFile(ZUKAN_INSTALLED_PKG_PATH, 'r') as zf:
        if dir_exist(zf, name):
            print('Moving {n} folder to {d}'.format(n=name, d=zukan_pkg_assets))
            for file_in_zip in zf.namelist():
                if file_in_zip.startswith(name):
                    zf.extract(file_in_zip, zukan_pkg_assets)
        else:
            raise FileNotFoundError(
                print(
                    'Folder {n} does not exist in {p}.'.format(
                        n=name, p=ZUKAN_INSTALLED_PKG_PATH
                    )
                )
            )


# extract_folder(messages_folder)
# extract_folder(icons_folder)
# extract_folder(icons_syntaxes_folder)


class MoveFolder:
    """
    Move folders and remove created folders. Used when installing and removing
    Zukan package.
    """

    def move_folder(name):
        """
        Move icons and icons_syntaxes folder if project in folder Installed Packages.

        Parameters:
        name (str) -- folder name.
        """
        try:
            # check if is in Installed Packages, move
            if os.path.exists(ZUKAN_INSTALLED_PKG_PATH):
                print('Zukan exist in Installed folder.')
                extract_folder(name)
                return name
            else:
                raise FileNotFoundError(
                    print('Folder %s does not exist in Installed Packages.' % name)
                )
        except FileNotFoundError:
            print_filenotfounderror(name)
        except OSError:
            print_oserror(name)

    def move_folders(zukan_folders):
        """
        Move icons and icons_syntaxes folder if project in folder Installed Packages.

        Parameters:
        zukan_folders (str) -- list of folders.
        """
        try:
            for folder in zukan_folders:
                MoveFolder.move_folder(folder)
            return zukan_folders
        except FileNotFoundError:
            print_filenotfounderror('icons and/or icons_syntaxes folder.')
        except OSError:
            print_oserror('icons and/or icons_syntaxes folder.')

    def remove_created_folder(name):
        """
        Remove created folder from Zukan Icon Theme installation.

        Parameters:
        name (str) -- folder name.
        """
        try:
            if os.path.exists(ZUKAN_PKG_ICONS_PATH) or os.path.exists(
                ZUKAN_PKG_ICONS_SYNTAXES_PATH
            ):
                print('Folder %s exists in Packages' % name)
                # After testing, change to Packages/Zukan Icon Theme
                shutil.rmtree(os.path.join(zukan_pkg_assets, name))
                print('%s deleted.' % os.path.join(zukan_pkg_assets, name))
                return name
            else:
                print('Folder does not exist in Packages.')
        except FileNotFoundError:
            print_filenotfounderror('icons and/or icons_syntaxes folder.')
        except OSError:
            print_oserror('icons and/or icons_syntaxes folder.')


# MoveFolder.move_folder(icons_folder)
# MoveFolder.move_folders(zukan_pkg_folders)

# print(MoveFolder.remove_created_folder(icons_folder))
# MoveFolder.remove_created_folder(test_path)
