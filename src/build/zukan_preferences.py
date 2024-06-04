import errno
import logging
import os
from collections import OrderedDict

from src.build.helpers.color import Color
from src.build.helpers.print_message import print_created_message, print_message
from src.build.helpers.read_write_data import (
    dump_pickle_data,
    read_yaml_data,
)

logger = logging.getLogger(__name__)


class ZukanPreference:
    """
    Create a data file, with all icon preferences, to be used by plugin to create
    tmPreferences.
    """

    def write_preference_data(dir_icon_data: str, dir_destiny: str, pickle_file: str):
        """
        Create zukan with icons tmPreferences data.

        The file will be saved in folder preferences.

        Parameters:
        dir_icon_data (str) -- path to directory with data files.
        dir_destiny (str) -- path destination of icon temPreferences files.
        pickle_file (str) -- path to zukan preferences data file.
        """
        try:
            if os.path.exists(pickle_file):
                os.remove(pickle_file)
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data = os.path.join(dir_icon_data, file_data)
                data = read_yaml_data(icon_data)
                # Check if dict preferences exist and if icon key exist with
                # value not empty.
                if (
                    any('preferences' in d for d in data)
                    and data['preferences']['settings'].get('icon') is not None
                    and data['preferences'].get('scope') is not None
                ):
                    preferences_name = data['preferences']['settings']['icon']
                    if not os.path.exists(dir_destiny):
                        os.makedirs(dir_destiny)
                    # OrderedDict only necessary if using python 3.3.
                    # Python 3.8, dict read ordered.
                    ordered_dict = OrderedDict(data['preferences'])
                    dump_pickle_data(ordered_dict, pickle_file)
                    print_created_message(
                        os.path.basename(icon_data),
                        preferences_name,
                        'added to zukan preferences data file.',
                    )
                elif icon_data.endswith('.yaml'):
                    print_message(
                        os.path.basename(icon_data),
                        'keys preferences, scope and icon, are essentials. Exception for '
                        'ST icons default.',
                        color=f'{ Color.GREEN }',
                        color_end=f'{ Color.END }',
                    )
            return files_in_dir
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                dir_icon_data,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                dir_icon_data,
            )
