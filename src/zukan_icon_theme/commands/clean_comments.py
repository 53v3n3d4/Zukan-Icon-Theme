import errno
import logging
import os
import re
import sublime_plugin

from ..utils.zukan_paths import (
    ZUKAN_USER_SUBLIME_SETTINGS,
)

logger = logging.getLogger(__name__)


class CleanComments:
    """
    Clean comments that is left when using ST TextCommands deleting dicts and list
    of dicts.
    """

    def __init__(self):
        self.file_path = ZUKAN_USER_SUBLIME_SETTINGS

    def clean_comments(self):
        try:
            if self._file_exists():
                clean_content = self._read_and_clean_file()
                self._write_cleaned_content(clean_content)
            else:
                logger.error('file not found: %s', self.file_path)
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                self.file_path,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                self.file_path,
            )

    def _file_exists(self) -> bool:
        return os.path.isfile(self.file_path)

    def _read_and_clean_file(self) -> str:
        with open(self.file_path, 'r+') as f:
            content = f.read()

        cleaned_content = self._remove_comments(content)
        cleaned_content = self._remove_empty_lines(cleaned_content)

        return cleaned_content

    def _remove_comments(self, content: str) -> str:
        return re.sub(r'/\*(?:\*(?!/)|[^*])*\*/', '', content)

    def _remove_empty_lines(self, content: str) -> str:
        return os.linesep.join([line for line in content.splitlines() if line.strip()])

    def _write_cleaned_content(self, content: str):
        with open(self.file_path, 'w') as f:
            f.write(content)


class CleanCommentsCommand(sublime_plugin.TextCommand, CleanComments):
    """
    Sublime command to clean comments in Zukan Icon Theme settings file.
    """

    def __init__(self, view):
        super().__init__(view)
        self.delete_comments = CleanComments()

    def run(self, edit):
        self.delete_comments.clean_comments()
