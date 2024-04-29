import errno
import os

from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_created_message,
    print_message,
)
from src.build.helpers.read_write_data import read_yaml_data
# from src.build.utils.build_dir_paths import DATA_PATH, ICON_THEME_TEST_PATH

# file_test = os.path.join(DATA_PATH, 'afpub.yaml')
# file_test = os.path.join(DATA_PATH, 'nodejs.yaml')


class TestIconTheme:
    """
    Test file extensions in data files.
    """

    def create_icon_file(icon_data: str, dir_destiny: str):
        """
        Create test file extension for a icon theme.

        Parameters:
        icon_data (str) -- path to data file.
        dir_destiny (str) -- path destination of test extensions files.
        """
        try:
            data = read_yaml_data(icon_data)
            if any('syntax' in d for d in data) and data.get('syntax') is not None:
                for k in data['syntax']:
                    # print(k['file_extensions'])
                    for e in k['file_extensions']:
                        # print(e)
                        if e.startswith('.'):
                            test_file = f'{ e }'
                            # print(test_file)
                        else:
                            test_file = f'{ e }.{ e }'
                            # print(test_file)
                        if not os.path.exists(dir_destiny):
                            os.makedirs(dir_destiny)
                        test_file_path = os.path.join(dir_destiny, test_file)
                        with open(test_file_path, 'w'):
                            pass
                        print_created_message(
                            os.path.basename(icon_data),
                            e,
                            'created.',
                        )
            elif icon_data.endswith('.yaml'):
                print_message(
                    os.path.basename(icon_data),
                    'yaml file does not have any file extension key or value.',
                    color=f'{ Color.GREEN }',
                    color_end=f'{ Color.END }',
                )
            else:
                return icon_data
        except FileNotFoundError:
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + icon_data)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + icon_data)

    def create_icons_files(dir_icon_data: str, dir_destiny: str):
        """
        Generate all test files extensions in data files.

        Parameters:
        dir_icon_data (str) -- path to directory with data files.
        dir_destiny (str) -- path destination of test extensions files.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                TestIconTheme.create_icon_file(icon_data_path, dir_destiny)
            return files_in_dir
        except FileNotFoundError:
            print(errno.ENOENT, os.strerror(errno.ENOENT), '-> ' + dir_icon_data)
        except OSError:
            print(errno.EACCES, os.strerror(errno.EACCES), '-> ' + dir_icon_data)


# TestIconTheme.create_icon_file(file_test, ICON_THEME_TEST_PATH)
# TestIconTheme.create_icons_files(DATA_PATH, ICON_THEME_TEST_PATH)