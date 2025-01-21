import errno
import logging
import os

from collections import OrderedDict

logger = logging.getLogger(__name__)


def save_sublime_syntax(data, file_path):
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


def build_syntax(data):
    content = ''
    content += add_directive()
    content += od_to_syntax(data)

    return content


def add_directive() -> str:
    new_line = '\n'

    # Directive
    first_line = '%YAML 1.2'
    start_doc = '---'
    directive = first_line + new_line + start_doc + new_line

    return directive


def od_to_syntax(syntax_od, multiplier=0):
    """
    Convert an OrderedDict to sublime-syntax string.
    """
    data = ''
    indent = '  ' * multiplier
    new_line = '\n'

    # print(syntax_od)

    # sublime-syntax
    for k, v in syntax_od.items():
        data += '{i}{k}:'.format(i=indent, k=k)

        # OD
        if isinstance(v, (OrderedDict, dict)):
            # print(v)
            data += new_line
            data += od_to_syntax(v, multiplier + 1)

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
