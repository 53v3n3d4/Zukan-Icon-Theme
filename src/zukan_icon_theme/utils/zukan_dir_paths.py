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
    fp (str) -- script directory + url path.
    """
    if isinstance(url, str):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        return fp
    else:
        raise ValueError('Url need to be string.')


# Build paths

ALIASES_PATH = filepath('../../../aliases')

ASSETS_PATH = filepath('../../../assets')

# DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
DATA_PATH = filepath('../../data')
# print('Data path is:' + os.path.realpath(DATA_PATH))
# print(DATA_PATH)

ICONS_PNG_PATH = filepath('../../../icons')

ICONS_SVG_PATH = filepath('../../icons')

ICONS_SYNTAXES_PATH = filepath('../../../icons_syntaxes')

PREFERENCES_PATH = filepath('../../../preferences')

ZUKAN_SYNTAXES_DATA_FILE = filepath('../../../icons_syntaxes/zukan_syntaxes_data.pkl')


# Zukan Icon Theme plugin paths

ZUKAN_INSTALLED_PKG_PATH = filepath(
    '../../../../../Installed Packages/Zukan Icon Theme.sublime-package'
)

ZUKAN_PKG_ICONS_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme/icons')

ZUKAN_PKG_ICONS_SYNTAXES_PATH = filepath(
    '../../../../../Packages/Zukan-Icon-Theme/icons_syntaxes'
)

ZUKAN_PKG_PATH = filepath('../../../../../Packages/Zukan-Icon-Theme')

PACKAGES_PATH = filepath('../../../../../Packages')

INSTALLED_PACKAGES_PATH = filepath('../../../../../Installed Packages')

SUBLIME_PATH = filepath('../../../../../../Sublime Text')

# make path work for 2 cases. Installed Packages and Packages installs.
# or make Installed and Packages same Zukan Icon Theme or Zuka-Icon-Theme name
TEMPLATE_JSON = filepath(
    '../../../../../Packages/Zukan-Icon-Theme/src/zukan_icon_theme/utils/template.json'
)

TEMPLATE_JSON_WITH_OPACITY = filepath(
    '../../../../../Packages/Zukan-Icon-Theme/src/zukan_icon_theme/utils/template-with-opacity.json'
)


# Testing only

TEST_NOT_EXIST_ZUKAN_ICONS_THEMES_PATH = filepath('../../../not/icons')
