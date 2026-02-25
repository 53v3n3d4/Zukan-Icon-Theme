import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import patch, mock_open

dict_to_syntax = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.dict_to_syntax'
)


class TestSublimeSyntax(TestCase):
    def test_add_directive(self):
        expected = '%YAML 1.2\n---\n'
        result = dict_to_syntax.add_directive()
        self.assertEqual(result, expected)

    def test_dict_to_syntax(self):
        syntax_dict = {
            'name': 'ATest',
            'hidden': True,
            'scope': 'source.atest',
            'file_extensions': ['abc', 'def'],
            'contexts': {
                'main': [{'include': 'scope:source.atest1', 'apply_prototype': True}]
            },
            'contexts_main': {'main': []},
        }

        expected = """name: ATest
hidden: true
scope: source.atest
file_extensions:
  - abc
  - def
contexts:
  main:
    - include: scope:source.atest1
      apply_prototype: true
contexts_main:
  main: []
"""
        result = dict_to_syntax.dict_to_syntax(syntax_dict)
        self.assertEqual(result, expected)

    def test_build_syntax(self):
        syntax_dict = {
            'name': 'ATest-2',
            'version': 2,
            'file_extensions': ['uvw', 'xyz'],
        }

        expected = (
            '%YAML 1.2\n---\nname: ATest-2\nversion: 2\nfile_extensions:\n'
            '  - uvw\n  - xyz\n'
        )
        result = dict_to_syntax.build_syntax(syntax_dict)
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(dict_to_syntax, 'logger')
    def test_save_sublime_syntax(self, mock_logger, mock_open):
        data = {'name': 'ATest-3', 'scope': 'source.atest3'}
        file_path = 'file.sublime-syntax'

        dict_to_syntax.save_sublime_syntax(data, file_path)

        mock_open.assert_called_once_with(file_path, 'w')
        mock_open().write.assert_called_once_with(
            '%YAML 1.2\n---\nname: ATest-3\nscope: source.atest3\n'
        )

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch.object(dict_to_syntax, 'logger')
    def test_save_sublime_syntax_file_not_found(self, mock_logger, mock_open):
        data = {'name': 'ATest-4', 'version': 2}

        file_path = 'invalid_path/file.sublime-syntax'

        dict_to_syntax.save_sublime_syntax(data, file_path)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )

    @patch('builtins.open', side_effect=OSError)
    @patch.object(dict_to_syntax, 'logger')
    def test_save_sublime_syntax_os_error(self, mock_logger, mock_open):
        data = {'name': 'ATest-5', 'contexts': {'prototype': [{'include': 'comments'}]}}

        file_path = 'invalid_path/file.sublime-syntax'

        dict_to_syntax.save_sublime_syntax(data, file_path)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )
