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
        'a, expected',
        [
            (TEST_SUBLIME_SYNTAXES_DICT, TEST_PICKLE_NESTED_ORDERED_DICT),
            (TEST_SUBLIME_SYNTAX_DICT, TEST_PICKLE_ORDERED_DICT),
            ('milk way', 'milk way'),
            (7, 7),
        ],
    )
    def test_nested_ordered_dict(self, a, expected):
        result = nested_ordered_dict(a)
        assert result == expected
        assert isinstance(TEST_SUBLIME_SYNTAXES_DICT, list)
        assert isinstance(TEST_PICKLE_NESTED_ORDERED_DICT, list)
        assert isinstance(TEST_SUBLIME_SYNTAX_DICT, dict)
        assert isinstance(TEST_PICKLE_ORDERED_DICT, dict)
        assert isinstance('milk way', str)
        assert isinstance('milk way', str)
        assert isinstance(7, int)
        assert isinstance(7, int)
