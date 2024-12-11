import errno
import logging
import os
import re

logger = logging.getLogger(__name__)


def clean_comments_settings(zukan_sublime_settings: str):
    """
    Clean comments that is left when using ST TextCommands deleting dicts and list
    of dicts.
    """
    try:
        if zukan_sublime_settings:
            with open(zukan_sublime_settings, 'r+') as f:
                clean_file = f.read()
                # clean_file = re.sub(r'(\t\t)\/[^)]*\/', '', clean_file)
                clean_file = re.sub(r'/\*(?:\*(?!/)|[^*])*\*/', '', clean_file)
                clean_file = clean_file.replace('\t\t\n', '')
                clean_file = os.linesep.join([s for s in clean_file.splitlines() if s])
            with open(zukan_sublime_settings, 'w') as f:
                f.write(clean_file)
            # print('clean settings')
    except FileNotFoundError:
        logger.error(
            '[Errno %d] %s: %r',
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            zukan_sublime_settings,
        )
    except OSError:
        logger.error(
            '[Errno %d] %s: %r',
            errno.EACCES,
            os.strerror(errno.EACCES),
            zukan_sublime_settings,
        )
