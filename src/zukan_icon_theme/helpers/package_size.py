import errno
import logging
import os

logger = logging.getLogger(__name__)


def get_file_size(file_path: str) -> int:
    """
    Calculate the size of a file.

    Returns:
    total_size (int) -- total size in bytes of a file.
    """
    total_size = 0

    if os.path.isfile(file_path):
        try:
            stat = os.lstat(file_path)
            total_size += stat.st_size
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                file_path,
            )

    return total_size


def get_folder_size(folder_path: str) -> int:
    """
    Code from
    https://stackoverflow.com/questions/1392413/
    calculating-a-directorys-size-using-python

    Calculate the size of a folder.

    Parameters:
    folder_path (str) -- path to folder.

    Returns:
    total_size (int) -- total size in bytes of a folder.
    """
    total_size = 0
    seen = {}

    for dir_path, dir_name, file_name in os.walk(folder_path):  # noqa B007
        # print(dir_name)
        for f in file_name:
            file_path = os.path.join(dir_path, f)
            try:
                stat = os.lstat(file_path)
            except OSError:
                logger.error(
                    '[Errno %d] %s: %r',
                    errno.EACCES,
                    os.strerror(errno.EACCES),
                    file_path,
                )
                continue

            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue

            total_size += stat.st_size

    return total_size


def bytes_to_readable_size(size: int, suffix='B'):
    """
    Code from
    https://stackoverflow.com/questions/1094841/
    get-a-human-readable-version-of-a-file-size

    Size in Bytes, KB, MB, And GB.

    Parameters:
    size (int) -- size in bytes.

    Returns:
    size (str) - human readable size.
    """
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(size) < 1024.0:
            return '{s:3.1f}{u}{x}'.format(s=size, u=unit, x=suffix)
            # return f'{size:3.1f}{unit}{suffix}'
        size /= 1024.0
    return '{s:.1f}Yi{x}'.format(s=size, x=suffix)
    # return f'{size:.1f}Yi{suffix}'
