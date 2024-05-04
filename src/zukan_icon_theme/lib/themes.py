import glob
import os
import shutil

from ..helpers.print_message import print_filenotfounderror, print_oserror
from ..helpers.search_themes import (
    search_resources_sublime_themes,
    # search_installed_pkgs_themes,
    # search_pkgs_themes,
)
from ..utils.zukan_dir_paths import (
    TEMPLATE_JSON,
    ZUKAN_ICONS_THEMES_PATH,
    TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH,
)


# installed_themes = search_installed_pkgs_themes()
# pkg_themes = search_pkgs_themes()
# all_themes = installed_themes + pkg_themes
all_themes = search_resources_sublime_themes()
# print(all_themes)


class ThemeFile:
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
                origin = TEMPLATE_JSON
                destiny = os.path.join(ZUKAN_ICONS_THEMES_PATH, theme_name)
                # print(ZUKAN_ICONS_THEMES_PATH + theme_name)
                shutil.copy(origin, destiny)
                print('[!] Creating icon theme: %s' % destiny)
                return theme_name
            else:
                raise FileNotFoundError(
                    print(
                        'Theme name does not exist. Use menu Command Palette > '
                        'View Package File > theme name.'
                    )
                )
        except FileNotFoundError:
            print_filenotfounderror(theme_name)
        except OSError:
            print_oserror(theme_name)

    def create_themes_files():
        """
        Create all sublime-themes files from instaled themes.
        """
        try:
            if all_themes is not None:
                for theme in all_themes:
                    # print(all_themes)
                    ThemeFile.create_theme_file(theme)
                return all_themes
            else:
                raise FileNotFoundError(print('List is empty.'))
        except FileNotFoundError:
            print_filenotfounderror(all_themes)
        except OSError:
            print_oserror(all_themes)

    def delete_created_theme_file(theme_name):
        """
        Delete sublime-theme file in Zukan Icon Theme/icons folder.

        Example: Treble Adaptive.sublime-theme

        Parameters:
        theme_name (str) -- installed theme name.
        """
        try:
            theme_file = os.path.join(ZUKAN_ICONS_THEMES_PATH, theme_name)
            os.remove(theme_file)
            print('[!] Deleting icon theme: %s' % theme_file)
            return theme_name
        except FileNotFoundError:
            print_filenotfounderror(theme_name)
        except OSError:
            print_oserror(theme_name)

    def delete_created_themes_files():
        """
        Delete all sublime-themes files in Zukan Icon Theme/icons folder.
        """
        zukan_installed_themes = ThemeFile.list_created_themes_files()
        # print(zukan_installed_themes)
        try:
            for theme in zukan_installed_themes:
                ThemeFile.delete_created_theme_file(theme)
            return zukan_installed_themes
        except FileNotFoundError:
            print_filenotfounderror(zukan_installed_themes)
        except OSError:
            print_oserror(zukan_installed_themes)

    def list_created_themes_files():
        """
        List all sublime-themes files in Zukan Icon Theme/icons folder.

        Returns:
        list_zukan_installed (list) -- list of sublime-themes in folder icons/.
        """
        try:
            list_zukan_installed = []
            icons_path = ZUKAN_ICONS_THEMES_PATH
            # icons_path = TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH
            if os.path.exists(icons_path):
                for file in glob.glob(icons_path + '/*.sublime-theme'):
                    list_zukan_installed.append(os.path.basename(file))
                return list_zukan_installed
            else:
                raise FileNotFoundError(print('File or directory do not exist.'))
            return list_zukan_installed
        except FileNotFoundError:
            print_filenotfounderror('Zukan Icon Theme/icons folder')
        except OSError:
            print_oserror('Zukan Icon Theme/icons folder')


# file_test = 'notexist.sublime-theme'
file_test = 'Treble Dark.sublime-theme.sublime-theme'
# file_test = 'Treble Dark.sublime-theme'


# ThemeFile.create_theme_file(file_test)
# ThemeFile.create_themes_files()

# print(ThemeFile.list_created_themes_files())

# print(ThemeFile.delete_created_theme_file(file_test))
# print(ThemeFile.delete_created_themes_files())
