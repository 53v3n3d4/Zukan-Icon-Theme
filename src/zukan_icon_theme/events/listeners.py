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


def save_current_ui_settings(current_theme: str, current_color_scheme: str):
    current_ui_settings = {}
    current_ui_settings.update({'theme': current_theme})
    current_ui_settings.update({'color_scheme': current_color_scheme})

    if os.path.exists(USER_CURRENT_UI_FILE):
        # Delete previous pickle file
        os.remove(USER_CURRENT_UI_FILE)

    dump_pickle_data(current_ui_settings, USER_CURRENT_UI_FILE)


def remove_orphan_icon_theme():
    """
    Remove orphan icon theme file.
    """

    # Compare a list of installed themes to a list of
    # created icon themes.
    # Remove icon themes files that are not present
    # in installed themes
    list_all_themes = search_resources_sublime_themes()
    list_icon_themes = ZukanTheme.list_created_icons_themes()

    list_themes = []

    for t in list_all_themes:
        n = os.path.basename(t)
        list_themes.append(n)

    list_orphan_icon_themes = list(set(list_icon_themes) - set(list_themes))

    for o in list_orphan_icon_themes:
        logger.info('removing orphan zukan icon theme, %s', o)
        ZukanTheme.delete_icon_theme(o)


class ThemeListener:
    def get_user_theme():
        """
        Using sublime function 'add_on_change' to know when 'Preferences' settings
        is activated.

        This also activate when syntax is created or deleted, Seems when ST write to
        console 'generating syntax summary' trigger 'Preferences'.

        This function will check if theme changed then create or delete syntaxes
        and preferences for a icon theme.

        It creates themes if setting 'auto_install_theme' is set to True. And
        do not create theme if theme name in 'ignored_theme' setting.
        """
        logger.debug('Preferences.sublime-settings changed')

        theme_name = get_settings(USER_SETTINGS, 'theme')
        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
        prefer_icon = get_settings(ZUKAN_SETTINGS, 'prefer_icon')
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')
        data = read_pickle_data(USER_CURRENT_UI_FILE)

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
        # Commands 'Delete Syntax', 'Delete Syntaxes', 'Install Syntax' and
        # 'Rebuild Syntaxes' are triggered here and build themes.
        #
        # Creating icon theme if does not exist.
        if auto_install_theme is True and not os.path.exists(icon_theme_file):
            if package_theme_exists(theme_name) and theme_name not in ignored_theme:
                theme_path = sublime.find_resources(theme_name)
                ZukanTheme.create_icon_theme(theme_path[0])

                if zukan_restart_message is True:
                    dialog_message = (
                        'You may have to restart ST, if all icons do not load in '
                        'current theme.'
                    )
                    sublime.message_dialog(dialog_message)

        # Delete orphan icon theme files
        remove_orphan_icon_theme()

        if (
            theme_name in ZukanTheme.list_created_icons_themes()
            and theme_name not in ignored_theme
        ):
            # Build preferences if icons_preferences empty or if theme
            # in 'prefer_icon' option
            if not any(
                preferences.endswith(TMPREFERENCES_EXTENSION)
                for preferences in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ) or (
                theme_name in prefer_icon
                and not any(d['theme'] == theme_name for d in data)
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
        # Use async: error, click to select UI Select UI Color Scheme / Theme does not
        # activate. Use 'enter' to select works. Seems happen with other functions.
        # With async seems not occurr.

        # color_scheme_background = self.view.style()['background']
        current_color_scheme = self.view.settings().get('color_scheme')
        current_theme = self.view.settings().get('theme')

        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        ignored_theme = get_settings(ZUKAN_SETTINGS, 'ignored_theme')
        icon_theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, current_theme)

        # create setting file with current ui if does not exist
        if not os.path.exists(USER_CURRENT_UI_FILE):
            save_current_ui_settings(current_theme, current_color_scheme)

        if os.path.exists(USER_CURRENT_UI_FILE):
            data = read_pickle_data(USER_CURRENT_UI_FILE)

            if (
                not any(d['theme'] == current_theme for d in data)
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
                save_current_ui_settings(current_theme, current_color_scheme)