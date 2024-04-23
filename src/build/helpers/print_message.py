from src.build.helpers.color import Color


def print_build_message(message: str, args: str) -> str:
    """
    Message used in argparse subcommands, file scripts.py.

    Parameters:
    message(str) -- text with info when scripts running.
    args(str) -- argparse args.

    Returns:
    str -- text with args.
    """
    return print(f'{ Color.BLUE }{ message }{ Color.END }{ args }')
