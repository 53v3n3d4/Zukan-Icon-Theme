import os


# Code from
# https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
def get_size(folders: list) -> int:
    """
    Calculate package instalation size.

    Parameters:
    folders (list) -- list of folders.

    Returns:
    total_size (int) - size in bytes.
    """
    total_size = 0
    seen = {}

    for folder in folders:
        if folder:
            for dir_path, dir_name, file_name in os.walk(folder):  # noqa B007
                # print(dir_name)
                for f in file_name:
                    file_path = os.path.join(dir_path, f)
                    try:
                        stat = os.lstat(file_path)
                    except OSError:
                        continue

                    try:
                        seen[stat.st_ino]
                    except KeyError:
                        seen[stat.st_ino] = True
                    else:
                        continue

                    total_size += stat.st_size

            return total_size


# Code from
# https://stackoverflow.com/questions/1094841/get-a-human-readable-version-of-a-file-size
def file_size(size: int, suffix='B'):
    """
    Size in Bytes, KB, MB, And GB.

    Parameters:
    size (int) -- size in bytes.

    Returns:
    size (str) - human readable size.
    """
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(size) < 1024.0:
            return f'{size:3.1f}{unit}{suffix}'
        size /= 1024.0
    return f'{size:.1f}Yi{suffix}'
