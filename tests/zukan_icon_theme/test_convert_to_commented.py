import pytest

from src.zukan_icon_theme.helpers.convert_to_commented import convert_to_commented
from tests.mocks.constants_icons_syntaxes import (
    TEST_SUBLIME_SYNTAX_DICT,
    TEST_SUBLIME_SYNTAXES_DICT,
)
from tests.mocks.constants_pickle import (
    TEST_PICKLE_NESTED_ORDERED_DICT,
    TEST_PICKLE_ORDERED_DICT,
)
from tests.mocks.constants_yaml import (
    TEST_YAML_ORDERED_DICT,
)


class TestConvertToCommented:
    @pytest.mark.parametrize(
        'a, expected',
        [
            (TEST_SUBLIME_SYNTAXES_DICT, TEST_PICKLE_NESTED_ORDERED_DICT),
            (TEST_SUBLIME_SYNTAX_DICT, TEST_PICKLE_ORDERED_DICT),
            ('milk way', 'milk way'),
            (7, 7),
            (TEST_YAML_ORDERED_DICT, TEST_YAML_ORDERED_DICT),
        ],
    )
    def test_convert_to_commented(self, a, expected):
        result = convert_to_commented(a)
        assert result == expected
        assert isinstance(TEST_SUBLIME_SYNTAXES_DICT, list)
        assert isinstance(TEST_PICKLE_NESTED_ORDERED_DICT, list)
        assert isinstance(TEST_SUBLIME_SYNTAX_DICT, dict)
        assert isinstance(TEST_PICKLE_ORDERED_DICT, dict)
        assert isinstance('milk way', str)
        assert isinstance('milk way', str)
        assert isinstance(7, int)
        assert isinstance(7, int)
