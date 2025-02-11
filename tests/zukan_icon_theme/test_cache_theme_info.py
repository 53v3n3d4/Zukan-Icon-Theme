import importlib
import json

from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import call, patch, mock_open

cache_theme_info = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info'
)


class TestCacheThemeInfo(TestCase):
    def setUp(self):
        self.test_theme_info = {
            'themes': [
                {
                    'name': 'Treble Adaptive.sublime-theme',
                    'source': '/test/path/Treble Adaptive.sublime-theme',
                    'st_version': cache_theme_info.sublime.version(),
                    'opacity': {'value': True, 'last_updated': 1000},
                }
            ]
        }
        self.test_theme_info_default = {
            'themes': [
                {
                    'name': 'Default.sublime-theme',
                    'st_version': cache_theme_info.sublime.version(),
                    'opacity': {'value': True, 'last_updated': 1000},
                }
            ]
        }
        self.test_theme = '/test/path/Treble Adaptive.sublime-theme'
        self.test_theme_default = '/test/path/Default.sublime-theme'

    @patch('os.path.getmtime')
    def test_get_modified_time(self, mock_getmtime):
        mock_getmtime.return_value = 1000
        result = cache_theme_info.get_modified_time(self.test_theme)
        self.assertEqual(result, 1000)
        result = cache_theme_info.get_modified_time(
            '/empty/dir/Treble Adaptive.sublime-theme'
        )
        self.assertIsInstance(result, float)

    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.datetime')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.os.path.getmtime'
    )
    def test_get_modified_time_defaut_st_themes(self, mock_getmtime, mock_datetime):
        mock_now = datetime(2025, 2, 5, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_getmtime.return_value = 1611168000
        mock_datetime.fromtimestamp.return_value = mock_now

        result = cache_theme_info.get_modified_time(self.test_theme)

        expected_result = mock_now.replace(microsecond=0).timestamp()
        self.assertEqual(result, expected_result)

    @patch('os.path.exists')
    def test_get_file_path(self, mock_exists):
        mock_exists.side_effect = [True, False]

        result = cache_theme_info.get_file_path(self.test_theme)
        self.assertEqual(result, self.test_theme)

        result = cache_theme_info.get_file_path(
            '/Theme - Default/Default.sublime-theme'
        )
        self.assertEqual(result, 'Theme - Default')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.THEME_INFO_FILE',
        '/mock/theme_info.json',
    )
    @patch('os.path.basename')
    def test_is_theme_info_valid(
        self, mock_basename, mock_get_file_path, mock_get_time, mock_file, mock_exists
    ):
        test_name = 'Treble Adaptive.sublime-theme'

        mock_exists.side_effect = [True, True]
        mock_get_file_path.return_value = self.test_theme
        mock_get_time.return_value = 1000
        mock_basename.return_value = test_name
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(
            self.test_theme_info
        )

        result = cache_theme_info.is_theme_info_valid(self.test_theme)
        self.assertEqual(result, True)

        mock_basename.assert_any_call(self.test_theme)
        mock_get_file_path.assert_called_once_with(self.test_theme)
        mock_get_time.assert_called_once_with(self.test_theme)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.THEME_INFO_FILE',
        '/mock/theme_info.json',
    )
    def test_is_theme_info_vaid_none(self, mock_file, mock_exists):
        test_path = None
        mock_exists.side_effect = [False, False]

        result = cache_theme_info.is_theme_info_valid(test_path)
        self.assertEqual(result, None)

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_path.return_value = self.test_theme
        mock_mod_time.return_value = 1000
        mock_data = {'themes': []}
        mock_file().read.return_value = json.dumps(mock_data)

        cache_theme_info.save_theme_info(self.test_theme, '0.5')

        written_data = ''
        for call_args in mock_file().write.call_args_list:
            written_data += call_args[0][0]

        parsed_data = json.loads(written_data)

        self.assertEqual(len(parsed_data['themes']), 1)
        theme = parsed_data['themes'][0]
        self.assertEqual(theme['opacity']['value'], '0.5')
        self.assertEqual(theme['name'], 'Treble Adaptive.sublime-theme')
        self.assertEqual(theme['source'], self.test_theme)
        self.assertEqual(theme['opacity']['last_updated'], 1000)

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info_default_theme_no_update(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_path.return_value = self.test_theme_default
        last_updated = 1000
        mock_mod_time.return_value = last_updated

        mock_file().read.return_value = json.dumps(self.test_theme_info_default)

        with patch.object(
            cache_theme_info, 'ST_DEFAULT_THEMES', ['Default.sublime-theme']
        ):
            cache_theme_info.save_theme_info(self.test_theme_default, True)

        mock_file().write.assert_not_called()

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info_default_theme_update(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_path.return_value = self.test_theme_default
        new_time = 2000
        mock_mod_time.return_value = new_time

        mock_file().read.return_value = json.dumps(self.test_theme_info_default)

        with patch.object(
            cache_theme_info, 'ST_DEFAULT_THEMES', ['Default.sublime-theme']
        ):
            cache_theme_info.save_theme_info(self.test_theme_default, False)

        written_data = ''
        for call_args in mock_file().write.call_args_list:
            written_data += call_args[0][0]
        parsed_data = json.loads(written_data)
        theme = parsed_data['themes'][0]
        self.assertEqual(theme['opacity']['value'], False)
        self.assertEqual(theme['opacity']['last_updated'], new_time)

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info_no_update(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_path.return_value = self.test_theme
        mock_mod_time.return_value = 1000

        mock_file().read.return_value = json.dumps(self.test_theme_info)

        cache_theme_info.save_theme_info(self.test_theme, True)

        mock_file().write.assert_not_called()

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info_update(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = True
        mock_get_path.return_value = self.test_theme
        new_time = 2000
        mock_mod_time.return_value = new_time

        mock_file().read.return_value = json.dumps(self.test_theme_info)

        cache_theme_info.save_theme_info(self.test_theme, False)

        written_data = ''
        for call_args in mock_file().write.call_args_list:
            written_data += call_args[0][0]
        parsed_data = json.loads(written_data)
        theme = parsed_data['themes'][0]
        self.assertEqual(theme['opacity']['value'], False)
        self.assertEqual(theme['opacity']['last_updated'], new_time)

    @patch('os.path.exists')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_modified_time'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_file_path'
    )
    @patch('builtins.open', new_callable=mock_open)
    def test_save_theme_info_no_theme_info_file(
        self, mock_file, mock_get_path, mock_mod_time, mock_exists
    ):
        mock_exists.return_value = False
        mock_get_path.return_value = self.test_theme
        mock_mod_time.return_value = 1000

        cache_theme_info.save_theme_info(self.test_theme, True)

        written_data = ''
        for call_args in mock_file().write.call_args_list:
            written_data += call_args[0][0]
        parsed_data = json.loads(written_data)

        self.assertIn('themes', parsed_data)
        self.assertEqual(len(parsed_data['themes']), 1)

        theme = parsed_data['themes'][0]
        self.assertEqual(theme['name'], 'Treble Adaptive.sublime-theme')
        self.assertEqual(theme['source'], self.test_theme)
        self.assertEqual(theme['opacity']['value'], True)
        self.assertEqual(theme['opacity']['last_updated'], 1000)

        mock_file.assert_has_calls([call(cache_theme_info.THEME_INFO_FILE, 'w')])

        mock_file().read.assert_not_called()

        self.assertEqual(parsed_data, self.test_theme_info)

    @patch('os.path.exists')
    @patch('os.path.getctime')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_cached_theme_info_lifespan'
    )
    def test_cache_theme_info_lifespan(self, mock_lifespan, mock_ctime, mock_exists):
        mock_exists.return_value = True
        mock_lifespan.return_value = 30
        # Set creation time to 31 days ago
        mock_ctime.return_value = (datetime.now() - timedelta(days=31)).timestamp()

        result = cache_theme_info.cache_theme_info_lifespan()
        self.assertTrue(result)

    @patch('os.path.exists')
    @patch('os.path.getctime')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.get_cached_theme_info_lifespan'
    )
    def test_cache_theme_info_not_expired(self, mock_lifespan, mock_ctime, mock_exists):
        mock_exists.return_value = True
        mock_lifespan.return_value = 30
        # Set creation time to 29 days ago
        mock_ctime.return_value = (datetime.now() - timedelta(days=29)).timestamp()

        result = cache_theme_info.cache_theme_info_lifespan()
        self.assertFalse(result)

    @patch('os.path.exists')
    def test_cache_theme_info_no_file(self, mock_exists):
        mock_exists.return_value = False
        result = cache_theme_info.cache_theme_info_lifespan()
        self.assertFalse(result)

    @patch('os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.cache_theme_info_lifespan'
    )
    def test_delete_cached_theme_info(self, mock_lifespan, mock_remove):
        mock_lifespan.return_value = True
        cache_theme_info.delete_cached_theme_info()
        mock_remove.assert_called_once_with(cache_theme_info.THEME_INFO_FILE)

    @patch('os.remove')
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.cache_theme_info.cache_theme_info_lifespan'
    )
    def test_delete_cached_theme_info_not_expired(self, mock_lifespan, mock_remove):
        mock_lifespan.return_value = False
        cache_theme_info.delete_cached_theme_info()
        mock_remove.assert_not_called()
