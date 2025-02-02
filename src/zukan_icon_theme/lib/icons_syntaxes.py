import errno
import glob
import logging
import os
import re
import sublime
import threading

from collections.abc import Set
from ..helpers.copy_primary_icons import copy_primary_icons
from ..helpers.custom_icon import generate_custom_icon
from ..helpers.dict_to_syntax import save_sublime_syntax
from ..helpers.edit_file_extension import edit_file_extension
from ..helpers.load_save_settings import (
    get_change_icon_settings,
    get_ignored_icon_settings,
)
from ..helpers.read_write_data import (
    edit_contexts_main,
    read_pickle_data,
)
from ..helpers.search_syntaxes import compare_scopes
from ..helpers.thread_progress import ThreadProgress
from ..utils.contexts_scopes import (
    CONTEXTS_SCOPES,
)
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    SVG_EXTENSION,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_ICONS_DATA_FILE,
)

logger = logging.getLogger(__name__)


class ZukanSyntax:
    """
    Create and remove sublime-syntaxes in icons_syntaxes folder.
    """

    def __init__(self):
        self.sublime_version = int(sublime.version())

    def zukan_icons_data(self) -> list:
        return read_pickle_data(ZUKAN_ICONS_DATA_FILE)

    def change_icon_file_extension_setting(self) -> list:
        _, change_icon_file_extension = get_change_icon_settings()
        return change_icon_file_extension

    def ignored_icon_setting(self) -> Set:
        return set(get_ignored_icon_settings())

    def install_syntax(self, file_name: str, syntax_name: str):
        """
        Using Thread to install syntax to avoid freezing ST to build syntax.

        Parameters:
        file_name (str) -- syntax file name, without extension.
        syntax_name (str) -- syntax name, file name and extension.
        """
        ts = threading.Thread(
            target=self.build_icon_syntax, args=(file_name, syntax_name)
        )
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_syntaxes(self):
        """
        Using Thread to install syntax to avoid freezing ST to build syntaxes.
        """
        ts = threading.Thread(target=self.build_icons_syntaxes)
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def build_icon_syntax(self, file_name: str, syntax_name: str):
        """
        Batch create syntax, edit context scope, and copy primary icons,
        to use with Thread together in install events.

        Parameters:
        file_name (str) -- syntax file name, without extension.
        syntax_name (str) -- syntax name, file name and extension.
        """
        self.create_icon_syntax(file_name)
        self.edit_context_scope(syntax_name)
        copy_primary_icons()

    def build_icons_syntaxes(self):
        """
        Batch create syntaxes, edit contexts scopes and copy primary icons,
        to use with Thread together in install events.
        """
        if not os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH):
            os.makedirs(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        # Deleting syntax for 'change_icon_file_extension' and 'create_custom_icon'
        if any(
            syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
            for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
        ):
            self.delete_icons_syntaxes()
        self.create_icons_syntaxes()
        self.edit_contexts_scopes()
        copy_primary_icons()

    def get_list_icons_syntaxes(self, zukan_icons: list) -> list:
        list_all_icons_syntaxes = []

        # 'create_custom_icon' setting
        custom_list = [s for s in generate_custom_icon(zukan_icons) if 'syntax' in s]
        list_all_icons_syntaxes = zukan_icons + custom_list

        return list_all_icons_syntaxes

    def get_compare_scopes(self, zukan_icons: list) -> Set:
        zukan_compare_scopes = compare_scopes(zukan_icons)

        compare_scopes_set = set(
            k['scope'] for k in zukan_compare_scopes if 'scope' in k
        )

        return compare_scopes_set

    def get_sublime_scope_set(self) -> Set:
        syntax_contexts_scope_set = set(c['scope'] for c in CONTEXTS_SCOPES)

        sublime_scope_set = {}
        for s in syntax_contexts_scope_set:
            sublime_scope = sublime.find_syntax_by_scope(s)
            if sublime_scope:
                sublime_scope_set[s] = True
            else:
                sublime_scope_set[s] = False

        # print(sublime_scope_set)
        return sublime_scope_set

    def create_icon_syntax(self, syntax_name: str):
        """
        Create icon sublime-syntax file.

        Parameters:
        syntax_name (str) -- syntax file name, without extension.
        """
        try:
            zukan_icons = self.zukan_icons_data()
            compare_scopes_set = self.get_compare_scopes(zukan_icons)
            change_icon_file_extension = self.change_icon_file_extension_setting()
            ignored_icon = self.ignored_icon_setting()

            list_all_icons_syntaxes = self.get_list_icons_syntaxes(zukan_icons)

            for s in list_all_icons_syntaxes:
                if (
                    any('syntax' in d for d in s)
                    and s.get('syntax') is not None
                    # 'ignored_icon' setting
                    and not (
                        s['name'] in ignored_icon
                        or (
                            # Icon can not exist in 'create_custom_icon' setting
                            # when only creating syntax
                            'preferences' in s
                            and (
                                s['preferences']['settings']['icon'] in ignored_icon
                                or (
                                    s['preferences']['settings']['icon'] + SVG_EXTENSION
                                )
                                in ignored_icon
                                or (
                                    s.get('tag') is not None
                                    and s['tag'] in ignored_icon
                                )
                            )
                        )
                    )
                ):
                    for k in s['syntax']:
                        scope = k.get('scope')

                        if (
                            scope
                            and scope not in compare_scopes_set
                            and k['name'] == syntax_name
                        ):
                            filename = k['name'] + SUBLIME_SYNTAX_EXTENSION

                            # 'change_scope_file_extension' setting
                            k['file_extensions'] = edit_file_extension(
                                k['file_extensions'],
                                k['scope'],
                                change_icon_file_extension,
                            )

                            # file_extensions list can be empty
                            if k['file_extensions']:
                                syntax_filepath = os.path.join(
                                    ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                                )
                                # print(save_sublime_syntax(k, syntax_filepath))
                                save_sublime_syntax(k, syntax_filepath)
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
            # return self.zukan_icons
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def create_icons_syntaxes(self):
        """
        Create icons sublime-syntaxes files.
        """
        try:
            zukan_icons = self.zukan_icons_data()
            compare_scopes_set = self.get_compare_scopes(zukan_icons)
            change_icon_file_extension = self.change_icon_file_extension_setting()
            ignored_icon = self.ignored_icon_setting()

            list_all_icons_syntaxes = self.get_list_icons_syntaxes(zukan_icons)

            for s in list_all_icons_syntaxes:
                if (
                    any('syntax' in d for d in s)
                    and s.get('syntax') is not None
                    # 'ignored_icon' setting
                    and not (
                        s['name'] in ignored_icon
                        or (
                            # Icon can not exist in 'create_custom_icon' setting
                            # when only creating syntax
                            'preferences' in s
                            and (
                                s['preferences']['settings']['icon'] in ignored_icon
                                or (
                                    s['preferences']['settings']['icon'] + SVG_EXTENSION
                                )
                                in ignored_icon
                                or (
                                    s.get('tag') is not None
                                    and s['tag'] in ignored_icon
                                )
                            )
                        )
                    )
                ):
                    for k in s['syntax']:
                        scope = k.get('scope')

                        # if k['scope'] not in compare_scopes_set:
                        if scope and scope not in compare_scopes_set:
                            filename = k['name'] + SUBLIME_SYNTAX_EXTENSION

                            # 'change_scope_file_extension' setting
                            k['file_extensions'] = edit_file_extension(
                                k['file_extensions'],
                                k['scope'],
                                change_icon_file_extension,
                            )

                            # file_extensions list can be empty
                            if k['file_extensions']:
                                syntax_filepath = os.path.join(
                                    ZUKAN_PKG_ICONS_SYNTAXES_PATH, filename
                                )

                                save_sublime_syntax(k, syntax_filepath)

                elif (
                    s['name'] in ignored_icon
                    or s['preferences']['settings']['icon'] in ignored_icon
                    or (s['preferences']['settings']['icon'] + SVG_EXTENSION)
                    in ignored_icon
                    or (s.get('tag') is not None and s['tag'] in ignored_icon)
                ):
                    logger.info('ignored icon %s', s['name'])
            logger.info('sublime-syntaxes created.')

            # return self.zukan_icons
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def delete_icon_syntax(self, syntax_name: str):
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

    def delete_icons_syntaxes(self):
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
            # '.sublime-syntax' not getting deleted. It can exist if 'create_custom_icon'
            # insert empty in 'syntax_name'.
            if os.path.exists(
                os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, SUBLIME_SYNTAX_EXTENSION)
            ):
                os.remove(
                    os.path.join(
                        ZUKAN_PKG_ICONS_SYNTAXES_PATH, SUBLIME_SYNTAX_EXTENSION
                    )
                )
            logger.info('sublime-syntaxes deleted.')
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), s
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), s
            )

    def edit_context_scope(self, syntax_name: str):
        """
        Edit contexts main in zukan icon sublime-syntax file.

        If syntax not installed or disabled, it changes contexts main for empty list.
        This avoid error in console about syntax not found.

        Parameters:
        syntax_name (str) -- icon syntax file name.
        """
        syntax_file = os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, syntax_name)
        # sublime_version = int(sublime.version())

        if os.path.exists(syntax_file):
            logger.info('editing icon context scope if syntax not installed.')

            try:
                with open(syntax_file, 'r') as f:
                    content = f.read()

                regex_contexts_main = (
                    r'contexts:\n\s*main:\n\s*- include: .*?\n\s*'
                    '  apply_prototype: .*?\n'
                )

                sublime_scope_set = self.get_sublime_scope_set()

                contexts_main_scope = content.find('- include: scope:')
                # Need to exclude the apply_prototype line
                if contexts_main_scope != -1:
                    scope_start = contexts_main_scope + len('- include: scope:')
                    scope_end = content.find(' ', scope_start)
                    if scope_end == -1:
                        scope_end = content.find('\n', scope_start)

                    scope = content[scope_start:scope_end].strip()
                else:
                    scope = ''

                # print(scope)

                if sublime_scope_set.get(scope) is True:
                    if self.sublime_version >= 4075:
                        return
                    else:
                        # Could not find other references, got this contexts main
                        # format, for ST versions lower than 4075, from A File
                        # Icon package.
                        include_scope_prop = 'scope:{s}#prototype'.format(s=scope)
                        include_scope = 'scope:{s}'.format(s=scope)

                        contexts_main = (
                            'contexts:\n  main:\n    - include: {p}\n      '
                            'include: {s}\n'.format(
                                p=include_scope_prop, s=include_scope
                            )
                        )

                        content = re.sub(regex_contexts_main, contexts_main, content)
                else:
                    contexts_main = 'contexts:\n  main: []\n'

                    content = re.sub(
                        regex_contexts_main,
                        contexts_main,
                        content,
                    )

                # print(content)

                with open(syntax_file, 'w') as f:
                    f.write(content)

            except FileNotFoundError:
                logger.error(
                    '[Errno %d] %s: %r',
                    errno.ENOENT,
                    os.strerror(errno.ENOENT),
                    syntax_file,
                )
            except OSError:
                logger.error(
                    '[Errno %d] %s: %r',
                    errno.EACCES,
                    os.strerror(errno.EACCES),
                    syntax_file,
                )

    def edit_contexts_scopes(self):
        """
        Edit contexts main in zukan icons sublime-syntax files.

        If syntax not installed or disabled, it changes contexts main for empty list.
        This avoid error in console about syntax not found.
        """
        logger.info('editing icons contexts scopes if syntax not installed.')

        # sublime_version = int(sublime.version())
        installed_syntaxes_list = self.list_created_icons_syntaxes()
        sublime_scope_set = self.get_sublime_scope_set()

        for c in CONTEXTS_SCOPES:
            if sublime_scope_set.get(c['scope']):
                # print(c)
                for i in installed_syntaxes_list:
                    # Change to compat with ST3 contexts main
                    if c['startsWith'] in i and self.sublime_version < 4075:
                        # print(i)
                        edit_contexts_main(
                            os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, i), c['scope']
                        )
            else:
                # Syntaxes not installed or disabled
                for i in installed_syntaxes_list:
                    # Change contexts main empty if not installed or disable
                    if c['startsWith'] in i:
                        # print(i)
                        edit_contexts_main(
                            os.path.join(ZUKAN_PKG_ICONS_SYNTAXES_PATH, i), None
                        )

    def list_created_icons_syntaxes(self) -> list:
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
