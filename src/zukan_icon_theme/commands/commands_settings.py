import errno
import logging
import os
import sublime
import sublime_plugin

from ..helpers.clean_settings import clean_comments_settings
from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.load_save_settings import get_settings, set_save_settings
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_themes import search_resources_sublime_themes
from ..utils.file_extensions import (
    PNG_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_USER_SUBLIME_SETTINGS,
)

logger = logging.getLogger(__name__)


class ChangeFileExtension(sublime_plugin.TextCommand):
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

        inserted_scope_file_extension = {
            'scope': change_file_extension_scope,
            'file_extensions': [
                s.strip() for s in change_file_extension_exts.split(',')
            ],
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
                    set(
                        [s.strip() for s in change_file_extension_exts.split(',')]
                    ).difference(d['file_extensions'])
                )

                # Scope do not exist in change_icon_file_extension
                # Duplicating new scopes.
                if (
                    not any(
                        d['scope'] == change_file_extension_scope
                        for d in change_icon_file_extension
                    )
                    and change_file_extension_scope != d['scope']
                ):
                    logger.debug(
                        '%s scope does not exist in change_icon_file_extension'
                    )

                    new_scopes_list.append(inserted_scope_file_extension)
                    # print(new_scopes_list)

                # Scope exist in change_icon_file_extension
                # Add if file extension do not exist
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
                        sublime.message_dialog(dialog_message)

        # change_icon_file_extension empty
        if not change_icon_file_extension:
            logger.debug('change_icon_file_extension is empty')
            change_icon_file_extension.append(inserted_scope_file_extension)

        # Cleaning duplicated from new_scopes_list
        file_extensions_list_not_duplicated = [
            f for i, f in enumerate(new_scopes_list) if new_scopes_list.index(f) == i
        ]

        set_save_settings(
            ZUKAN_SETTINGS,
            'change_icon_file_extension',
            change_icon_file_extension + file_extensions_list_not_duplicated,
        )

    def input(self, args):
        if not args.get('change_file_extension_scope'):
            return ChangeFileExtensionScopeInputHandler()

        if not args.get('change_file_extension_exts'):
            return ChangeFileExtensionExtsInputHandler()


class ChangeFileExtensionScopeInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        sublime.status_message('Scope name to be used')
        return 'Type scope. Example: source.js'

    def next_input(self, args):
        if 'change_file_extension_exts' not in args:
            return ChangeFileExtensionExtsInputHandler()


class ChangeFileExtensionExtsInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        sublime.status_message('Icon syntaxes files in "icons_syntaxes" folder')
        return 'Type file extensions, separated by commma. Example: js, cjs, mjs'

    def confirm(self, text):
        self.text = text

    def next_input(self, args):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class ChangeIcon(sublime_plugin.TextCommand):
    """
    Sublime command to change icon.
    """

    def run(self, edit, change_icon_name: str, change_icon_file: str):
        change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
        if not isinstance(change_icon, dict):
            logger.warning('change_icon option malformed, need to be a dict')

        inserted_change_icon = {change_icon_name: change_icon_file}

        if (change_icon_name, change_icon_file) not in change_icon.items():
            change_icon.update(inserted_change_icon)
            set_save_settings(ZUKAN_SETTINGS, 'change_icon', change_icon)

            # Check if PNG exist
            if not os.path.exists(
                os.path.join(ZUKAN_PKG_ICONS_PATH, change_icon_file + PNG_EXTENSION)
            ):
                dialog_message = (
                    '{i} icon PNGs not found.\n\n'
                    'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                        i=change_icon_name, p=ZUKAN_PKG_ICONS_PATH
                    )
                )
                sublime.message_dialog(dialog_message)

            # Check if icon exist

        elif (change_icon_name, change_icon_file) in change_icon.items():
            dialog_message = '{n} icon already in setting "change_icon"'.format(
                n=change_icon_name
            )
            sublime.message_dialog(dialog_message)

    def input(self, args):
        if not args.get('change_icon_name'):
            return ChangeIconNameInputHandler()

        if not args.get('change_icon_file'):
            return ChangeIconFileInputHandler()


class ChangeIconNameInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        sublime.status_message('Zukan repo has a list of icons name, file-icon.md')
        return 'Type icon name. Example: Node.js'

    def next_input(self, args):
        if 'change_icon_file' not in args:
            return ChangeIconFileInputHandler()


class ChangeIconFileInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        sublime.status_message('Configuration in Zukan Icon Theme > Settings')
        return 'Type icon file name, without extension. Example: nodejs-1'

    def confirm(self, text):
        self.text = text

    def next_input(self, args):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class CleanComments(sublime_plugin.TextCommand):
    """
    Sublime command to clean commanets in Zukan Icon Theme.sublime-settings.
    """

    def run(self, edit):
        clean_comments_settings(ZUKAN_USER_SUBLIME_SETTINGS)


class DisableIcon(sublime_plugin.TextCommand):
    """
    Sublime command to disable icon from a list of Zukan icons.
    """

    def run(self, edit, icon_name: str):
        ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')

        if icon_name not in ignored_icon:
            ignored_icon.append(icon_name)
            sort_list = sorted(ignored_icon)
            set_save_settings(ZUKAN_SETTINGS, 'ignored_icon', sort_list)
            logger.info('%s icon ignored', icon_name)

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
                return sorted(ignored_icon_list)
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


class DisableTheme(sublime_plugin.TextCommand):
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


class EnableIcon(sublime_plugin.TextCommand):
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
                logger.info('enabling %s icon', icon_name)

            if icon_name == 'All':
                new_list = []
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
            new_list = all_option + sorted(ignored_icon)
            return new_list
        else:
            raise TypeError(logger.info('no icons ignored, list is empty.'))


class EnableTheme(sublime_plugin.TextCommand):
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
                logger.info('enabling %s', theme_name)

            if theme_name == 'All':
                new_list = []
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


class ResetFileExtension(sublime_plugin.TextCommand):
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
                    i for i in change_icon_file_extension if not (i['scope'] == scope_name)
                ]
                logger.info('reseting file extensions for %s', scope_name)

            if scope_name == 'All':
                change_icon_file_extension_updated = []
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
            change_icon_file_extension_list = [
                d.get('scope') for d in change_icon_file_extension if 'scope' in d
            ]
            new_list = all_option + sorted(change_icon_file_extension_list)
            return new_list

        else:
            raise TypeError(
                logger.info('no file extenions for any scope to reset, list is empty.')
            )


class ResetIcon(sublime_plugin.TextCommand):
    """
    Sublime command to reset icon.
    """

    def run(self, edit, icon_name: str):
        change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')

        if change_icon:
            if not icon_name == 'All':
                if icon_name in change_icon.keys():
                    icon_dict_updated = {k: v for k, v in change_icon.items() if k != icon_name}
                    logger.info('reseting icon %s', icon_name)

            if icon_name == 'All':
                icon_dict_updated = {}
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
            change_icon_list = [k for k in change_icon]
            new_list = all_option + sorted(change_icon_list)
            return new_list

        else:
            raise TypeError(logger.info('no icons to reset, list is empty.'))
