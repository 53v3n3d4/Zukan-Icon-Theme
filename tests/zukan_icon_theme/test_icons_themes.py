import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import call, MagicMock, mock_open, patch

icons_themes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes'
)


class TestZukanTheme(TestCase):
    def setUp(self):
        self.zukan_theme = icons_themes.ZukanTheme()
        self.sample_themes = [
            'Packages/Theme - Default/Default.sublime-theme',
            'Packages/Theme - Treble/Treble Dark.sublime-theme',
            'Packages/Theme - Treble/Treble Light.sublime-theme',
            'Packages/Theme - Treble/Treble Adaptive.sublime-theme',
        ]
        self.sample_ignored_themes = ['Ignored Theme.sublime-theme']
        self.icons_path = icons_themes.ZUKAN_PKG_ICONS_PATH
        self.theme_extension = icons_themes.SUBLIME_THEME_EXTENSION

        self.test_theme_path = 'Packages/Theme - Test/Test.sublime-theme'

    def tearDown(self):
        self.zukan_theme = None

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.get_theme_settings')
    def test_ignored_theme_setting_with_themes(self, mock_get_settings):
        mock_get_settings.return_value = (self.sample_ignored_themes, None)
        result = self.zukan_theme.ignored_theme_setting()
        self.assertEqual(result, self.sample_ignored_themes)
        mock_get_settings.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.get_theme_settings')
    def test_ignored_theme_setting_empty(self, mock_get_settings):
        mock_get_settings.return_value = ([], None)
        result = self.zukan_theme.ignored_theme_setting()
        self.assertEqual(result, [])
        mock_get_settings.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    def test_get_all_sublime_themes_with_themes(self, mock_search):
        mock_search.return_value = self.sample_themes
        result = self.zukan_theme.get_all_sublime_themes()
        self.assertEqual(result, self.sample_themes)
        mock_search.assert_called_once()

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    def test_get_all_sublime_themes_empty(self, mock_search):
        mock_search.return_value = []
        result = self.zukan_theme.get_all_sublime_themes()
        self.assertEqual(result, [])
        mock_search.assert_called_once()

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.theme_with_opacity')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.get_theme_settings')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_icon_theme_with_opacity(
        self, mock_file, mock_settings, mock_search, mock_opacity
    ):
        theme_path = 'Packages/Theme - Default/Default.sublime-theme'
        mock_settings.return_value = ([], None)
        mock_search.return_value = self.sample_themes
        mock_opacity.return_value = True

        result = self.zukan_theme.create_icon_theme(theme_path)

        self.assertEqual(result, theme_path)
        mock_file.assert_called_once()
        mock_file().write.assert_called_once_with(icons_themes.TEMPLATE_JSON)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.theme_with_opacity')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.get_theme_settings')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_icon_theme_without_opacity(
        self, mock_file, mock_settings, mock_search, mock_opacity
    ):
        theme_path = 'Packages/Theme - Treble/Treble Adaptive.sublime-theme'
        mock_settings.return_value = ([], None)
        mock_search.return_value = self.sample_themes
        mock_opacity.return_value = False

        result = self.zukan_theme.create_icon_theme(theme_path)

        self.assertEqual(result, theme_path)
        mock_file.assert_called_once()
        mock_file().write.assert_called_once_with(
            icons_themes.TEMPLATE_JSON_WITH_OPACITY
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.get_theme_settings')
    def test_create_icon_theme_not_exists(self, mock_settings, mock_search):
        theme_path = 'Packages/Theme - Nonexistent/Theme.sublime-theme'
        mock_settings.return_value = ([], None)
        mock_search.return_value = self.sample_themes

        result = self.zukan_theme.create_icon_theme(theme_path)

        self.assertIsNone(result)

    @patch('os.path.basename')
    @patch('os.path.join')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logger.info')
    def test_create_icon_theme_ignored(
        self, mock_logger_info, mock_join, mock_basename
    ):
        mock_basename.return_value = 'Ignored Theme.sublime-theme'
        mock_join.return_value = '/Packages/Theme - Ignored/Ignored Theme.sublime-theme'

        self.zukan_theme.ignored_theme_setting = MagicMock(
            return_value=['Ignored Theme.sublime-theme']
        )
        self.zukan_theme.get_all_sublime_themes = MagicMock(
            return_value=[self.test_theme_path]
        )

        result = self.zukan_theme.create_icon_theme(self.test_theme_path)

        self.assertIsNone(result)
        mock_logger_info.assert_called_once_with(
            'ignored theme %s', 'Ignored Theme.sublime-theme'
        )

    @patch('os.path.basename')
    @patch('os.path.join')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logger.error')
    def test_create_icon_theme_file_not_found(
        self, mock_logger_error, mock_join, mock_basename
    ):
        mock_basename.return_value = 'Theme.sublime-theme'
        mock_join.return_value = 'Packages/Theme - Nonexistent/Theme.sublime-theme'
        self.zukan_theme.ignored_theme_setting = MagicMock(return_value=[])
        self.zukan_theme.get_all_sublime_themes = MagicMock(return_value=[])

        result = self.zukan_theme.create_icon_theme(self.test_theme_path)

        self.assertIsNone(result)
        mock_logger_error.assert_any_call(
            'theme name does not exist. Use menu Command Palette > View Package File '
            '> theme name.'
        )
        mock_logger_error.assert_called_with(
            '[Errno %d] %s: %r',
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            self.test_theme_path,
        )
        self.assertEqual(mock_logger_error.call_count, 2)

    @patch('os.path.basename')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_icon_theme_os_error(self, mock_file, mock_join, mock_basename):
        mock_basename.return_value = 'Theme.sublime-theme'
        mock_join.return_value = '/Packages/Test/Theme.sublime-theme'
        mock_file.side_effect = OSError(errno.EACCES, 'Permission denied')

        self.zukan_theme.ignored_theme_setting = MagicMock(return_value=[])
        self.zukan_theme.get_all_sublime_themes = MagicMock(
            return_value=[self.test_theme_path]
        )

        result = self.zukan_theme.create_icon_theme(self.test_theme_path)
        self.assertIsNone(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    def test_create_icons_themes(self, mock_search):
        mock_search.return_value = self.sample_themes
        with patch.object(self.zukan_theme, 'create_icon_theme') as mock_create:
            result = self.zukan_theme.create_icons_themes()
            self.assertEqual(result, self.sample_themes)
            self.assertEqual(mock_create.call_count, len(self.sample_themes))

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    def test_create_icons_themes_empty(self, mock_search):
        mock_search.return_value = None
        result = self.zukan_theme.create_icons_themes()
        self.assertIsNone(result)

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logging.Logger.error'
    )
    def test_create_icons_themes_file_not_found(self, mock_logger):
        with patch.object(
            self.zukan_theme, 'get_all_sublime_themes', return_value=None
        ):
            self.zukan_theme.create_icons_themes()
            mock_logger.assert_has_calls(
                [
                    call('list is empty.'),
                    call(
                        '[Errno %d] %s: %r',
                        errno.ENOENT,
                        os.strerror(errno.ENOENT),
                        None,
                    ),
                ]
            )

    @patch('os.remove')
    def test_delete_icon_theme(self, mock_remove):
        theme_name = 'Treble Light.sublime-theme'
        result = self.zukan_theme.delete_icon_theme(theme_name)
        self.assertEqual(result, theme_name)
        mock_remove.assert_called_once()

    @patch('os.remove')
    def test_delete_icon_theme_file_not_found(self, mock_remove):
        mock_remove.side_effect = FileNotFoundError()
        theme_name = 'Not Found.sublime-theme'
        result = self.zukan_theme.delete_icon_theme(theme_name)
        self.assertIsNone(result)

    @patch('os.remove')
    def test_delete_icon_theme_os_error(self, mock_remove):
        mock_remove.side_effect = OSError(errno.EACCES, 'Permission denied')
        theme_name = 'Permission Error.sublime-theme'
        result = self.zukan_theme.delete_icon_theme(theme_name)
        self.assertIsNone(result)

    @patch('glob.iglob')
    @patch('os.remove')
    def test_delete_icons_themes(self, mock_remove, mock_iglob):
        mock_themes = [
            os.path.join(self.icons_path, 'Treble Dark.sublime-theme'),
            os.path.join(self.icons_path, 'Treble Light.sublime-theme'),
        ]
        mock_iglob.return_value = mock_themes

        self.zukan_theme.delete_icons_themes()

        self.assertEqual(mock_remove.call_count, len(mock_themes))
        mock_remove.assert_has_calls([call(theme) for theme in mock_themes])

    @patch('glob.iglob')
    @patch('os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logging.Logger.error'
    )
    def test_delete_icons_themes_file_not_found(
        self, mock_logger, mock_remove, mock_iglob
    ):
        mock_themes = ['Treble Adaptive.sublime-theme']
        mock_iglob.return_value = mock_themes
        mock_remove.side_effect = FileNotFoundError()

        self.zukan_theme.delete_icons_themes()

        mock_remove.assert_called_once_with('Treble Adaptive.sublime-theme')
        mock_logger.assert_called_once_with(
            '[Errno %d] %s: %r',
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            'Treble Adaptive.sublime-theme',
        )

    @patch('glob.iglob')
    @patch('os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logging.Logger.error'
    )
    def test_delete_icons_themes_os_error(self, mock_logger, mock_remove, mock_iglob):
        mock_themes = ['Treble Adaptive.sublime-theme']
        mock_iglob.return_value = mock_themes
        mock_error = OSError()
        mock_error.errno = errno.EACCES
        mock_remove.side_effect = mock_error

        self.zukan_theme.delete_icons_themes()

        mock_remove.assert_called_once_with('Treble Adaptive.sublime-theme')
        mock_logger.assert_called_once_with(
            '[Errno %d] %s: %r',
            errno.EACCES,
            os.strerror(errno.EACCES),
            'Treble Adaptive.sublime-theme',
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    @patch('glob.glob')
    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_unused_icon_theme(
        self, mock_remove, mock_exists, mock_glob, mock_search
    ):
        installed_themes = ['path_icons/Treble Adaptive.sublime-theme']
        created_themes = ['Treble Adaptive.sublime-theme', 'unused.sublime-theme']

        mock_search.return_value = installed_themes
        mock_exists.return_value = True
        mock_glob.return_value = [
            os.path.join(self.icons_path, theme) for theme in created_themes
        ]

        self.zukan_theme.delete_unused_icon_theme()

        mock_remove.assert_called_once_with(
            os.path.join(self.icons_path, 'unused.sublime-theme')
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.search_resources_sublime_themes'
    )
    @patch('glob.glob')
    @patch('os.path.exists')
    def test_delete_unused_icon_theme_no_unused(
        self, mock_exists, mock_glob, mock_search
    ):
        installed_themes = ['Packages/Theme - Name/Theme-1.sublime-theme']
        created_themes = ['Theme-1.sublime-theme']

        mock_search.return_value = installed_themes
        mock_exists.return_value = True
        mock_glob.return_value = [
            os.path.join(self.icons_path, theme) for theme in created_themes
        ]

        with patch.object(self.zukan_theme, 'delete_icon_theme') as mock_delete:
            self.zukan_theme.delete_unused_icon_theme()
            mock_delete.assert_not_called()

    @patch('os.path.exists')
    @patch('glob.glob')
    def test_list_created_icons_themes(self, mock_glob, mock_exists):
        mock_exists.return_value = True
        expected_themes = ['theme1.sublime-theme', 'theme2.sublime-theme']
        mock_glob.return_value = [
            os.path.join(self.icons_path, theme) for theme in expected_themes
        ]

        result = self.zukan_theme.list_created_icons_themes()

        self.assertEqual(result, expected_themes)
        mock_exists.assert_called_once()
        mock_glob.assert_called_once()

    @patch('os.path.exists')
    def test_list_created_icons_themes_directory_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = self.zukan_theme.list_created_icons_themes()
        self.assertIsNone(result)

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.lib.icons_themes.logger')
    def test_list_created_icons_themes_os_error(
        self, mock_logger, mock_glob, mock_exists
    ):
        mock_exists.return_value = True
        mock_glob.side_effect = OSError

        result = self.zukan_theme.list_created_icons_themes()

        self.assertIsNone(result)
        mock_logger.error.assert_called()
