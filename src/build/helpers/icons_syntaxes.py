import errno
import logging
import os

from src.build.helpers.color import Color
from src.build.helpers.print_message import print_created_message, print_message
from src.build.helpers.read_write_data import dump_yaml_data, read_yaml_data
from src.build.utils.file_extensions import SUBLIME_SYNTAX_EXTENSION

logger = logging.getLogger(__name__)


class IconSyntax:
    """
    Sublime Text need an icon sublime-syntax file to show icon beside a file.
    """

    def icon_syntax(icon_data: str, dir_destiny: str):
        """
        Create icon sublime-syntax file.

        The file name will be name of icon stored in file data, Preferences >
        Settings > Icon. Info is stored in src/data directory.

        It will be also the name of png and tmPreferences generated.

        Parameters:
        icon_data (str) -- path to data file.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            data = read_yaml_data(icon_data)
            # print(isinstance(data, dict))
            # print(icon_data)
            # Check if there is no syntax(list) and if syntax key is not
            # empty.
            if any('syntax' in d for d in data) and data.get('syntax') is not None:
                for k in data['syntax']:
                    # print(k['name'])
                    iconsyntax = f'{ k["name"] }{ SUBLIME_SYNTAX_EXTENSION }'
                    if not os.path.exists(dir_destiny):
                        os.makedirs(dir_destiny)
                    iconsyntax_path = os.path.join(dir_destiny, iconsyntax)
                    dump_yaml_data(k, iconsyntax_path)
                    print_created_message(
                        os.path.basename(icon_data),
                        iconsyntax,
                        'created.',
                    )
            elif icon_data.endswith('.yaml'):
                print_message(
                    os.path.basename(icon_data),
                    'file does not have any syntax.',
                    color=f'{ Color.GREEN }',
                    color_end=f'{ Color.END }',
                )
                return data
            else:
                return icon_data
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), icon_data
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), icon_data
            )

    def icons_syntaxes(dir_icon_data: str, dir_destiny: str):
        """
        Generate all icons sublime-syntax files from data files.

        Parameters:
        dir_icon_data (str) -- path to directory with data files.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                IconSyntax.icon_syntax(icon_data_path, dir_destiny)
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
