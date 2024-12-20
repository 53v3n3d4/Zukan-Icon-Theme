import logging
import os
import sublime
import sublime_plugin
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.delete_unused import delete_unused_icon_theme
from ..helpers.load_save_settings import (
    get_prefer_ignore_icon_settings,
    get_settings,
    get_theme_name,
    get_theme_settings,
    save_current_ui_settings,
)
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_themes import (
    get_sidebar_bgcolor,
    package_theme_exists,
)
from ..helpers.system_theme import system_theme
from ..helpers.theme_dark_light import scheme_background_dark_light
from ..helpers.thread_progress import ThreadProgress
from ..utils.file_extensions import (
    SUBLIME_SYNTAX_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    USER_SETTINGS,
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    USER_UI_SETTINGS_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
    ZUKAN_PKG_SUBLIME_PATH,
)

logger = logging.getLogger(__name__)


class ThemeListener:
    def get_user_theme():
        """
        This function will act, when theme or zukan settings change, then
        create or delete syntaxes and preferences for a icon theme.

        It auto creates themes if setting 'auto_install_theme' is set to True.
        And do not create theme if theme name in 'ignored_theme' setting.

        It also used to select an icon version, dark or light, for a theme.
        """
        logger.debug('Preferences.sublime-settings changed')

        auto_install_theme, ignored_theme = get_theme_settings()
        auto_prefer_icon, prefer_icon, _ = get_prefer_ignore_icon_settings()

        color_scheme_name = get_settings(USER_SETTINGS, 'color_scheme')
        user_ui_settings = read_pickle_data(USER_UI_SETTINGS_FILE)
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        theme_name = get_theme_name()
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)

        if not isinstance(ignored_theme, list):
            logger.warning('ignored_theme option malformed, need to be a string list')

        if (
            theme_name not in ZukanTheme.list_created_icons_themes()
            and auto_install_theme is False
        ) or theme_name in ignored_theme:
            # Delete preferences to avoid error unable to decode 'icon_file_type'
            # Example of extensions that this errors show: HAML, LICENSE, README,
            # Makefile
            if any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ZukanSyntax.delete_icons_syntaxes()
            if any(
                preferences.endswith(TMPREFERENCES_EXTENSION)
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                ZukanPreference.delete_icons_preferences()

        # 'auto_install_theme' setting
        # Creating icon theme if does not exist.
        if (
            auto_install_theme is True
            and not os.path.exists(icon_theme_file)
            and package_theme_exists(theme_name)
            and theme_name not in ignored_theme
        ):
            theme_path = sublime.find_resources(theme_name)
            ZukanTheme.create_icon_theme(theme_path[0])

            if zukan_restart_message is True:
                dialog_message = (
                    'You may have to restart ST, if all icons do not load in '
                    'current theme.'
                )
                sublime.message_dialog(dialog_message)

        # Delete unused icon theme files
        delete_unused_icon_theme()

        if (
            theme_name in ZukanTheme.list_created_icons_themes()
            and theme_name not in ignored_theme
        ):
            # Build preferences if icons_preferences empty or if theme
            # in 'prefer_icon' option
            if (
                not any(
                    preferences.endswith(TMPREFERENCES_EXTENSION)
                    for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                )
                or (
                    theme_name in prefer_icon
                    and not any(d['theme'] == theme_name for d in user_ui_settings)
                )
                or (
                    # 'auto_prefer_icon' setting
                    auto_prefer_icon is True
                    and theme_name not in prefer_icon
                    and (
                        not any(d['theme'] == theme_name for d in user_ui_settings)
                        or not any(
                            d['color_scheme'] == color_scheme_name
                            for d in user_ui_settings
                        )
                    )
                )
            ):
                threading.Thread(target=ZukanPreference.build_icons_preferences).start()

            if not any(
                syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ):
                ts = threading.Thread(target=ZukanSyntax.build_icons_syntaxes)
                ts.start()
                ThreadProgress(ts, 'Building zukan files', 'Build done')

        # Deleting ignored theme in case it already exists before ignoring.
        if theme_name in ignored_theme and os.path.exists(icon_theme_file):
            if zukan_restart_message is True:
                dialog_message = (
                    'You may have to restart ST, for all icons do not show.'
                )
                sublime.message_dialog(dialog_message)
            ZukanTheme.delete_icon_theme(theme_name)


class SchemeThemeListener(sublime_plugin.ViewEventListener):
    """
    Color scheme and Theme event listener.

    Get the select theme, create/delete zukan files or apply zukan settings
    if needed.
    """

    def on_activated_async(self):
        # Use async: click to select UI Select UI Color Scheme / Theme does not
        # activate. Use 'enter' to select works. Seems happen with other functions.
        # With async seems not occurr.

        auto_install_theme, ignored_theme = get_theme_settings()

        color_scheme_background = self.view.style()['background']
        current_color_scheme = self.view.settings().get('color_scheme')
        current_dark_theme = self.view.settings().get('dark_theme')
        current_light_theme = self.view.settings().get('light_theme')
        current_theme = self.view.settings().get('theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, current_theme)

        # Get system theme
        theme_name = current_theme

        if theme_name == 'auto' and not system_theme():
            theme_name = current_light_theme

        if theme_name == 'auto' and system_theme():
            theme_name = current_dark_theme

        # create setting file with current ui if does not exist
        if not os.path.exists(ZUKAN_PKG_SUBLIME_PATH):
            os.makedirs(ZUKAN_PKG_SUBLIME_PATH)

        if not os.path.exists(USER_UI_SETTINGS_FILE):
            save_current_ui_settings(
                color_scheme_background,
                current_color_scheme,
                current_dark_theme,
                current_light_theme,
                current_theme,
            )

        # Do not save sidebar_bgcolor to save_current_ui_settings this time
        # Error in find_variables user_ui_settings does not exist
        theme_st_path = sublime.find_resources(theme_name)
        sidebar_bgcolor = get_sidebar_bgcolor(theme_st_path)

        if os.path.exists(USER_UI_SETTINGS_FILE):
            user_ui_settings = read_pickle_data(USER_UI_SETTINGS_FILE)

            # Get current sidebar when color scheme change
            scheme_dark_light = scheme_background_dark_light(color_scheme_background)

            if (
                os.path.exists(ZUKAN_PKG_ICONS_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ) and (
                # Need fix: entering get_user_theme when sidebar dark/light do not changed,
                # color-scheme dark/light changed, not adaptive, changing when move from
                # color-scheme dark -> light.
                # Background color-scheme issue because it is used in find_variables getting
                # from file. In this case, color-scheme changing before updating file.
                not any(
                    d['sidebar_bgcolor'][0] == sidebar_bgcolor[0]
                    for d in user_ui_settings
                )
                or not any(
                    scheme_background_dark_light(d['background']) == scheme_dark_light
                    for d in user_ui_settings
                )
                or theme_name not in ZukanTheme.list_created_icons_themes()
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
                ThemeListener.get_user_theme()
                logger.debug('SchemeTheme ViewListener on_activated_async')

            # update current ui
            save_current_ui_settings(
                color_scheme_background,
                current_color_scheme,
                current_dark_theme,
                current_light_theme,
                current_theme,
                sidebar_bgcolor,
            )
