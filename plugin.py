import os
import sublime
import sublime_plugin
import sys

from .src.zukan_icon_theme.lib.icons_syntaxes import ZukanSyntax
from .src.zukan_icon_theme.lib.move_folders import MoveFolder
from .src.zukan_icon_theme.lib.themes import ThemeFile
from .src.zukan_icon_theme.utils.zukan_dir_paths import (
    ZUKAN_PKG_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)
from .src.zukan_icon_theme.utils.zukan_pkg_folders import zukan_pkg_folders


# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules


# From A File Icon https://github.com/SublimeText/AFileIcon/blob/master/plugin.py
# Clear module cache to force reloading all modules of this package.
prefix = __package__ + '.'  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
del prefix

# This sometimes raise errors
# sublime_plugin.reload_plugin(module_name)


zukan_pkg_assets = os.path.join(ZUKAN_PKG_PATH + '/assets')
test_path = os.path.join(zukan_pkg_assets, 'Zukan Icon Theme')


# def plugin_loaded():
#     ThemeFile.create_themes_files()
#     MoveFolder.move_folders(zukan_pkg_folders)
#     # Create icons sublime-syntaxes
#     ZukanSyntax.create_icons_syntaxes()


# def plugin_unloaded():
#     # delete created themes not needed. Remove created folder would remove
#     # Packages/Zukan Icon Theme directory
#     # ThemeFile.delete_created_themes_files()
#     MoveFolder.remove_created_folder(test_path)
