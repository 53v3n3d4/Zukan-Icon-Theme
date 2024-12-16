import errno
import logging
import os

logger = logging.getLogger(__name__)


def get_size(file_folder: list) -> int:
    """
    Adapt from
    https://stackoverflow.com/questions/1392413/
    calculating-a-directorys-size-using-python

    Calculate the total size of files and folders.

    Parameters:
    file_folder (list) -- List of file or folder paths.

    Returns:
    total_size (int) -- Total size in bytes of all files and folders.
    """
    total_size = 0
    seen = {}

    for f in file_folder:
        if f:
            if os.path.isfile(f):
                try:
                    stat = os.lstat(f)
                    total_size += stat.st_size
                except OSError:
                    logger.error(
                        '[Errno %d] %s: %r',
                        errno.EACCES,
                        os.strerror(errno.EACCES),
                        f,
                    )
                    continue

            elif os.path.isdir(f):
                for dir_path, dir_name, file_names in os.walk(f):  # noqa B007
                    for file_name in file_names:
                        file_path = os.path.join(dir_path, file_name)
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


def file_size(size: int, suffix='B'):
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
