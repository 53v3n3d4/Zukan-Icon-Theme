import errno
import os


def print_filenotfounderror(filename: str) -> str:
    """
    Errno ENOENT, FileNotFoundError message.

    Parameters:
    filename (str) -- path to file.

    Returns:
    str -- Errno code, description and filename.
    """
    return print(
        errno.ENOENT,
        os.strerror(errno.ENOENT),
        ('-> %s' % filename),
    )


def print_oserror(filename: str) -> str:
    """
    Errno EACCES, OSError message.

    Parameters:
    filename (str) -- path to file.

    Returns:
    str -- Errno code, description and filename.
    """
    return print(
        errno.EACCES,
        os.strerror(errno.EACCES),
        ('-> %s' % filename),
    )
