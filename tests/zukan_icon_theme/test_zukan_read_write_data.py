import _pickle as pickle
import importlib
import os
import sublime

from unittest import TestCase
from unittest.mock import mock_open, patch

constants_json = importlib.import_module('Zukan-Icon-Theme.tests.mocks.constants_json')
constants_pickle = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_pickle'
)
constants_plist = importlib.import_module(
    'Zukan-Icon-Theme.tests.mocks.constants_plist'
)
constants_yaml = importlib.import_module('Zukan-Icon-Theme.tests.mocks.constants_yaml')
read_write_data = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data'
)
theme_templates = importlib.import_module(
    'Zukan-Icon-Theme.src.zukan_icon_theme.utils.theme_templates'
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

    def test_load_yaml(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml.yaml',
        )
        result = read_write_data.read_yaml_data(test_file_path)
        self.assertEqual(result, constants_yaml.TEST_YAML_EXPECTED)


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
        with self.assertRaises(OSError):
            read_write_data.dump_yaml_data(
                constants_yaml.TEST_YAML_CONTENT, 'tests/yaml.yaml'
            )


class TestLoadYamlData(TestCase):
    def test_read_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.read_yaml_data('tests/mocks/not_found_yaml.yaml')
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            str(e.exception),
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data')
    def test_read_file_oserror(self, read_yaml_data_mock):
        read_yaml_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testsyaml.yaml'"
        )
        with self.assertRaises(OSError):
            read_write_data.read_yaml_data('tests/yaml.yaml')


class TestDumpJsonData(TestCase):
    def test_write_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.dump_json_data(
                theme_templates.TEMPLATE_JSON, 'tests/mocks/not_found_json.json'
            )
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_json.json'",
            str(e.exception),
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data')
    def test_read_file_oserror(self, read_pickle_data_mock):
        read_pickle_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testspjson.json'"
        )
        with self.assertRaises(OSError):
            read_write_data.dump_json_data(
                theme_templates.TEMPLATE_JSON, 'tests/json.json'
            )


class TestDumpPlistData(TestCase):
    def test_write_file_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError) as e:
            read_write_data.dump_plist_data(
                constants_plist.TEST_PLIST_DICT_PLUGIN,
                'tests/mocks/not_found_plist.plist',
            )
        self.assertEqual(
            "[Errno 2] No such file or directory: 'tests/mocks/not_found_plist.plist'",
            str(e.exception),
        )

    @patch('Zukan-Icon-Theme.src.zukan_icon_theme.helpers.read_write_data')
    def test_read_file_oserror(self, read_pickle_data_mock):
        read_pickle_data_mock.side_effect = OSError(
            "[Errno 13] Permission denied: 'testsplist.plist'"
        )
        with self.assertRaises(OSError):
            read_write_data.dump_plist_data(
                constants_plist.TEST_PLIST_DICT_PLUGIN, 'tests/plist.plist'
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
        with self.assertRaises(OSError):
            read_write_data.read_pickle_data('tests/pickle.pkl')


class TestEditContextMain(TestCase):
    def test_edit_contexts_main_with_scope(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml_edit_contexts_main.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
        )
        read_write_data.edit_contexts_main(test_file_path, 'source.json')
        with open(test_file_path, 'r+') as f:
            result = f.read()
        self.assertEqual(
            constants_yaml.TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITH_SCOPES,
            result,
        )

    def test_edit_contexts_main_without_scope(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml_edit_contexts_main.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
        )
        read_write_data.edit_contexts_main(test_file_path, None)
        with open(test_file_path, 'r+') as f:
            result = f.read()
        self.assertEqual(
            constants_yaml.TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITHOUT_SCOPES,
            result,
        )


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


class TestReadYamlData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml.yaml',
        )
        read_write_data.read_yaml_data(test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

    def test_read_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml.yaml',
        )
        read_write_data.read_yaml_data(test_file_path)
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)


class TestEditYamlDataContextsMain(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml_edit_contexts_main.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
        )
        self.assertTrue(os.path.exists(test_file_path))

    def test_edit_yaml_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            'yaml_edit_contexts_main.yaml',
        )
        read_write_data.dump_yaml_data(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, test_file_path
        )
        self.assertIsInstance(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, dict
        )
        self.assertNotIsInstance(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, int
        )
        self.assertNotIsInstance(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, bool
        )
        self.assertNotIsInstance(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, str
        )
        self.assertNotIsInstance(
            constants_yaml.TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN, list
        )
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)


class TestWriteJsonData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            constants_json.TEST_JSON_FILE,
        )
        read_write_data.dump_json_data(theme_templates.TEMPLATE_JSON, test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

    def test_dump_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            constants_json.TEST_JSON_FILE,
        )
        read_write_data.dump_json_data(theme_templates.TEMPLATE_JSON, test_file_path)
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
        self.assertIsInstance(theme_templates.TEMPLATE_JSON, list)
        self.assertNotIsInstance(theme_templates.TEMPLATE_JSON, dict)
        self.assertNotIsInstance(theme_templates.TEMPLATE_JSON, int)
        self.assertNotIsInstance(theme_templates.TEMPLATE_JSON, bool)
        self.assertNotIsInstance(theme_templates.TEMPLATE_JSON, str)


class TestWritePlistData(TestCase):
    def test_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            constants_plist.TEST_PLIST_FILE_PLUGIN,
        )
        read_write_data.dump_plist_data(
            constants_plist.TEST_PLIST_DICT_PLUGIN, test_file_path
        )
        self.assertTrue(os.path.exists(test_file_path))

    def test_dump_params(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan-Icon-Theme',
            'tests',
            'mocks',
            constants_plist.TEST_PLIST_FILE_PLUGIN,
        )
        read_write_data.dump_plist_data(
            constants_plist.TEST_PLIST_DICT_PLUGIN, test_file_path
        )
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
        self.assertIsInstance(constants_plist.TEST_PLIST_DICT_PLUGIN, dict)
        self.assertNotIsInstance(constants_plist.TEST_PLIST_DICT_PLUGIN, int)
        self.assertNotIsInstance(constants_plist.TEST_PLIST_DICT_PLUGIN, list)
        self.assertNotIsInstance(constants_plist.TEST_PLIST_DICT_PLUGIN, bool)
        self.assertNotIsInstance(constants_plist.TEST_PLIST_DICT_PLUGIN, str)


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
        self.assertIsInstance(test_file_path, str)
        self.assertNotIsInstance(test_file_path, int)
        self.assertNotIsInstance(test_file_path, list)
        self.assertNotIsInstance(test_file_path, bool)
        self.assertNotIsInstance(test_file_path, dict)
