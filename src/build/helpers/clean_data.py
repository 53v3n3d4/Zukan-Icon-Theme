import errno
import logging
import os


logger = logging.getLogger(__name__)


def clean_yaml_tabs(filename: str):
    """
    Clean tabs, replace for spaces. Because of error when reading yaml, if tabs used in front of a
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
