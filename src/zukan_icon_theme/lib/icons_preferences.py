import errno
import glob
import logging
import os

from ..helpers.clean_data import clean_plist_tag
from ..helpers.copy_primary_icons import copy_primary_icons
from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.load_save_settings import get_settings
from ..helpers.read_write_data import (
    dump_plist_data,
    read_pickle_data,
)
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.primary_icons import (
    PRIMARY_ICONS,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
    ZUKAN_PKG_ICONS_PREFERENCES_PATH,
    ZUKAN_ICONS_DATA_FILE,
)

logger = logging.getLogger(__name__)


class ZukanPreference:
    """
    Create and remove tmPreferences in preferences folder.
    """

    def build_icon_preference(file_name: str, preference_name: str):
        """
        Batch create preference, delete plist tag and copy primary icons, to
        use with Thread together in install events.
        """
        ZukanPreference.create_icon_preference(file_name)
        # Remove plist tag <!DOCTYPE plist>
        ZukanPreference.delete_plist_tag(preference_name)
        copy_primary_icons()

    def build_icons_preferences():
        """
        Batch create preferences, delete plist tags and copy primary icons, to
        use with Thread together in install events.
        """
        if not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH):
            os.makedirs(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        # Deleting orphans files for 'create_custom_icon' if preferences do not exist
        # and not in 'create_custom_icon' anymore.
        if any(
            preference.endswith(TMPREFERENCES_EXTENSION)
            for preference in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
        ):
            ZukanPreference.delete_icons_preferences()
        ZukanPreference.create_icons_preferences()
        # Remove plist tag <!DOCTYPE plist>
        ZukanPreference.delete_plist_tags()
        copy_primary_icons()

    def create_icon_preference(preference_name: str):
        """
        Create icon tmPreferences file.
        """
        try:
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
            if not isinstance(change_icon, dict):
                logger.warning('change_icon option malformed, need to be a dict')

            # 'create_custom_icon' setting
            custom_list = [p for p in create_custom_icon() if 'preferences' in p]
            new_list = zukan_icons + custom_list

            for p in new_list:
                if (
                    p['preferences']['settings']['icon'] == preference_name
                    and p['preferences'].get('scope') is not None
                    and not (
                        p['name'] in ignored_icon
                        or p['preferences']['settings']['icon'] in ignored_icon
                        or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                        in ignored_icon
                        or (p.get('tag') is not None and p['tag'] in ignored_icon)
                    )
                ):
                    filename = (
                        p['preferences']['settings']['icon'] + TMPREFERENCES_EXTENSION
                    )

                    # 'change_icon' setting
                    if change_icon:
                        for k, v in change_icon.items():
                            if p['name'] == k:
                                p['preferences']['settings']['icon'] = v

                                # Copy primary icons, rename if icon option because
                                # primary icons do not work with any other names
                                for primary in PRIMARY_ICONS:
                                    if len(primary) >= 3 and p['name'] == primary[0]:
                                        p['preferences']['settings']['icon'] = primary[
                                            2
                                        ]
                                        logger.info(
                                            'renaming primary icon option necessary, %s',
                                            primary[1],
                                        )

                                # Check if PNG exist
                                if not os.path.exists(
                                    os.path.join(
                                        ZUKAN_PKG_ICONS_PATH, v + PNG_EXTENSION
                                    )
                                ):
                                    logger.warning('%s%s not found', v, PNG_EXTENSION)

                    preferences_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename
                    )
                    dump_plist_data(p['preferences'], preferences_filepath)
                    logger.info('%s created.', filename)
                elif (
                    p['preferences']['settings']['icon'] == preference_name
                    and p['preferences'].get('scope') is not None
                    and (
                        p['name'] in ignored_icon
                        or p['preferences']['settings']['icon'] in ignored_icon
                        or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                        in ignored_icon
                        or (p.get('tag') is not None and p['tag'] in ignored_icon)
                    )
                ):
                    logger.info('ignored icon %s', p['name'])
            return zukan_icons
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
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
            ignored_icon = get_settings(ZUKAN_SETTINGS, 'ignored_icon')
            if not isinstance(ignored_icon, list):
                logger.warning(
                    'ignored_icon option malformed, need to be a string list'
                )
            change_icon = get_settings(ZUKAN_SETTINGS, 'change_icon')
            if not isinstance(change_icon, dict):
                logger.warning('change_icon option malformed, need to be a dict')

            # 'create_custom_icon' setting
            custom_list = [p for p in create_custom_icon() if 'preferences' in p]
            new_list = zukan_icons + custom_list

            for p in new_list:
                if p['preferences'].get('scope') is not None and not (
                    p['name'] in ignored_icon
                    or p['preferences']['settings']['icon'] in ignored_icon
                    or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                    in ignored_icon
                    or (p.get('tag') is not None and p['tag'] in ignored_icon)
                ):
                    filename = (
                        p['preferences']['settings']['icon'] + TMPREFERENCES_EXTENSION
                    )

                    # 'change_icon' setting
                    if change_icon:
                        for k, v in change_icon.items():
                            if p['name'] == k:
                                p['preferences']['settings']['icon'] = v

                                # Copy primary icons, rename if icon option because
                                # primary icons do not work with any other names
                                for primary in PRIMARY_ICONS:
                                    if len(primary) >= 3 and p['name'] == primary[0]:
                                        p['preferences']['settings']['icon'] = primary[
                                            2
                                        ]
                                        logger.info(
                                            'renaming primary icon option necessary, %s',
                                            primary[1],
                                        )

                                # Check if PNG exist
                                if not os.path.exists(
                                    os.path.join(
                                        ZUKAN_PKG_ICONS_PATH, v + PNG_EXTENSION
                                    )
                                ):
                                    logger.warning('%s%s not found', v, PNG_EXTENSION)

                    preferences_filepath = os.path.join(
                        ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename
                    )
                    dump_plist_data(p['preferences'], preferences_filepath)
                elif (
                    p['name'] in ignored_icon
                    or p['preferences']['settings']['icon'] in ignored_icon
                    or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                    in ignored_icon
                    or (p.get('tag') is not None and p['tag'] in ignored_icon)
                ):
                    logger.info('ignored icon %s', p['name'])
            logger.info('tmPreferences created.')
            return zukan_icons
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
        if os.path.exists(preference_file):
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
