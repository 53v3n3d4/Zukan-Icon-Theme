from src.build.helpers.color import Color


def print_build_message(message: str, args: str) -> str:
    """
    Message used in argparse subcommands, file scripts.py.

    Parameters:
    message (str) -- text with info when scripts running.
    args (str) -- argparse args.

    Returns:
    str -- description text when file built.
    """
    return print(f'{ Color.BLUE }{ message }{ Color.END }{ args }')


def print_created_message(
    filepath: str, created_filename: str, message: str, **kwargs
) -> str:
    """
    Message used when a PNG, sublime-syntax or tmPreference is created.

    Parameters:
    filepath (str) -- path to data file.
    created_filename (str) -- PNG, sublime-syntax or tmPreference
        file name.
    message (str) -- description text.
    **kwargs -- additional keyword arguments passed to message. Arguments
        are filename, suffix and extesion used when creating PNGs.

    Returns:
    str -- description text when file created.
    """
    filename = kwargs.get('filename', '')
    suffix = kwargs.get('suffix', '')
    extension = kwargs.get('extension', '')
    return print(
        f'{ Color.CYAN }[!] { filepath }{ filename }{ Color.END } '
        f'-> { Color.YELLOW }{ created_filename }{ suffix }'
        f'{ extension }{ Color.END } { message }'
    )


def print_message(filepath: str, message: str, **kwargs) -> str:
    """
    Message with one color text, filepath, followed by a description.

    Parameters:
    filepath (str) -- path to data file.
    message (str) -- description text.
    **kwargs -- additional keyword arguments passed to message. Arguments
        are used by Ansi color open and close tag to color text.

    Returns:
    str -- description text with color filepath.
    """
    color = kwargs.get('color', '')
    color_end = kwargs.get('color_end', '')
    return print(f'{ color }[!] { filepath }:{ color_end } { message }')


def print_remove_tag(filepath: str, created_filename: str) -> str:
    """
    Message used in preferences, when removing tag <!DOCTYPE plist>.

    Parameters:
    filepath (str) -- path to data file.
    created_filename (str) -- tmPreferences file name created in dump.

    Returns:
    str -- tmPreferences remove tag description text.
    """
    return print(
        f'{ Color.CYAN }[!] { filepath }{ Color.END } -> Deleting '
        f'{ Color.YELLOW }tag <!DOCTYPE plist>{ Color.END } from '
        f'{ created_filename }.'
    )


def print_special_char(filepath: str, filename: str) -> str:
    """
    Message used in icons, if special chars used this message is
    presented.

    Parameters:
    filepath (str) -- path to data file.
    filename (str) -- Icon PNG name from data file

    Returns:
    str -- Special chars found description text.
    """
    return print(
        f'{ Color.RED }[!] { filepath }:{ Color.END } icon value can not '
        f'contain special characters { Color.RED }(filename would be '
        f'{ filename }.png){ Color.END }.'
    )
