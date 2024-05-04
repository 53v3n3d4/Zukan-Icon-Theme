import os
import _pickle as pickle
import plistlib

from ruamel.yaml import YAML
from src.build.helpers.clean_data import clean_yaml_tabs
from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_filenotfounderror,
    print_message,
    print_oserror,
)


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
    # comments. Dump use defaut 'rt' to avoid ordering keys.
    yaml = YAML(typ='safe')
    try:
        if yaml_file.endswith('.yaml') and os.path.exists(yaml_file):
            clean_yaml_tabs(yaml_file)
            with open(yaml_file) as f:
                file_data = yaml.load(f)
                # yaml.dump(file_data, sys.stdout)
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
            raise FileNotFoundError(
                print_message(
                    os.path.abspath(yaml_file),
                    'file or directory do not exist.',
                    color=f'{ Color.RED }',
                    color_end=f'{ Color.END }',
                )
            )
    except FileNotFoundError:
        print_filenotfounderror(yaml_file)
    except OSError:
        print_oserror(yaml_file)


def dump_yaml_data(file_data: dict, yaml_file: str):
    """
    Write yaml file (sublime-syntaxes).

    Parameters:
    file_data (dict) -- contents of yaml file.
    yaml_file (str) -- path to where yaml file will be saved.
    """
    # Line below is inside because we use typ 'rt' instead of 'safe'.
    # Important because if typ 'safe' it is going to order keys.
    yaml = YAML()
    yaml.version = (1, 2)
    try:
        with open(yaml_file, 'w') as f:
            yaml.dump(file_data, f)
    except FileNotFoundError:
        print_filenotfounderror(yaml_file)
    except OSError:
        print_oserror(yaml_file)


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
    except FileNotFoundError:
        print_filenotfounderror(plist_file)
    except OSError:
        print_oserror(plist_file)


def read_pickle_data(pickle_file: str) -> dict:
    """
    Pickle reader.

    Read sublime-syntaxes data.

    Paramenters:
    pickle_file (str) -- path to pickle file

    Returns:
    pickle_data (dict) -- pickle contents
    """
    try:
        pickle_data = []
        with open(pickle_file, 'rb') as f:
            try:
                while True:
                    pickle_data.append(pickle.load(f))
            except EOFError:
                print_message(
                    os.path.basename(pickle_file),
                    'end of file.',
                    color=f'{ Color.CYAN }',
                    color_end=f'{ Color.END }',
                )
        print(pickle_data)
        return pickle_data
    except FileNotFoundError:
        print_filenotfounderror(pickle_file)
    except OSError:
        print_oserror(pickle_file)


def dump_pickle_data(pickle_data: dict, pickle_file: str):
    """
    Write pickle file (sublime-syntaxes).

    Parameters:
    pickle_data (dict) -- contents of pickle file.
    pickle_file (str) -- path to where pickle file will be saved.
    """
    try:
        with open(pickle_file, 'ab+') as f:
            # In ST Python 3.3, fail if use protocol 4 or 5
            pickle.dump(pickle_data, f, protocol=3)
    except FileNotFoundError:
        print_filenotfounderror(pickle_file)
    except OSError:
        print_oserror(pickle_file)
