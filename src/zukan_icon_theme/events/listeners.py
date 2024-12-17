import logging
import os
import sublime
import sublime_plugin
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.load_save_settings import get_settings
from ..helpers.read_write_data import dump_pickle_data, read_pickle_data
from ..helpers.search_themes import (
    package_theme_exists,
    search_resources_sublime_themes,
)
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
    USER_CURRENT_UI_FILE,
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PKG_ICONS_SYNTAXES_PATH,
)

logger = logging.getLogger(__name__)


def save_current_ui_settings(
    color_scheme_background: str, current_theme: str, current_color_scheme: str
):
    """
    Save current user UI theme and color-scheme.

    Parameters:
    color_scheme_background (str) - color scheme background.
    current_theme (str) -- user theme in Preferences.
    current_color_scheme (str) -- user color-scheme in Preferences.
    """
    current_ui_settings = {}
    current_ui_settings.update({'background': color_scheme_background})
    current_ui_settings.update({'theme': current_theme})
    current_ui_settings.update({'color_scheme': current_color_scheme})

    if os.path.exists(USER_CURRENT_UI_FILE):
        # Delete previous pickle file
        os.remove(USER_CURRENT_UI_FILE)

    dump_pickle_data(current_ui_settings, USER_CURRENT_UI_FILE)


def delete_unused_icon_theme():
    """
    Delete unused icon theme file.

    When uninstall a theme package, it leaves an icon-theme file.
    """
    list_all_themes = search_resources_sublime_themes()
    list_icon_themes = ZukanTheme.list_created_icons_themes()

    list_themes = []

    for t in list_all_themes:
        n = os.path.basename(t)
        list_themes.append(n)

    list_unused_icon_themes = list(set(list_icon_themes) - set(list_themes))

    for o in list_unused_icon_themes:
        logger.info('removing unused zukan icon theme, %s', o)
        ZukanTheme.delete_icon_theme(o)


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

        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        auto_prefer_icon = get_settings(ZUKAN_SETTINGS, 'auto_prefer_icon')
        color_scheme_name = get_settings(USER_SETTINGS, 'color_scheme')
        data = read_pickle_data(USER_CURRENT_UI_FILE)
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')
        theme_name = get_settings(USER_SETTINGS, 'theme')
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

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
                    and not any(d['theme'] == theme_name for d in data)
                )
                or (
                    # 'auto_prefer_icon' setting
                    auto_prefer_icon is True
                    and theme_name not in prefer_icon
                    and (
                        not any(d['theme'] == theme_name for d in data)
                        or not any(d['color_scheme'] == color_scheme_name for d in data)
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

        color_scheme_background = self.view.style()['background']
        current_color_scheme = self.view.settings().get('color_scheme')
        current_theme = self.view.settings().get('theme')

        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, current_theme)

        # create setting file with current ui if does not exist
        if not os.path.exists(USER_CURRENT_UI_FILE):
            save_current_ui_settings(
                color_scheme_background, current_theme, current_color_scheme
            )

        if os.path.exists(USER_CURRENT_UI_FILE):
            data = read_pickle_data(USER_CURRENT_UI_FILE)

            if (
                os.path.exists(ZUKAN_PKG_ICONS_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                and os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
            ) and (
                not any(d['theme'] == current_theme for d in data)
                or not any(d['color_scheme'] == current_color_scheme for d in data)
                or current_theme not in ZukanTheme.list_created_icons_themes()
                or current_theme in ignored_theme
                or (auto_install_theme is True and not os.path.exists(icon_theme_file))
                # Check user theme, if has to delete or create zukan files.
                or (
                    (
                        current_theme in ZukanTheme.list_created_icons_themes()
                        and current_theme not in ignored_theme
                        and os.path.exists(ZUKAN_PKG_ICONS_PATH)
                        and os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
                        and os.path.exists(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
                    )
                    and (
                        not any(
                            preferences.endswith(TMPREFERENCES_EXTENSION)
                            for preferences in os.listdir(
                                ZUKAN_PKG_ICONS_PREFERENCES_PATH
                            )
                        )
                        or not any(
                            syntax.endswith(SUBLIME_SYNTAX_EXTENSION)
                            for syntax in os.listdir(ZUKAN_PKG_ICONS_SYNTAXES_PATH)
                        )
                    )
                )
            ):
                ThemeListener.get_user_theme()
                logger.debug('SchemeTheme ViewListener on_activated_async')

                # update current ui
                save_current_ui_settings(
                    color_scheme_background, current_theme, current_color_scheme
                )
