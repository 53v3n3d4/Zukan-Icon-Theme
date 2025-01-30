import errno
import logging
import os

logger = logging.getLogger(__name__)


def save_sublime_syntax(data: dict, file_path: str):
    """
    Write sublime-syntax file.

    Parameters:
    data (dict) -- sublime-syntax ordered dict.
    file_path (str) -- path to directory where sublime-syntax will be saved.
    """
    content = build_syntax(data)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )

    # return content


def build_syntax(data: dict) -> str:
    """
    Build sublime-syntax string with YAML directive.

    Parameters:
    data (dict) -- sublime-syntax ordered dict.

    Returns:
    content (str) -- sublime-syntax string with YAML directive.
    """
    content = ''
    content += add_directive()
    content += dict_to_syntax(data)

    return content


def add_directive() -> str:
    """
    Add YAML directive.

    Returns:
    content (str) -- YAML directive.
    """
    new_line = '\n'

    # Directive
    first_line = '%YAML 1.2'
    start_doc = '---'
    directive = first_line + new_line + start_doc + new_line

    return directive


def dict_to_syntax(syntax_dict: dict, multiplier: int = 0) -> str:
    """
    Convert sublime-syntax ordered dict to string.

    Parameters:
    syntax_dict (dict) -- sublime-syntax ordered dict.
    multiplier (int) -- indentation multiplier.

    Returns:
    data (str) -- sublime-syntax string.
    """
    data = ''
    indent = '  ' * multiplier
    new_line = '\n'

    # print(syntax_dict)

    # sublime-syntax
    for k, v in syntax_dict.items():
        data += '{i}{k}:'.format(i=indent, k=k)

        # OD
        if isinstance(v, dict):
            # print(v)
            data += new_line
            data += dict_to_syntax(v, multiplier + 1)

        # List
        elif isinstance(v, list):
            # List empty, main: []
            if not v:
                data += ' []\n'

            # List str
            if v and all(isinstance(i, str) for i in v):
                # print(v)
                data += new_line

                for list_item in v:
                    data += '{i}  - {l}\n'.format(i=indent, l=list_item)

            # Tuple list
            if v and all(isinstance(i, dict) for i in v):
                # print('include')
                # print(v)
                data += new_line

                for tuple_list in v:
                    for i, (x, y) in enumerate(tuple_list.items()):
                        # Change to yaml bool
                        if isinstance(y, bool):
                            y = 'true' if y is True else 'false'

                        if i == 0:
                            data += '{i}  - {k}: {v}\n'.format(i=indent, k=x, v=y)
                        else:
                            data += '{i}    {k}: {v}\n'.format(i=indent, k=x, v=y)

        # String or boolean
        else:
            # Change to yaml bool
            if isinstance(v, bool):
                v = 'true' if v is True else 'false'

            data += ' {v}\n'.format(v=v)

    return data
