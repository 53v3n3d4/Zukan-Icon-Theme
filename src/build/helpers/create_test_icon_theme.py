import os

from src.build.helpers.clean_data import clean_yaml_tabs
from src.build.helpers.color import Color
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
        # YAML
        try:
            # test line below in read_writer_data
            if icon_data.endswith('.yaml') and os.path.exists(icon_data):
                data = clean_yaml_tabs(icon_data)
                data = read_yaml_data(icon_data)
                if data is None:
                    print(
                        f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                        f'{ Color.END } yaml file is empty.'
                    )
                elif (
                    any('syntax' in d for d in data) and data.get('syntax') is not None
                ):
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
                            print(
                                f'{ Color.CYAN }[!] { os.path.basename(icon_data) }'
                                f'{ Color.END } -> { Color.YELLOW }{ e }'
                                f'{ Color.END } created.'
                            )
                else:
                    print(
                        f'{ Color.GREEN }[!] { os.path.basename(icon_data) }: '
                        f'{ Color.END }file does not have any file extension.'
                    )
            elif not icon_data.endswith('.yaml'):
                print(
                    f'{ Color.PURPLE }[!] { os.path.basename(icon_data) }'
                    f'{ Color.END }: file extension is not yaml.'
                )
            else:
                raise ValueError('Yaml file does not exist.')
        except FileNotFoundError as error:
            # log here
            print(error.args)

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
        except FileNotFoundError as error:
            # log here
            print(error.args)


# TestIconTheme.create_icon_file(file_test, ICON_THEME_TEST_PATH)
# TestIconTheme.create_icons_files(DATA_PATH, ICON_THEME_TEST_PATH)
