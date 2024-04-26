import os
import plistlib

from ruamel.yaml import YAML
from src.build.helpers.clean_data import clean_yaml_tabs
from src.build.helpers.color import Color
from src.build.helpers.print_message import print_message


def read_yaml_data(yaml_file: str) -> dict:
    """
    YAML reader.

    Read data to generate png icons, icons_syntaxes and preferences.

    Paramenters:
    yaml_file (str) -- path to yaml file

    Returns:
    file_data (dict) -- yaml contents
    """
    # Line below is inside function because we load using typ 'safe' to remove
    # comments. But dump defaut 'rt' to not order keys.
    yaml = YAML(typ='safe')
    try:
        if yaml_file.endswith('.yaml') and os.path.exists(yaml_file):
            clean_yaml_tabs(yaml_file)
            with open(yaml_file) as f:
                file_data = yaml.load(f)
                # print( f'Yaml file, name is: { file_data["name"] }')
                # yaml.dump(file_data, sys.stdout)
                # return file_data
            if file_data is None:
                print_message(
                    os.path.basename(yaml_file),
                    'yaml file is empty.',
                    color=f'{ Color.RED }',
                    color_end=f'{ Color.END }',
                )
                return yaml_file
            return file_data
        elif not yaml_file.endswith('.yaml') and os.path.exists(yaml_file):
            print_message(
                os.path.basename(yaml_file),
                'file extension is not yaml.',
                color=f'{ Color.PURPLE }',
                color_end=f'{ Color.END }',
            )
            return yaml_file
        else:
            return yaml_file
    except FileNotFoundError as error:
        # log here
        print(error.args)


def dump_yaml_data(file_data, yaml_file):
    """
    Write yaml file (sublime-syntaxes).

    Parameters:
    file_data (str) -- contents of yaml file.
    yaml_file (str) -- path to where yaml file will be saved.
    """
    # Line below is inside because we use typ 'rt' instead of 'safe'.
    # Important because if typ 'safe' it is going to order keys.
    yaml = YAML()
    yaml.version = (1, 2)
    try:
        with open(yaml_file, 'w') as f:
            yaml.dump(file_data, f)
    except FileNotFoundError as error:
        # log here
        print(error.args)


def dump_plist_data(preferences_dict: dict, plist_file: str):
    """
    Write plist file (tmPreferences).

    Parameters:
    preferences_dict (dict) --  key preferences from yaml file.
    plist_file (str) -- path to directory where tmPreferences will be saved.
    """
    try:
        # Plist
        # print(plistlib.dumps(preferences_dict).decode())
        # print(plistlib.dumps(preferences_dict))
        with open(plist_file, 'wb') as f:
            plistlib.dump(preferences_dict, f)
    except FileNotFoundError as error:
        # log here
        print(error.args)
