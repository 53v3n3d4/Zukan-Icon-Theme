import pytest

from src.build.helpers.nested_ordered_dict import nested_ordered_dict
from tests.build.mocks.constants_icons_syntaxes import (
    TEST_SUBLIME_SYNTAX_DICT,
    TEST_SUBLIME_SYNTAXES_DICT,
)
from tests.build.mocks.constants_pickle import (
    TEST_PICKLE_NESTED_ORDERED_DICT,
    TEST_PICKLE_ORDERED_DICT,
)


class TestNestedOrderedDict:
    @pytest.mark.parametrize(
        'a, expected', [(TEST_SUBLIME_SYNTAXES_DICT, TEST_PICKLE_NESTED_ORDERED_DICT)]
    )
    def test_nested_ordered_dict(self, a, expected):
        result = nested_ordered_dict(a)
        assert result == expected
        assert isinstance(a, list)
        assert isinstance(expected, list)

    @pytest.mark.parametrize(
        'a, expected', [(TEST_SUBLIME_SYNTAX_DICT, TEST_PICKLE_ORDERED_DICT)]
    )
    def test_ordered_dict(self, a, expected):
        result = nested_ordered_dict(a)
        assert result == expected
        assert isinstance(a, dict)
        assert isinstance(expected, dict)

    @pytest.mark.parametrize('a, expected', [('milk way', 'milk way')])
    def test_string(self, a, expected):
        result = nested_ordered_dict(a)
        assert result == expected
        assert isinstance(a, str)
        assert isinstance(expected, str)

    @pytest.mark.parametrize('a, expected', [(7, 7)])
    def test_interger(self, a, expected):
        result = nested_ordered_dict(a)
        assert result == expected
        assert isinstance(a, int)
        assert isinstance(expected, int)
