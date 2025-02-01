import errno
import importlib
import os

from unittest import TestCase
from unittest.mock import patch, mock_open

dict_to_preference = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.dict_to_preference'
)


class TestPreferencesFunctions(TestCase):
    def test_build_preference(self):
        data = {
            'key1': 'value1',
            'key2': 'value2',
        }

        result = dict_to_preference.build_preference(data)

        expected_result = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<plist version="1.0">\n'
            '\t<dict>\n'
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<string>value2</string>\n'
            '\t</dict>\n'
            '</plist>\n'
        )
        self.assertEqual(result, expected_result)

    def test_dict_to_preference(self):
        data = {
            'key1': 'value1',
            'key2': 'value2',
        }

        result = dict_to_preference.dict_to_preference(data)

        expected_result = (
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<string>value2</string>\n'
        )
        self.assertEqual(result, expected_result)

    def test_dict_to_preference_nested(self):
        data = {
            'key1': 'value1',
            'key2': {
                'sub_key1': 'sub_value1',
                'sub_key2': 'sub_value2',
            },
        }

        result = dict_to_preference.dict_to_preference(data)

        expected_result = (
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<dict>\n'
            '\t\t\t<key>sub_key1</key>\n'
            '\t\t\t<string>sub_value1</string>\n'
            '\t\t\t<key>sub_key2</key>\n'
            '\t\t\t<string>sub_value2</string>\n'
            '\t\t</dict>\n'
        )
        self.assertEqual(result, expected_result)

    def test_dict_to_preference_empty(self):
        data = {}

        result = dict_to_preference.dict_to_preference(data)
        self.assertEqual(result, '')

    @patch('builtins.open', new_callable=mock_open)
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.dict_to_preference.logger')
    def test_save_tm_preferences(self, mock_logger, mock_open):
        data = {
            'key1': 'value1',
            'key2': 'value2',
        }
        file_path = 'file.tmPreferences'

        dict_to_preference.save_tm_preferences(data, file_path)

        expected_result = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<plist version="1.0">\n'
            '\t<dict>\n'
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<string>value2</string>\n'
            '\t</dict>\n'
            '</plist>\n'
        )

        mock_open.assert_called_once_with(file_path, 'w')
        mock_open().write.assert_called_once_with(expected_result)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.dict_to_preference.logger.error'
    )
    def test_save_tm_preferences_file_not_found(self, mock_logger, mock_open):
        data = {
            'key1': 'value1',
            'key2': 'value2',
        }

        file_path = 'invalid_path/file.tmPreferences'

        dict_to_preference.save_tm_preferences(data, file_path)
        mock_logger.assert_called_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )

    @patch('builtins.open', side_effect=OSError)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.dict_to_preference.logger.error'
    )
    def test_save_tm_preferences_os_error(self, mock_logger, mock_open):
        data = {
            'key1': 'value1',
            'key2': 'value2',
        }

        file_path = 'invalid_path/file.tmPreferences'

        dict_to_preference.save_tm_preferences(data, file_path)
        mock_logger.assert_called_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )
