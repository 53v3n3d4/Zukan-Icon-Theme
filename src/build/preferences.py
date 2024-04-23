import os

from src.build.helpers.color import Color
from src.build.helpers.read_write_data import clean_tag, dump_plist_data, read_yaml_data
from src.build.utils.build_dir_paths import (
    DATA_PATH,
    ICONS_TEST_NOT_EXIST_PATH,
    PREFERENCES_TEST_PATH,
)
from src.build.utils.file_extensions import PLIST_EXTENSION
from src.build.utils.plist_unused_line import UNUSED_LINE

# file_test = os.path.join(DATA_PATH, 'test_empty_file.yaml')
# file_test = os.path.join(DATA_PATH, 'afpub.yaml')
file_test = os.path.join(DATA_PATH, 'test_no_icon_file.yaml')
# file_test = os.path.join(DATA_PATH, 'afpub_not_exist.yaml')
# file_test = os.path.join(DATA_PATH, 'afpub_not_yaml.toml')


class Preference:
    """
    Sublime Text need a tmPreferences file to show icon beside a file.
    """

    def preferences(icon_data: str, dir_destiny: str):
        """
        Generate icon tmPreferences file.

        The file name will be name of icon stored in file data, Preferences >
        Settings > Icon. Info is stored in src/data directory.

        It will be also the name of png and sublime-syntax generated.


        Parameters:
        icon_data(str) -- path to data file.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            if icon_data.endswith('.yaml') and os.path.exists(icon_data):
                data = read_yaml_data(icon_data)
                if data is None:
                    print(
                        f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                        f'{ Color.END } yaml file is empty.'
                    )
                # Check if dict preferences exist and if icon key exist with
                # value not empty.
                elif (
                    any('preferences' in d for d in data)
                    and data['preferences']['settings'].get('icon') is not None
                ):
                    # print(isinstance(data, dict))
                    iconpreferences = (
                        f'{ data["preferences"]["settings"]["icon"] }'
                        f'{ PLIST_EXTENSION }'
                    )
                    # print(iconpreferences)
                    if not os.path.exists(dir_destiny):
                        os.makedirs(dir_destiny)
                    iconpreferences_path = os.path.join(dir_destiny, iconpreferences)
                    preferences_dict = data['preferences']
                    # print(preferences_dict)
                    # Write plist, tmPreferences file
                    dump_plist_data(
                        iconpreferences_path,
                        preferences_dict,
                        icon_data,
                        iconpreferences,
                    )
                    # Clean tag <!DOCTYPE plist>. It will always exist after dump.
                    clean_tag(iconpreferences_path)
                    print(
                        f'{ Color.CYAN }[!] { os.path.basename(icon_data) }'
                        f'{ Color.END } -> Deleting { Color.YELLOW }tag <!DOCTYPE '
                        f'plist>{ Color.END } from { iconpreferences }.'
                    )
                else:
                    print(
                        f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                        f'{ Color.END } key preferences, scope and icon are required.'
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

    def preferences_all(dir_icon_data: str, dir_destiny: str):
        """
        Create all icons tmPreferences files from data files.

        Parameters:
        dir_icon_data(str) -- path to directory with data files.
        dir_destiny (str) -- path destination of icon sublime-synthax files.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                Preference.preferences(icon_data_path, dir_destiny)
            return files_in_dir
        except FileNotFoundError as error:
            # log here
            print(error.args, 'Icons error')


# Preference.preferences(file_test, PREFERENCES_TEST_PATH)
# Preference.preferences_all(DATA_PATH, PREFERENCES_TEST_PATH)
