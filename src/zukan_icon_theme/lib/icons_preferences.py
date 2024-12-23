import errno
import glob
import logging
import os
import sublime

from ..helpers.clean_data import clean_plist_tag
from ..helpers.copy_primary_icons import copy_primary_icons
from ..helpers.create_custom_icon import create_custom_icon
from ..helpers.load_save_settings import (
    get_change_icon_settings,
    get_prefer_ignore_icon_settings,
    get_theme_name,
)
from ..helpers.read_write_data import (
    dump_plist_data,
    read_pickle_data,
)
from ..helpers.search_themes import get_sidebar_bgcolor
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.primary_icons import (
    PRIMARY_ICONS,
    TAG_PRIMARY,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
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
        try:
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
        finally:
            # Remove plist tag <!DOCTYPE plist>
            ZukanPreference.delete_plist_tags()
            copy_primary_icons()

    def handle_icon_preferences(
        p: dict,
        theme_name: str,
        ignored_icon: list,
        change_icon: dict,
        prefer_icon: dict,
        auto_prefer_icon: bool,
        bgcolor: list,
        icon_name: str,
        filename: str,
    ):
        """
        Handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        p (dict) -- dict with icon data.
        theme_name (str) -- theme name.
        ignored_icon (list) -- list of ignored_icon setting.
        change_icon (dict) --  dict with change_icon setting.
        prefer_icon (dict) --  dict with prefer_icon setting.
        auto_prefer_icon (bool) -- True or False for auto_prefer_icon setting.
        bgcolor (list) -- sidebar background color list.
        icon_name (str) -- icon name or icon option name.
        filename (str) -- icon name or icon option name with tmPreferences file
        extension, excluding '-dark' or '-light' from name.
        """
        # 'change_icon' setting
        if change_icon:
            for k, v in change_icon.items():
                if p['name'] == k:
                    p['preferences']['settings']['icon'] = v

        # 'prefer_icon' setting
        prefer_icon_version = ''

        if prefer_icon:
            for k, v in prefer_icon.items():
                if theme_name == k:
                    # Prefer light icon
                    if v == 'light' and p['preferences']['settings']['icon'].endswith(
                        '-dark'
                    ):
                        prefer_icon_version = p['preferences']['settings'][
                            'icon'
                        ].replace('-dark', '-light')

                    # Prefer dark icon
                    if v == 'dark' and p['preferences']['settings']['icon'].endswith(
                        '-light'
                    ):
                        prefer_icon_version = p['preferences']['settings'][
                            'icon'
                        ].replace('-light', '-dark')

                    if os.path.exists(
                        os.path.join(
                            ZUKAN_PKG_ICONS_PATH,
                            prefer_icon_version + PNG_EXTENSION,
                        )
                    ) or os.path.exists(
                        os.path.join(
                            ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                            prefer_icon_version + PNG_EXTENSION,
                        )
                    ):
                        p['preferences']['settings']['icon'] = prefer_icon_version
                        logger.debug(
                            'prefer icon %s',
                            p['preferences']['settings']['icon'],
                        )

        # 'auto_prefer_icon' setting
        if theme_name not in prefer_icon and auto_prefer_icon:
            # Default dark icon
            if not bgcolor:
                prefer_icon_version = p['preferences']['settings']['icon']

            if bgcolor:
                # Prefer light icon
                if bgcolor == 'dark' and p['preferences']['settings'][
                    'icon'
                ].endswith('-dark'):
                    prefer_icon_version = p['preferences']['settings']['icon'].replace(
                        '-dark', '-light'
                    )

                # Prefer dark icon
                if bgcolor == 'light' and p['preferences']['settings'][
                    'icon'
                ].endswith('-light'):
                    prefer_icon_version = p['preferences']['settings']['icon'].replace(
                        '-light', '-dark'
                    )

                if os.path.exists(
                    os.path.join(
                        ZUKAN_PKG_ICONS_PATH,
                        prefer_icon_version + PNG_EXTENSION,
                    )
                ) or os.path.exists(
                    os.path.join(
                        ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                        prefer_icon_version + PNG_EXTENSION,
                    )
                ):
                    p['preferences']['settings']['icon'] = prefer_icon_version
                    logger.debug(
                        'prefer icon %s',
                        p['preferences']['settings']['icon'],
                    )

        # Check if PNG exist
        if (
            'tag' in p
            and p['tag'] != TAG_PRIMARY
            and not os.path.exists(
                os.path.join(
                    ZUKAN_PKG_ICONS_PATH,
                    p['preferences']['settings']['icon'] + PNG_EXTENSION,
                )
            )
        ) or (
            'tag' in p
            and p['tag'] == TAG_PRIMARY
            and not os.path.exists(
                os.path.join(
                    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                    p['preferences']['settings']['icon'] + PNG_EXTENSION,
                )
            )
        ):
            logger.warning(
                '%s%s not found',
                p['preferences']['settings']['icon'],
                PNG_EXTENSION,
            )

        # Rename if icon is primary icons do not work with any other names
        for primary in PRIMARY_ICONS:
            for i in primary[2]:
                if (
                    p['name'] == primary[0]
                    and p['preferences']['settings']['icon'] == i
                ):
                    p['preferences']['settings']['icon'] = primary[1]
                    logger.debug(
                        'renaming primary icon option necessary, %s',
                        i,
                    )

        preferences_filepath = os.path.join(ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename)
        dump_plist_data(p['preferences'], preferences_filepath)

    def prepare_icon_preference_file(
        preference_name: str,
        zukan_icons: list,
        theme_name: str,
        ignored_icon: list,
        change_icon: dict,
        prefer_icon: dict,
        auto_prefer_icon: bool,
        bgcolor: list,
    ):
        """
        Prepare icon preference file, from icons data and setting 'create_custom_icon'.
        And handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        preference_name (str) -- icon or icon option.
        zukan_icons (list)-- icons data.
        theme_name (str) -- theme name.
        ignored_icon (list) -- list of ignored_icon setting.
        change_icon (dict) --  dict with change_icon setting.
        prefer_icon (dict) --  dict with prefer_icon setting.
        auto_prefer_icon (bool) -- True or False for auto_prefer_icon setting.
        bgcolor (list) -- sidebar background color list.
        """
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
                    # Icons options
                    # Need to add SVG_EXTENSION to icons options
                    or (
                        'icons' in p and any(x for x in p['icons'] if x in ignored_icon)
                    )
                )
            ):
                # Remove '-dark' and '-light' from tmPreferences name.
                icon_name = p['preferences']['settings']['icon']
                if icon_name.endswith('-dark'):
                    icon_name = icon_name[:-5]
                if icon_name.endswith('-light'):
                    icon_name = icon_name[:-6]

                filename = icon_name + TMPREFERENCES_EXTENSION

                ZukanPreference.handle_icon_preferences(
                    p,
                    theme_name,
                    ignored_icon,
                    change_icon,
                    prefer_icon,
                    auto_prefer_icon,
                    bgcolor,
                    icon_name,
                    filename,
                )

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

    def create_icon_preference(preference_name: str):
        """
        Create icon tmPreferences file.

        Parameters:
        preference_name (str) -- icon or icon option.
        """
        try:
            auto_prefer_icon, prefer_icon, ignored_icon = (
                get_prefer_ignore_icon_settings()
            )
            change_icon, _ = get_change_icon_settings()
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

            theme_name = get_theme_name()
            theme_st_path = sublime.find_resources(theme_name)
            bgcolor = get_sidebar_bgcolor(theme_st_path[0])

            ZukanPreference.prepare_icon_preference_file(
                preference_name,
                zukan_icons,
                theme_name,
                ignored_icon,
                change_icon,
                prefer_icon,
                auto_prefer_icon,
                bgcolor,
            )

            if preference_name.endswith('-dark'):
                fname = preference_name[:-5] + TMPREFERENCES_EXTENSION
            if preference_name.endswith('-light'):
                fname = preference_name[:-6] + TMPREFERENCES_EXTENSION

            logger.info('%s created.', fname)

            return zukan_icons

        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                fname,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                fname,
            )

    def prepare_icons_preferences_list(
        zukan_icons: list,
        theme_name: str,
        ignored_icon: list,
        change_icon: dict,
        prefer_icon: dict,
        auto_prefer_icon: bool,
        bgcolor: list,
    ):
        """
        Prepare icons preferences list, from icons data and setting 'create_custom_icon'.
        And handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        zukan_icons (list)-- icons data.
        theme_name (str) -- theme name.
        ignored_icon (list) -- list of ignored_icon setting.
        change_icon (dict) --  dict with change_icon setting.
        prefer_icon (dict) --  dict with prefer_icon setting.
        auto_prefer_icon (bool) -- True or False for auto_prefer_icon setting.
        bgcolor (list) -- sidebar background color list.
        """
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
                # Icons options
                # Need to add SVG_EXTENSION to icons options
                or ('icons' in p and any(x for x in p['icons'] if x in ignored_icon))
            ):
                # Remove '-dark' and '-light' from tmPreferences name.
                icon_name = p['preferences']['settings']['icon']
                if icon_name.endswith('-dark'):
                    icon_name = icon_name[:-5]
                if icon_name.endswith('-light'):
                    icon_name = icon_name[:-6]

                filename = icon_name + TMPREFERENCES_EXTENSION

                ZukanPreference.handle_icon_preferences(
                    p,
                    theme_name,
                    ignored_icon,
                    change_icon,
                    prefer_icon,
                    auto_prefer_icon,
                    bgcolor,
                    icon_name,
                    filename,
                )

            elif (
                p['name'] in ignored_icon
                or p['preferences']['settings']['icon'] in ignored_icon
                or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                in ignored_icon
                or (p.get('tag') is not None and p['tag'] in ignored_icon)
            ):
                logger.info('Ignored icon %s', p['name'])

    def create_icons_preferences():
        """
        Create icons tmPreferences files.
        """
        try:
            auto_prefer_icon, prefer_icon, ignored_icon = (
                get_prefer_ignore_icon_settings()
            )
            change_icon, _ = get_change_icon_settings()
            zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)

            theme_name = get_theme_name()
            theme_st_path = sublime.find_resources(theme_name)
            bgcolor = get_sidebar_bgcolor(theme_st_path[0])

            ZukanPreference.prepare_icons_preferences_list(
                zukan_icons,
                theme_name,
                ignored_icon,
                change_icon,
                prefer_icon,
                auto_prefer_icon,
                bgcolor,
            )

            logger.info('tmPreferences created.')

            return zukan_icons

        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                ZUKAN_ICONS_DATA_FILE,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                ZUKAN_ICONS_DATA_FILE,
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
