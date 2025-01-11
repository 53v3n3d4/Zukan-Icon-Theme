import logging
import os
import sublime
import sublime_plugin

from ..helpers.edit_file_extension import edit_file_extension
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_syntaxes import compare_scopes
from ..lib.icons_syntaxes import ZukanSyntax
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
)

logger = logging.getLogger(__name__)


class Syntaxes(ZukanSyntax):
    """
    Syntaxes list, install and delete.
    """

    def __init__(self, syntaxes_path: str, sublime_syntax_extension: str):
        ZukanSyntax.__init__(self)

        self.syntaxes_path = syntaxes_path
        self.sublime_syntax_extension = sublime_syntax_extension

    def delete_single_icon_syntax(self, syntax_name: str):
        self.delete_icon_syntax(syntax_name)

    def delete_all_icons_syntaxes(self):
        self.delete_icons_syntaxes()

    def get_installed_syntaxes(self):
        installed_syntaxes_list = sorted(
            self.list_created_icons_syntaxes(), key=lambda x: x.upper()
        )
        return sorted(installed_syntaxes_list)

    def get_not_installed_syntaxes(self):
        zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

        list_syntaxes_not_installed = []
        list_all_icons_syntaxes = self.get_list_icons_syntaxes(zukan_icons)

        # zukan_icons = read_pickle_data(self.icons_data_file)

        # # 'create_custom_icon' setting
        # custom_list = [s for s in generate_custom_icon() if 'syntax' in s]
        # new_list = zukan_icons + custom_list

        for s in list_all_icons_syntaxes:
            if s.get('syntax') is not None:
                for k in s['syntax']:
                    if k not in compare_scopes(zukan_icons):
                        # 'change_file_extension' setting
                        k['file_extensions'] = edit_file_extension(
                            k['file_extensions'], k['scope']
                        )
                        # file_extensions list can be empty
                        if k['file_extensions']:
                            list_syntaxes_not_installed.append(
                                k['name'] + self.sublime_syntax_extension
                            )
        list_syntaxes_not_installed = list(
            set(list_syntaxes_not_installed).difference(
                self.list_created_icons_syntaxes()
            )
        )

        return list_syntaxes_not_installed

    def install_icon_syntax(self, syntax_name: str):
        file_name, _ = os.path.splitext(syntax_name)
        # ZukanSyntax.create_icon_syntax(file_name)
        # Edit icon syntax contexts main if syntax not installed or ST3.
        # ZukanSyntax.edit_context_scope(syntax_name)
        # 'ignored_icon' setting

        # ignored_icon = get_ignored_icon_settings()

        zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

        # # 'create_custom_icon' setting
        # custom_list = [s for s in generate_custom_icon() if 'syntax' in s]
        # new_list = zukan_icons + custom_list

        list_all_icons_syntaxes = self.get_list_icons_syntaxes(zukan_icons)

        for d in list_all_icons_syntaxes:
            if 'syntax' in d:
                for s in d['syntax']:
                    if s['name'] == file_name and d['name'] in self.ignored_icon:
                        dialog_message = (
                            '{i} icon is disabled. Need to enable first.'.format(
                                i=d['name']
                            )
                        )
                        sublime.message_dialog(dialog_message)

        self.install_syntax(file_name, syntax_name)

    def install_all_icons_syntaxes(self):
        self.install_syntaxes()

    def confirm_delete(self, message: str):
        return sublime.ok_cancel_dialog(message)


class DeleteSyntaxCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete syntax from a list of created syntaxes.
    """

    def __init__(self, view):
        super().__init__(view)
        self.syntaxes = Syntaxes(
            ZUKAN_PKG_ICONS_SYNTAXES_PATH,
            SUBLIME_SYNTAX_EXTENSION,
        )

    def run(self, edit, syntax_name: str):
        if syntax_name == 'All':
            dialog_message = (
                "Are you sure you want to delete all syntaxes in '{f}'?".format(
                    f=self.syntaxes.syntaxes_path
                )
            )
            if self.syntaxes.confirm_delete(dialog_message):
                self.syntaxes.delete_all_icons_syntaxes()

        else:
            dialog_message = "Are you sure you want to delete '{s}'?".format(
                s=os.path.join(self.syntaxes.syntaxes_path, syntax_name)
            )
            if self.syntaxes.confirm_delete(dialog_message):
                self.syntaxes.delete_single_icon_syntax(syntax_name)

    def input(self, args: dict):
        # print(args)
        return DeleteSyntaxInputHandler(self.syntaxes)


class DeleteSyntaxInputHandler(sublime_plugin.ListInputHandler):
    """
    List of created syntaxes and return syntax_name to DeleteSyntax.
    """

    def __init__(self, syntaxes):
        self.syntaxes = syntaxes

    def name(self) -> str:
        return 'syntax_name'

    def placeholder(self) -> str:
        return 'List of created syntaxes'

    def list_items(self) -> list:
        installed_syntaxes_list = self.syntaxes.get_installed_syntaxes()

        if installed_syntaxes_list:
            all_option = ['All']
            installed_syntaxes_list = sorted(
                installed_syntaxes_list, key=lambda x: x.upper()
            )
            new_list = all_option + installed_syntaxes_list
            return new_list
        else:
            raise TypeError(
                logger.info('it does not exist any created syntax, list is empty')
            )


class InstallSyntaxCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create syntax from zukan syntaxes list.
    """

    def __init__(self, view):
        super().__init__(view)
        self.syntaxes = Syntaxes(
            ZUKAN_PKG_ICONS_SYNTAXES_PATH,
            SUBLIME_SYNTAX_EXTENSION,
        )

    def run(self, edit, syntax_name: str):
        if syntax_name == 'All':
            self.syntaxes.install_all_icons_syntaxes()
        else:
            self.syntaxes.install_icon_syntax(syntax_name)

    def input(self, args: dict):
        return InstallSyntaxInputHandler(self.syntaxes)


class InstallSyntaxInputHandler(sublime_plugin.ListInputHandler):
    """
    Zukan syntaxes list, created syntaxes excluded, and return syntax_name
    to InstallSyntax.
    """

    def __init__(self, syntaxes):
        self.syntaxes = syntaxes

    def name(self) -> str:
        return 'syntax_name'

    def placeholder(self) -> str:
        return 'Zukan syntaxes list'

    def list_items(self) -> list:
        list_syntaxes_not_installed = self.syntaxes.get_not_installed_syntaxes()

        if list_syntaxes_not_installed:
            all_option = ['All']
            syntaxes_list = sorted(list_syntaxes_not_installed, key=lambda x: x.upper())
            new_list = all_option + syntaxes_list
            return new_list
        else:
            raise TypeError(
                logger.info('all syntaxes are already created, list is empty.')
            )
