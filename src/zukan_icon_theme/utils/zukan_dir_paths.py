import os


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
    FILEPATH (str) -- script directory + url path.
    """
    if isinstance(url, str):
        FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), url)
        return FILEPATH
    else:
        raise ValueError('Url need to be string.')


# Build paths

ALIASES_PATH = filepath('../../../aliases')
# print('Aliases path is:' + os.path.realpath(ALIASES_PATH))

ASSETS_PATH = filepath('../../../assets')
# print('Assets path is:' + os.path.realpath(ASSETS_PATH))

# DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
DATA_PATH = filepath('../../data')
# print('Data path is:' + os.path.realpath(DATA_PATH))
# print(DATA_PATH)

ICONS_PNG_PATH = filepath('../../../icons')
# print('Icons png path is:' + os.path.realpath(ICONS_PNG_PATH))

ICONS_SVG_PATH = filepath('../../icons')
# print('Icons svg path is:' + os.path.realpath(ICONS_SVG_PATH))

ICONS_SYNTAXES_PATH = filepath('../../../icons_syntaxes')
# print('Icons syntaxes path is:' + os.path.realpath(ICONS_SYNTAXES_PATH))

PREFERENCES_PATH = filepath('../../../preferences')
# print('Preferences path is:' + os.path.realpath(PREFERENCES_PATH))


# Zukan Icon Theme plugin paths

# Read sublime api reference
# https://www.sublimetext.com/docs/api_reference.html
# python modules not present https://www.sublimetext.com/docs/api_environments.html#modules

# print(sublime.find_resources("*.sublime-theme"))
# ZUKAN_PATH = filepath('../../../../Zukan Icon Theme')
ZUKAN_PKG_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme')
# print('Zukan Icon Theme path is:' + os.path.realpath(ZUKAN_PATH))

ZUKAN_ICONS_THEMES_PATH = filepath('../../../icons')
# print('Zukan Icon Theme path is:' + os.path.realpath(ZUKAN_PATH))

ZUKAN_INSTALLED_PKG_PATH = filepath(
    '../../../../../Installed Packages/Zukan-Icon-Theme'
)
# print('Zukan Icon Theme path is:' + os.path.realpath(ZUKAN_PATH))

PACKAGES_PATH = filepath('../../../../../Packages')
# print('Packages path is:' + os.path.realpath(PACKAGES_PATH))

INSTALLED_PACKAGES_PATH = filepath('../../../../../Installed Packages')
# print('Installed Packages path is:' + os.path.realpath(INSTALLED_PACKAGES_PATH))

SUBLIME_PATH = filepath('../../../../../../Sublime Text')
# print('Sublime Text path is:' + os.path.realpath(SUBLIME_PATH))

TEMPLATE_JSON = filepath(
    '../../../../../Packages/Zukan-Icon-Theme/src/zukan_icon_theme/utils/template.json'
)


# Testing only

TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH = filepath('../../../not/icons')
# print('Zukan Icon Theme path is:' + os.path.realpath(ZUKAN_PATH))
