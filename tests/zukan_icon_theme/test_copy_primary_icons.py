import importlib
import os
import unittest

from unittest.mock import call, patch


copy_primary_icons = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.copy_primary_icons'
)

file_extensions = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.file_extensions'
)

icons_suffix = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.icons_suffix'
)

zukan_paths = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.utils.zukan_paths'
)


class TestCopyPrimaryIcons(unittest.TestCase):
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
    def test_copy_primary_icons(
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
        mock_get_prefer_icon_settings.return_value = (True, {'theme_name': 'dark'})
        mock_get_change_icon_settings.return_value = (
            {'file_type_source-light': 'some_value'},
            {},
        )
        mock_get_ignored_icon_settings.return_value = [
            'file_type_source-light',
            'file_type_source-dark',
        ]
        mock_get_theme_name.return_value = 'theme_name'
        mock_get_sidebar_bgcolor.return_value = 'dark'
        mock_get_icon_dark_light.return_value = 'dark'

        mock_copy2.return_value = None
        mock_remove.return_value = None

        copy_primary_icons.copy_primary_icons()

        mock_copy2.assert_called_with(
            os.path.join(
                zukan_paths.ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
                'file_type_source-light'
                + str(icons_suffix.ICONS_SUFFIX[2])
                + file_extensions.PNG_EXTENSION,
            ),
            os.path.join(
                zukan_paths.ZUKAN_PKG_ICONS_PATH,
                'file_type_source'
                + str(icons_suffix.ICONS_SUFFIX[2])
                + file_extensions.PNG_EXTENSION,
            ),
        )

        remove_calls = [
            call(
                os.path.join(
                    zukan_paths.ZUKAN_PKG_ICONS_PATH, f'file_type_source{suffix}.png'
                )
            )
            for suffix in icons_suffix.ICONS_SUFFIX
        ]

        mock_remove.assert_has_calls(remove_calls, any_order=True)

        mock_debug.assert_called_with(
            '%s not in change_icon, copying prefer icon %s%s',
            'Source',
            'file_type_source-1-dark',
            str(icons_suffix.ICONS_SUFFIX[2]),
        )
