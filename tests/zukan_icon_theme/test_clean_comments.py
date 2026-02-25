import os
import errno
import importlib

from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock

clean_comments = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.clean_comments'
)


class TestCleanComments(TestCase):
    def setUp(self):
        self.cleaner = clean_comments.CleanComments()
        self.test_file_path = clean_comments.ZUKAN_USER_SUBLIME_SETTINGS

    def normalize_str(self, crlf_str: str) -> str:
        return crlf_str.replace('\r\n', '\n')

    def test_remove_comments(self):
        list_comments = [
            ('/* Line comment */ "log_level": "INFO"', ' "log_level": "INFO"'),
            ('"log_level": "INFO" /* Comment at end */', '"log_level": "INFO" '),
            ('/* Multi\nline\ncomment */ "log_level": "INFO"', ' "log_level": "INFO"'),
            ('No comments here', 'No comments here'),
            ('/* */ Empty comment', ' Empty comment'),
        ]

        for p1, p2 in list_comments:
            with self.subTest(list_comments):
                result = self.cleaner._remove_comments(p1)
                self.assertEqual(self.normalize_str(result), p2)

    def test_remove_empty_lines(self):
        list_comments = [
            ('line1\n\nline2\n  \nline3', 'line1\nline2\nline3'),
            ('\n\nline1\nline2\n\n', 'line1\nline2'),
            ('single line', 'single line'),
            ('   \n  \n  ', ''),
        ]

        for p1, p2 in list_comments:
            with self.subTest(list_comments):
                result = self.cleaner._remove_empty_lines(p1)
                self.assertEqual(self.normalize_str(result), self.normalize_str(p2))

    @patch('os.path.isfile')
    def test_file_exists(self, mock_isfile):
        mock_isfile.return_value = True
        self.assertTrue(self.cleaner._file_exists())

        mock_isfile.return_value = False
        self.assertFalse(self.cleaner._file_exists())

        mock_isfile.assert_called_with(self.test_file_path)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile')
    def test_read_and_clean_file(self, mock_isfile, mock_file):
        mock_isfile.return_value = True
        mock_file.return_value.read.return_value = (
            '/* Comment */\n"prefer_icon": {},\n\n"ignored_icon": []'
        )

        result = self.cleaner._read_and_clean_file()

        expected_output = '"prefer_icon": {},\n"ignored_icon": []'
        self.assertEqual(
            self.normalize_str(result), self.normalize_str(expected_output)
        )
        mock_file.assert_called_once_with(self.test_file_path, 'r+')

    @patch('builtins.open', new_callable=mock_open)
    def test_write_cleaned_content(self, mock_file):
        content = '"change_icon": {},'
        self.cleaner._write_cleaned_content(content)

        mock_file.assert_called_once_with(self.test_file_path, 'w')
        mock_file().write.assert_called_once_with(content)

    @patch.object(clean_comments.logger, 'error')
    @patch('os.path.isfile')
    def test_clean_comments_file_not_found(self, mock_isfile, mock_logger):
        mock_isfile.return_value = False

        self.cleaner.clean_comments()

        mock_logger.assert_called_once_with('file not found: %s', self.test_file_path)

    @patch('builtins.open')
    @patch('os.path.isfile')
    def test_clean_comments_file_os_error(self, mock_isfile, mock_open):
        mock_isfile.return_value = True
        mock_open.side_effect = OSError(errno.EACCES, 'Permission denied')

        with patch.object(clean_comments.logger, 'error') as mock_logger:
            self.cleaner.clean_comments()

            mock_logger.assert_called_once_with(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                self.test_file_path,
            )


class TestCleanCommentsCommand(TestCase):
    def setUp(self):
        self.view = MagicMock()
        self.command = clean_comments.CleanCommentsCommand(self.view)

    def test_clean_comments_command(self):
        self.assertIsInstance(
            self.command.delete_comments, clean_comments.CleanComments
        )
        self.assertEqual(self.command.view, self.view)

    @patch.object(clean_comments.CleanComments, 'clean_comments')
    def test_clean_comments_command_run(self, mock_clean_comments):
        edit = MagicMock()
        self.command.run(edit)
        mock_clean_comments.assert_called_once()
