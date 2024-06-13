import errno
import glob
import logging
import os

from ..helpers.clean_data import clean_plist_tag
from ..helpers.read_write_data import (
    dump_plist_data,
    read_pickle_data,
)
from ..utils.file_extensions import (
    TMPREFERENCES_EXTENSION,
)
from ..utils.zukan_dir_paths import (
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_PREFERENCES_DATA_FILE,
)

logger = logging.getLogger(__name__)


class ZukanPreference:
    """
    Create and remove tmPreferences in preferences folder.
    """

    def build_icons_preferences():
        """
        Batch create preferences and delete plist tags, to use with Thread together
        in install events.
        """
        ZukanPreference.create_icons_preferences()
        # Remove plist tag <!DOCTYPE plist>
        ZukanPreference.delete_plist_tags()

    def create_icon_preference(preference_name: str):
        """
        Create icon tmPreferences file.
        """
        try:
            zukan_icons_preferences = read_pickle_data(ZUKAN_PREFERENCES_DATA_FILE)
            for p in zukan_icons_preferences:
                if p['settings']['icon'] == preference_name:
                    filename = p['settings']['icon'] + TMPREFERENCES_EXTENSION
                    preferences_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename
                    )
                    dump_plist_data(p, preferences_filepath)
            logger.info('%s created.', filename)
            return zukan_icons_preferences
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def create_icons_preferences():
        """
        Create icons tmPreferences files.
        """
        try:
            zukan_icons_preferences = read_pickle_data(ZUKAN_PREFERENCES_DATA_FILE)
            for p in zukan_icons_preferences:
                filename = p['settings']['icon'] + TMPREFERENCES_EXTENSION
                preferences_filepath = os.path.join(
                    ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename
                )
                dump_plist_data(p, preferences_filepath)
            logger.info('tmPreferences created.')
            return zukan_icons_preferences
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), filename
            )

    def delete_icons_preference(preference_name: str):
        """
        Delete tmPreference file in Zukan Icon Theme/preferences folder.

        Example: ai.tmPreferences

        Parameters:
        preference_name (str) -- installed preference name.
        """
        try:
            preference_file = os.path.join(
                ZUKAN_PKG_ICONS_PREFERENCES_PATH, preference_name
            )
            os.remove(preference_file)
            logger.info(
                'deleting icon preference %s', os.path.basename(preference_file)
            )
            return preference_name
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                preference_name,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                preference_name,
            )

    def delete_icons_preferences():
        """
        Delete all tmPreferences files, leaving pickle file.
        """
        try:
            for p in glob.iglob(
                os.path.join(
                    ZUKAN_PKG_ICONS_PREFERENCES_PATH, '*' + TMPREFERENCES_EXTENSION
                )
            ):
                os.remove(p)
            logger.info('tmPreferences deleted.')
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), p
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), p
            )

    def delete_plist_tag(preference_name: str):
        """
        Delete tag <!DOCTYPE plist> from tmPreferences file created.

        Parameters:
        preference_name (str) -- icon preference file name.
        """
        logger.debug('deleting plist tag <!DOCTYPE plist>.')
        preference_file = os.path.join(
            ZUKAN_PKG_ICONS_PREFERENCES_PATH, preference_name
        )
        clean_plist_tag(preference_file)

    def delete_plist_tags():
        """
        Delete tag <!DOCTYPE plist> from all tmPreferences files created.
        """
        try:
            logger.debug('deleting plist tag <!DOCTYPE plist>.')
            for p in glob.glob(
                os.path.join(
                    ZUKAN_PKG_ICONS_PREFERENCES_PATH, '*' + TMPREFERENCES_EXTENSION
                )
            ):
                clean_plist_tag(p)
            return p
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'Zukan Icon Theme/preferences folder',
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'Zukan Icon Theme/preferences folder',
            )

    def list_created_icons_preferences() -> list:
        """
        List all tmPreferences files in Zukan Icon Theme/preferences folder.

        Returns:
        list_preferences_installed (list) -- list of tmPreferences in folder
        preferences/.
        """
        try:
            list_preferences_installed = []
            if os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH):
                for file in glob.glob(
                    os.path.join(
                        ZUKAN_PKG_ICONS_PREFERENCES_PATH, '*' + TMPREFERENCES_EXTENSION
                    )
                ):
                    list_preferences_installed.append(os.path.basename(file))
                return list_preferences_installed
            else:
                raise FileNotFoundError(logger.error('file or directory do not exist.'))
            return list_preferences_installed
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                'Zukan Icon Theme/preferences folder',
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                'Zukan Icon Theme/preferences folder',
            )
