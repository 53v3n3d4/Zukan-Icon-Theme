import importlib
import os
import sublime

from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, patch

clean_data = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.clean_data'
)
constants_plist = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_plist'
)
read_write_data = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data'
)


class TestWriteFile(TestCase):
    def test_mock_write_plist(self):
        mock = Mock()
        mock.clean_data.clean_plist_tag(constants_plist.TEST_PLIST_FILE_PLUGIN)
        mock.clean_data.clean_plist_tag.assert_called_with(
            constants_plist.TEST_PLIST_FILE_PLUGIN
        )


params_list = [
    (constants_plist.TEST_PLIST_DICT_PLUGIN, constants_plist.TEST_PLIST_EXPECTED_PLUGIN)
]


class TestCleanPlistTag(TestCase):
    def test_clean_plist_tag(self):
        for p1, p2 in params_list:
            with self.subTest(params_list):
                test_file_path = os.path.join(
                    sublime.packages_path(),
                    'Zukan-Icon-Theme',
                    'tests',
                    'mocks',
                    constants_plist.TEST_PLIST_FILE_PLUGIN,
                )
                read_write_data.dump_plist_data(p1, test_file_path)
                clean_data.clean_plist_tag(test_file_path)
                with open(test_file_path, 'r+') as f:
                    result = f.read()
                self.assertEqual(result, p2)

    def test_replace_line(self):
        test_line = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        test_removed = ''
        result = clean_data._replace_line(test_line)
        self.assertEqual(result, test_removed)

    def test_replace_line_not_remove(self):
        test_line = 'Text not unused'
        test_removed = ''
        result = clean_data._replace_line(test_line)
        self.assertNotEqual(result, test_removed)

    def test_write_plist_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            clean_data.clean_plist_tag(constants_plist.TEST_PLIST_FILE)
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/bar.plist'", str(e.exception)
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.clean_data')
    def test_write_plist_file_oserror(self, clean_plist_tag_mock):
        clean_plist_tag_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'tests/mock/plist.plist'"
        )
        with self.assertRaises(OSError) as e:
            clean_data.clean_plist_tag('tests/mocks/plist.plist')

    # def test_write_plist_file_stdout(self):
    #     with patch('sys.stderr', new = StringIO()) as fake_out:
    #         clean_data.clean_plist_tag(constants_plist.TEST_PLIST_FILE)

    #         # Expect a warning message to stderr
    #         expected_err = "[Errno 2] No such file or directory: 'tests/bar.plist'"
    #         self.assertEqual(fake_out.getvalue(), expected_err)

    # @patch('sys.stderr', new_callable = StringIO)
    # def test_write_plist_file_stdout(self, stderr):
    #     clean_data.clean_plist_tag(constants_plist.TEST_PLIST_FILE)

    #     # Expect a warning message to stderr
    #     expected_err = "[Errno 2] No such file or directory: 'tests/bar.plist'"
    #     self.assertEqual(stderr.getvalue(), expected_err)
