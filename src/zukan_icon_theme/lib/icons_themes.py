import errno
import glob
import logging
import os

from ..helpers.read_write_data import dump_json_data
from ..helpers.search_themes import (
    list_theme_with_opacity,
    search_resources_sublime_themes,
)
from ..utils.file_extensions import (
    SUBLIME_THEME_EXTENSION,
)
from ..utils.theme_templates import (
    TEMPLATE_JSON,
    TEMPLATE_JSON_WITH_OPACITY,
)
from ..utils.zukan_dir_paths import (
    ZUKAN_PKG_ICONS_PATH,
)

logger = logging.getLogger(__name__)


class ZukanTheme:
    """
    Create, list and remove sublime-themes files in Zukan Icon Theme/icons folder
    """

    def create_icon_theme(theme_name: str):
        """
        Create sublime-theme file with icon_file_type scope. Copy a json template
        to Zukan Icon Theme/icons folder with the theme name.

        Example: Treble Adaptive.sublime-theme

        Parameters:
        theme_name (str) -- installed theme name.
        """
        try:
            list_all_themes = search_resources_sublime_themes()
            list_themes_has_opacity = list_theme_with_opacity()
            list_themes_no_opacity = list(
                set(list_all_themes).difference(list_themes_has_opacity)
            )
            # Check if installed theme file exist.
            if any(theme_name in t for t in list_all_themes):
                # print(theme_name)
                theme_filepath = os.path.join(
                    ZUKAN_PKG_ICONS_PATH, os.path.basename(theme_name)
                )
                if theme_name in list_themes_has_opacity:
                    file_content = TEMPLATE_JSON
                if theme_name in list_themes_no_opacity:
                    file_content = TEMPLATE_JSON_WITH_OPACITY
                dump_json_data(file_content, theme_filepath)
                logger.info('creating icon theme %s', os.path.basename(theme_filepath))
                return theme_name
            else:
                raise FileNotFoundError(
                    logger.error(
                        'theme name does not exist. Use menu Command Palette > View '
                        'Package File > theme name.'
                    )
                )
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), theme_name
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), theme_name
            )

    def create_icons_themes():
        """
        Create all sublime-themes files from installed themes.
        """
        try:
            list_all_themes = search_resources_sublime_themes()
            if list_all_themes is not None:
                for theme in list_all_themes:
                    ZukanTheme.create_icon_theme(theme)
                return list_all_themes
            else:
                raise FileNotFoundError(logger.error('list is empty.'))
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                list_all_themes,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                list_all_themes,
            )

    def delete_created_theme_file(theme_name: str):
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

    def delete_created_themes_files():
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

    def list_created_themes_files() -> list:
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
