import errno
import glob
import logging
import os

from collections.abc import Set
from ..helpers.copy_primary_icons import copy_primary_icons
from ..helpers.custom_icon import generate_custom_icon
from ..helpers.dict_to_preference import save_tm_preferences
from ..helpers.load_save_settings import (
    get_change_icon_settings,
    get_ignored_icon_settings,
    get_prefer_icon_settings,
    get_theme_name,
)
from ..helpers.read_write_data import read_pickle_data
from ..helpers.search_themes import get_sidebar_bgcolor
from ..utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
    TMPREFERENCES_EXTENSION,
)
from ..utils.primary_icons import (
    PRIMARY_ICONS,
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

    def change_icon_setting(self) -> dict:
        change_icon, _ = get_change_icon_settings()
        return change_icon

    def ignored_icon_setting(self) -> Set:
        return set(get_ignored_icon_settings())

    def prefer_icon_setting(self) -> tuple:
        auto_prefer_icon, prefer_icon = get_prefer_icon_settings()
        return auto_prefer_icon, prefer_icon

    def theme_name_setting(self) -> str:
        return get_theme_name()

    def zukan_icons_data(self) -> list:
        return read_pickle_data(ZUKAN_ICONS_DATA_FILE)

    def sidebar_bgcolor(self, theme_name: str) -> str:
        return get_sidebar_bgcolor(theme_name)

    def build_icon_preference(self, file_name: str):
        """
        Batch create preference, delete plist tag and copy primary icons, to
        use with Thread together in install events.
        """
        theme_name = self.theme_name_setting()
        bgcolor = self.sidebar_bgcolor(theme_name)
        self.create_icon_preference(file_name, bgcolor, theme_name)
        copy_primary_icons(bgcolor, theme_name)

    def build_icons_preferences(self):
        """
        Batch create preferences, delete plist tags and copy primary icons, to
        use with Thread together in install events.
        """
        try:
            if not os.path.exists(ZUKAN_PKG_ICONS_PREFERENCES_PATH):
                os.makedirs(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            # Deleting unused files for 'create_custom_icon' if preferences do not exist
            # and not in 'create_custom_icon' anymore.
            if any(
                preference.endswith(TMPREFERENCES_EXTENSION)
                for preference in os.listdir(ZUKAN_PKG_ICONS_PREFERENCES_PATH)
            ):
                self.delete_icons_preferences()
        finally:
            theme_name = self.theme_name_setting()
            bgcolor = self.sidebar_bgcolor(theme_name)
            self.create_icons_preferences(bgcolor, theme_name)
            copy_primary_icons(bgcolor, theme_name)

    def _apply_change_icon(self, p: dict, change_icon: dict):
        if change_icon:
            for k, v in change_icon.items():
                if p['name'] == k:
                    p['preferences']['settings']['icon'] = v

    def _apply_prefer_icon(
        self, p: dict, prefer_icon_version: str, theme_name: str, prefer_icon: dict
    ):
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

    def _apply_auto_prefer_icon(
        self,
        p: dict,
        prefer_icon_version: str,
        bgcolor: str,
        theme_name: str,
        auto_prefer_icon: bool,
        prefer_icon: dict,
    ):
        if theme_name not in prefer_icon and auto_prefer_icon:
            # Default dark icon
            if not bgcolor:
                prefer_icon_version = p['preferences']['settings']['icon']

            if bgcolor:
                # Prefer light icon
                if bgcolor == 'dark' and p['preferences']['settings']['icon'].endswith(
                    '-dark'
                ):
                    prefer_icon_version = p['preferences']['settings']['icon'].replace(
                        '-dark', '-light'
                    )

                # Prefer dark icon
                if bgcolor == 'light' and p['preferences']['settings']['icon'].endswith(
                    '-light'
                ):
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

    def _rename_primary_icons(self, p: dict):
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

    def _png_exists(self, p: dict):
        if not os.path.exists(
            os.path.join(
                ZUKAN_PKG_ICONS_PATH,
                p['preferences']['settings']['icon'] + PNG_EXTENSION,
            )
        ):
            logger.warning(
                '%s%s not found',
                p['preferences']['settings']['icon'],
                PNG_EXTENSION,
            )

    def handle_icon_preferences(
        self,
        p: dict,
        icon_name: str,
        filename: str,
        bgcolor: str,
        theme_name: str,
        change_icon: dict,
        auto_prefer_icon: bool,
        prefer_icon: dict,
    ):
        """
        Handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        p (dict) -- dict with icon data.
        icon_name (str) -- icon name or icon option name.
        filename (str) -- icon name or icon option name with tmPreferences file
        extension, excluding '-dark' or '-light' from name.
        bgcolor (str) -- theme background color.
        theme_name (str) -- theme name.
        change_icon (dict) -- dictionary with name and icon name.
        auto_prefer_icon (bool) -- auto prefere icon settiong, true or false.
        prefer_icon (dict) -- dictionary with theme name and prefer icon, light or dark.
        """
        # 'change_icon' setting
        self._apply_change_icon(p, change_icon)

        # 'prefer_icon'  and 'auto_prefer_icon' setting
        prefer_icon_version = ''

        # 'prefer_icon' setting
        self._apply_prefer_icon(p, prefer_icon_version, theme_name, prefer_icon)

        # 'auto_prefer_icon' setting
        self._apply_auto_prefer_icon(
            p, prefer_icon_version, bgcolor, theme_name, auto_prefer_icon, prefer_icon
        )

        # Rename if icon is primary icons do not work with any other names
        self._rename_primary_icons(p)

        # Check if PNG exist
        self._png_exists(p)

        # print(p['preferences'])

        preferences_filepath = os.path.join(ZUKAN_PKG_ICONS_PREFERENCES_PATH, filename)

        save_tm_preferences(p['preferences'], preferences_filepath)

    def get_list_icons_preferences(self):
        list_all_icons_preferences = []
        zukan_icons = self.zukan_icons_data()

        # 'create_custom_icon' setting
        custom_list = [
            p for p in generate_custom_icon(zukan_icons) if 'preferences' in p
        ]
        list_all_icons_preferences = zukan_icons + custom_list

        return list_all_icons_preferences

    def _get_file_name(self, icon_name: str) -> str:
        # Remove '-dark' and '-light' from tmPreferences name.
        if icon_name.endswith('-dark'):
            icon_name = icon_name[:-5]
        if icon_name.endswith('-light'):
            icon_name = icon_name[:-6]

        return icon_name + TMPREFERENCES_EXTENSION

    def prepare_icon_preference_file(
        self,
        preference_name: str,
        bgcolor: str,
        theme_name: str,
    ):
        """
        Prepare icon preference file, from icons data and setting 'create_custom_icon'.
        And handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        preference_name (str) -- icon or icon option.
        bgcolor (str) -- theme background color.
        theme_name (str) -- theme name.
        """
        list_all_icons_preferences = self.get_list_icons_preferences()
        # print(list_all_icons_preferences)

        auto_prefer_icon, prefer_icon = self.prefer_icon_setting()
        change_icon = self.change_icon_setting()
        ignored_icon = self.ignored_icon_setting()

        for p in list_all_icons_preferences:
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
                filename = self._get_file_name(icon_name)

                self.handle_icon_preferences(
                    p,
                    icon_name,
                    filename,
                    bgcolor,
                    theme_name,
                    change_icon,
                    auto_prefer_icon,
                    prefer_icon,
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

    def create_icon_preference(
        self, preference_name: str, bgcolor: str, theme_name: str
    ):
        """
        Create icon tmPreferences file.

        Parameters:
        preference_name (str) -- icon or icon option.
        bgcolor (str) -- theme background color.
        theme_name (str) -- theme name.
        """
        if preference_name.endswith('-dark'):
            fname = preference_name[:-5] + TMPREFERENCES_EXTENSION
        elif preference_name.endswith('-light'):
            fname = preference_name[:-6] + TMPREFERENCES_EXTENSION
        else:
            fname = preference_name + TMPREFERENCES_EXTENSION

        try:
            self.prepare_icon_preference_file(preference_name, bgcolor, theme_name)

            logger.info('%s created.', fname)

            # return self.zukan_icons

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

    def prepare_icons_preferences_list(self, bgcolor: str, theme_name: str):
        """
        Prepare icons preferences list, from icons data and setting 'create_custom_icon'.
        And handle the zukan settings to choose icon option, version or ignore an icon.

        Parameters:
        bgcolor (str) -- theme background color.
        theme_name (str) -- theme name.
        """
        list_all_icons_preferences = self.get_list_icons_preferences()

        auto_prefer_icon, prefer_icon = self.prefer_icon_setting()
        change_icon = self.change_icon_setting()
        ignored_icon = self.ignored_icon_setting()

        for p in list_all_icons_preferences:
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
                filename = self._get_file_name(icon_name)

                self.handle_icon_preferences(
                    p,
                    icon_name,
                    filename,
                    bgcolor,
                    theme_name,
                    change_icon,
                    auto_prefer_icon,
                    prefer_icon,
                )

            elif (
                p['name'] in ignored_icon
                or p['preferences']['settings']['icon'] in ignored_icon
                or (p['preferences']['settings']['icon'] + SVG_EXTENSION)
                in ignored_icon
                or (p.get('tag') is not None and p['tag'] in ignored_icon)
            ):
                logger.info('Ignored icon %s', p['name'])

    def create_icons_preferences(self, bgcolor: str, theme_name: str):
        """
        Create icons tmPreferences files.

        Parameters:
        bgcolor (str) -- theme background color.
        theme_name (str) -- theme name.
        """
        try:
            self.prepare_icons_preferences_list(bgcolor, theme_name)

            logger.info('tmPreferences created.')

            # return self.zukan_icons

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

    def delete_icon_preference(self, preference_name: str):
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

    def delete_icons_preferences(self):
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

    def list_created_icons_preferences(self) -> list:
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
