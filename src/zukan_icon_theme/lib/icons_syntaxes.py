import errno
import glob
import logging
import os
import sublime

# from ..helpers.print_message import print_filenotfounderror, print_oserror
from ..helpers.read_write_data import (
    dump_yaml_data,
    edit_contexts_main,
    read_pickle_data,
)
from ..helpers.search_syntaxes import compare_scopes
from ..utils.contexts_scopes import (
    CONTEXTS_SCOPES,
)
from ..utils.zukan_dir_paths import (
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)

logger = logging.getLogger(__name__)


class ZukanSyntax:
    """
    Create and remove sublime-syntaxes in icons_syntaxes folder.
    """

    def create_icon_syntax(syntax_name: str):
        """
        Create icon sublime-syntax file.
        """
        try:
            zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
            for s in zukan_icons_syntaxes:
                if s not in compare_scopes() and s['name'] == syntax_name:
                    filename = s['name'] + '.sublime-syntax'
                    syntax_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                    )
                    # print(syntax_filepath)
                    dump_yaml_data(s, syntax_filepath)
            logger.info('%s created.', filename)
            return zukan_icons_syntaxes
        except FileNotFoundError:
            # print_filenotfounderror(filename)
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            # print_oserror(filename)
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def create_icons_syntaxes():
        """
        Create icons sublime-syntaxes files.
        """
        try:
            zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
            for s in zukan_icons_syntaxes:
                if s not in compare_scopes():
                    filename = s['name'] + '.sublime-syntax'
                    syntax_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                    )
                    # print(syntax_filepath)
                    dump_yaml_data(s, syntax_filepath)
            logger.info('sublime-syntaxes created.')
            return zukan_icons_syntaxes
        except FileNotFoundError:
            # print_filenotfounderror(filename)
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            # print_oserror(filename)
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def delete_icon_syntax(syntax_name: str):
        """
        Delete sublime-syntax file in Zukan Icon Theme/icons_syntaxes folder.

        Example: Binary (Adobe Illustrator).sublime-syntax

        Parameters:
        syntax_name (str) -- installed syntax name.
        """
        try:
            syntax_file = os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
            os.remove(syntax_file)
            logger.info('deleting icon syntax %s', os.path.basename(syntax_file))
            return syntax_name
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                syntax_name,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                syntax_name,
            )

    def delete_icons_syntaxes():
        """
        Delete all sublime-syntaxes files, leaving pickle file.
        """
        try:
            for s in glob.iglob(
                os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, '*.sublime-syntax')
            ):
                os.remove(s)
            logger.info('sublime-syntaxes deleted.')
        except FileNotFoundError:
            # print_filenotfounderror(s)
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), s
            )
        except OSError:
            # print_oserror(s)
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), s
            )

    def edit_context_scope(syntax_name: str):
        logger.info('checking icon context scope if syntax not installed.')
        for c in CONTEXTS_SCOPES:
            if sublime.find_syntax_by_scope(c['scope']):
                # Change to compat with ST3 contexts main
                if c['startsWith'] in syntax_name and int(sublime.version()) < 4075:
                    edit_contexts_main(
                        os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name), c['scope']
                    )
            else:
                # Syntaxes not installed or disabled
                # Change contexts main empty if not installed or disable
                if c['startsWith'] in syntax_name:
                    edit_contexts_main(
                        os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name), None
                    )

    def edit_contexts_scopes():
        logger.info('checking icons contexts scopes if syntax not installed.')
        for c in CONTEXTS_SCOPES:
            if sublime.find_syntax_by_scope(c['scope']):
                # print(c)
                for i in ZukanSyntax.list_created_icons_syntaxes():
                    # Change to compat with ST3 contexts main
                    if c['startsWith'] in i and int(sublime.version()) < 4075:
                        # print(i)
                        edit_contexts_main(
                            os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, i), c['scope']
                        )
            else:
                # Syntaxes not installed or disabled
                for i in ZukanSyntax.list_created_icons_syntaxes():
                    # Change contexts main empty if not installed or disable
                    if c['startsWith'] in i:
                        # print(i)
                        edit_contexts_main(
                            os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, i), None
                        )

    def list_created_icons_syntaxes() -> list:
        """
        List all sublime-syntax files in Zukan Icon Theme/icons_syntaxes folder.

        Returns:
        list_syntaxes_installed (list) -- list of sublime-syntaxes in folder
        icons_syntaxes/.
        """
        try:
            list_syntaxes_installed = []
            if os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH):
                for file in glob.glob(
                    ZUKAN_PKG_ICONS_SYNTAXES_PATH + '/*.sublime-syntax'
                ):
                    list_syntaxes_installed.append(os.path.basename(file))
                return list_syntaxes_installed
            else:
                raise FileNotFoundError(logger.error('file or directory do not exist.'))
            return list_syntaxes_installed
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'Zukan Icon Theme/icons_syntaxes folder',
            )
        except OSError:
            # print_oserror(s)
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'Zukan Icon Theme/icons_syntaxes folder',
            )
