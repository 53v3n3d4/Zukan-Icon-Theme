import os
import plistlib

from ruamel.yaml import YAML
from src.build.helpers.color import Color
from src.build.utils.plist_unused_line import UNUSED_LINE

# Confirgurations
yaml = YAML(typ='safe')
yaml.preserve_quotes = True
yaml.default_flow_style = False
yaml.sort_keys = False
yaml.version = (1, 2)


def read_yaml_data(yaml_file: str) -> dict:
    """
    YAML reader.

    Read data to generate png icons, icons_syntaxes and preferences.

    Paramenters:
    yaml_file(str) -- path to yaml file

    Returns:
    file_data(dict) -- yaml contents
    """
    # YAML
    try:
        with open(yaml_file) as f:
            file_data = yaml.load(f)
            # print( f'Yaml file, name is: { file_data["name"] }')
            # yaml.dump(file_data, sys.stdout)
            return file_data
    except FileNotFoundError as error:
        # log here
        print(error.args)


def dump_yaml_data(file_data, yaml_file):
    """
    Write yaml file (sublime-syntaxes).

    Parameters:
    file_data(str) -- contents of yaml file.
    yaml_file(str) -- path to where yaml file will be saved.
    """
    try:
        with open(yaml_file, 'w') as f:
            yaml.dump(file_data, f)
    except FileNotFoundError as error:
        # log here
        print(error.args)


def clean_tag(file: str):
    """
    Clean tag <!DOCTYPE plist>. It is generated after plistlib dump.

    Parameters:
    file(str) -- path to icon tmPreferences file
    """
    try:
        with open(file, 'r+') as f:
            clean_file = f.read()
            clean_file = clean_file.replace(UNUSED_LINE, '')
            return clean_file
            # print(clean_file)
        with open(file, 'w') as f:
            f.write(clean_file)
    except FileNotFoundError as error:
        # log here
        print(error.args)


def dump_plist_data(
    plist_file: str, preferences_dict: dict, icon_data: str, plist_filename: str
):
    """
    Write plist file (tmPreferences).

    Parameters:
    plist_file(str) -- path to directory where tmPreferences will be saved.
    preferences_dict(dict) --  key preferences from yaml file.
    icon_data(str) --  path to yaml file containing info.
    plist_filename(str) -- tmPreferences file name. Key icon value
    wiih extension. Example: afdesign.tmPreferences.
    """
    try:
        # Plist
        # print(plistlib.dumps(preferences_dict).decode())
        # print(plistlib.dumps(preferences_dict))
        with open(plist_file, 'wb') as f:
            plistlib.dump(preferences_dict, f)
            print(
                f'{ Color.CYAN }[!] { os.path.basename(icon_data) }'
                f'{ Color.END } -> { Color.YELLOW }{ plist_filename }'
                f'{ Color.END } created.'
            )
    except FileNotFoundError as error:
        # log here
        print(error.args)
