import _pickle as pickle
import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.read_write_data import (
    dump_pickle_data,
    read_pickle_data,
    read_yaml_data,
)
from tests.build.mocks.constants_pickle import (
    TEST_PICKLE_AUDIO_FILE,
    TEST_PICKLE_FILE,
    TEST_PICKLE_ORDERED_DICT,
)
from tests.build.mocks.constants_yaml import (
    TEST_YAML_EMPTY_FILE,
    TEST_YAML_EXPECTED,
)
from unittest.mock import patch, mock_open


class TestDumpFile:
    def test_dump_pickle(self):
        with patch(
            'src.build.helpers.read_write_data.open', mock_open()
        ) as mocked_open:
            dump_pickle_data(TEST_PICKLE_ORDERED_DICT, TEST_PICKLE_FILE)
            mocked_open.assert_called_with(TEST_PICKLE_FILE, 'ab+')


class TestLoadFile:
    def load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    # From https://stackoverflow.com/questions/60761451/how-to-use-mock-open-with-pickle-load
    def test_load_pickle(self):
        read_data = pickle.dumps(TEST_PICKLE_ORDERED_DICT)
        with patch(
            'src.build.helpers.read_write_data.open', mock_open(read_data=read_data)
        ):
            result = TestLoadFile.load_pickle(self, TEST_PICKLE_AUDIO_FILE)
            assert result == TEST_PICKLE_ORDERED_DICT

    @pytest.fixture(autouse=True)
    def test_read_pickle_data_file_not_found(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            read_pickle_data('test/pickle.pkl')

        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 2] No such file or directory: 'test/pickle.pkl'",
            )
        ]
        assert mock_open.call_count == 1

    @pytest.fixture(autouse=True)
    def test_read_pickle_data_os_error(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = OSError
            read_pickle_data('test/pickle.pkl')

        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 13] Permission denied: 'test/pickle.pkl'",
            )
        ]
        assert mock_open.call_count == 1

    def test_read_yaml_empty_file(self):
        with patch('src.build.helpers.read_write_data.open', mock_open()):
            file_data = read_yaml_data(TEST_YAML_EMPTY_FILE)
            assert file_data is None

    def test_read_yaml_file(self):
        with patch(
            'src.build.helpers.read_write_data.open', mock_open()
        ) as mocked_open:
            read_yaml_data('tests/build/mocks/yaml.yaml')
            mocked_open.assert_called_with('tests/build/mocks/yaml.yaml')


class TestYamlData:
    @pytest.mark.parametrize(
        'a, expected', [('tests/build/mocks/yaml.yaml', TEST_YAML_EXPECTED)]
    )
    def test_load_yaml(self, a, expected):
        result = read_yaml_data(a)
        assert result == TEST_YAML_EXPECTED

    @pytest.fixture(autouse=True)
    def test_empty_file(self, capfd):
        read_yaml_data('tests/build/mocks/test_empty_file.yaml')

        out, err = capfd.readouterr()
        assert out == '\x1b[91m[!] test_empty_file.yaml:\x1b[0m yaml file is empty.\n'

    @pytest.fixture(autouse=True)
    def test_not_yaml_file(self, capfd):
        read_yaml_data('tests/build/mocks/plist.plist')

        out, err = capfd.readouterr()
        assert out == '\x1b[35m[!] plist.plist:\x1b[0m file extension is not yaml.\n'

    # This only work is one computer
    # @pytest.fixture(autouse=True)
    # def test_not_exist_yaml_file(self, capfd):
    #     read_yaml_data('tests/build/mocks/test_yaml_file_not_exist.yaml')

    #     out, err = capfd.readouterr()
    #     assert (
    #         out
    #         == '\x1b[91m[!] /Users/macbookpro14/Library/Application Support/Sublime Text/Packages/Zukan Icon Theme/tests/build/mocks/test_yaml_file_not_exist.yaml:\x1b[0m file or directory do not exist.\n'
    #     )

    @pytest.fixture(autouse=True)
    def test_read_yaml_data_file_not_found(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            read_yaml_data('tests/build/mocks/not_found_yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_read_yaml_data_os_error(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = OSError
            read_yaml_data('tests/build/mocks/yaml.yaml')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/yaml.yaml'",
            )
        ]


class TestPickletData:
    @pytest.mark.parametrize(
        'a, b, expected',
        [
            (
                TEST_PICKLE_ORDERED_DICT,
                TEST_PICKLE_FILE,
                TEST_PICKLE_FILE,
            )
        ],
    )
    def test_dump_pickle(self, a, b, expected):
        result = dump_pickle_data(a, b)
        return result
        assert result == TEST_PICKLE_FILE

    @pytest.fixture(autouse=True)
    def test_dump_pickle_data_file_not_found(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            dump_pickle_data(
                TEST_PICKLE_ORDERED_DICT, 'tests/build/mocks/not_found_pickle.pkl'
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks/not_found_pickle.pkl'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_dump_pickle_data_os_error(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.read_write_data.open') as mock_open:
            mock_open.side_effect = OSError
            dump_pickle_data(TEST_PICKLE_ORDERED_DICT, 'tests/build/mocks/plist.plist')
        assert caplog.record_tuples == [
            (
                'src.build.helpers.read_write_data',
                40,
                "[Errno 13] Permission denied: 'tests/build/mocks/plist.plist'",
            )
        ]


class TestReadWriteYamlData(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml', contents='test')
        cls.fake_fs().create_file('data/afphoto.yaml', contents='test')
        cls.fake_fs().create_file('data/afpub.yaml', contents='test')
        cls.fake_fs().create_file('data/ai.yaml', contents='test')
        cls.fake_fs().create_file('data/angular.yaml', contents='test')


#     def test_file_not_found(self):
#         read_yaml_data('tests/build/build/mocks/not_found_yaml.yaml')
#         self.assertFalse(os.path.exists('tests/build/build/mocks/not_found_yaml.yaml'))

#     def test_load_params(self):
#         read_yaml_data('data/afdesign.yaml')
#         self.assertTrue(isinstance('data/afdesign.yaml', str))
#         self.assertFalse(isinstance('data/afdesign.yaml', int))
#         self.assertFalse(isinstance('data/afdesign.yaml', list))
#         self.assertFalse(isinstance('data/afdesign.yaml', bool))
#         self.assertFalse(isinstance('data/afdesign.yaml', dict))

#     def test_dump_params(self):
#         dump_yaml_data(TEST_YAML_DICT, 'data/afdesign.yaml')
#         self.assertTrue(isinstance('data/afdesign.yaml', str))
#         self.assertFalse(isinstance('data/afdesign.yaml', int))
#         self.assertFalse(isinstance('data/afdesign.yaml', list))
#         self.assertFalse(isinstance('data/afdesign.yaml', bool))
#         self.assertFalse(isinstance('data/afdesign.yaml', dict))
#         self.assertTrue(isinstance(TEST_YAML_DICT, dict))
#         self.assertFalse(isinstance(TEST_YAML_DICT, int))
#         self.assertFalse(isinstance(TEST_YAML_DICT, list))
#         self.assertFalse(isinstance(TEST_YAML_DICT, bool))
#         self.assertFalse(isinstance(TEST_YAML_DICT, str))


class TestReadWritePickleData(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/pickle.pkl')

    def test_file_exist(self):
        read_pickle_data('data/pickle.pkl')
        self.assertTrue(os.path.exists('data/pickle.pkl'))


#     def test_file_not_found(self):
#         read_pickle_data('tests/build/build/mocks/not_found_pickle.pkl')
#         self.assertFalse(os.path.exists('tests/build/build/mocks/not_found_pickle.pkl'))

#     def test_read_pickle_params(self):
#         read_pickle_data('data/pickle.pkl')
#         self.assertTrue(isinstance('data/pickle.pkl', str))
#         self.assertFalse(isinstance('data/pickle.pkl', int))
#         self.assertFalse(isinstance('data/pickle.pkl', list))
#         self.assertFalse(isinstance('data/pickle.pkl', bool))
#         self.assertFalse(isinstance('data/pickle.pkl', dict))

#     def test_dump_pickle_params(self):
#         dump_pickle_data(TEST_PICKLE_ORDERED_DICT, 'data/pickle.pkl')
#         self.assertTrue(isinstance('data/pickle.pkl', str))
#         self.assertFalse(isinstance('data/pickle.pkl', int))
#         self.assertFalse(isinstance('data/pickle.pkl', list))
#         self.assertFalse(isinstance('data/pickle.pkl', bool))
#         self.assertFalse(isinstance('data/pickle.pkl', dict))
#         self.assertTrue(isinstance(TEST_PICKLE_ORDERED_DICT, dict))
#         self.assertFalse(isinstance(TEST_PICKLE_ORDERED_DICT, int))
#         self.assertFalse(isinstance(TEST_PICKLE_ORDERED_DICT, list))
#         self.assertFalse(isinstance(TEST_PICKLE_ORDERED_DICT, bool))
#         self.assertFalse(isinstance(TEST_PICKLE_ORDERED_DICT, str))
