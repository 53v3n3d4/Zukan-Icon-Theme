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
    fp (str) -- script directory + url path.
    """
    if isinstance(url, str):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        return fp
    else:
        raise ValueError('Url need to be string.')


# Dir paths

ASSETS_PATH = filepath('../../../assets')

DATA_PATH = filepath('../../data')

ICONS_DATA_PATH = filepath('../../../icons_data')

ICONS_DATA_PRIMARY_ICONS_PATH = filepath('../../../icons_data/primary_icons')

ICONS_PNG_PATH = filepath('../../../icons')

ICONS_SVG_PATH = filepath('../../icons')

ICONS_SYNTAXES_PATH = filepath('../../../icons_syntaxes')

ICONS_PREFERENCES_PATH = filepath('../../../icons_preferences')


# File paths


CONCAT_SVGS_FILE = filepath('../../../assets/file-icons-concat.svg')

CONCAT_SVGS_FILE_SAMPLE = filepath('../../../assets/file-icons-concat-sample.svg')

ZUKAN_ICONS_DATA_FILE = filepath('../../../icons_data/zukan_icons_data.pkl')

# ZUKAN_PREFERENCES_DATA_FILE = filepath(
#     '../../../icons_preferences/zukan_preferences_data.pkl'
# )

# ZUKAN_SYNTAXES_DATA_FILE = filepath('../../../icons_syntaxes/zukan_syntaxes_data.pkl')

# Testing paths

ICON_THEME_TEST_PATH = filepath('../../../tests_icon_theme')

ICONS_PNG_TEST_PATH = filepath('../../icons_png_test')

ICONS_TEST_PATH = filepath('../../icons_test')

ICONS_TEST_NOT_EXIST_PATH = filepath('../../icons_test_not_exist')

ICONS_SYNTAXES_TEST_PATH = filepath('../../icons_syntaxes_test')

PREFERENCES_TEST_PATH = filepath('../../preferences_test')
