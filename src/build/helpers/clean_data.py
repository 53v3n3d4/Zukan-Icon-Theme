import errno
import os

from src.build.utils.plist_unused_line import UNUSED_LINE


def clean_plist_tag(file: str):
    """
    Clean tag <!DOCTYPE plist>. It is generated after plistlib dump.

    Parameters:
    file (str) -- path to icon tmPreferences file
    """
    try:
        with open(file, 'r+') as f:
            clean_file = f.read()
            clean_file = _replace_line(clean_file)
        with open(file, 'w') as f:
            f.write(clean_file)
    except FileNotFoundError:
        print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + file)
    except OSError:
        print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + file)


def _replace_line(file_info: str) -> str:
    """
    Remove unwanted line from tmPreference file.

    Parameters:
    file_info (str) -- info of data file.

    Returns:
    str -- text with line removed if found.
    """
    return file_info.replace(UNUSED_LINE, '')


def clean_yaml_tabs(file: str):
    """
    Clean tabs to spaces. Reading error if tabs used in front of dict key.

    Parameters:
    file (str) -- path to icon data file
    """
    try:
        with open(file, 'r+') as f:
            clean_file = f.read()
            clean_file = _replace_tabs(clean_file)
            # print(clean_file)
        with open(file, 'w') as f:
            f.write(clean_file)
    except FileNotFoundError:
        print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + file)
    except OSError:
        print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + file)


def _replace_tabs(file_info: str) -> str:
    """
    Replace tabs for double spaces.

    Parameters:
    file (str) -- info of data file.

    Returns:
    str -- text with tabs converted to double spaces if found.
    """
    return file_info.replace('\t', '  ')
