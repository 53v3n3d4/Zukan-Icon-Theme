import os
import pytest

from src.build.utils.build_dir_paths import filepath, DATA_PATH


def test_param_is_string():
    TESTS_FOLDER = filepath('../tests')
    assert isinstance(TESTS_FOLDER, str)
    # assert type(TESTS_FOLDER) is str


# Using relpath, relative path from start directory, to make path
# test possible in diferent machines.
# https://docs.python.org/3/library/os.path.html#os.path.relpath
def test_relative_path():
    TESTS_FOLDER = filepath('../tests')
    SHORT_URL = os.path.relpath(TESTS_FOLDER, start=DATA_PATH)
    TESTS_RELATIVE_PATH = '../build/tests'
    assert SHORT_URL == TESTS_RELATIVE_PATH


def test_param_fails_int():
    with pytest.raises(ValueError, match=r'Url need to be string.'):
        filepath(7)


def test_param_fails_array():
    with pytest.raises(ValueError, match=r'Url need to be string.'):
        array_fail = ['milk', 'way']
        filepath(array_fail)
