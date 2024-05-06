import _pickle as pickle
import os

from .convert_to_commented import convert_to_commented
from .print_message import print_filenotfounderror, print_oserror
from ruamel.yaml import YAML


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
                print('[!] %s: End of file.' % os.path.basename(pickle_file))
        # print(pickle_data)
        return pickle_data
    except FileNotFoundError:
        print_filenotfounderror(pickle_file)
    except OSError:
        print_oserror(pickle_file)


def dump_yaml_data(file_data: dict, yaml_file: str):
    """
    Write yaml file (sublime-syntaxes).

    Parameters:
    file_data (dict) -- contents of yaml file.
    yaml_file (str) -- path to where yaml file will be saved.
    """
    yaml = YAML()
    yaml.version = (1, 2)

    # Converting OrderedDict to ruamel CommentMap
    # OrderedDict only necessary if using python 3.3
    # Python 3.8, dict read ordered.
    file_data = convert_to_commented(file_data)
    # print(isinstance(file_data, dict))
    try:
        with open(yaml_file, 'w') as f:
            yaml.dump(file_data, f)
    except FileNotFoundError:
        print_filenotfounderror(yaml_file)
    except OSError:
        print_oserror(yaml_file)
