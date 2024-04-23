import pytest

from build.helpers.special_chars import special_chars
from pyfakefs.fake_filesystem_unittest import TestCase


def test_special_chars_true():
    filename = 'c#.png'
    assert special_chars(filename) == True


def test_special_chars_false():
    filename = 'csharp.png'
    assert special_chars(filename) == False
