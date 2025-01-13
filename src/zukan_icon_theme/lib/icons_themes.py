import errno
import glob
import logging
import os

from ..helpers.load_save_settings import get_theme_settings
from ..helpers.read_write_data import dump_json_data
from ..helpers.search_themes import (
    search_resources_sublime_themes,
    theme_with_opacity,
)
from ..utils.file_extensions import (
    SUBLIME_THEME_EXTENSION,
)
from ..utils.theme_templates import (
    TEMPLATE_JSON,
    TEMPLATE_JSON_WITH_OPACITY,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
)

logger = logging.getLogger(__name__)


class ZukanTheme:
    """
    Create, list and remove sublime-themes files in Zukan Icon Theme/icons folder
    """

    def __init__(self):
        self.ignored_theme, self.auto_install_theme = get_theme_settings()
        self.list_all_themes = search_resources_sublime_themes()

    def create_icon_theme(self, theme_st_path: str):
        """
        Create sublime-theme file with icon_file_type scope. Copy a json template
        to Zukan Icon Theme/icons folder with the theme name.

        Example: Packages/Theme - Treble/Treble Adaptive.sublime-theme

        Parameters:
        theme_st_path (str) -- installed theme name.
        """
        try:
            file_name = os.path.basename(theme_st_path)

            # Check if installed theme file exist and not in 'ignored_theme'
            # settings.
            if (
                any(theme_st_path in t for t in self.list_all_themes)
                and file_name not in self.ignored_theme
            ):
                # print(theme_st_path)
                theme_filepath = os.path.join(
                    ZUKAN_PKG_ICONS_PATH, os.path.basename(theme_st_path)
                )

                if theme_with_opacity(theme_st_path):
                    file_content = TEMPLATE_JSON
                else:
                    file_content = TEMPLATE_JSON_WITH_OPACITY

                dump_json_data(file_content, theme_filepath)
                logger.info('creating icon theme %s', os.path.basename(theme_filepath))
                return theme_st_path
            elif file_name in self.ignored_theme:
                logger.info('ignored theme %s', file_name)
            else:
                raise FileNotFoundError(
                    logger.error(
                        'theme name does not exist. Use menu Command Palette > View '
                        'Package File > theme name.'
                    )
                )
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                theme_st_path,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                theme_st_path,
            )

    def create_icons_themes(self):
        """
        Create all sublime-themes files from installed themes.
        """
        try:
            # list_all_themes = search_resources_sublime_themes()
            if self.list_all_themes is not None:
                for theme in self.list_all_themes:
                    self.create_icon_theme(theme)
                return self.list_all_themes
            else:
                raise FileNotFoundError(logger.error('list is empty.'))
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                self.list_all_themes,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                self.list_all_themes,
            )

    def delete_icon_theme(self, theme_name: str):
        """
        Delete sublime-theme file in Zukan Icon Theme/icons folder.

        Example: Treble Adaptive.sublime-theme

        Parameters:
        theme_name (str) -- installed theme name.
        """
        try:
            theme_file = os.path.join(ZUKAN_PKG_ICONS_PATH, theme_name)
            os.remove(theme_file)
            logger.info('deleting icon theme %s', os.path.basename(theme_file))
            return theme_name
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), theme_name
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), theme_name
            )

    def delete_icons_themes(self):
        """
        Delete all sublime-themes files in Zukan Icon Theme/icons folder.
        """
        try:
            for t in glob.iglob(
                os.path.join(ZUKAN_PKG_ICONS_PATH, '*' + SUBLIME_THEME_EXTENSION)
            ):
                os.remove(t)
                logger.info('deleting icon theme %s', os.path.basename(t))
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                t,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                t,
            )

    def delete_unused_icon_theme(self):
        """
        Delete unused icon theme file.

        When uninstall a theme package, it leaves an icon-theme file.
        """
        list_all_themes = search_resources_sublime_themes()
        list_icon_themes = self.list_created_icons_themes()

        list_themes = []

        for t in list_all_themes:
            n = os.path.basename(t)
            list_themes.append(n)

        list_unused_icon_themes = list(set(list_icon_themes) - set(list_themes))

        for o in list_unused_icon_themes:
            logger.info('removing unused zukan icon theme, %s', o)
            self.delete_icon_theme(o)

    def list_created_icons_themes(self) -> list:
        """
        List all sublime-themes files in Zukan Icon Theme/icons folder.

        Returns:
        list_themes_installed (list) -- list of sublime-themes in folder icons/.
        """
        try:
            list_themes_installed = []
            if os.path.exists(ZUKAN_PKG_ICONS_PATH):
                for file in glob.glob(
                    os.path.join(ZUKAN_PKG_ICONS_PATH, '*' + SUBLIME_THEME_EXTENSION)
                ):
                    list_themes_installed.append(os.path.basename(file))
                return list_themes_installed
            else:
                raise FileNotFoundError(logger.error('file or directory do not exist.'))
            return list_themes_installed
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'Zukan Icon Theme/icons folder',
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'Zukan Icon Theme/icons folder',
            )
