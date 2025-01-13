import errno
import logging
import os

from src.build.helpers.clean_data import clean_plist_tag
from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_created_message,
    print_message,
    print_remove_tag,
)
from src.build.helpers.read_write_data import dump_plist_data, read_yaml_data
from src.build.utils.file_extensions import TMPREFERENCES_EXTENSION

logger = logging.getLogger(__name__)


class Preference:
    """
    Sublime Text need a tmPreferences file to show icon beside a file.
    """

    def preferences(self, icon_data: str, dir_destiny: str):
        """
        Generate icon tmPreferences file.

        The file name will be name of icon stored in file data, Preferences >
        Settings > Icon. Info is stored in src/data directory.

        It will be also the name of png and sublime-syntax generated.


        Parameters:
        icon_data (str) -- path to data file.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            data = read_yaml_data(icon_data)
            # Check if dict preferences exist and if icon key exist with
            # value not empty.
            if (
                any('preferences' in d for d in data)
                and data['preferences']['settings'].get('icon') is not None
                and data['preferences'].get('scope') is not None
            ):
                # print(isinstance(data, dict))
                # print(data)
                iconpreferences = (
                    f'{data["preferences"]["settings"]["icon"]}'
                    f'{TMPREFERENCES_EXTENSION}'
                )
                # print(iconpreferences)
                if not os.path.exists(dir_destiny):
                    os.makedirs(dir_destiny)
                iconpreferences_path = os.path.join(dir_destiny, iconpreferences)
                preferences_dict = data['preferences']
                # print(preferences_dict)
                # Write plist, tmPreferences file
                dump_plist_data(
                    preferences_dict,
                    iconpreferences_path,
                )
                print_created_message(
                    os.path.basename(icon_data),
                    iconpreferences,
                    'created.',
                )
                # Clean tag <!DOCTYPE plist>. It will always exist after dump.
                clean_plist_tag(iconpreferences_path)
                print_remove_tag(os.path.basename(icon_data), iconpreferences)
            elif icon_data.endswith('.yaml'):
                print_message(
                    os.path.basename(icon_data),
                    'keys preferences, scope and icon, are essentials. Exception for '
                    'ST icons default.',
                    color=f'{Color.RED}',
                    color_end=f'{Color.END}',
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

    def preferences_all(self, dir_icon_data: str, dir_destiny: str):
        """
        Create all icons tmPreferences files from data files.

        Parameters:
        dir_icon_data (str) -- path to directory with data files.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                self.preferences(icon_data_path, dir_destiny)
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
