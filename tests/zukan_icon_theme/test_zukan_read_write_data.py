# import _pickle as pickle
# import os
# import pytest

# from pyfakefs.fake_filesystem_unittest import TestCase
# from tests.mocks.constants_pickle import (
#     TEST_PICKLE_AUDIO_FILE,
#     TEST_PICKLE_ORDERED_DICT,
# )
# from tests.mocks.constants_yaml import (
#     TEST_YAML_CONTENT,
#     TEST_YAML_DICT,
# )
# from src.zukan_icon_theme.helpers.read_write_data import (
#     dump_yaml_data,
#     read_pickle_data,
# )
# from unittest.mock import patch, mock_open


# class TestLoadFile:
#     def load_pickle(self, path):
#         with open(path, 'rb') as f:
#             return pickle.load(f)

#     # From https://stackoverflow.com/questions/60761451/how-to-use-mock-open-with-pickle-load
#     def test_load_pickle(self):
#         read_data = pickle.dumps(TEST_PICKLE_ORDERED_DICT)
#         with patch(
#             'src.zukan_icon_theme.helpers.read_write_data.open',
#             mock_open(read_data=read_data),
#         ):
#             result = TestLoadFile.load_pickle(self, TEST_PICKLE_AUDIO_FILE)
#             assert result == TEST_PICKLE_ORDERED_DICT


# class TestDumpYamlData:
#     @pytest.fixture(autouse=True)
#     def test_write_file_filenotfounderror(self, caplog):
#         caplog.clear()
#         with patch('src.zukan_icon_theme.helpers.read_write_data.open') as mock_open:
#             mock_open.side_effect = FileNotFoundError
#             dump_yaml_data(TEST_YAML_CONTENT, 'tests/mocks/not_found_yaml.yaml')
#         assert caplog.record_tuples == [
#             (
#                 'src.zukan_icon_theme.helpers.read_write_data',
#                 40,
#                 "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
#             )
#         ]

#     @pytest.fixture(autouse=True)
#     def test_write_file_oserror(self, caplog):
#         caplog.clear()
#         with patch('src.zukan_icon_theme.helpers.read_write_data.open') as mock_open:
#             mock_open.side_effect = OSError
#             dump_yaml_data(TEST_YAML_CONTENT, 'tests/yaml.yaml')
#         assert caplog.record_tuples == [
#             (
#                 'src.zukan_icon_theme.helpers.read_write_data',
#                 40,
#                 "[Errno 13] Permission denied: 'testsyaml.yaml'",
#             )
#         ]


# class TestLoadPickleData:
#     @pytest.fixture(autouse=True)
#     def test_read_file_filenotfounderror(self, caplog):
#         caplog.clear()
#         with patch('src.zukan_icon_theme.helpers.read_write_data.open') as mock_open:
#             mock_open.side_effect = FileNotFoundError
#             read_pickle_data('tests/mocks/not_found_pickle.pkl')
#         assert caplog.record_tuples == [
#             (
#                 'src.zukan_icon_theme.helpers.read_write_data',
#                 40,
#                 "[Errno 2] No such file or directory: 'tests/mocks/not_found_pickle.pkl'",
#             )
#         ]

#     @pytest.fixture(autouse=True)
#     def test_read_file_oserror(self, caplog):
#         caplog.clear()
#         with patch('src.zukan_icon_theme.helpers.read_write_data.open') as mock_open:
#             mock_open.side_effect = OSError
#             read_pickle_data('tests/pickle.pkl')
#         assert caplog.record_tuples == [
#             (
#                 'src.zukan_icon_theme.helpers.read_write_data',
#                 40,
#                 "[Errno 13] Permission denied: 'testspickle.pkl'",
#             )
#         ]


# class TestWriteYamlData(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.setUpClassPyfakefs()
#         cls.fake_fs().create_file('data/afdesign.yaml', contents='test')
#         cls.fake_fs().create_file('data/afphoto.yaml', contents='test')
#         cls.fake_fs().create_file('data/afpub.yaml', contents='test')
#         cls.fake_fs().create_file('data/ai.yaml', contents='test')
#         cls.fake_fs().create_file('data/angular.yaml', contents='test')

#     def test_file_exist(self):
#         dump_yaml_data('test', 'data/afpub.yaml')
#         self.assertTrue(os.path.exists('data/afpub.yaml'))

#     def test_file_not_found(self):
#         dump_yaml_data(TEST_YAML_DICT, 'tests/build/mocks/not_found_yaml.yaml')
#         self.assertFalse(os.path.exists('tests/build/mocks/not_found_yaml.yaml'))

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


# class TestReadPickleData(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.setUpClassPyfakefs()
#         cls.fake_fs().create_file('data/pickle.pkl')

#     def test_file_exist(self):
#         read_pickle_data('data/pickle.pkl')
#         self.assertTrue(os.path.exists('data/pickle.pkl'))

#     def test_file_not_found(self):
#         read_pickle_data('tests/build/mocks/not_found_pickle.pkl')
#         self.assertFalse(os.path.exists('tests/build/mocks/not_found_pickle.pkl'))

#     def test_read_pickle_params(self):
#         read_pickle_data('data/pickle.pkl')
#         self.assertTrue(isinstance('data/pickle.pkl', str))
#         self.assertFalse(isinstance('data/pickle.pkl', int))
#         self.assertFalse(isinstance('data/pickle.pkl', list))
#         self.assertFalse(isinstance('data/pickle.pkl', bool))
#         self.assertFalse(isinstance('data/pickle.pkl', dict))
