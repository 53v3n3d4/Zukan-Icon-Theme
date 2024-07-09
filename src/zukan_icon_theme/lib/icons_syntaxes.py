import errno
import glob
import logging
import os
import sublime

from ..helpers.copy_primary_icons import copy_primary_icons
from ..helpers.get_settings import get_settings
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
    SVG_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_ICONS_DATA_FILE,
    # ZUKAN_SYNTAXES_DATA_FILE,
)
from collections import OrderedDict

logger = logging.getLogger(__name__)


class ZukanSyntax:
    """
    Create and remove sublime-syntaxes in icons_syntaxes folder.
    """

    def build_icon_syntax(file_name: str, syntax_name: str):
        """
        Batch create syntax, edit context scope, and copy primary icons,
        to use with Thread together in install events.

        Parameters:
        file_name (str) -- syntax file name, without extension.
        syntax_name (str) -- syntax name, file name and extension.
        """
        ZukanSyntax.create_icon_syntax(file_name)
        ZukanSyntax.edit_context_scope(syntax_name)
        copy_primary_icons()

    def build_icons_syntaxes():
        """
        Batch create syntaxes, edit contexts scopes and copy primary icons,
        to use with Thread together in install events.
        """
        if not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH):
            os.makedirs(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        ZukanSyntax.create_icons_syntaxes()
        ZukanSyntax.edit_contexts_scopes()
        copy_primary_icons()

    def create_icon_syntax(syntax_name: str):
        """
        Create icon sublime-syntax file.

        Parameters:
        syntax_name (str) -- syntax name, file name and extension.
        """
        try:
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            for s in zukan_icons:
                if (
                    any('syntax' in d for d in s)
                    and s.get('syntax') is not None
                    and not (
                        s['name'] in ignored_icon
                        or s['preferences']['settings']['icon'] in ignored_icon
                        or (s['preferences']['settings']['icon'] + SVG_EXTENSION)
                        in ignored_icon
                        or (s.get('tag') is not None and s['tag'] in ignored_icon)
                    )
                ):
                    for k in s['syntax']:
                        if k not in compare_scopes() and k['name'] == syntax_name:
                            filename = k['name'] + SUBLIME_SYNTAX_EXTENSION
                            syntax_filepath = os.path.join(
                                ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                            )
                            # print(syntax_filepath)
                            dump_yaml_data(k, syntax_filepath)
                            logger.info('%s created.', filename)
                elif (
                    any('syntax' in d for d in s)
                    and s.get('syntax') is not None
                    and (
                        s['name'] in ignored_icon
                        or s['preferences']['settings']['icon'] in ignored_icon
                        or (s['preferences']['settings']['icon'] + SVG_EXTENSION)
                        in ignored_icon
                        or (s.get('tag') is not None and s['tag'] in ignored_icon)
                    )
                ):
                    for k in s['syntax']:
                        if k['name'] == syntax_name:
                            logger.info('ignored icon %s', s['name'])
            return zukan_icons
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
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            for s in zukan_icons:
                if (
                    any('syntax' in d for d in s)
                    and s.get('syntax') is not None
                    and not (
                        s['name'] in ignored_icon
                        or s['preferences']['settings']['icon'] in ignored_icon
                        or (s['preferences']['settings']['icon'] + SVG_EXTENSION)
                        in ignored_icon
                        or (s.get('tag') is not None and s['tag'] in ignored_icon)
                    )
                ):
                    for k in s['syntax']:
                        if k not in compare_scopes():
                            filename = k['name'] + SUBLIME_SYNTAX_EXTENSION
                            syntax_filepath = os.path.join(
                                ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                            )
                            # print(syntax_filepath)
                            dump_yaml_data(k, syntax_filepath)
                elif (
                    s['name'] in ignored_icon
                    or s['preferences']['settings']['icon'] in ignored_icon
                    or (s['preferences']['settings']['icon'] + SVG_EXTENSION)
                    in ignored_icon
                    or (s.get('tag') is not None and s['tag'] in ignored_icon)
                ):
                    logger.info('ignored icon %s', s['name'])
            logger.info('sublime-syntaxes created.')
            return zukan_icons
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
        syntax_file = os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
        if os.path.exists(syntax_file):
            logger.info('editing icon context scope if syntax not installed.')
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
