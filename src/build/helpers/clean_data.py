import errno
import logging
import os

from src.build.utils.plist_unused_line import UNUSED_LINE

logger = logging.getLogger(__name__)


def clean_plist_tag(filename: str):
    """
    Clean tag <!DOCTYPE plist>. It is generated after plistlib dump.

    Parameters:
    filename (str) -- path to icon tmPreferences file
    """
    try:
        with open(filename, 'r+') as f:
            clean_file = f.read()
            clean_file = _replace_line(clean_file)
        with open(filename, 'w') as f:
            f.write(clean_file)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
        )


def _replace_line(file_info: str) -> str:
    """
    Remove unwanted line from tmPreference file.

    Parameters:
    file_info (str) -- info of data file.

    Returns:
    str -- text with line removed if found.
    """
    return file_info.replace(UNUSED_LINE, '')


def clean_yaml_tabs(filename: str):
    """
    Clean tabs, replace for spaces. Reading yaml error if tabs used in front of a
    dict key.

    Parameters:
    filename (str) -- path to icon data file
    """
    try:
        with open(filename, 'r+') as f:
            clean_file = f.read()
            clean_file = _replace_tabs(clean_file)
            # print(clean_file)
        with open(filename, 'w') as f:
            f.write(clean_file)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
        )


def _replace_tabs(file_info: str) -> str:
    """
    Replace tabs for double spaces.

    Parameters:
    file (str) -- info of data file.

    Returns:
    str -- text with tabs converted to double spaces if found.
    """
    return file_info.replace('\t', '  ')
