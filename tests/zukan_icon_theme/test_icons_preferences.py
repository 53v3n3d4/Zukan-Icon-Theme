import errno
import importlib
import os
import platform

from collections.abc import Set
from unittest import TestCase
from unittest.mock import MagicMock, patch

icons_preferences = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences'
)


class TestZukanPreference(TestCase):
    def setUp(self):
        self.zukan = icons_preferences.ZukanPreference()
        self.test_theme = 'test_theme'
        self.test_preference = {
            'name': 'ATest',
            'preferences': {
                'settings': {'icon': 'atest'},
                'scope': 'source.atest',
            },
        }
        self.test_dark_theme = 'Treble Dark.sublime-theme'
        self.test_light_theme = 'Treble Light.sublime-theme'
        self.bgcolor_dark = 'dark'
        self.bgcolor_light = 'light'

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.get_change_icon_settings'
    )
    def test_change_icon_setting(self, mock_get_settings):
        expected = {'Rust': 'rust-1', 'Go': 'go-1'}
        mock_get_settings.return_value = (expected, None)

        result = self.zukan.change_icon_setting()

        self.assertEqual(result, expected)
        mock_get_settings.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.get_ignored_icon_settings'
    )
    def test_ignored_icon_setting(self, mock_get_settings):
        expected = {'Ignored-1', 'Ignored-2'}
        mock_get_settings.return_value = expected

        result = self.zukan.ignored_icon_setting()

        self.assertIsInstance(result, Set)
        self.assertEqual(result, expected)
        mock_get_settings.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.get_prefer_icon_settings'
    )
    def test_prefer_icon_setting(self, mock_get_settings):
        expected = (True, {self.test_dark_theme: 'light'})
        mock_get_settings.return_value = expected

        result = self.zukan.prefer_icon_setting()

        self.assertEqual(result, expected)
        mock_get_settings.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.get_theme_name')
    def test_theme_name_setting(self, mock_get_theme):
        expected = self.test_dark_theme
        mock_get_theme.return_value = expected

        result = self.zukan.theme_name_setting()

        self.assertEqual(result, expected)
        mock_get_theme.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.read_pickle_data'
    )
    def test_zukan_icons_data(self, mock_read_pickle):
        expected = [{'name': 'ATest-1'}, {'name': 'ATest-2'}]
        mock_read_pickle.return_value = expected

        result = self.zukan.zukan_icons_data()

        self.assertEqual(result, expected)
        mock_read_pickle.assert_called_once_with(
            icons_preferences.ZUKAN_ICONS_DATA_FILE
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.get_sidebar_bgcolor'
    )
    def test_sidebar_bgcolor(self, mock_get_bgcolor):
        mock_get_bgcolor.return_value = self.bgcolor_dark

        result = self.zukan.sidebar_bgcolor(self.test_theme)

        self.assertEqual(result, self.bgcolor_dark)
        mock_get_bgcolor.assert_called_once_with(self.test_theme)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.copy_primary_icons'
    )
    def test_build_icon_preference(self, mock_copy_icons):
        # fmt: off
        with patch.object(self.zukan, 'create_icon_preference') as mock_create, \
             patch.object(self.zukan, 'theme_name_setting') as mock_theme_name, \
             patch.object(self.zukan, 'sidebar_bgcolor') as mock_bgcolor:
             # fmt: on

                    mock_theme_name.return_value = self.test_dark_theme
                    mock_bgcolor.return_value = self.bgcolor_dark

                    test_file_name = 'atest'

                    self.zukan.build_icon_preference(test_file_name)

                    mock_theme_name.assert_called_once()
                    mock_bgcolor.assert_called_once_with(self.test_dark_theme)
                    mock_create.assert_called_once_with(
                        test_file_name, self.bgcolor_dark, self.test_dark_theme
                    )
                    mock_copy_icons.assert_called_once_with(
                        self.bgcolor_dark, self.test_dark_theme
                    )

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('os.listdir')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.copy_primary_icons'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.system_theme.subprocess.check_output'
    )
    def test_build_icons_preferences(
        self,
        mock_subprocess,
        mock_copy_icons,
        mock_listdir,
        mock_makedirs,
        mock_exists,
    ):
        if platform.system() == 'Linux':
            mock_subprocess.return_value = '{"data":[{"data":1}]}'

        mock_exists.return_value = False

        with patch.object(self.zukan, 'create_icons_preferences') as mock_create:
            self.zukan.build_icons_preferences()

            mock_makedirs.assert_called_once_with(
                icons_preferences.ZUKAN_PKG_ICONS_PREFERENCES_PATH
            )
            mock_create.assert_called_once()
            mock_copy_icons.assert_called_once()

    def test_build_icons_preferences_deletes_existing_preferences(self):
        # fmt: off
        with patch('os.path.exists') as mock_exists, \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.listdir') as mock_listdir, \
             patch.object(self.zukan, 'delete_icons_preferences') as mock_delete, \
             patch.object(self.zukan, 'theme_name_setting') as mock_theme_name, \
             patch.object(self.zukan, 'sidebar_bgcolor') as mock_bgcolor, \
             patch.object(
                self.zukan, 'create_icons_preferences'
             ) as mock_create_icons_preferences, \
             patch(
                'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.copy_primary_icons'
             ) as mock_copy_icons:
             # fmt: on

            mock_exists.return_value = True
            mock_listdir.return_value = ["atest1.tmPreferences", "atest2.tmPreferences"]
            mock_theme_name.return_value = self.test_dark_theme
            mock_bgcolor.return_value = self.bgcolor_dark

            self.zukan.build_icons_preferences()

            mock_delete.assert_called_once()
            mock_create_icons_preferences.assert_called_once_with(
                self.bgcolor_dark, self.test_dark_theme
            )
            mock_copy_icons.assert_called_once_with(self.bgcolor_dark, self.test_dark_theme)

    def test_apply_change_icon(self):
        test_pref = {
            'name': 'Rust',
            'preferences': {'settings': {'icon': 'rust'}},
        }
        change_icon = {'Rust': 'rust-1'}

        self.zukan._apply_change_icon(test_pref, change_icon)

        self.assertEqual(test_pref['preferences']['settings']['icon'], 'rust-1')

    @patch('os.path.exists')
    def test_apply_prefer_icon(self, mock_exists):
        test_pref = {
            'name': 'Ada',
            'preferences': {'settings': {'icon': 'ada-dark'}},
        }
        prefer_icon = {'test_theme': 'light'}
        mock_exists.return_value = True

        self.zukan._apply_prefer_icon(
            test_pref, 'ada-light', self.test_theme, prefer_icon
        )

        self.assertEqual(test_pref['preferences']['settings']['icon'], 'ada-light')

    @patch('os.path.exists')
    def test_apply_auto_prefer_icon(self, mock_exists):
        test_pref = {
            'name': 'Ada',
            'preferences': {'settings': {'icon': 'ada-dark'}},
        }
        mock_exists.return_value = True

        self.zukan._apply_auto_prefer_icon(
            test_pref, 'ada-light', self.bgcolor_dark, self.test_theme, True, {}
        )

        self.assertEqual(test_pref['preferences']['settings']['icon'], 'ada-light')

    def test_rename_primary_icons(self):
        PRIMARY_ICONS = [
            (
                'Image',
                'file_type_image-dark',
                ['file_type_image-light', 'file_type_image-1'],
            )
        ]

        test_pref = {
            'name': 'Image',
            'preferences': {'settings': {'icon': 'file_type_image-light'}},
        }

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.PRIMARY_ICONS',
            PRIMARY_ICONS,
        ):
            self.zukan._rename_primary_icons(test_pref)

            self.assertEqual(
                test_pref['preferences']['settings']['icon'], 'file_type_image-dark'
            )

    @patch('os.path.exists')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_png_exists(self, mock_logger, mock_exists):
        mock_exists.return_value = False
        test_pref = {'preferences': {'settings': {'icon': 'missing_icon'}}}

        self.zukan._png_exists(test_pref)

        mock_logger.warning.assert_called_once_with(
            '%s%s not found', 'missing_icon', icons_preferences.PNG_EXTENSION
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.save_tm_preferences'
    )
    def test_handle_icon_preferences(self, mock_save):
        test_pref = self.test_preference.copy()
        test_params = {
            'icon_name': 'ATest',
            'filename': 'atest.tmPreferences',
            'bgcolor': self.bgcolor_dark,
            'theme_name': 'Treble Adaptive.sublime-theme',
            'change_icon': {},
            'auto_prefer_icon': True,
            'prefer_icon': {},
        }

        with patch.multiple(
            self.zukan,
            _apply_change_icon=MagicMock(),
            _apply_prefer_icon=MagicMock(),
            _apply_auto_prefer_icon=MagicMock(),
            _rename_primary_icons=MagicMock(),
            _png_exists=MagicMock(),
        ):
            self.zukan.handle_icon_preferences(test_pref, **test_params)

            self.zukan._apply_change_icon.assert_called_once()
            self.zukan._apply_prefer_icon.assert_called_once()
            self.zukan._apply_auto_prefer_icon.assert_called_once()
            self.zukan._rename_primary_icons.assert_called_once()
            self.zukan._png_exists.assert_called_once()
            mock_save.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.generate_custom_icon'
    )
    def test_get_list_icons_preferences(self, mock_generate):
        mock_zukan_icons = [{'name': 'ATest-1', 'preferences': {}}]
        mock_custom_icons = [
            {'name': 'Custom-1', 'preferences': {}},
            {'name': 'Custom-2'},
        ]

        with patch.object(
            self.zukan, 'zukan_icons_data', return_value=mock_zukan_icons
        ):
            mock_generate.return_value = mock_custom_icons

            result = self.zukan.get_list_icons_preferences()

            self.assertEqual(len(result), 2)
            self.assertIn(mock_zukan_icons[0], result)

    def test_get_file_name(self):
        test_cases = [
            ('ada-dark', 'ada.tmPreferences'),
            ('ada-light', 'ada.tmPreferences'),
            ('ada', 'ada.tmPreferences'),
        ]

        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = self.zukan._get_file_name(input_name)
                self.assertEqual(result, expected)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_prepare_icon_preference_file(self, mock_logger):
        test_preference = 'atest'
        mock_icons = [
            {
                'name': 'ATest',
                'preferences': {
                    'settings': {'icon': 'atest'},
                    'scope': 'source.atest',
                },
            }
        ]

        with patch.multiple(
            self.zukan,
            get_list_icons_preferences=MagicMock(return_value=mock_icons),
            theme_name_setting=MagicMock(return_value='Treble Adaptive.sublime-theme'),
            sidebar_bgcolor=MagicMock(return_value=self.bgcolor_dark),
            prefer_icon_setting=MagicMock(return_value=(True, {})),
            change_icon_setting=MagicMock(return_value={}),
            ignored_icon_setting=MagicMock(return_value=set()),
            handle_icon_preferences=MagicMock(),
        ):
            self.zukan.prepare_icon_preference_file(
                test_preference, self.bgcolor_dark, self.test_dark_theme
            )

            self.zukan.handle_icon_preferences.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icon_preference(self, mock_logger):
        with patch.object(self.zukan, 'prepare_icon_preference_file'):
            self.zukan.create_icon_preference(
                'atest', self.bgcolor_dark, self.test_dark_theme
            )
            mock_logger.info.assert_called_once_with(
                '%s created.', 'atest.tmPreferences'
            )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icon_preference_file_not_found(self, mock_logger):
        test_name = 'not_found'
        expected_fname = test_name + icons_preferences.TMPREFERENCES_EXTENSION

        def side_effect(*args, **kwargs):
            raise FileNotFoundError()

        with patch.object(
            self.zukan, 'prepare_icon_preference_file', side_effect=side_effect
        ):
            self.zukan.create_icon_preference(
                test_name, self.bgcolor_dark, self.test_dark_theme
            )

            mock_logger.error.assert_called_once_with(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                expected_fname,
            )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icon_preference_os_error(self, mock_logger):
        test_name = 'os_error'
        expected_fname = test_name + icons_preferences.TMPREFERENCES_EXTENSION

        def side_effect(*args, **kwargs):
            raise OSError()

        with patch.object(
            self.zukan, 'prepare_icon_preference_file', side_effect=side_effect
        ):
            self.zukan.create_icon_preference(
                test_name, self.bgcolor_dark, self.test_dark_theme
            )

            mock_logger.error.assert_called_once_with(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                expected_fname,
            )

    def test_create_icon_preference_with_icon_version(self):
        test_cases = [
            ('ada', 'ada'),
            ('ada-dark', 'ada'),
            ('ada-light', 'ada'),
        ]

        for input_name, expected_base in test_cases:
            with self.subTest(input_name=input_name):
                with patch.multiple(
                    self.zukan,
                    prepare_icon_preference_file=MagicMock(),
                    _get_file_name=MagicMock(
                        return_value=expected_base
                        + icons_preferences.TMPREFERENCES_EXTENSION
                    ),
                ), patch(
                    'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger'
                ) as mock_logger:
                    self.zukan.create_icon_preference(
                        input_name, self.bgcolor_light, self.test_light_theme
                    )

                    self.zukan.prepare_icon_preference_file.assert_called_once_with(
                        input_name, self.bgcolor_light, self.test_light_theme
                    )
                    mock_logger.info.assert_called_once_with(
                        '%s created.',
                        expected_base + icons_preferences.TMPREFERENCES_EXTENSION,
                    )

    def test_create_icon_preference_with_dark_suffix(self):
        with patch.multiple(
            self.zukan,
            prepare_icon_preference_file=MagicMock(),
            _get_file_name=MagicMock(),
        ):
            test_name = 'ada-dark'
            self.zukan.create_icon_preference(
                test_name, self.bgcolor_light, self.test_light_theme
            )

            self.zukan.prepare_icon_preference_file.assert_called_once_with(
                test_name, self.bgcolor_light, self.test_light_theme
            )

    def test_create_icon_preference_with_light_suffix(self):
        with patch.multiple(
            self.zukan,
            prepare_icon_preference_file=MagicMock(),
            _get_file_name=MagicMock(),
        ):
            test_name = 'ada-light'
            self.zukan.create_icon_preference(
                test_name, self.bgcolor_dark, self.test_dark_theme
            )

            self.zukan.prepare_icon_preference_file.assert_called_once_with(
                test_name, self.bgcolor_dark, self.test_dark_theme
            )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_prepare_icons_preferences_list(self, mock_logger):
        mock_list = [
            {
                'name': 'ATest-1',
                'preferences': {
                    'settings': {'icon': 'atest1'},
                    'scope': 'source.atest1',
                },
            }
        ]

        with patch.multiple(
            self.zukan,
            get_list_icons_preferences=MagicMock(return_value=mock_list),
            theme_name_setting=MagicMock(return_value='Treble Adaptive.sublime-theme'),
            sidebar_bgcolor=MagicMock(return_value=self.bgcolor_dark),
            prefer_icon_setting=MagicMock(return_value=(True, {})),
            change_icon_setting=MagicMock(return_value={}),
            ignored_icon_setting=MagicMock(return_value=set()),
            handle_icon_preferences=MagicMock(),
        ):
            self.zukan.prepare_icons_preferences_list(
                self.bgcolor_dark, self.test_dark_theme
            )

            self.zukan.handle_icon_preferences.assert_called_once()

    def test_prepare_icons_preferences_list_with_ignored(self):
        mock_list = [
            {
                'name': 'Ignored-1',
                'preferences': {
                    'settings': {'icon': 'ignored-icon'},
                    'scope': 'source.ignored',
                },
            }
        ]

        with patch.multiple(
            self.zukan,
            get_list_icons_preferences=MagicMock(return_value=mock_list),
            theme_name_setting=MagicMock(return_value='Treble Adaptive.sublime-theme'),
            sidebar_bgcolor=MagicMock(return_value=self.bgcolor_dark),
            prefer_icon_setting=MagicMock(return_value=(True, {})),
            change_icon_setting=MagicMock(return_value={}),
            ignored_icon_setting=MagicMock(return_value={'Ignored-1'}),
            handle_icon_preferences=MagicMock(),
        ), patch(
            'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger'
        ) as mock_logger:
            self.zukan.prepare_icons_preferences_list(
                self.bgcolor_dark, self.test_dark_theme
            )

            self.zukan.handle_icon_preferences.assert_not_called()
            mock_logger.info.assert_called_with('ignored icon %s', 'Ignored-1')

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icons_preferences(self, mock_logger):
        with patch.object(self.zukan, 'prepare_icons_preferences_list'):
            self.zukan.create_icons_preferences(self.bgcolor_dark, self.test_dark_theme)
            mock_logger.info.assert_called_once_with('tmPreferences created.')

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icons_preferences_file_not_found(self, mock_logger):
        with patch.object(
            self.zukan, 'prepare_icons_preferences_list', side_effect=FileNotFoundError
        ):
            self.zukan.create_icons_preferences(self.bgcolor_dark, self.test_dark_theme)
            mock_logger.error.assert_called_once_with(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                icons_preferences.ZUKAN_ICONS_DATA_FILE,
            )

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_create_icons_preferences_os_error(self, mock_logger):
        with patch.object(
            self.zukan, 'prepare_icons_preferences_list', side_effect=OSError
        ):
            self.zukan.create_icons_preferences(self.bgcolor_dark, self.test_dark_theme)
            mock_logger.error.assert_called_once_with(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                icons_preferences.ZUKAN_ICONS_DATA_FILE,
            )

    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icon_preference(self, mock_logger, mock_remove):
        preference_name = 'atest.tmPreferences'
        result = self.zukan.delete_icon_preference(preference_name)

        self.assertEqual(result, preference_name)
        mock_logger.info.assert_called_once()
        mock_remove.assert_called_once()

    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icon_preference_file_not_found(self, mock_logger, mock_remove):
        mock_remove.side_effect = FileNotFoundError
        preference_name = 'not_found.tmPreferences'

        result = self.zukan.delete_icon_preference(preference_name)

        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r',
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            preference_name,
        )

    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icon_preference_os_error(self, mock_logger, mock_remove):
        mock_remove.side_effect = OSError
        preference_name = 'os_error.tmPreferences'

        result = self.zukan.delete_icon_preference(preference_name)

        self.assertIsNone(result)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r',
            errno.EACCES,
            os.strerror(errno.EACCES),
            preference_name,
        )

    @patch('glob.iglob')
    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icons_preferences(self, mock_logger, mock_remove, mock_iglob):
        mock_iglob.return_value = ['atest1.tmPreferences', 'atest2.tmPreferences']

        self.zukan.delete_icons_preferences()

        self.assertEqual(mock_remove.call_count, 2)
        mock_logger.info.assert_called_once_with('tmPreferences deleted.')

    @patch('glob.iglob')
    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icons_preferences_file_not_found(
        self, mock_logger, mock_remove, mock_iglob
    ):
        mock_remove.side_effect = FileNotFoundError
        mock_iglob.return_value = ['atest1.tmPreferences']

        self.zukan.delete_icons_preferences()

        mock_logger.error.assert_called_once()

    @patch('glob.iglob')
    @patch('os.remove')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_delete_icons_preferences_os_error(
        self, mock_logger, mock_remove, mock_iglob
    ):
        mock_remove.side_effect = OSError
        mock_iglob.return_value = ['atest1.tmPreferences']

        self.zukan.delete_icons_preferences()

        mock_logger.error.assert_called_once()

    @patch('os.path.exists')
    @patch('glob.glob')
    def test_list_created_icons_preferences(self, mock_glob, mock_exists):
        mock_exists.return_value = True
        expected_files = ['atest1.tmPreferences', 'atest2.tmPreferences']
        mock_glob.return_value = [os.path.join('path', f) for f in expected_files]

        result = self.zukan.list_created_icons_preferences()

        self.assertEqual(result, expected_files)

    @patch('os.path.exists')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_list_created_icons_preferences_directory_not_found(
        self, mock_logger, mock_exists
    ):
        mock_exists.return_value = False

        result = self.zukan.list_created_icons_preferences()

        self.assertIsNone(result)
        mock_logger.error.assert_called()

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_preferences.logger')
    def test_list_created_icons_preferences_os_error(
        self, mock_logger, mock_glob, mock_exists
    ):
        mock_exists.return_value = True
        mock_glob.side_effect = OSError

        result = self.zukan.list_created_icons_preferences()

        self.assertIsNone(result)
        mock_logger.error.assert_called()
