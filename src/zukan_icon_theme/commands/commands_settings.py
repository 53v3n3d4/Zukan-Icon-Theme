import errno
import logging
import os
import sublime
import sublime_plugin

from ..lib.icons_themes import ZukanTheme
from ..helpers.clean_data import clean_comments_settings
from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.load_save_settings import (
    get_settings,
    set_save_settings,
    is_zukan_listener_enabled,
)
from ..helpers.read_write_data import read_pickle_data
from ..helpers.remove_empty_dict import remove_empty_dict
from ..helpers.search_themes import search_resources_sublime_themes
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
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_USER_SUBLIME_SETTINGS,
)

logger = logging.getLogger(__name__)

zukan_listener_enabled = is_zukan_listener_enabled()


class ChangeFileExtensionCommand(sublime_plugin.TextCommand):
    """
    Sublime command to change icon file extension.
    """

    def run(
        self, edit, change_file_extension_scope: str, change_file_extension_exts: str
    ):
        change_icon_file_extension = get_settings(
            ZUKAN_SETTINGS, 'change_icon_file_extension'
        )
        if not isinstance(change_icon_file_extension, list):
            logger.warning(
                'change_icon_file_extension option malformed, need to be a list'
            )

        # Required name and icon input
        if not change_file_extension_scope or not change_file_extension_exts:
            dialog_message = 'Scope and file extension inputs are required'
            sublime.error_message(dialog_message)

        if change_file_extension_scope and change_file_extension_exts:
            # Convert change_file_extension_exts to list
            list_change_file_extension_exts = [
                s.strip() for s in change_file_extension_exts.split(',')
            ]
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

                            d['file_extensions'] = (
                                d['file_extensions'] + list_extesnions_difference
                            )
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

                    # File extension exist
                    if change_file_extension_scope != d['scope'] and not set(
                        list_change_file_extension_exts
                    ).isdisjoint(set(d['file_extensions'])):
                        dialog_message = 'File extension present in different scope'
                        sublime.error_message(dialog_message)

                        return None

            # change_icon_file_extension empty
            if not change_icon_file_extension:
                logger.debug('change_icon_file_extension is empty')
                change_icon_file_extension.append(inserted_scope_file_extension)

            # Cleaning duplicated
            file_extensions_list_not_duplicated = [
                f
                for i, f in enumerate(new_scopes_list)
                if new_scopes_list.index(f) == i
            ]

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

    def next_input(self, args):
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

    def next_input(self, args):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class ChangeIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to change icon.
    """

    def run(self, edit, change_icon_name: str, change_icon_file: str):
        change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
        if not isinstance(change_icon, dict):
            logger.warning('change_icon option malformed, need to be a dict')

        inserted_change_icon = {change_icon_name: change_icon_file}

        # Required name and icon input
        if not change_icon_name or not change_icon_file:
            dialog_message = 'Name and icon name inputs are required'
            sublime.error_message(dialog_message)

        if change_icon_name and change_icon_file:
            if (change_icon_name, change_icon_file) not in change_icon.items():
                change_icon.update(inserted_change_icon)
                set_save_settings(ZUKAN_SETTINGS, 'change_icon', change_icon)

                # Check if PNG exist
                primary_file_list = []

                for i in PRIMARY_ICONS:
                    for j in i[2]:
                        primary_file_list.append(j)
                # primary_file_list = [real_name for name, file_name, real_name in PRIMARY_ICONS]

                if (
                    not os.path.exists(
                        os.path.join(
                            ZUKAN_PKG_ICONS_PATH, change_icon_file + PNG_EXTENSION
                        )
                    )
                    # Primary icons list excluded because 'file_type_image-1' does not
                    # exist in 'icons' folder. It is been renamed to 'file_type_image'
                    and change_icon_file not in primary_file_list
                ):
                    dialog_message = (
                        '{i} icon PNGs not found.\n\n'
                        'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                            i=change_icon_name, p=ZUKAN_PKG_ICONS_PATH
                        )
                    )
                    sublime.error_message(dialog_message)

            elif (change_icon_name, change_icon_file) in change_icon.items():
                dialog_message = '{n} icon already in setting "change_icon"'.format(
                    n=change_icon_name
                )
                sublime.error_message(dialog_message)

    def input(self, args: dict):
        if not args.get('change_icon_name'):
            return ChangeIconNameInputHandler()

        if not args.get('change_icon_file'):
            return ChangeIconFileInputHandler()


class ChangeIconNameInputHandler(sublime_plugin.TextInputHandler):
    """
    Return change_icon_name to ChangeIcon.
    """

    def placeholder(self):
        sublime.status_message('Zukan repo has a list of icons name, file-icon.md')
        return 'Type icon name. E.g. Node.js'

    def next_input(self, args):
        if 'change_icon_file' not in args:
            return ChangeIconFileInputHandler()


class ChangeIconFileInputHandler(sublime_plugin.TextInputHandler):
    """
    Return change_icon_file to ChangeIcon.
    """

    def placeholder(self):
        sublime.status_message('Configuration in Zukan Icon Theme > Settings')
        return 'Type icon file name, without extension. E.g. nodejs-1'

    def confirm(self, text):
        self.text = text

    def next_input(self, args):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class CleanCommentsCommand(sublime_plugin.TextCommand):
    """
    Sublime command to clean commanets in Zukan Icon Theme.sublime-settings.
    """

    def run(self, edit):
        clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)


class CreateCustomIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to create custom icon.
    """

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
        create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')
        if not isinstance(create_custom_icon, list):
            logger.warning('create_custom_icon option malformed, need to be a list')

        # Convert create_custom_icon_extensions to list
        list_create_custom_icon_extensions = [
            s.strip() for s in create_custom_icon_extensions.split(',')
        ]
        custom_icon_data = {
            'name': create_custom_icon_name,
            'icon': create_custom_icon_file,
            'syntax_name': create_custom_icon_syntax,
            'scope': create_custom_icon_scope,
            'file_extensions': list_create_custom_icon_extensions,
            'contexts_scope': create_custom_icon_contexts,
        }

        # Required name input
        if not create_custom_icon_name:
            dialog_message = 'Name input is required'
            sublime.error_message(dialog_message)

        if create_custom_icon_name:
            if create_custom_icon:
                for d in create_custom_icon:
                    # print(d)

                    # Name in create_custom_icon, update.
                    if d['name'] == custom_icon_data['name']:
                        # print(d)
                        # Update previous values with custom_icon_data values.
                        if (
                            create_custom_icon_file
                            and d['icon'] != custom_icon_data['icon']
                        ):
                            d['icon'] = custom_icon_data['icon']
                            # print(d['icon'])
                        if (
                            create_custom_icon_syntax
                            and d['syntax_name'] != custom_icon_data['syntax_name']
                        ):
                            d['syntax_name'] = custom_icon_data['syntax_name']
                        if (
                            create_custom_icon_scope
                            and d['scope'] != custom_icon_data['scope']
                        ):
                            d['scope'] = custom_icon_data['scope']
                        if (
                            create_custom_icon_contexts
                            and d['contexts_scope']
                            != custom_icon_data['contexts_scope']
                        ):
                            d['contexts_scope'] = custom_icon_data['contexts_scope']
                        # Handling file_extensions update if not exist in list.
                        if (
                            list_create_custom_icon_extensions
                            and 'file_extensions' in d
                        ):
                            list_extesnions_difference = list(
                                set(list_create_custom_icon_extensions).difference(
                                    d['file_extensions']
                                )
                            )
                            logger.debug(
                                'ading file extensions %s',
                                list_extesnions_difference,
                            )

                            d['file_extensions'] = (
                                d['file_extensions'] + list_extesnions_difference
                            )
                            # print(d['file_extensions'])

                    # Name not in create_custom_icon.
                    if d['name'] != custom_icon_data['name']:
                        # Scope does not exist in create_custom_icon
                        if (
                            not any(
                                d['name'] == create_custom_icon_name
                                for d in create_custom_icon
                            )
                            and create_custom_icon_name != d['name']
                        ):
                            logger.debug(
                                '%s does not exist in create_custom_icon',
                                create_custom_icon_name,
                            )

                            create_custom_icon.append(custom_icon_data)

                        # If syntax_name exist.
                        if (
                            'syntax_name' in d
                            and create_custom_icon_syntax == d['syntax_name']
                        ):
                            dialog_message = (
                                'Syntax name alredy exist in "create_custom_icon"\n\n'
                                'Syntax name should be unique.'
                            )
                            sublime.error_message(dialog_message)

                            return None

                        # If scope different and same file extension.
                        if (
                            'file_extensions' in d
                            and create_custom_icon_scope != d['scope']
                            and not set(list_create_custom_icon_extensions).isdisjoint(
                                set(d['file_extensions'])
                            )
                        ):
                            dialog_message = 'File extension present in different scope'
                            sublime.error_message(dialog_message)

                            return None

            # Check if PNG exist
            primary_file_list = [file_name for name, file_name, *_ in PRIMARY_ICONS]
            if (
                not os.path.exists(
                    os.path.join(
                        ZUKAN_PKG_ICONS_PATH, create_custom_icon_file + PNG_EXTENSION
                    )
                )
                # Primary icons list excluded because 'file_type_image-1' does not
                # exist in 'icons' folder. It is been renamed to 'file_type_image'
                and create_custom_icon_file not in primary_file_list
            ):
                dialog_message = (
                    '{i} icon PNGs not found.\n\n'
                    'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                        i=create_custom_icon_name, p=ZUKAN_PKG_ICONS_PATH
                    )
                )
                sublime.error_message(dialog_message)

            # create_custom_icon empty
            if not create_custom_icon:
                logger.debug('create_custom_icon is empty')
                create_custom_icon.append(custom_icon_data)

            # Remove empty keys.
            complete_list_filtered = remove_empty_dict(create_custom_icon)
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

    def run(self, edit, name: str):
        create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')

        if not name == 'All':
            create_custom_icon_updated = [
                i for i in create_custom_icon if not (i['name'] == name)
            ]
            if zukan_listener_enabled:
                logger.info('deleting %s customized icon', name)

        if name == 'All':
            create_custom_icon_updated = []
            if zukan_listener_enabled:
                logger.info('deleting all customized icon')

        set_save_settings(
            ZUKAN_SETTINGS, 'create_custom_icon', create_custom_icon_updated
        )

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
        create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')
        if not isinstance(create_custom_icon, list):
            logger.warning('create_custom_icon option malformed, need to be a list')

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


class DisableIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to disable icon from a list of Zukan icons.
    """

    def run(self, edit, icon_name: str):
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

        if icon_name not in ignored_icon:
            ignored_icon.append(icon_name)
            sort_list = sorted(ignored_icon)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', sort_list)

            if not icon_name == 'primary':
                logger.info('%s icon ignored', icon_name)
            if icon_name == 'primary':
                logger.info('icons with %s tag ignored', icon_name)

            # Rebuild syntax and preference

    def input(self, args: dict):
        return DisableIconInputHandler()


class DisableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of Zukan icons, and return icon_name to DisableIcon.
    """

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of icons'

    def list_items(self) -> list:
        try:
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            ignored_icon_list = []

            # 'create_custom_icon' setting
            custom_list = [s for s in create_custom_icon() if 'syntax' in s]
            new_list = zukan_icons + custom_list

            for i in new_list:
                if i.get('name') is not None and i.get('name') not in ignored_icon:
                    ignored_icon_list.append(i['name'])
            if ignored_icon_list:
                icon_tag = ['database', 'primary']
                icon_list_with_tag = icon_tag + ignored_icon_list
                return sorted(icon_list_with_tag, key=lambda x: x.upper())

            else:
                raise TypeError(
                    logger.info('all icons are already disabled, list is empty.')
                )
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), i
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), i
            )


class DisableThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to disable theme from a list of installed themes.
    """

    def run(self, edit, theme_st_path: str):
        theme_name = os.path.basename(theme_st_path)
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')

        if theme_name not in ignored_theme:
            ignored_theme.append(theme_name)
            sort_list = sorted(ignored_theme)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_theme', sort_list)
            logger.info('%s ignored', theme_name)

    def input(self, args: dict):
        return DisableThemeInputHandler()


class DisableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of installed themes, excluding ignored themes, and return theme_st_path
    to DisableTheme.
    """

    def name(self) -> str:
        return 'theme_st_path'

    def placeholder(self) -> str:
        return 'List of installed themes'

    def list_items(self) -> list:
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')
        ignored_theme_list = []

        for name in search_resources_sublime_themes():
            file_path, file_name = name.rsplit('/', 1)
            if file_name not in ignored_theme:
                ignored_theme_list.append(name)
        if ignored_theme_list:
            return sorted(ignored_theme_list)
        else:
            raise TypeError(
                logger.info('all themes are already disabled, list is empty.')
            )


class EnableIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to enable icon from a list of ignored icons.
    """

    def run(self, edit, icon_name: str):
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

        if ignored_icon:
            if not icon_name == 'All':
                # Remove icon_name
                ignored_icon = [i for i in ignored_icon if not i == icon_name]
                new_list = sorted(ignored_icon)

                if zukan_listener_enabled:
                    logger.info('enabling %s icon', icon_name)

            if icon_name == 'All':
                new_list = []

                if zukan_listener_enabled:
                    logger.info('enabling all icons')

            set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', new_list)

            # Rebuild syntax and preference

    def input(self, args: dict):
        return EnableIconInputHandler()


class EnableIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored icons, and return icon_name to EnableTheme.
    """

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of ignored icons'

    def list_items(self) -> list:
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
        if not isinstance(ignored_icon, list):
            logger.warning('ignored_icon option malformed, need to be a string list')

        if ignored_icon:
            all_option = ['All']
            new_list = all_option + sorted(ignored_icon, key=lambda x: x.upper())
            return new_list
        else:
            raise TypeError(logger.info('no icons ignored, list is empty.'))


class EnableThemeCommand(sublime_plugin.TextCommand):
    """
    Sublime command to enable theme from a list of ignored themes.
    """

    def run(self, edit, theme_name: str):
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')

        if ignored_theme:
            if not theme_name == 'All':
                # Remove theme_name
                ignored_theme = [t for t in ignored_theme if not t == theme_name]
                new_list = sorted(ignored_theme)

                if zukan_listener_enabled:
                    logger.info('enabling %s', theme_name)

            if theme_name == 'All':
                new_list = []

                if zukan_listener_enabled:
                    logger.info('enabling all themes')

            set_save_settings(ZUKAN_SETTINGS, 'ignored_theme', new_list)

    def input(self, args: dict):
        return EnableThemeInputHandler()


class EnableThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    List of ignored themes, and return theme_name to EnableTheme.
    """

    def name(self) -> str:
        return 'theme_name'

    def placeholder(self) -> str:
        return 'List of ignored themes'

    def list_items(self) -> list:
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')

        if ignored_theme:
            all_option = ['All']
            new_list = all_option + sorted(ignored_theme)
            return new_list
        else:
            raise TypeError(logger.info('no themes ignored, list is empty.'))


class RemovePreferIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to remove prefer icon.
    """

    def run(self, edit, select_prefer_icon_theme: str):
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')

        if prefer_icon:
            if not select_prefer_icon_theme == 'All':
                if select_prefer_icon_theme in prefer_icon.keys():
                    icon_dict_updated = {
                        k: v
                        for k, v in prefer_icon.items()
                        if k != select_prefer_icon_theme
                    }

                    if zukan_listener_enabled:
                        logger.info('reseting icon %s', select_prefer_icon_theme)

            if select_prefer_icon_theme == 'All':
                icon_dict_updated = {}

                if zukan_listener_enabled:
                    logger.info('removing all prefer icons')

            set_save_settings(ZUKAN_SETTINGS, 'prefer_icon', icon_dict_updated)

    def input(self, args: dict):
        return RemovePreferIconInputHandler()


class RemovePreferIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of prefered icons, and return select_prefer_icon_theme to RemovePreferIcon.
    """

    def name(self) -> str:
        return 'select_prefer_icon_theme'

    def placeholder(self) -> str:
        return 'List of prefered icons'

    def list_items(self) -> list:
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')
        if not isinstance(prefer_icon, dict):
            logger.warning('prefer_icon option malformed, need to be a dict')

        if prefer_icon:
            all_option = ['All']

            new_list = all_option + [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(text=i[0], value=i[0], annotation=i[1])
                for i in prefer_icon.items()
            ]

            return new_list

        else:
            raise TypeError(logger.info('no prefer icons to remove, list is empty.'))


class ResetFileExtensionCommand(sublime_plugin.TextCommand):
    """
    Sublime command to reset icon file extension.
    """

    def run(self, edit, scope_name: str):
        change_icon_file_extension = get_settings(
            ZUKAN_SETTINGS, 'change_icon_file_extension'
        )

        if change_icon_file_extension:
            if not scope_name == 'All':
                change_icon_file_extension_updated = [
                    i
                    for i in change_icon_file_extension
                    if not (i['scope'] == scope_name)
                ]

                if zukan_listener_enabled:
                    logger.info('reseting file extensions for %s', scope_name)

            if scope_name == 'All':
                change_icon_file_extension_updated = []

                if zukan_listener_enabled:
                    logger.info('reseting file extensions for all scopes')

            set_save_settings(
                ZUKAN_SETTINGS,
                'change_icon_file_extension',
                change_icon_file_extension_updated,
            )

    def input(self, args: dict):
        return ResetFileExtensionInputHandler()


class ResetFileExtensionInputHandler(sublime_plugin.ListInputHandler):
    """
    List of changed icons file extensions, and return scope_name to ResetFileExtension.
    """

    def name(self) -> str:
        return 'scope_name'

    def placeholder(self) -> str:
        return 'List of changed icons file extensions'

    def list_items(self) -> list:
        change_icon_file_extension = get_settings(
            ZUKAN_SETTINGS, 'change_icon_file_extension'
        )
        if not isinstance(change_icon_file_extension, list):
            logger.warning(
                'change_icon_file_extension option malformed, need to be a list'
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


class ResetIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to reset icon.
    """

    def run(self, edit, icon_name: str):
        change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')

        if change_icon:
            if not icon_name == 'All':
                if icon_name in change_icon.keys():
                    icon_dict_updated = {
                        k: v for k, v in change_icon.items() if k != icon_name
                    }

                    if zukan_listener_enabled:
                        logger.info('reseting icon %s', icon_name)

            if icon_name == 'All':
                icon_dict_updated = {}

                if zukan_listener_enabled:
                    logger.info('reseting all icons')

            set_save_settings(ZUKAN_SETTINGS, 'change_icon', icon_dict_updated)

    def input(self, args: dict):
        return ResetIconInputHandler()


class ResetIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of changed icons, and return icon_name to ResetIcon.
    """

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of changed icons'

    def list_items(self) -> list:
        change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
        if not isinstance(change_icon, dict):
            logger.warning('change_icon option malformed, need to be a dict')

        if change_icon:
            all_option = ['All']
            # change_icon_list = [k for k in change_icon]
            # new_list = all_option + sorted(change_icon_list, key=lambda x: x.upper())

            new_list = all_option + [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(text=i[0], value=i[0], annotation=i[1])
                for i in change_icon.items()
            ]

            return new_list

        else:
            raise TypeError(logger.info('no icons to reset, list is empty.'))


class SelectPreferIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to prefer icon.
    """

    def run(self, edit, select_prefer_icon_theme: str, select_prefer_icon_version: str):
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')

        if not isinstance(prefer_icon, dict):
            logger.warning('prefer_icon option malformed, need to be a dict')

        selected_prefer_icon = {select_prefer_icon_theme: select_prefer_icon_version}

        if select_prefer_icon_theme and select_prefer_icon_version:
            prefer_icon.update(selected_prefer_icon)
            set_save_settings(ZUKAN_SETTINGS, 'prefer_icon', prefer_icon)

    def input(self, args: dict):
        if not args.get('select_prefer_icon_theme'):
            return SelectPreferIconThemeInputHandler()

        if not args.get('select_prefer_icon_version'):
            return SelectPreferIconVersionInputHandler()


class SelectPreferIconThemeInputHandler(sublime_plugin.ListInputHandler):
    """
    Return select_prefer_icon_theme to SelectPreferIcon.
    """

    def name(self) -> str:
        return 'select_prefer_icon_theme'

    def placeholder(self) -> str:
        sublime.status_message('Select theme to prefer icon.')
        return 'List of created themes'

    def list_items(self) -> list:
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')

        if not isinstance(prefer_icon, dict):
            logger.warning('prefer_icon option malformed, need to be a dict')

        if ZukanTheme.list_created_icons_themes():
            # Create a dict with prefer icon value, empty string.
            # Then update with prefer icon to show 'dark' or 'light'
            empty_str = ''
            created_themes_with_prefer_icon = dict.fromkeys(
                ZukanTheme.list_created_icons_themes(), empty_str
            )
            created_themes_with_prefer_icon.update(prefer_icon)

            installed_themes_list = [
                # 'sublime.ListInputItem' since ST 4095
                sublime.ListInputItem(text=k[0], value=k[0], annotation=k[1])
                for k in sorted(created_themes_with_prefer_icon.items())
            ]

            return installed_themes_list
        else:
            raise TypeError(
                logger.info('it does not exist any created theme, list is empty')
            )

    def next_input(self, args):
        if 'select_prefer_icon_theme' not in args:
            return SelectPreferIconVersionInputHandler()


class SelectPreferIconVersionInputHandler(sublime_plugin.ListInputHandler):
    """
    Return select_prefer_icon_version to SelectPreferIcon.
    """

    def name(self) -> str:
        return 'select_prefer_icon_version'

    def placeholder(self) -> str:
        sublime.status_message('Select prefer icon version.')
        return 'Icon options: dark and light'

    def list_items(self) -> list:
        version_opts = ['dark', 'light']
        return version_opts
