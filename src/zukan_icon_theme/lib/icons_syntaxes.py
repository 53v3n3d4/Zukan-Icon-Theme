import errno
import glob
import logging
import os
import sublime

from ..helpers.read_write_data import (
    dump_yaml_data,
    edit_contexts_main,
    read_pickle_data,
    read_yaml_data,
)
from ..helpers.search_syntaxes import compare_scopes
from ..utils.contexts_scopes import (
    CONTEXTS_MAIN,
    CONTEXTS_SCOPES,
)
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
)
from ..utils.zukan_dir_paths import (
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)
from collections import OrderedDict

logger = logging.getLogger(__name__)


class ZukanSyntax:
    """
    Create and remove sublime-syntaxes in icons_syntaxes folder.
    """

    def build_icon_syntax(file_name: str, syntax_name: str):
        ZukanSyntax.create_icon_syntax(file_name)
        ZukanSyntax.edit_context_scope(syntax_name)

    def build_icons_syntaxes():
        ZukanSyntax.create_icons_syntaxes()
        ZukanSyntax.edit_contexts_scopes()

    def create_icon_syntax(syntax_name: str):
        """
        Create icon sublime-syntax file.
        """
        try:
            zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
            for s in zukan_icons_syntaxes:
                if s not in compare_scopes() and s['name'] == syntax_name:
                    filename = s['name'] + SUBLIME_SYNTAX_EXTENSION
                    syntax_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                    )
                    # print(syntax_filepath)
                    dump_yaml_data(s, syntax_filepath)
            logger.info('%s created.', filename)
            return zukan_icons_syntaxes
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
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
                    filename = s['name'] + SUBLIME_SYNTAX_EXTENSION
                    syntax_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                    )
                    # print(syntax_filepath)
                    dump_yaml_data(s, syntax_filepath)
            logger.info('sublime-syntaxes created.')
            return zukan_icons_syntaxes
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
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
                os.path.join(
                    ZUKAN_PKG_ICONS_SYNTAXES_PATH, '*' + SUBLIME_SYNTAX_EXTENSION
                )
            ):
                os.remove(s)
            logger.info('sublime-syntaxes deleted.')
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), s
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), s
            )

    def edit_context_scope(syntax_name: str):
        """
        Edit contexts main in zukan icon sublime-syntax file.

        If syntax not installed or disabled, it changes contexts main for empty list.
        This avoid error in console about syntax not found.

        Parameters:
        syntax_name (str) -- icon syntax file name.
        """
        logger.info('editing icon context scope if syntax not installed.')
        syntax_file = os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
        file_content = read_yaml_data(syntax_file)
        ordered_dict = OrderedDict(file_content)
        # print(ordered_dict['contexts']['main'])
        for od in ordered_dict['contexts']['main']:
            # Only with contexts main include
            if od['include']:
                # print(od['include'])
                scope = od['include'].replace('scope:', '')
                # print(scope)
                if (
                    sublime.find_syntax_by_scope(scope)
                    and scope is not None
                    and int(sublime.version()) > 4075
                ):
                    return ordered_dict
                if (
                    sublime.find_syntax_by_scope(scope)
                    and scope is not None
                    and int(sublime.version()) < 4075
                ):
                    # Could not find other references, got this contexts main format,
                    # for ST versions lower than 4075, from A File Icon package.
                    include_scope_prop = 'scope:{s}#prototype'.format(s=scope)
                    include_scope = 'scope:{s}'.format(s=scope)
                    CONTEXTS_MAIN['contexts']['main'] = [
                        {'include': include_scope_prop},
                        {'include': include_scope},
                    ]
                if scope is None:
                    # print(ordered_dict)
                    CONTEXTS_MAIN['contexts']['main'] = []
                # print(CONTEXTS_MAIN)
                ordered_dict.update(CONTEXTS_MAIN)
                # print(ordered_dict)
                dump_yaml_data(ordered_dict, syntax_file)

    def edit_contexts_scopes():
        """
        Edit contexts main in zukan icons sublime-syntax files.

        If syntax not installed or disabled, it changes contexts main for empty list.
        This avoid error in console about syntax not found.
        """
        logger.info('editing icons contexts scopes if syntax not installed.')
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
                    os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, '*' + SUBLIME_SYNTAX_EXTENSION
                    )
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
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'Zukan Icon Theme/icons_syntaxes folder',
            )
