import importlib

from unittest import TestCase

edit_file_extension = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.edit_file_extension'
)

SCOPES_FILE_EXTENSIONS = [
    {
        'scope': 'source.arduino',
        'file_extensions': ['ino', 'pde'],
    },  # arduino.yaml
    {'scope': 'source.asp', 'file_extensions': ['vbs']},  # asp.yaml
    {
        'scope': 'source.bazel',
        'file_extensions': ['bazel', 'bzl'],
    },  # bazel.yaml
    {'scope': 'source.c++', 'file_extensions': ['h']},  # cuda.yaml
    {'scope': 'source.css', 'file_extensions': ['css']},
    {
        'scope': 'source.cmake',
        'file_extensions': ['CMakeLists.txt'],
    },  # cmake.yaml
    {
        'scope': 'source.fortran',
        'file_extensions': ['f90', 'F90', 'f95', 'F95', 'f03', 'F03', 'f08', 'F08'],
    },  # fortran.yaml
    {'scope': 'source.toml.python', 'file_extensions': ['pyproject.toml']},
    {'scope': 'source.tex', 'file_extensions': ['cls']},  # tex.yaml
]


class TestEditFileExtension(TestCase):
    # No file extension to change
    def test_no_file_extension_to_change(self):
        syntax_file_extensions = ['py', 'pyc']
        syntax_scope = 'source.python'

        change_icon_file_extension = [
            {'scope': 'text.plain.wwpdb', 'file_extensions': ['pdb']}
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, ['py', 'pyc'])

    # Change file extension case
    # Should exclude file extension from `SCOPES_FILE_EXTENSIONS` and return the list empty
    def test_change_file_extension_return_empty_1(self):
        syntax_file_extensions = ['pyproject.toml']
        syntax_scope = 'source.toml.python'

        change_icon_file_extension = [
            {'scope': 'source.toml.poetry', 'file_extensions': ['pyproject.toml']}
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, [])

    # Change file extension case
    # Should exclude file extension from `SCOPES_FILE_EXTENSIONS` and return the list empty
    def test_change_file_extension_return_empty_2(self):
        syntax_file_extensions = [
            'f90',
            'F90',
            'f95',
            'F95',
            'f03',
            'F03',
            'f08',
            'F08',
        ]
        syntax_scope = 'source.fortran'

        change_icon_file_extension = [
            {
                'scope': 'source.modern-fortran',
                'file_extensions': [
                    'f90',
                    'F90',
                    'f95',
                    'F95',
                    'f03',
                    'F03',
                    'f08',
                    'F08',
                ],
            }
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, [])

    # Change file extension case
    # Should exclude file extension from `SCOPES_FILE_EXTENSIONS` and return the list without
    # the file extension in `change_icon_file_extension`
    def test_change_file_extension_return_not_empty_1(self):
        syntax_file_extensions = ['bazel', 'bzl']
        syntax_scope = 'source.bazel'

        change_icon_file_extension = [
            {'scope': 'source.starlark', 'file_extensions': ['bzl']}
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, ['bazel'])

    # Change file extension case
    # Should exclude file extension from `SCOPES_FILE_EXTENSIONS` and return the list without
    # the file extension in `change_icon_file_extension`
    def test_change_file_extension_return_not_empty_2(self):
        syntax_file_extensions = ['sty', 'cls']
        syntax_scope = 'source.tex'

        change_icon_file_extension = [
            {'scope': 'source.vbs', 'file_extensions': ['cls']}
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, ['sty'])

    # Change file extension case
    # Should exclude file extension from `SCOPES_FILE_EXTENSIONS` and return the list without
    # the file extension in `change_icon_file_extension`
    def test_change_file_extension_return_not_empty_3(self):
        syntax_file_extensions = ['cmake', 'CMakeLists.txt']
        syntax_scope = 'source.cmake'

        change_icon_file_extension = [
            {'scope': 'source.cmakeeditor', 'file_extensions': ['CMakeLists.txt']}
        ]

        result = edit_file_extension.edit_file_extension(
            syntax_file_extensions, syntax_scope, change_icon_file_extension
        )

        self.assertEqual(result, ['cmake'])
