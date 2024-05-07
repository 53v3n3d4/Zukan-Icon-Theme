import errno
import logging
import os

from collections import OrderedDict
from src.build.helpers.color import Color
from src.build.helpers.print_message import print_created_message, print_message
from src.build.helpers.read_write_data import dump_pickle_data, read_yaml_data
from src.build.utils.build_dir_paths import (
    # DATA_PATH,
    ICONS_SYNTAXES_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)

logger = logging.getLogger(__name__)


class ZukanSyntax:
    """
    Create a data file, with all icon syntaxes, to be used by plugin to create
    sublime-syntaxes.
    """

    def write_zukan_data(dir_icon_data: str):
        """
        Create zukan with icons sublime-syntaxes data.

        The file will be saved in folder icons_syntaxes/

        Parameters:
        icon_data (str) -- path to data file.
        """
        try:
            if os.path.exists(ZUKAN_SYNTAXES_DATA_FILE):
                os.remove(ZUKAN_SYNTAXES_DATA_FILE)
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data = os.path.join(dir_icon_data, file_data)
                data = read_yaml_data(icon_data)
                # Check if there is no syntax(list) and if syntax key is not
                # empty.
                if any('syntax' in d for d in data) and data.get('syntax') is not None:
                    for k in data['syntax']:
                        if not os.path.exists(ICONS_SYNTAXES_PATH):
                            os.makedirs(ICONS_SYNTAXES_PATH)
                        # OrderedDict only necessary if using python 3.3
                        # Python 3.8, dict read ordered.
                        ordered_dict = OrderedDict(k)
                        dump_pickle_data(ordered_dict, ZUKAN_SYNTAXES_DATA_FILE)
                        print_created_message(
                            os.path.basename(icon_data),
                            k['name'],
                            'added to zukan data file.',
                        )
                elif icon_data.endswith('.yaml'):
                    print_message(
                        os.path.basename(icon_data),
                        'file does not have any syntax.',
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


# ZukanSyntax.write_zukan_data(DATA_PATH)
