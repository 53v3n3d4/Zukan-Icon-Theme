import errno
import importlib
import os

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

od_to_preference = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.od_to_preference'
)


class TestPreferencesFunctions(TestCase):
    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.od_to_preference.logger.error'
    )
    def test_save_tm_preferences_file_not_found(self, mock_logger, mock_open):
        data = OrderedDict(
            [
                ('key1', 'value1'),
                ('key2', 'value2'),
            ]
        )
        file_path = 'invalid_path/tmPreferences.plist'

        od_to_preference.save_tm_preferences(data, file_path)
        mock_logger.assert_called_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )

    @patch('builtins.open', side_effect=OSError)
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.od_to_preference.logger.error'
    )
    def test_save_tm_preferences_os_error(self, mock_logger, mock_open):
        data = OrderedDict(
            [
                ('key1', 'value1'),
                ('key2', 'value2'),
            ]
        )
        file_path = 'invalid_path/tmPreferences.plist'

        od_to_preference.save_tm_preferences(data, file_path)
        mock_logger.assert_called_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )

    def test_build_preference(self):
        data = OrderedDict(
            [
                ('key1', 'value1'),
                ('key2', 'value2'),
            ]
        )

        result = od_to_preference.build_preference(data)

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

    def test_od_to_preference(self):
        data = OrderedDict(
            [
                ('key1', 'value1'),
                ('key2', 'value2'),
            ]
        )

        result = od_to_preference.od_to_preference(data)

        expected_result = (
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<string>value2</string>\n'
        )
        self.assertEqual(result, expected_result)

    def test_od_to_preference_nested(self):
        data = OrderedDict(
            [
                ('key1', 'value1'),
                (
                    'key2',
                    OrderedDict(
                        [
                            ('subkey1', 'subvalue1'),
                            ('subkey2', 'subvalue2'),
                        ]
                    ),
                ),
            ]
        )

        result = od_to_preference.od_to_preference(data)

        expected_result = (
            '\t\t<key>key1</key>\n'
            '\t\t<string>value1</string>\n'
            '\t\t<key>key2</key>\n'
            '\t\t<dict>\n'
            '\t\t\t<key>subkey1</key>\n'
            '\t\t\t<string>subvalue1</string>\n'
            '\t\t\t<key>subkey2</key>\n'
            '\t\t\t<string>subvalue2</string>\n'
            '\t\t</dict>\n'
        )
        self.assertEqual(result, expected_result)

    def test_od_to_preference_empty(self):
        data = OrderedDict()

        result = od_to_preference.od_to_preference(data)
        self.assertEqual(result, '')
