import os
import sublime


def filepath(url: str) -> str:
    """
    Get the relative path to script directory.
    Paths are relative to the working directory.
    Script diretory is
        .../Sublime Text/Packages/Zukan-Icon-Theme/src/zukan_icon_theme/utils
    If installed trough packagecontrol.io, instead of Packages, folder is
    Installed Packages.

    Parameters:
    url (str) -- destination path.

    Returns:
    fp (str) -- script directory + url path.
    """
    if isinstance(url, str):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        return fp
    else:
        raise ValueError('Url need to be string.')


# ZUKAN_SYNTAXES_DATA_FILE = filepath('../../../icons_syntaxes/zukan_syntaxes_data.pkl')
ZUKAN_SYNTAXES_DATA_FILE = os.path.join(
    sublime.packages_path(),
    'Zukan-Icon-Theme',
    'icons_syntaxes',
    'zukan_syntaxes_data.pkl',
)

# ZUKAN_INSTALLED_PKG_PATH = filepath(
#     '../../../../../Installed Packages/Zukan Icon Theme.sublime-package'
# )
ZUKAN_INSTALLED_PKG_PATH = os.path.join(
    sublime.installed_packages_path(), 'Zukan-Icon-Theme.sublime-package'
)

# ZUKAN_PKG_ICONS_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme/icons')
ZUKAN_PKG_ICONS_PATH = os.path.join(
    sublime.packages_path(), 'Zukan-Icon-Theme', 'icons'
)

# ZUKAN_PKG_ICONS_SYNTAXES_PATH = filepath(
#     '../../../../../Packages/Zukan-Icon-Theme/icons_syntaxes'
# )
ZUKAN_PKG_ICONS_SYNTAXES_PATH = os.path.join(
    sublime.packages_path(), 'Zukan-Icon-Theme', 'icons_syntaxes'
)

# ZUKAN_PKG_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme')
ZUKAN_PKG_PATH = os.path.join(sublime.packages_path(), 'Zukan-Icon-Theme')

# Testing only

# TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH = filepath('../../../not/icons')
