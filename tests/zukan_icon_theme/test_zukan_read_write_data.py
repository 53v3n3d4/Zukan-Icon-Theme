import _pickle as pickle
import importlib
import os
import sublime

from unittest import TestCase
from unittest.mock import mock_open, patch

constants_pickle = importlib.import_module(
    'Zukan Icon Theme.tests.mocks.constants_pickle'
)
read_write_data = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data'
)


class TestLoadFile(TestCase):
    def load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    # From https://stackoverflow.com/questions/60761451/how-to-use-mock-open-with-pickle-load
    def test_load_pickle(self):
        read_data = pickle.dumps(constants_pickle.TEST_PICKLE_ORDERED_DICT)
        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data',
            mock_open(read_data=read_data),
        ):
            test_file_path = os.path.join(
                sublime.packages_path(),
                'Zukan Icon Theme',
                constants_pickle.TEST_PICKLE_AUDIO_FILE,
            )
            result = TestLoadFile.load_pickle(self, test_file_path)
            self.assertEqual(result, constants_pickle.TEST_PICKLE_ORDERED_DICT)


class TestLoadPickleData(TestCase):
    def test_read_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.read_pickle_data('tests/mocks/not_found_pickle.pkl')
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_pickle.pkl'",
            str(e.exception),
        )

    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data.read_pickle_data'
    )
    def test_read_file_oserror(self, read_pickle_data_mock):
        read_pickle_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testspickle.pkl'"
        )
        with self.assertRaises(OSError):
            read_write_data.read_pickle_data('tests/pickle.pkl')


# class TestEditContextMain(TestCase):
#     def test_edit_contexts_main_with_scope(self):
#         test_file_path = os.path.join(
#             sublime.packages_path(),
#             'Zukan Icon Theme',
#             'tests',
#             'mocks',
#             'yaml_edit_contexts_main.yaml',
#         )
#         read_write_data.dump_yaml_data(
#             constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
#         )
#         read_write_data.edit_contexts_main(test_file_path, 'source.json')
#         with open(test_file_path, 'r+') as f:
#             result = f.read()
#         self.assertEqual(
#             constants_yaml.TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITH_SCOPES,
#             result,
#         )

#     def test_edit_contexts_main_without_scope(self):
#         test_file_path = os.path.join(
#             sublime.packages_path(),
#             'Zukan Icon Theme',
#             'tests',
#             'mocks',
#             'yaml_edit_contexts_main.yaml',
#         )
#         read_write_data.dump_yaml_data(
#             constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
#         )
#         read_write_data.edit_contexts_main(test_file_path, None)
#         with open(test_file_path, 'r+') as f:
#             result = f.read()
#         self.assertEqual(
#             constants_yaml.TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITHOUT_SCOPES,
#             result,
#         )


class TestReadPickleData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan Icon Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )
        read_write_data.read_pickle_data(test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

    def test_read_pickle_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan Icon Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )
        read_write_data.read_pickle_data(test_file_path)
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
