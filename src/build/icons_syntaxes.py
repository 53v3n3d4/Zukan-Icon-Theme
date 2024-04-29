import errno
import os

from src.build.helpers.color import Color
from src.build.helpers.print_message import print_created_message, print_message
from src.build.helpers.read_write_data import dump_yaml_data, read_yaml_data

# from src.build.utils.build_dir_paths import DATA_PATH, ICONS_SYNTAXES_TEST_PATH
from src.build.utils.file_extensions import SYNTAX_EXTENSION

# file_test = os.path.join(DATA_PATH, 'test_empty_file.yaml')
# file_test = os.path.join(DATA_PATH, 'afpub.yaml')
# file_test = os.path.join(DATA_PATH, 'css.yaml') # does not have syntax
# file_test = os.path.join(DATA_PATH, 'afpub_not_exist.yaml')


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
                    iconsyntax = f'{ k["name"] }{ SYNTAX_EXTENSION }'
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
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + icon_data)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + icon_data)

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
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + dir_icon_data)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + dir_icon_data)


# IconSyntax.icon_syntax(file_test, ICONS_SYNTAXES_TEST_PATH)
# IconSyntax.icons_syntaxes(DATA_PATH, ICONS_SYNTAXES_TEST_PATH)
