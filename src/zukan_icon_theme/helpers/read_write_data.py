import _pickle as pickle
import errno
import json
import logging
import os
import plistlib
import re

from .convert_to_commented import convert_to_commented
from ..utils.st_py_version import (
    PYTHON_VERSION,
)
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


def dump_pickle_data(pickle_data: dict, pickle_file: str):
    """
    Write pickle file (zukan-current-version).

    Parameters:
    pickle_data (dict) -- contents of pickle file.
    pickle_file (str) -- path to where pickle file will be saved.
    """
    try:
        with open(pickle_file, 'ab+') as f:
            # Python 3.3, fail if use protocol 4 or 5
            pickle.dump(pickle_data, f, protocol=3)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), pickle_file
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), pickle_file
        )


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
                logger.debug('%s end of file.', os.path.basename(pickle_file))
        # print(pickle_data)
        return pickle_data
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), pickle_file
        )
        raise
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), pickle_file
        )
        raise


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
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), yaml_file
        )
        raise
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), yaml_file
        )
        raise


def read_yaml_data(yaml_file: str) -> dict:
    """
    YAML reader.

    Read icons sublime-syntax files.

    Paramenters:
    yaml_file (str) -- path to yaml file

    Returns:
    file_data (dict) -- yaml contents
    """
    # If use typ='safe', it is not ordering correct.
    yaml = YAML()
    try:
        with open(yaml_file) as f:
            file_data = yaml.load(f)
        return file_data
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), yaml_file
        )
        raise
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), yaml_file
        )
        raise


def edit_contexts_main(file_path: str, scope: str = None):
    """
    Edit contexts main for empty list if scope None. If scope exists, it changes
    for a format compat to ST version < 4075.

    Parameters:
    file_path (str) -- path to icon syntax file.
    scope (Optional[str]) -- scope name, default to None.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    regex_contexts_main = (
        r'contexts:\n\s*main:\n\s*- include: .*?\n\s*  apply_prototype: .*?\n'
    )

    if scope is not None:
        # Could not find other references, got this contexts main format, for 
        # ST versions lower than 4075, from A File Icon package.
        include_scope_prop = 'scope:{s}#prototype'.format(s=scope)
        include_scope = 'scope:{s}'.format(s=scope)

        contexts_main = (
            'contexts:\n  main:\n    - include: {p}\n      include: {s}\n'.format(
                p=include_scope_prop, s=include_scope
            )
        )

        content = re.sub(regex_contexts_main, contexts_main, content)
    else:
        contexts_main = 'contexts:\n  main: []\n'

        content = re.sub(
            regex_contexts_main,
            contexts_main,
            content,
        )

    with open(file_path, 'w') as f:
        f.write(content)

    logger.debug('edited file %r contaxts main.', file_path)


def dump_json_data(file_data: dict, json_file: str):
    """
    Write json file (sublime-themes).

    Parameters:
    file_data (dict) -- contents of json file.
    json_file (str) -- path to where json file will be saved.
    """
    try:
        with open(json_file, 'w') as f:
            json.dump(file_data, f, indent=4)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), json_file
        )
        raise
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), json_file
        )
        raise


def dump_plist_data(plist_dict: dict, plist_file: str):
    """
    Write plist file (tmPreferences).

    Parameters:
    plist_dict (dict) --  key preferences from yaml file.
    plist_file (str) -- path to directory where tmPreferences will be saved.
    """
    try:
        # Plist
        with open(plist_file, 'wb') as f:
            if PYTHON_VERSION < 3.8:
                plistlib.writePlist(plist_dict, f)
            else:
                plistlib.dump(plist_dict, f)
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), plist_file
        )
        raise
    except OSError:
        logger.error(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), plist_file
        )
        raise
