import errno
import glob
import os
import shutil
# import sublime

# Most of times only work relaitve path, but it also fails.
# Sometimes absolute path work
# ..utils.zukan_dir_paths
# zukan_icon_theme.utils.zukan_dir_paths
from src.zukan_icon_theme.helpers.search_themes import (
    search_installed_pkgs_themes,
    search_pkgs_themes,
)
from src.zukan_icon_theme.utils.zukan_dir_paths import (
    INSTALLED_PACKAGES_PATH,
    PACKAGES_PATH,
    TEMPLATE_JSON,
    ZUKAN_ICONS_THEMES_PATH,
    ZUKAN_INSTALLED_PKG_PATH,
    ZUKAN_PKG_PATH,
    TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH,
)


installed_themes = search_installed_pkgs_themes()
pkg_themes = search_pkgs_themes()
all_themes = installed_themes + pkg_themes
# print(all_themes)


class ThemeFiles:
    """
    Create, list and remove sublime-themes files in Zukan Icon Theme/icons folder
    """

    def create_theme_file(theme_name):
        """
        Create sublime-theme file with icon_file_type scope. It copy josn template
        to Zukan Icon Theme/icons folder with the theme name.

        Example: Treble Adaptive.sublime-theme

        Parameters:
        theme_name (str) -- installed theme name.
        """
        try:
            # Check if dir Packages/Zukan-Icon-Theme/icons do not exist
            # Check if installed theme file exist.
            if any(theme_name in t for t in all_themes):
                origin = os.path.abspath(TEMPLATE_JSON)
                destiny = os.path.abspath(ZUKAN_PKG_PATH + '/icons/' + theme_name)
                # print(os.path.abspath(ZUKAN_PKG_PATH + '/icons/' + theme_name))
                shutil.copy(origin, destiny)
                print('[!] Creating icon theme: ' + destiny)
            else:
                raise FileNotFoundError(
                    print(
                        'Theme name do not exist. Use menu Command Palette > '
                        'View Package File > theme name.'
                    )
                )
        except FileNotFoundError:
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + theme_name)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + theme_name)

    def create_themes_files():
        """
        Create all sublime-themes files from instaled themes.
        """
        try:
            for theme in all_themes:
                ThemeFiles.create_theme_file(theme)
            return all_themes
        except FileNotFoundError:
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + all_themes)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + all_themes)

    def delete_created_theme_file(theme_name):
        """
        Delete sublime-theme file in Zukan Icon Theme/icons folder.

        Example: Treble Adaptive.sublime-theme

        Parameters:
        theme_name (str) -- installed theme name.
        """
        try:
            theme_file = os.path.abspath(ZUKAN_PKG_PATH + '/icons/' + theme_name)
            os.remove(theme_file)
            print('[!] Deleting icon theme: ' + theme_file)
        except FileNotFoundError:
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + theme_name)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + theme_name)

    def delete_created_themes_files():
        """
        Delete all sublime-themes files in Zukan Icon Theme/icons folder.
        """
        zukan_installed_themes = ThemeFiles.list_created_themes_files()
        # print(zukan_installed_themes)
        try:
            for theme in zukan_installed_themes:
                ThemeFiles.delete_created_theme_file(theme)
            return zukan_installed_themes
        except FileNotFoundError:
            print(
                errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + zukan_installed_themes
            )
        except OSError:
            print(
                errno.EACCES, os.strerror(errno.EACCES), '-> ' + zukan_installed_themes
            )

    def list_created_themes_files():
        """
        List all sublime-themes files in Zukan Icon Theme/icons folder.
        """
        try:
            list_zukan_installed = []
            icons_path = ZUKAN_ICONS_THEMES_PATH
            # icons_path = TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH
            if os.path.exists(icons_path):
                # for files in glob.glob(sublime.packages_path() + '/*/*.sublime-theme'):
                # for files in glob.glob(PACKAGES_PATH + '/*/*/*.sublime-theme'):
                for file in glob.glob(icons_path + '/*.sublime-theme'):
                    list_zukan_installed.append(os.path.basename(file))
                return list_zukan_installed
            else:
                raise FileNotFoundError(print('File or directory do not exist.'))
            return list_zukan_installed
        except FileNotFoundError:
            print(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                '-> Zukan Icon Theme/icons folder ',
            )
        except OSError:
            print(
                errno.EACCES,
                os.strerror(errno.EACCES),
                '-> Zukan Icon Theme/icons folder ',
            )


# file_test = 'notexist.sublime-theme'
file_test = 'Treble Dark.sublime-theme.sublime-theme'
# file_test = 'Treble Dark.sublime-theme'


# print(os.path.abspath(ZUKAN_PKG_PATH + '/icons'))
# print(ThemeFiles.create_theme_file(file_test))
# ThemeFiles.create_themes_files()

# print(ThemeFiles.list_created_themes_files())

# print(ThemeFiles.delete_created_theme_file(file_test))
# print(ThemeFiles.delete_created_themes_files())
