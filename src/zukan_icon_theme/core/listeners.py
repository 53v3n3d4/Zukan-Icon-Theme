import logging
import os
import sublime
import sublime_plugin
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.load_save_settings import (
    get_prefer_icon_settings,
    get_settings,
    get_theme_name,
    get_theme_settings,
    is_zukan_restart_message,
    save_current_ui_settings,
)
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_themes import (
    get_sidebar_bgcolor,
    package_theme_exists,
)
from ..helpers.system_theme import system_theme
from ..helpers.color_dark_light import hex_dark_light
from ..helpers.thread_progress import ThreadProgress
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    USER_SETTINGS,
)
from ..utils.zukan_paths import (
    USER_UI_SETTINGS_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
)

logger = logging.getLogger(__name__)


class SchemeTheme:
    def __init__(self):
        self.zukan_preference = ZukanPreference()
        self.zukan_syntax = ZukanSyntax()
        self.zukan_theme = ZukanTheme()

        self.auto_prefer_icon, self.prefer_icon = get_prefer_icon_settings()
        self.ignored_theme, self.auto_install_theme = get_theme_settings()

        self.color_scheme_name = get_settings(USER_SETTINGS, 'color_scheme')
        self.user_ui_settings = read_pickle_data(USER_UI_SETTINGS_FILE)
        self.zukan_restart_message = is_zukan_restart_message()

    def theme_name_setting(self) -> str:
        return get_theme_name()

    def theme_file(self) -> str:
        return os.path.join(ZUKAN_PKG_ICONS_PATH, self.theme_name_setting())

    def get_user_theme(self):
        """
        This function will act, when theme or zukan settings change, then
        create or delete syntaxes and preferences for an icon theme.

        It auto creates themes if setting 'auto_install_theme' is set to True.
        And do not create theme if theme name in 'ignored_theme' setting.

        It also used to select an icon version, dark or light, for a theme.
        """
        theme_name = self.theme_name_setting()
        icon_theme_file = self.theme_file()

        if (
            theme_name not in self.zukan_theme.list_created_icons_themes()
            and self.auto_install_theme is False
        ) or theme_name in self.ignored_theme:
            # Delete preferences to avoid error unable to decode 'icon_file_type'
            # Example of extensions that this errors show: HAML, LICENSE, README,
            # Makefile
            if any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                self.zukan_syntax.delete_icons_syntaxes()
            if any(
                preferences.endswith(TMPREFERENCES_EXTENSION)
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                self.zukan_preference.delete_icons_preferences()

        # 'auto_install_theme' setting
        # Creating icon theme if does not exist.
        if (
            self.auto_install_theme is True
            and not os.path.exists(icon_theme_file)
            and package_theme_exists(theme_name)
            and theme_name not in self.ignored_theme
        ):
            theme_path = sublime.find_resources(theme_name)
            self.zukan_theme.create_icon_theme(theme_path[0])

            if self.zukan_restart_message:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in '
                    'current theme.'
                )
                sublime.message_dialog(dialog_message)

        # Delete unused icon theme files
        self.zukan_theme.delete_unused_icon_theme()

        if (
            theme_name in self.zukan_theme.list_created_icons_themes()
            and theme_name not in self.ignored_theme
        ):
            if not any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ts = threading.Thread(target=self.zukan_syntax.build_icons_syntaxes)
                ts.start()
                ThreadProgress(ts, 'Building zukan files', 'Build done')

            # Build preferences if icons_preferences empty or if theme
            # in 'prefer_icon' option
            if (
                not any(
                    preferences.endswith(TMPREFERENCES_EXTENSION)
                    for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                )
                or (
                    theme_name in self.prefer_icon
                    and not any(d['theme'] == theme_name for d in self.user_ui_settings)
                )
                or (
                    # 'auto_prefer_icon' setting
                    self.auto_prefer_icon is True
                    and theme_name not in self.prefer_icon
                    and (
                        not any(d['theme'] == theme_name for d in self.user_ui_settings)
                        or not any(
                            d['color_scheme'] == self.color_scheme_name
                            for d in self.user_ui_settings
                        )
                    )
                )
            ):
                threading.Thread(
                    target=self.zukan_preference.build_icons_preferences
                ).start()
                # self.zukan_preference.build_icons_preferences()

        # Deleting ignored theme in case it already exists before ignoring.
        if theme_name in self.ignored_theme and os.path.exists(icon_theme_file):
            if self.zukan_restart_message:
                dialog_message = (
                    'You may have to restart ST, for all icons do not show.'
                )
                sublime.message_dialog(dialog_message)
            self.zukan_theme.delete_icon_theme(theme_name)


class SchemeThemeListener(sublime_plugin.ViewEventListener):
    """
    Color scheme and Theme event listener.

    Get the select theme, create/delete zukan files or apply zukan settings
    if needed.
    """

    def on_activated_async(self):
        # Use async: click to select UI Select UI Color Scheme / Theme does not
        # activate. Use 'enter' to select works. Seems happen with other functions.
        # With async seems not occur.

        ignored_theme, auto_install_theme = get_theme_settings()

        color_scheme_background = self.view.style()['background']
        current_color_scheme = self.view.settings().get('color_scheme')
        current_dark_theme = self.view.settings().get('dark_theme')
        current_light_theme = self.view.settings().get('light_theme')
        current_system_theme = system_theme()
        current_theme = self.view.settings().get('theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, current_theme)

        theme_name = current_theme

        if theme_name == 'auto' and not system_theme():
            theme_name = current_light_theme

        if theme_name == 'auto' and system_theme():
            theme_name = current_dark_theme

        # create setting file with current UI if does not exist
        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        # Do not include sidebar_bgcolor to save_current_ui_settings this time
        # Error in find_variables user_ui_settings does not exist
        if not os.path.exists(USER_UI_SETTINGS_FILE):
            save_current_ui_settings(
                color_scheme_background,
                current_color_scheme,
                current_dark_theme,
                current_light_theme,
                current_system_theme,
                current_theme,
            )

        sidebar_bgcolor = get_sidebar_bgcolor(theme_name)

        if os.path.exists(USER_UI_SETTINGS_FILE):
            user_ui_settings = read_pickle_data(USER_UI_SETTINGS_FILE)

            # Get current sidebar background dark/light when adaptive
            scheme_dark_light = hex_dark_light(color_scheme_background)

            if (
                os.path.exists(ZUKAN_PKG_ICONS_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ) and (
                (
                    not any(
                        hex_dark_light(d['background']) == scheme_dark_light
                        for d in user_ui_settings
                    )
                    and (
                        sidebar_bgcolor == scheme_dark_light
                        or sidebar_bgcolor != scheme_dark_light
                    )
                )
                # Adaptive light -> Dark light does not change icons or vice versa.
                or (
                    sidebar_bgcolor != scheme_dark_light
                    and not any(d['theme'] == current_theme for d in user_ui_settings)
                )
                # Avoid change icons between themes with same dark/light background.
                # It does not work for condition above, it is going to pass when
                # sidebar background != scheme background.
                or (
                    not any(
                        d['sidebar_bgcolor'] == sidebar_bgcolor
                        for d in user_ui_settings
                    )
                    and not any(d['theme'] == current_theme for d in user_ui_settings)
                )
                # Theme 'auto' does not change icons.
                or (
                    current_theme == 'auto'
                    and (
                        not any(
                            d['dark_theme'] == current_dark_theme
                            for d in user_ui_settings
                        )
                        or not any(
                            d['light_theme'] == current_light_theme
                            for d in user_ui_settings
                        )
                        or not any(
                            d['system_theme'] == current_system_theme
                            for d in user_ui_settings
                        )
                    )
                )
                or theme_name not in ZukanTheme().list_created_icons_themes()
                or theme_name in ignored_theme
                or (auto_install_theme is True and not os.path.exists(icon_theme_file))
                # Move from ignored theme, need to create files.
                or not any(
                    preferences.endswith(TMPREFERENCES_EXTENSION)
                    for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                )
                or not any(
                    syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                    for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
                )
            ):
                SchemeTheme().get_user_theme()

                logger.debug('SchemeTheme ViewListener on_activated_async')

            # update current UI
            save_current_ui_settings(
                color_scheme_background,
                current_color_scheme,
                current_dark_theme,
                current_light_theme,
                current_system_theme,
                current_theme,
                sidebar_bgcolor,
            )
