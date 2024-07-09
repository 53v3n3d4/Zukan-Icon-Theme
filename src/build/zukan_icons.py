import errno
import logging
import os

from src.build.helpers.color import Color
from src.build.helpers.nested_ordered_dict import nested_ordered_dict
from src.build.helpers.print_message import print_created_message, print_message
from src.build.helpers.read_write_data import (
    dump_pickle_data,
    read_yaml_data,
)
from src.build.utils.icons_no_syntax import (
    ICONS_NO_SYNTAX,
)

logger = logging.getLogger(__name__)


class ZukanIcon:
    """
    Create an icons data file to be used by plugin to create syntax and preferences
    files.
    """

    def write_icon_data(dir_icon_data: str, dir_destiny: str, pickle_file: str):
        """
        Create zukan with icons data.

        The file will be saved in folder icons.

        Parameters:
        dir_icon_data (str) -- path to directory with data files.
        dir_destiny (str) -- path destination of icon data files.
        pickle_file (str) -- path to zukan icons data file.
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
                    (
                        any('preferences' in d for d in data)
                        and data['preferences']['settings'].get('icon') is not None
                        and data['preferences'].get('scope') is not None
                    )
                    and (
                        any('syntax' in d for d in data)
                        and data.get('syntax') is not None
                    )
                    or (file_data in ICONS_NO_SYNTAX)
                ):
                    if not os.path.exists(dir_destiny):
                        os.makedirs(dir_destiny)
                    # OrderedDict only necessary if using python 3.3.
                    # Python 3.8, dict read ordered.
                    # ordered_dict = OrderedDict(data)
                    ordered_dict = nested_ordered_dict(data)
                    dump_pickle_data(ordered_dict, pickle_file)
                    print_created_message(
                        os.path.basename(icon_data),
                        data['name'],
                        'added to zukan icons data file.',
                    )
                elif icon_data.endswith('.yaml'):
                    print_message(
                        os.path.basename(icon_data),
                        'File does not have any syntax, preferences, scope and icon.'
                        ' Exception for ST icons default.',
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
