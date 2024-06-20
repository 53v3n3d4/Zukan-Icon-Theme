import _pickle as pickle
import importlib
import plistlib
import os
import sublime

from unittest import TestCase
from unittest.mock import mock_open, patch

constants_pickle = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_pickle'
)
constants_yaml = importlib.import_module('Zukan-Icon-Theme.tests.mocks.constants_yaml')
read_write_data = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data'
)


class TestLoadFile(TestCase):
    def load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    # From https://stackoverflow.com/questions/60761451/how-to-use-mock-open-with-pickle-load
    def test_load_pickle(self):
        read_data = pickle.dumps(constants_pickle.TEST_PICKLE_ORDERED_DICT)
        with patch(
            'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data.open',
            mock_open(read_data=read_data),
        ):
            test_file_path = os.path.join(
                sublime.packages_path(),
                'Zukan-Icon-Theme',
                constants_pickle.TEST_PICKLE_AUDIO_FILE,
            )
            result = TestLoadFile.load_pickle(self, test_file_path)
            self.assertEqual(result, constants_pickle.TEST_PICKLE_ORDERED_DICT)


class TestDumpYamlData(TestCase):
    def test_write_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.dump_yaml_data(
                constants_yaml.TEST_YAML_CONTENT, 'tests/mocks/not_found_yaml.yaml'
            )
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            str(e.exception),
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data')
    def test_read_file_oserror(self, read_pickle_data_mock):
        read_pickle_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testsyaml.yaml'"
        )
        with self.assertRaises(OSError) as e:
            read_write_data.dump_yaml_data(
                constants_yaml.TEST_YAML_CONTENT, 'tests/yaml.yaml'
            )


class TestLoadPickleData(TestCase):
    def test_read_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.read_pickle_data('tests/mocks/not_found_pickle.pkl')
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_pickle.pkl'",
            str(e.exception),
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data')
    def test_read_file_oserror(self, read_pickle_data_mock):
        read_pickle_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testspickle.pkl'"
        )
        with self.assertRaises(OSError) as e:
            read_write_data.read_pickle_data('tests/pickle.pkl')


class TestWriteYamlData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_EXPECTED, test_file_path
        )
        self.assertTrue(os.path.exists(test_file_path))

    def test_dump_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_EXPECTED, test_file_path
        )
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
        self.assertIsInstance(constants_yaml.TEST_YAML_EXPECTED, dict)
        self.assertNotIsInstance(constants_yaml.TEST_YAML_EXPECTED, int)
        self.assertNotIsInstance(constants_yaml.TEST_YAML_EXPECTED, list)
        self.assertNotIsInstance(constants_yaml.TEST_YAML_EXPECTED, bool)
        self.assertNotIsInstance(constants_yaml.TEST_YAML_EXPECTED, str)


class TestReadPickleData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )
        read_write_data.read_pickle_data(test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

    def test_read_pickle_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )
        read_write_data.read_pickle_data(test_file_path)
        self.assertIsInstance('data/pickle.pkl', str)
        self.assertNotIsInstance('data/pickle.pkl', int)
        self.assertNotIsInstance('data/pickle.pkl', list)
        self.assertNotIsInstance('data/pickle.pkl', bool)
        self.assertNotIsInstance('data/pickle.pkl', dict)
