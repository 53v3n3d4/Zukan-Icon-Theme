import logging
import os
import sublime
import sublime_plugin

from ..helpers.load_save_settings import (
    get_change_icon_settings,
    is_zukan_listener_enabled,
    set_save_settings,
)
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


class ChangeResetIcon:
    def __init__(self, zukan_preferences_file: str):
        self.zukan_preferences_file = zukan_preferences_file

        self.icon_path = ZUKAN_PKG_ICONS_PATH
        self.zukan_listener_enabled = is_zukan_listener_enabled()

    def change_icon_setting(self) -> dict:
        change_icon, _ = get_change_icon_settings()
        return change_icon

    def message_required_icon_name_file(
        self, change_icon_name: str, change_icon_file: str
    ):
        # Required name and icon input
        if not change_icon_name or not change_icon_file:
            dialog_message = 'Name and icon name inputs are required'
            sublime.error_message(dialog_message)

    def png_exists(self, change_icon_name: str, change_icon_file: str):
        # Check if PNG exist
        primary_file_list = []

        for i in PRIMARY_ICONS:
            for j in i[2]:
                primary_file_list.append(j)
        # primary_file_list = [real_name for name, file_name, real_name in PRIMARY_ICONS]
        # primary_file_list = [j for i in PRIMARY_ICONS for j in i[2]]

        if (
            not os.path.exists(
                os.path.join(self.icon_path, change_icon_file + PNG_EXTENSION)
            )
            # Primary icons list excluded because 'file_type_image-1' does not
            # exist in 'icons' folder. It is been renamed to 'file_type_image'
            and change_icon_file not in primary_file_list
        ):
            dialog_message = (
                '{i} icon PNGs not found.\n\n'
                'Insert PNGs in 3 sizes ( 18x16, 36x32, 54x48 ) in {p}'.format(
                    i=change_icon_name, p=self.icon_path
                )
            )
            sublime.error_message(dialog_message)

    def message_icon_exists_in_change_icon(self, change_icon_name: str):
        dialog_message = '{n} icon already in setting "change_icon"'.format(
            n=change_icon_name
        )
        sublime.error_message(dialog_message)

    def reset_change_icon(self, change_icon: dict, icon_name: str):
        # icon_dict_updated = {
        #     k: v for k, v in change_icon.items() if k != icon_name
        # }
        del change_icon[icon_name]

        if self.zukan_listener_enabled:
            logger.info('reseting icon %s', icon_name)

        self._save_change_icon_setting(change_icon)

    def reset_all_change_icons(self, change_icon: dict):
        # icon_dict_updated = {}
        change_icon.clear()

        if self.zukan_listener_enabled:
            logger.info('reseting all icons')

        self._save_change_icon_setting(change_icon)

    def _save_change_icon_setting(self, change_icon: dict):
        set_save_settings(self.zukan_preferences_file, 'change_icon', change_icon)


class ChangeIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to change an icon's settings.
    """

    def __init__(self, view):
        super().__init__(view)
        self.change_reset_icon = ChangeResetIcon(ZUKAN_SETTINGS)

    def run(self, edit, change_icon_name: str, change_icon_file: str):
        # change_icon, _ = get_change_icon_settings()
        change_icon = self.change_reset_icon.change_icon_setting()

        inserted_change_icon = {change_icon_name: change_icon_file}

        self.change_reset_icon.message_required_icon_name_file(
            change_icon_name, change_icon_file
        )

        if change_icon_name and change_icon_file:
            if (change_icon_name, change_icon_file) not in change_icon.items():
                change_icon.update(inserted_change_icon)
                set_save_settings(
                    self.change_reset_icon.zukan_preferences_file,
                    'change_icon',
                    change_icon,
                )

                self.change_reset_icon.png_exists(change_icon_name, change_icon_file)

            elif (change_icon_name, change_icon_file) in change_icon.items():
                self.change_reset_icon.message_icon_exists_in_change_icon(
                    change_icon_name
                )

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

    def next_input(self, args: dict):
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

    def next_input(self, args: dict):
        if self.text == 'back':
            return sublime_plugin.BackInputHandler()


class ResetIconCommand(sublime_plugin.TextCommand):
    """
    Sublime command to reset icon.
    """

    def __init__(self, view):
        super().__init__(view)
        self.change_reset_icon = ChangeResetIcon(ZUKAN_SETTINGS)

    def run(self, edit, icon_name: str):
        # change_icon, _ = get_change_icon_settings()
        change_icon = self.change_reset_icon.change_icon_setting()

        if change_icon:
            if icon_name == 'All':
                self.change_reset_icon.reset_all_change_icons(change_icon)

            else:
                if icon_name in change_icon.keys():
                    self.change_reset_icon.reset_change_icon(change_icon, icon_name)

    def is_enabled(self):
        change_reset_icon = self.change_reset_icon.change_icon_setting()
        return change_reset_icon is not None and len(change_reset_icon) > 0

    def input(self, args: dict):
        return ResetIconInputHandler(self.change_reset_icon)


class ResetIconInputHandler(sublime_plugin.ListInputHandler):
    """
    List of changed icons, and return icon_name to ResetIcon.
    """

    def __init__(self, change_reset_icon: ChangeResetIcon):
        self.change_reset_icon = change_reset_icon

    def name(self) -> str:
        return 'icon_name'

    def placeholder(self) -> str:
        return 'List of changed icons'

    def list_items(self) -> list:
        # change_icon, _ = get_change_icon_settings()
        change_icon = self.change_reset_icon.change_icon_setting()

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
