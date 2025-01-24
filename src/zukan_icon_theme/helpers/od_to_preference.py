import errno
import logging
import os

from collections import OrderedDict

logger = logging.getLogger(__name__)


def save_tm_preferences(data: dict, file_path):
    """
    Write tmPreferences file.

    Parameters:
    data (dict) -- tmPreferences ordered dict.
    file_path (str) -- path to directory where tmPreferences will be saved.
    """
    content = build_preference(data)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )


def build_preference(data: dict) -> str:
    """
    Build tmPreferences string with plist version.

    Parameters:
    data (dict) -- tmPreferences ordered dict.

    Returns:
    content_with_plist_version (str) -- tmPreferences string with plist version.
    """
    content = od_to_preference(data)

    # Add plist version
    content_with_plist_version = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<plist version="1.0">\n\t<dict>\n'
        + content
        + '\t</dict>\n</plist>\n'
    )

    return content_with_plist_version


def od_to_preference(preference_od: dict, multiplier: int = 2) -> str:
    """
    Convert tmPreferences ordered dict to string.

    Parameters:
    preference_od (dict) -- tmPreferences ordered dict.
    multiplier (int) -- indentation multiplier.

    Returns:
    data (str) -- tmPreferences string.
    """
    indent = '\t' * multiplier
    data = ''

    for k, v in preference_od.items():
        if isinstance(v, OrderedDict):
            data += '{i}<key>{k}</key>\n'.format(i=indent, k=k)
            data += '{i}<dict>\n'.format(i=indent)
            data += od_to_preference(v, multiplier + 1)
            data += '{i}</dict>\n'.format(i=indent)
        else:
            data += '{i}<key>{k}</key>\n'.format(i=indent, k=k)
            data += '{i}<string>{v}</string>\n'.format(i=indent, v=v)

    return data
