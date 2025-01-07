import logging
import os
import sublime
import sublime_plugin

from ..helpers.load_save_settings import (
    get_create_custom_icon_settings,
    is_zukan_listener_enabled,
    set_save_settings,
)
from ..helpers.remove_empty_dict import remove_empty_dict
from ..utils.file_extensions import (
    PNG_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.primary_icons import (
    PRIMARY_ICONS,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
)

logger = logging.getLogger(__name__)


class CreateDeleteCustomIcon:
    """
    Class to handle creating or updating a custom icon based on user input.
    """

    def __init__(self):
        self.zukan_pkg_icons_path = ZUKAN_PKG_ICONS_PATH
        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def convert_to_list(self, custom_icon_extensions: str):
        # Convert custom_icon_extensions to list
        list_custom_icon_extensions = [
            s.strip() for s in custom_icon_extensions.split(',')
        ]

        return list_custom_icon_extensions

    def message_required_name(self, custom_icon_name: str):
        # Required name input
        if not custom_icon_name:
            dialog_message = 'Name input is required'
            sublime.error_message(dialog_message)

    def custom_icon_name_exists(
        self,
        d: dict,
        custom_icon_data: dict,
        custom_icon_file: str,
        custom_icon_syntax: str,
        custom_icon_scope: str,
        custom_icon_contexts: str,
        list_custom_icon_extensions: list,
    ):
        # Name in create_custom_icon, update.
        if d['name'] == custom_icon_data['name']:
            # print(d)
            # Update previous values with custom_icon_data values.
            if custom_icon_file and d['icon'] != custom_icon_data['icon']:
                d['icon'] = custom_icon_data['icon']
                # print(d['icon'])
            if (
                custom_icon_syntax
                and d['syntax_name'] != custom_icon_data['syntax_name']
            ):
                d['syntax_name'] = custom_icon_data['syntax_name']
            if custom_icon_scope and d['scope'] != custom_icon_data['scope']:
                d['scope'] = custom_icon_data['scope']
            if (
                custom_icon_contexts
                and d['contexts_scope'] != custom_icon_data['contexts_scope']
            ):
                d['contexts_scope'] = custom_icon_data['contexts_scope']
            # Handling file_extensions update if not exist in list.
            if list_custom_icon_extensions and 'file_extensions' in d:
                list_extesnions_difference = list(
                    set(list_custom_icon_extensions).difference(d['file_extensions'])
                )
                logger.debug(
                    'ading file extensions %s',
                    list_extesnions_difference,
                )

                d['file_extensions'] = d['file_extensions'] + list_extesnions_difference
                # print(d['file_extensions'])

    def custom_icon_name_not_exists(
        self,
        d: dict,
        create_custom_icon: list,
        custom_icon_data: dict,
        custom_icon_name: str,
        custom_icon_syntax: str,
        custom_icon_scope: str,
        list_custom_icon_extensions: list,
    ):
        # Name not in create_custom_icon.
        if d['name'] != custom_icon_data['name']:
            # Scope does not exist in create_custom_icon
            if (
                not any(d['name'] == custom_icon_name for d in create_custom_icon)
                and custom_icon_name != d['name']
            ):
                logger.debug(
                    '%s does not exist in create_custom_icon',
                    custom_icon_name,
                )

                create_custom_icon.append(custom_icon_data)

            # If syntax_name exist.
            if 'syntax_name' in d and custom_icon_syntax == d['syntax_name']:
                dialog_message = (
                    'Syntax name alredy exist in "create_custom_icon"\n\n'
                    'Syntax name should be unique.'
                )
                sublime.error_message(dialog_message)

                return None

            # If scope different and same file extension.
            if (
                'file_extensions' in d
                and custom_icon_scope != d['scope']
                and not set(list_custom_icon_extensions).isdisjoint(
                    set(d['file_extensions'])
                )
            ):
                dialog_message = 'File extension present in different scope'
                sublime.error_message(dialog_message)

                return None

    def png_exists(self, custom_icon_file: str):
        # Check if PNG exist
        primary_file_list = [file_name for name, file_name, *_ in PRIMARY_ICONS]
        if (
            not os.path.exists(
                os.path.join(
                    self.zukan_pkg_icons_path, custom_icon_file + PNG_EXTENSION
                )
            )
            # Primary icons list excluded because 'file_type_image-1' does not
            # exist in 'icons' folder. It is been renamed to 'file_type_image'
            and custom_icon_file not in primary_file_list
        ):
            dialog_message = (
                '{i} icon PNGs not found.\n\n'
                'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                    i=custom_icon_file, p=self.zukan_pkg_icons_path
                )
            )
            sublime.error_message(dialog_message)

    def remove_empty_keys(self, create_custom_icon: dict):
        # Remove empty keys.
        complete_list_filtered = remove_empty_dict(create_custom_icon)
        # print(complete_list_filtered)

        return complete_list_filtered

    def delete_custom_icon(self, create_custom_icon: dict, name: str):
        create_custom_icon_updated = [
            i for i in create_custom_icon if not (i['name'] == name)
        ]

        if self.zukan_listener_enabled:
            logger.info('deleting %s customized icon', name)

        self._save_create_custom_icon_setting(create_custom_icon_updated)

    def delete_all_customs_icons(self, create_custom_icon: dict):
        create_custom_icon = []

        if self.zukan_listener_enabled:
            logger.info('deleting all customized icon')

        self._save_create_custom_icon_setting(create_custom_icon)

    def _save_create_custom_icon_setting(self, create_custom_icon: dict):
        set_save_settings(ZUKAN_SETTINGS, 'create_custom_icon', create_custom_icon)


class CreateCustomIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create custom icon.
    """

    def __init__(self, view):
        super().__init__(view)
        self.create_delete_custom_icon = CreateDeleteCustomIcon()

    def run(
        self,
        edit,
        create_custom_icon_name: str,
        create_custom_icon_file: str,
        create_custom_icon_syntax: str,
        create_custom_icon_scope: str,
        create_custom_icon_extensions: str,
        create_custom_icon_contexts: str,
    ):
        create_custom_icon = get_create_custom_icon_settings()

        # Convert create_custom_icon_extensions to list
        list_custom_icon_extensions = self.create_delete_custom_icon.convert_to_list(
            create_custom_icon_extensions
        )

        create_custom_icon_data = {
            'name': create_custom_icon_name,
            'icon': create_custom_icon_file,
            'syntax_name': create_custom_icon_syntax,
            'scope': create_custom_icon_scope,
            'file_extensions': list_custom_icon_extensions,
            'contexts_scope': create_custom_icon_contexts,
        }

        self.create_delete_custom_icon.message_required_name(create_custom_icon_name)

        if create_custom_icon_name:
            if create_custom_icon:
                for d in create_custom_icon:
                    # print(d)

                    # Name in create_custom_icon, update.
                    self.create_delete_custom_icon.custom_icon_name_exists(
                        d,
                        create_custom_icon_data,
                        create_custom_icon_file,
                        create_custom_icon_syntax,
                        create_custom_icon_scope,
                        create_custom_icon_contexts,
                        list_custom_icon_extensions,
                    )

                    # Name not in create_custom_icon.
                    self.create_delete_custom_icon.custom_icon_name_not_exists(
                        d,
                        create_custom_icon,
                        create_custom_icon_data,
                        create_custom_icon_name,
                        create_custom_icon_syntax,
                        create_custom_icon_scope,
                        list_custom_icon_extensions,
                    )

            # Check if PNG exist
            self.create_delete_custom_icon.png_exists(create_custom_icon_file)

            # create_custom_icon empty
            if not create_custom_icon:
                logger.debug('create_custom_icon is empty')
                create_custom_icon.append(create_custom_icon_data)

            # Remove empty keys.
            complete_list_filtered = self.create_delete_custom_icon.remove_empty_keys(
                create_custom_icon
            )
            # print(complete_list_filtered)

            set_save_settings(
                ZUKAN_SETTINGS,
                'create_custom_icon',
                complete_list_filtered,
            )

    def input(self, args: dict):
        if not args.get('create_custom_icon_name'):
            return CreateCustomIconNameInputHandler()

        if not args.get('create_custom_icon_file'):
            return CreateCustomIconFileInputHandler()

        if not args.get('create_custom_icon_syntax'):
            return CreateCustomIconSyntaxInputHandler()

        if not args.get('create_custom_icon_scope'):
            return CreateCustomIconFileInputHandler()

        if not args.get('create_custom_icon_extensions'):
            return CreateCustomIconNameInputHandler()

        if not args.get('create_custom_icon_contexts'):
            return CreateCustomIconFileInputHandler()


class CreateCustomIconNameInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_name to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message('Name is required field.')
        return 'Type a Name. E.g. Pip'

    def next_input(self, args):
        if 'create_custom_icon_file' not in args:
            return CreateCustomIconFileInputHandler()


class CreateCustomIconFileInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_file to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message('Hit enter if field not needed')
        return 'Type icon file name, without extension. E.g. pip'

    def next_input(self, args):
        if 'create_custom_icon_syntax' not in args:
            return CreateCustomIconSyntaxInputHandler()


class CreateCustomIconSyntaxInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_syntax to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message('Type syntax name. E.g. INI (Pip)')
        return 'Type syntax name. E.g. INI (Pip)'

    def next_input(self, args):
        if 'create_custom_icon_scope' not in args:
            return CreateCustomIconScopeInputHandler()


class CreateCustomIconScopeInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_scope to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message('Type scope. E.g. source.ini.pip')
        return 'Type scope. E.g. source.ini.pip'

    def next_input(self, args):
        if 'create_custom_icon_extensions' not in args:
            return CreateCustomIconExtensionsInputHandler()


class CreateCustomIconExtensionsInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_extensions to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message(
            'Type file extensions, separated by commas. E.g. pip.conf'
        )
        return 'Type file extensions, separated by commas. E.g. pip.conf'

    def next_input(self, args):
        if 'create_custom_icon_contexts' not in args:
            return CreateCustomIconContextsInputHandler()


class CreateCustomIconContextsInputHandler(sublime_plugin.TextInputHandler):
    """
    Return create_custom_icon_contexts to CreateCustomIcon.
    """

    def placeholder(self):
        sublime.status_message('Type contexts main. E.g. source.ini')
        return 'Type contexts main. E.g. source.ini'

    def confirm(self, text):
        self.text = text

    def next_input(self, args):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class DeleteCustomIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to delete customized icon.
    """

    def __init__(self, view):
        super().__init__(view)
        self.create_delete_custom_icon = CreateDeleteCustomIcon()

    def run(self, edit, name: str):
        create_custom_icon = get_create_custom_icon_settings()

        if name == 'All':
            self.create_delete_custom_icon.delete_all_customs_icons(create_custom_icon)

        else:
            self.create_delete_custom_icon.delete_custom_icon(create_custom_icon, name)

    def input(self, args: dict):
        return DeleteCustomIconInputHandler()


class DeleteCustomIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of customized icons, and return name to DeleteCustomIcon.
    """

    def name(self) -> str:
        return 'name'

    def placeholder(self) -> str:
        return 'List of customized icons'

    def list_items(self) -> list:
        create_custom_icon = get_create_custom_icon_settings()

        if create_custom_icon:
            all_option = ['All']
            customized_icons_list = [
                d.get('name') for d in create_custom_icon if 'name' in d
            ]
            new_list = all_option + sorted(
                customized_icons_list, key=lambda x: x.upper()
            )
            return new_list

        else:
            raise TypeError(logger.info('customized icon not found, list is empty.'))


# class CreateCustomIcon:
#     """
#     Class to handle creating or updating a custom icon based on user input.
#     """

#     def __init__(
#         self,
#         custom_icon_name: str,
#         custom_icon_file: str,
#         custom_icon_syntax: str,
#         custom_icon_scope: str,
#         custom_icon_extensions: str,
#         custom_icon_contexts: str,
#     ):
#         self.custom_icon_name = custom_icon_name
#         self.custom_icon_file = custom_icon_file
#         self.custom_icon_syntax = custom_icon_syntax
#         self.custom_icon_scope = custom_icon_scope
#         self.custom_icon_extensions = custom_icon_extensions
#         self.custom_icon_contexts = custom_icon_contexts
#         self.create_custom_icon = get_create_custom_icon_settings()

#     def create(self):
#         # Convert create_custom_icon_extensions to list
#         list_create_custom_icon_extensions = [
#             s.strip() for s in self.custom_icon_extensions.split(',')
#         ]

#         custom_icon_data = self._custom_icon_data(list_create_custom_icon_extensions)

#         # Required name input
#         if not self.custom_icon_name:
#             dialog_message = 'Name input is required'
#             sublime.error_message(dialog_message)

#         if self.custom_icon_name:
#             if self._handler_create_custom_icon(
#                 custom_icon_data, list_create_custom_icon_extensions
#             ):
#                 return

#     def _custom_icon_data(self, list_create_custom_icon_extensions):
#         return {
#             'name': self.custom_icon_name,
#             'icon': self.custom_icon_file,
#             'syntax_name': self.custom_icon_syntax,
#             'scope': self.custom_icon_scope,
#             'file_extensions': list_create_custom_icon_extensions,
#             'contexts_scope': self.custom_icon_contexts,
#         }

#     def _handler_create_custom_icon(
#         self, custom_icon_data, list_create_custom_icon_extensions
#     ):
#         # Update previous values with custom_icon_data values.
#         if self.create_custom_icon:
#             for d in self.create_custom_icon:
#                 # print(d)

#                 # Name in create_custom_icon, update.
#                 if d['name'] == self.custom_icon_name:
#                     self._update_icon_fields(
#                         d, custom_icon_data, list_create_custom_icon_extensions
#                     )

#                 # Name not in create_custom_icon.
#                 if d['name'] != custom_icon_data['name']:
#                     self._add_new_scope(d, custom_icon_data)
#                     self._syntax_name_exists(d)
#                     self._file_extension_exists(d, list_create_custom_icon_extensions)

#         self._png_exists()
#         self._create_custom_icon_empty(custom_icon_data)
#         self._remove_empyt_keys()
#         self._save_settings()

#     def _update_icon_fields(
#         self, d, custom_icon_data, list_create_custom_icon_extensions
#     ):
#         # Update previous values with custom_icon_data values.
#         if self.custom_icon_file and d['icon'] != custom_icon_data['icon']:
#             d['icon'] = custom_icon_data['icon']
#             # print(d['icon'])

#         if (
#             self.custom_icon_syntax
#             and d['syntax_name'] != custom_icon_data['syntax_name']
#         ):
#             d['syntax_name'] = custom_icon_data['syntax_name']

#         if self.custom_icon_scope and d['scope'] != custom_icon_data['scope']:
#             d['scope'] = custom_icon_data['scope']

#         if (
#             self.custom_icon_contexts
#             and d['contexts_scope'] != custom_icon_data['contexts_scope']
#         ):
#             d['contexts_scope'] = custom_icon_data['contexts_scope']

#         self._update_file_extensions(d, list_create_custom_icon_extensions)

#     def _update_file_extensions(self, d, list_create_custom_icon_extensions):
#         # extensions_to_add = set(custom_icon_data['file_extensions']) - set(
#         #     icon['file_extensions']
#         # )
#         # if extensions_to_add:
#         #     icon['file_extensions'].extend(extensions_to_add)
#         #     logger.debug(f'Adding file extensions {extensions_to_add}')

#         # Handling file_extensions update if not exist in list.
#         if list_create_custom_icon_extensions and 'file_extensions' in d:
#             list_extesnions_difference = list(
#                 set(list_create_custom_icon_extensions).difference(d['file_extensions'])
#             )
#             logger.debug(
#                 'ading file extensions %s',
#                 list_extesnions_difference,
#             )

#             d['file_extensions'] = d['file_extensions'] + list_extesnions_difference
#             # print(d['file_extensions'])

#     def _add_new_scope(self, d, custom_icon_data):
#         # Scope does not exist in create_custom_icon
#         if (
#             not any(d['name'] == self.custom_icon_name for d in self.create_custom_icon)
#             and self.custom_icon_name != d['name']
#         ):
#             logger.debug(
#                 '%s does not exist in create_custom_icon',
#                 self.custom_icon_name,
#             )

#             self.create_custom_icon.append(custom_icon_data)

#     def _syntax_name_exists(self, d):
#         # If syntax_name exist.
#         if 'syntax_name' in d and self.custom_icon_syntax == d['syntax_name']:
#             dialog_message = (
#                 'Syntax name alredy exist in "create_custom_icon"\n\n'
#                 'Syntax name should be unique.'
#             )
#             sublime.error_message(dialog_message)

#             return None

#     def _file_extension_exists(self, d, list_create_custom_icon_extensions):
#         # If scope different and same file extension.
#         if (
#             'file_extensions' in d
#             and self.custom_icon_scope != d['scope']
#             and not set(list_create_custom_icon_extensions).isdisjoint(
#                 set(d['file_extensions'])
#             )
#         ):
#             dialog_message = 'File extension present in different scope'
#             sublime.error_message(dialog_message)

#             return None

#     def _png_exists(self):
#         # Check if PNG exist
#         primary_file_list = [file_name for name, file_name, *_ in PRIMARY_ICONS]
#         if (
#             not os.path.exists(
#                 os.path.join(
#                     ZUKAN_PKG_ICONS_PATH, self.custom_icon_file + PNG_EXTENSION
#                 )
#             )
#             # Primary icons list excluded because 'file_type_image-1' does not
#             # exist in 'icons' folder. It is been renamed to 'file_type_image'
#             and self.custom_icon_file not in primary_file_list
#         ):
#             dialog_message = (
#                 '{i} icon PNGs not found.\n\n'
#                 'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
#                     i=self.custom_icon_name, p=ZUKAN_PKG_ICONS_PATH
#                 )
#             )
#             sublime.error_message(dialog_message)

#     def _create_custom_icon_empty(self, custom_icon_data):
#         # create_custom_icon empty
#         if not self.create_custom_icon:
#             logger.debug('create_custom_icon is empty')
#             self.create_custom_icon.append(custom_icon_data)

#     def _remove_empyt_keys(self):
#         # Remove empty keys.
#         complete_list_filtered = remove_empty_dict(self.create_custom_icon)
#         # print(complete_list_filtered)

#         return complete_list_filtered

#     def _save_settings(self, complete_list_filtered):
#         set_save_settings(
#             ZUKAN_SETTINGS,
#             'create_custom_icon',
#             complete_list_filtered,
#         )


# class CreateCustomIconCommand(sublime_plugin.TextCommand):
#     """
#     Sublime command to create or update a custom icon.
#     """

#     def run(self, edit, **args):
#         """
#         Run the command to create or update a custom icon.
#         """
#         custom_icon = CreateCustomIcon(**args)
#         custom_icon.create()

#     def input(self, args: dict):
#         if not args.get('create_custom_icon_name'):
#             return CreateCustomIconNameInputHandler()

#         if not args.get('create_custom_icon_file'):
#             return CreateCustomIconFileInputHandler()

#         if not args.get('create_custom_icon_syntax'):
#             return CreateCustomIconSyntaxInputHandler()

#         if not args.get('create_custom_icon_scope'):
#             return CreateCustomIconFileInputHandler()

#         if not args.get('create_custom_icon_extensions'):
#             return CreateCustomIconNameInputHandler()

#         if not args.get('create_custom_icon_contexts'):
#             return CreateCustomIconFileInputHandler()


# class CreateCustomIconNameInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_name to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message('Name is required field.')
#         return 'Type a Name. E.g. Pip'

#     def next_input(self, args):
#         if 'create_custom_icon_file' not in args:
#             return CreateCustomIconFileInputHandler()


# class CreateCustomIconFileInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_file to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message('Hit enter if field not needed')
#         return 'Type icon file name, without extension. E.g. pip'

#     def next_input(self, args):
#         if 'create_custom_icon_syntax' not in args:
#             return CreateCustomIconSyntaxInputHandler()


# class CreateCustomIconSyntaxInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_syntax to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message('Type syntax name. E.g. INI (Pip)')
#         return 'Type syntax name. E.g. INI (Pip)'

#     def next_input(self, args):
#         if 'create_custom_icon_scope' not in args:
#             return CreateCustomIconScopeInputHandler()


# class CreateCustomIconScopeInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_scope to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message('Type scope. E.g. source.ini.pip')
#         return 'Type scope. E.g. source.ini.pip'

#     def next_input(self, args):
#         if 'create_custom_icon_extensions' not in args:
#             return CreateCustomIconExtensionsInputHandler()


# class CreateCustomIconExtensionsInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_extensions to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message(
#             'Type file extensions, separated by commas. E.g. pip.conf'
#         )
#         return 'Type file extensions, separated by commas. E.g. pip.conf'

#     def next_input(self, args):
#         if 'create_custom_icon_contexts' not in args:
#             return CreateCustomIconContextsInputHandler()


# class CreateCustomIconContextsInputHandler(sublime_plugin.TextInputHandler):
#     """
#     Return create_custom_icon_contexts to CreateCustomIcon.
#     """

#     def placeholder(self):
#         sublime.status_message('Type contexts main. E.g. source.ini')
#         return 'Type contexts main. E.g. source.ini'

#     def confirm(self, text):
#         self.text = text

#     def next_input(self, args):
#         if self.text == 'back':
#             return sublime_plugin.BackInputHandler()


# class DeleteCustomIcon:
#     def __init__(self, name: str):
#         self.name = name
#         self.create_custom_icon = get_create_custom_icon_settings()

#     def delete(self):
#         """
#         Deletes a custom icon by name or all custom icons.
#         """
#         if self.name == 'All':
#             self._delete_all_customized_icons()
#         else:
#             self._delete_customized_icon()

#         self._save_create_custom_icon()

#     def _delete_customized_icon(self):
#         self.create_custom_icon = [
#             i for i in self.create_custom_icon if not (i['name'] == self.name)
#         ]
#         if self.zukan_listener_enabled:
#             logger.info('deleting %s customized icon', self.name)

#     def _delete_all_customized_icons(self):
#         self.create_custom_icon = []
#         if self.zukan_listener_enabled:
#             logger.info('deleting all customized icon')

#     def _save_create_custom_icon(self):
#         set_save_settings(ZUKAN_SETTINGS, 'create_custom_icon', self.create_custom_icon)


# class DeleteCustomIconCommand(sublime_plugin.TextCommand):
#     """
#     Sublime command to delete customized icon.
#     """

#     def run(self, edit, name: str):
#         delete_custom_icon = DeleteCustomIcon(name)
#         delete_custom_icon.delete()

#     def input(self, args: dict):
#         return DeleteCustomIconInputHandler()


# class DeleteCustomIconInputHandler(sublime_plugin.ListInputHandler):
#     """
#     List of customized icons, and return name to DeleteCustomIcon.
#     """

#     def name(self) -> str:
#         return 'name'

#     def placeholder(self) -> str:
#         return 'List of customized icons'

#     def list_items(self) -> list:
#         create_custom_icon = get_create_custom_icon_settings()

#         if create_custom_icon:
#             all_option = ['All']
#             customized_icons_list = [
#                 d.get('name') for d in create_custom_icon if 'name' in d
#             ]
#             new_list = all_option + sorted(
#                 customized_icons_list, key=lambda x: x.upper()
#             )
#             return new_list

#         else:
#             raise TypeError(logger.info('customized icon not found, list is empty.'))
