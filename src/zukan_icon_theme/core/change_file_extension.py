import logging
import sublime
import sublime_plugin

from ..helpers.load_save_settings import (
    get_change_icon_settings,
    set_save_settings,
    is_zukan_listener_enabled,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)

logger = logging.getLogger(__name__)


class ChangeResetFileExtension:
    def __init__(self):
        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def change_icon_file_extension_setting(self) -> list:
        _, change_icon_file_extension = get_change_icon_settings()
        return change_icon_file_extension

    def message_required_change_file_scope_extension(
        self, change_file_extension_scope: str, change_file_extension_exts: str
    ):
        # Required name and icon input
        if not change_file_extension_scope or not change_file_extension_exts:
            dialog_message = 'Scope and file extension inputs are required'
            sublime.error_message(dialog_message)

    def convert_to_list(self, change_file_extension_exts: str) -> list:
        # Convert change_file_extension_exts to list
        list_change_file_extension_exts = [
            s.strip() for s in change_file_extension_exts.split(',')
        ]

        return list_change_file_extension_exts

    def scope_not_exists(
        self,
        d: dict,
        change_file_extension_scope: str,
        change_icon_file_extension: list,
        new_scopes_list: list,
        inserted_scope_file_extension: dict,
    ):
        # Scope does not exist in change_icon_file_extension
        if (
            not any(
                d['scope'] == change_file_extension_scope
                for d in change_icon_file_extension
            )
            and change_file_extension_scope != d['scope']
        ):
            logger.debug(
                '%s scope does not exist in change_icon_file_extension',
                change_file_extension_scope,
            )

            new_scopes_list.append(inserted_scope_file_extension)
            # print(new_scopes_list)

    def scope_exists(
        self,
        d: dict,
        change_file_extension_scope: str,
        change_file_extension_exts: str,
        change_icon_file_extension: list,
        list_extesnions_difference: list,
    ):
        # Scope exists in change_icon_file_extension
        # Add if file extension does not exist
        if (
            any(
                d['scope'] == change_file_extension_scope
                for d in change_icon_file_extension
            )
            and change_file_extension_scope == d['scope']
        ):
            if list_extesnions_difference:
                logger.debug(
                    '%s scope exists and adding file extensions %s',
                    change_file_extension_scope,
                    list_extesnions_difference,
                )

                d['file_extensions'] = d['file_extensions'] + list_extesnions_difference
                # print(d['file_extensions'])

            if not list_extesnions_difference:
                dialog_message = (
                    '"{s}" and "{f}" already in setting '
                    '"change_icon_file_extension"'.format(
                        s=change_file_extension_scope,
                        f=change_file_extension_exts,
                    )
                )
                sublime.error_message(dialog_message)

    def file_extension_exists(
        self,
        d: dict,
        change_file_extension_scope: str,
        list_change_file_extension_exts: list,
    ):
        if change_file_extension_scope != d['scope'] and not set(
            list_change_file_extension_exts
        ).isdisjoint(set(d['file_extensions'])):
            dialog_message = 'File extension present in different scope'
            sublime.error_message(dialog_message)

            return None

    def cleaning_duplicated(self, new_scopes_list: list) -> list:
        # Cleaning duplicated
        file_extensions_list_not_duplicated = [
            f for i, f in enumerate(new_scopes_list) if new_scopes_list.index(f) == i
        ]

        return file_extensions_list_not_duplicated

    def reset_file_extension(self, change_icon_file_extension: list, scope_name: str):
        change_icon_file_extension = [
            i for i in change_icon_file_extension if not (i['scope'] == scope_name)
        ]

        if self.zukan_listener_enabled:
            logger.info('reseting file extensions for %s', scope_name)

        self._save_change_file_extension_setting(change_icon_file_extension)

    def reset_all_file_extensions(self, change_icon_file_extension: list):
        change_icon_file_extension = []

        if self.zukan_listener_enabled:
            logger.info('reseting file extensions for all scopes')

        self._save_change_file_extension_setting(change_icon_file_extension)

    def _save_change_file_extension_setting(self, change_icon_file_extension: list):
        set_save_settings(
            ZUKAN_SETTINGS,
            'change_icon_file_extension',
            change_icon_file_extension,
        )


class ChangeFileExtensionCommand(sublime_plugin.TextCommand):
    """
    Sublime command to change icon file extension.
    """

    def __init__(self, view):
        super().__init__(view)
        self.change_reset_file_extension = ChangeResetFileExtension()

    def run(
        self, edit, change_file_extension_scope: str, change_file_extension_exts: str
    ):
        change_icon_file_extension = (
            self.change_reset_file_extension.change_icon_file_extension_setting()
        )

        self.change_reset_file_extension.message_required_change_file_scope_extension(
            change_file_extension_scope, change_file_extension_exts
        )

        if change_file_extension_scope and change_file_extension_exts:
            list_change_file_extension_exts = (
                self.change_reset_file_extension.convert_to_list(
                    change_file_extension_exts
                )
            )

            inserted_scope_file_extension = {
                'scope': change_file_extension_scope,
                'file_extensions': list_change_file_extension_exts,
            }
            # Could not work OrderedDict, still insert unordered.
            # inserted_scope_file_extension = OrderedDict(
            #     [
            #         ('scope', change_file_extension_scope),
            #         ('file_extensions', change_file_extension_exts.split(','),
            #     ]
            # )
            new_scopes_list = []

            if change_icon_file_extension:
                for d in change_icon_file_extension:
                    # print(change_icon_file_extension)
                    list_extesnions_difference = list(
                        set(list_change_file_extension_exts).difference(
                            d['file_extensions']
                        )
                    )

                    # Scope does not exist in change_icon_file_extension
                    self.change_reset_file_extension.scope_not_exists(
                        d,
                        change_file_extension_scope,
                        change_icon_file_extension,
                        new_scopes_list,
                        inserted_scope_file_extension,
                    )

                    # Scope exists in change_icon_file_extension
                    # Add if file extension does not exist
                    self.change_reset_file_extension.scope_exists(
                        d,
                        change_file_extension_scope,
                        change_file_extension_exts,
                        change_icon_file_extension,
                        list_extesnions_difference,
                    )

                    # File extension exist
                    self.change_reset_file_extension.file_extension_exists(
                        d,
                        change_file_extension_scope,
                        list_change_file_extension_exts,
                    )

            # change_icon_file_extension empty
            if not change_icon_file_extension:
                logger.debug('change_icon_file_extension is empty')
                change_icon_file_extension.append(inserted_scope_file_extension)

            # Cleaning duplicated
            file_extensions_list_not_duplicated = (
                self.change_reset_file_extension.cleaning_duplicated(new_scopes_list)
            )

            set_save_settings(
                ZUKAN_SETTINGS,
                'change_icon_file_extension',
                change_icon_file_extension + file_extensions_list_not_duplicated,
            )

    def input(self, args: dict):
        if not args.get('change_file_extension_scope'):
            return ChangeFileExtensionScopeInputHandler()

        if not args.get('change_file_extension_exts'):
            return ChangeFileExtensionExtsInputHandler()


class ChangeFileExtensionScopeInputHandler(sublime_plugin.TextInputHandler):
    """
    Return change_file_extension_scope to ChangeFileExtension.
    """

    def placeholder(self):
        sublime.status_message('Scope name to be used')
        return 'Type scope. E.g. source.js'

    def next_input(self, args: dict):
        if 'change_file_extension_exts' not in args:
            return ChangeFileExtensionExtsInputHandler()


class ChangeFileExtensionExtsInputHandler(sublime_plugin.TextInputHandler):
    """
    Return change_file_extension_exts to ChangeFileExtension.
    """

    def placeholder(self):
        sublime.status_message('Icon syntaxes files in "icons_syntaxes" folder')
        return 'Type file extensions, separated by commma. E.g. js, cjs, mjs'

    def confirm(self, text):
        self.text = text

    def next_input(self, args: dict):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class ResetFileExtensionCommand(sublime_plugin.TextCommand):
    """
    Sublime command to reset icon file extension.
    """

    def __init__(self, view):
        super().__init__(view)
        self.change_reset_file_extension = ChangeResetFileExtension()

    def run(self, edit, scope_name: str):
        change_icon_file_extension = (
            self.change_reset_file_extension.change_icon_file_extension_setting()
        )

        if change_icon_file_extension:
            if scope_name == 'All':
                self.change_reset_file_extension.reset_all_file_extensions(
                    change_icon_file_extension
                )

            else:
                self.change_reset_file_extension.reset_file_extension(
                    change_icon_file_extension, scope_name
                )

    def is_enabled(self):
        change_icon_file_extension = (
            self.change_reset_file_extension.change_icon_file_extension_setting()
        )
        return (
            change_icon_file_extension is not None
            and len(change_icon_file_extension) > 0
        )

    def input(self, args: dict):
        return ResetFileExtensionInputHandler(self.change_reset_file_extension)


class ResetFileExtensionInputHandler(sublime_plugin.ListInputHandler):
    """
    List of changed icons file extensions, and return scope_name to ResetFileExtension.
    """

    def __init__(self, change_reset_file_extension: ChangeResetFileExtension):
        self.change_reset_file_extension = change_reset_file_extension

    def name(self) -> str:
        return 'scope_name'

    def placeholder(self) -> str:
        return 'List of changed icons file extensions'

    def list_items(self) -> list:
        change_icon_file_extension = (
            self.change_reset_file_extension.change_icon_file_extension_setting()
        )

        if change_icon_file_extension:
            all_option = ['All']

            # change_icon_file_extension_list = [
            #     d.get('scope') for d in change_icon_file_extension if 'scope' in d
            # ]

            # new_list = all_option + sorted(
            #     change_icon_file_extension_list, key=lambda x: x.upper()
            # )

            change_icon_file_extension_list = [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(
                    text=d.get('scope'),
                    value=d.get('scope'),
                    annotation=(', '.join(map(str, d.get('file_extensions')))),
                )
                for d in sorted(change_icon_file_extension, key=lambda k: k['scope'])
                if 'scope' in d
            ]

            new_list = all_option + change_icon_file_extension_list

            return new_list

        else:
            raise TypeError(
                logger.info('no file extenions for any scope to reset, list is empty.')
            )
