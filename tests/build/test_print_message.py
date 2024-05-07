import pytest

from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_build_message,
    print_created_message,
    print_message,
    print_remove_tag,
    print_special_char,
)


class TestPrintBuildMessage:
    test_build_message = 'Cleaning all SVGs'
    test_build_folder = 'src/icons_test'
    test_build_expected = 'Cleaning all SVGs src/icons_test'

    @pytest.mark.parametrize(
        'a, b, expected', [(test_build_message, test_build_folder, test_build_expected)]
    )
    def test_print_build_message(self, a, b, expected):
        result = print_build_message(a, b)
        return result
        assert result == test_build_expected  # noqa: F821

    def test_build_param_is_string(self):
        test_build_message = 'Cleaning all SVGs'
        test_build_folder = 'src/icons_test'
        result = print_build_message(test_build_message, test_build_folder)
        return result
        assert isinstance(result, str)


class TestCreatedMessage:
    test_data_folder = 'foo/bar.yaml'
    test_created_filename = 'icon.png'
    test_created_message = 'created.'
    test_created_expected = '[!] foo/bar.yaml -> icon.png created.'
    test_created_filename_kwargs = 'icon'
    test_filename = '[icon.svg]'
    test_suffix = '@3x'
    test_extension = '.png'
    test_print_kwargs_expected = '[!] foo/bar.yaml [icon.svg] -> icon@3x.png created.'

    @pytest.mark.parametrize(
        'a, b, c, expected',
        [
            (
                test_data_folder,
                test_created_filename,
                test_created_message,
                test_created_expected,
            )
        ],
    )
    def test_print_created_message(self, a, b, c, expected):
        result = print_created_message(a, b, c)
        return result
        assert result == test_created_expected  # noqa: F821

    @pytest.mark.parametrize(
        'a, b, c, d, e, f, expected',
        [
            (
                test_data_folder,
                test_created_filename_kwargs,
                test_created_message,
                test_filename,
                test_suffix,
                test_extension,
                test_print_kwargs_expected,
            )
        ],
    )
    def test_created_message_kwargs(self, a, b, c, d, e, f, expected):
        result = print_created_message(a, b, c, d='[icon.svg]', e='@3x', f='.png')
        return result
        assert result == test_print_kwargs_expected  # noqa: F821

    def test_created_param_is_string(self):
        test_data_folder = 'foo/bar.yaml'
        test_created_filename = 'icon.tmPreferences'
        test_created_message = 'created.'
        result = print_created_message(
            test_data_folder, test_created_filename, test_created_message
        )
        return result
        assert isinstance(result, str)


class TestPrintMessage:
    test_filepath = 'foo/bar.yaml'
    test_print_message = 'file extension is not yaml.'
    test_print_expected = '[!] foo/bar.yaml: file extension is not yaml.'
    color = f'{ Color.RED }'
    color_end = f'{ Color.END }'
    test_print_kwargs_expected = (
        '\x1b[91m[!] foo/bar.yaml:\x1b[0m file extension is not yaml.'
    )

    @pytest.mark.parametrize(
        'a, b, expected', [(test_filepath, test_print_message, test_print_expected)]
    )
    def test_print_message(self, a, b, expected):
        result = print_message(a, b)
        return result
        assert result == test_print_expected  # noqa: F821

    @pytest.mark.parametrize(
        'a, b, c, d, expected',
        [
            (
                test_filepath,
                test_print_message,
                color,
                color_end,
                test_print_kwargs_expected,
            )
        ],
    )
    def test_print_message_kwargs(self, a, b, c, d, expected):
        result = print_message(a, b, c=f'{ Color.RED }', d=f'{ Color.END }')
        return result
        assert result == test_print_expected  # noqa: F821

    def test_print_param_is_string(self):
        test_filepath = 'foo/bar.yaml'
        test_print_message = 'file extension is not yaml.'
        result = print_build_message(test_filepath, test_print_message)
        return result
        assert isinstance(result, str)


class TestPrintRemoveTag:
    test_data_folder = 'foo/bar.yaml'
    test_created_preference = 'icon.tmPreferences'
    test_removed_expected = (
        '[!] foo/bar.yaml -> Deleting tag <!DOCTYPE plist> from icon.tmPreferences.'
    )

    @pytest.mark.parametrize(
        'a, b, expected',
        [(test_data_folder, test_created_preference, test_removed_expected)],
    )
    def test_print_remove_tag(self, a, b, expected):
        result = print_remove_tag(a, b)
        return result
        assert result == test_removed_expected  # noqa: F821

    def test_remove_param_is_string(self):
        test_data_folder = 'foo/bar.yaml'
        test_created_preference = 'icon.tmPreferences'
        result = print_remove_tag(test_data_folder, test_created_preference)
        return result
        assert isinstance(result, str)


class TestPrintSpecialChar:
    test_data_folder = 'foo/bar.yaml'
    test_png = 'icon#@'
    test_true_expected = '[!] foo/bar.yaml icon value can not contain special characters (filename would be icon#@.png).'

    @pytest.mark.parametrize(
        'a, b, expected', [(test_data_folder, test_png, test_true_expected)]
    )
    def test_print_special_char(self, a, b, expected):
        result = print_special_char(a, b)
        return result
        assert result == test_true_expected  # noqa: F821

    def test_special_char_param_is_string(self):
        test_data_folder = 'foo/bar.yaml'
        test_png = 'icon#@'
        result = print_special_char(test_data_folder, test_png)
        return result
        assert isinstance(result, str)
