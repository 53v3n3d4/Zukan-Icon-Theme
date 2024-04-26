import os


def filepath(url: str) -> str:
    """
    Get the relative path to script directory.
    Paths are relative to the working directory.
    Script diretory is
        .../Sublime Text/Packages/Zukan-Icon-Theme/src/build/utils
    If installed trough packagecontrol.io, instead of Packages, folder is
    Installed Packages.

    Parameters:
    url (str) -- destination path.

    Returns:
    filepath (str) -- script directory + url path.
    """
    if isinstance(url, str):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), url)
        return filepath
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


# Testing paths

ICON_THEME_TEST_PATH = filepath('../../../tests_icon_theme')

ICONS_PNG_TEST_PATH = filepath('../../icons_png_test')

ICONS_TEST_PATH = filepath('../../icons_test')

ICONS_TEST_NOT_EXIST_PATH = filepath('../../icons_test_not_exist')

ICONS_SYNTAXES_TEST_PATH = filepath('../../icons_syntaxes_test')

PREFERENCES_TEST_PATH = filepath('../../preferences_test')
