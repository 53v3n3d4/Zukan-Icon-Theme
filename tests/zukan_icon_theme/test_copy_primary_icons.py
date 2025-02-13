import importlib
import os

from unittest import TestCase
from unittest.mock import call, patch


copy_primary_icons = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons'
)


class TestCopyPrimaryIcons(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_dark(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {'Treble Light.sublime-theme': 'dark'},
        )
        mock_get_change_icon_settings.return_value = (
            {},
            [],
        )
        mock_get_ignored_icon_settings.return_value = []
        mock_get_theme_name.return_value = 'Treble Light.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'light'
        mock_get_icon_dark_light.return_value = 'dark'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        mock_copy2.assert_called_with(
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                'file_type_source-dark'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                'file_type_source'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
        )

        mock_debug.assert_called_with(
            '%s not in change_icon, copying prefer icon %s%s',
            'Source',
            'file_type_source-1-dark',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_light(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {},
        )
        mock_get_change_icon_settings.return_value = (
            {},
            [],
        )
        mock_get_ignored_icon_settings.return_value = []
        mock_get_theme_name.return_value = 'Treble Dark.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'dark'
        mock_get_icon_dark_light.return_value = 'light'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        mock_copy2.assert_called_with(
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                'file_type_source-light'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                'file_type_source'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
        )

        mock_debug.assert_called_with(
            '%s not in change_icon, copying prefer icon %s%s',
            'Source',
            'file_type_source-1-light',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_change_icon_dark(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {'Treble Light.sublime-theme': 'dark'},
        )
        mock_get_change_icon_settings.return_value = (
            {'Source': 'file_type_source-1-dark'},
            [],
        )
        mock_get_ignored_icon_settings.return_value = []
        mock_get_theme_name.return_value = 'Treble Light.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'light'
        mock_get_icon_dark_light.return_value = 'dark'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        mock_copy2.assert_called_with(
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                'file_type_source-1-dark'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                'file_type_source'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
        )

        mock_debug.assert_called_with(
            '%s in change_icon, renaming PNGs to %s%s',
            'Source',
            'file_type_source',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_change_icon_light(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {'Treble Dark.sublime-theme': 'light'},
        )
        mock_get_change_icon_settings.return_value = (
            {'Source': 'file_type_source-1-dark'},
            [],
        )
        mock_get_ignored_icon_settings.return_value = []
        mock_get_theme_name.return_value = 'Treble Dark.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'dark'
        mock_get_icon_dark_light.return_value = 'light'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        mock_copy2.assert_called_with(
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                'file_type_source-1-light'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
            os.path.join(
                copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                'file_type_source'
                + str(copy_primary_icons.ICONS_SUFFIX[2])
                + copy_primary_icons.PNG_EXTENSION,
            ),
        )

        mock_debug.assert_called_with(
            '%s in change_icon, renaming PNGs to %s%s',
            'Source',
            'file_type_source',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_remove(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {'Treble Dark.sublime-theme': 'light'},
        )
        mock_get_change_icon_settings.return_value = (
            {},
            [],
        )
        mock_get_ignored_icon_settings.return_value = ['Source']
        mock_get_theme_name.return_value = 'Treble Dark.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'dark'
        mock_get_icon_dark_light.return_value = 'light'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        remove_calls = [
            call(
                os.path.join(
                    copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                    f'file_type_source{suffix}.png',
                )
            )
            for suffix in copy_primary_icons.ICONS_SUFFIX
        ]

        mock_remove.assert_has_calls(remove_calls, any_order=True)

        mock_debug.assert_called_with(
            '%s not in change_icon, removing %s%s',
            'Source',
            'file_type_source',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_prefer_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_change_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_ignored_icon_settings'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_theme_name'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_sidebar_bgcolor'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.get_icon_dark_light'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.shutil.copy2'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons.logger.debug'
    )
    def test_copy_primary_icons_remove_change_icon(
        self,
        mock_debug,
        mock_remove,
        mock_copy2,
        mock_get_icon_dark_light,
        mock_get_sidebar_bgcolor,
        mock_get_theme_name,
        mock_get_ignored_icon_settings,
        mock_get_change_icon_settings,
        mock_get_prefer_icon_settings,
    ):
        mock_copy2.reset_mock()

        mock_get_prefer_icon_settings.return_value = (
            True,
            {'Treble Dark.sublime-theme': 'light'},
        )
        mock_get_change_icon_settings.return_value = (
            {'Source': 'file_type_source-1-dark'},
            [],
        )
        mock_get_ignored_icon_settings.return_value = ['Source']
        mock_get_theme_name.return_value = 'Treble Dark.sublime-theme'
        mock_get_sidebar_bgcolor.return_value = 'dark'
        mock_get_icon_dark_light.return_value = 'light'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        remove_calls = [
            call(
                os.path.join(
                    copy_primary_icons.ZUKAN_PKG_ICONS_PATH,
                    f'file_type_source{suffix}.png',
                )
            )
            for suffix in copy_primary_icons.ICONS_SUFFIX
        ]

        mock_remove.assert_has_calls(remove_calls, any_order=True)

        mock_debug.assert_called_with(
            '%s in change_icon, removing renamed %s%s',
            'Source',
            'file_type_source',
            str(copy_primary_icons.ICONS_SUFFIX[2]),
        )
