import _pickle as pickle
import errno
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


class TestReadPickleData(TestCase):
    def setUp(self):
        self.test_file = 'zukan.pkl'

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
            result = TestReadPickleData.load_pickle(self, test_file_path)
            self.assertEqual(result, constants_pickle.TEST_PICKLE_ORDERED_DICT)

    @patch('builtins.open')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data.logger')
    def test_read_pickle_data_file_not_found(self, mock_logger, mock_file):
        mock_file.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError):
            read_write_data.read_pickle_data(self.test_file)

        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), self.test_file
        )

    @patch('builtins.open')
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data.logger')
    def test_read_pickle_data_os_error(self, mock_logger, mock_file):
        mock_file.side_effect = OSError()

        with self.assertRaises(OSError):
            read_write_data.read_pickle_data(self.test_file)

        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), self.test_file
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('_pickle.load')
    def test_read_pickle_data(self, mock_pickle_load, mock_file):
        mock_pickle_load.side_effect = [
            {'key1': 'value1'},
            {'key2': 'value2'},
            EOFError(),
        ]

        result = read_write_data.read_pickle_data(self.test_file)

        self.assertEqual(result, [{'key1': 'value1'}, {'key2': 'value2'}])
        mock_file.assert_called_once_with(self.test_file, 'rb')

    def test_read_pickle_data_file_exist(self):
        test_file_path = os.path.join(
            sublime.packages_path(),
            'Zukan Icon Theme',
            constants_pickle.TEST_PICKLE_AUDIO_FILE,
        )
        read_write_data.read_pickle_data(test_file_path)
        self.assertTrue(os.path.exists(test_file_path))

    def test_read_pickle_data_params(self):
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


class TestDumpPickleData(TestCase):
    def setUp(self):
        self.test_data = {'key': 'value'}
        self.test_file = 'zukan.pkl'

    @patch('builtins.open', new_callable=mock_open)
    @patch('_pickle.dump')
    def test_dump_pickle_data(self, mock_pickle_dump, mock_file):
        read_write_data.dump_pickle_data(self.test_data, self.test_file)

        mock_file.assert_called_once_with(self.test_file, 'ab+')
        mock_pickle_dump.assert_called_once_with(
            self.test_data, mock_file(), protocol=3
        )

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data.logger')
    def test_dump_pickle_data_file_not_found(self, mock_logger, mock_open):
        data = {'name': 'ATest-1', 'version': 2}

        file_path = 'invalid_path/zukan.pkl'

        read_write_data.dump_pickle_data(data, file_path)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )

    @patch('builtins.open', side_effect=OSError)
    @patch('Zukan Icon Theme.src.zukan_icon_theme.helpers.read_write_data.logger')
    def test_dump_pickle_data_os_error(self, mock_logger, mock_open):
        data = {'name': 'ATest-2', 'version': 2}

        file_path = 'invalid_path/zukan.pkl'

        read_write_data.dump_pickle_data(data, file_path)
        mock_logger.error.assert_called_once_with(
            '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), file_path
        )


class TestEdtiContextsMain(TestCase):
    def setUp(self):
        self.test_syntax_file = 'ATest.sublime-syntax'

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(read_write_data.logger, 'error')
    def test_edit_contexts_main_file_not_found(self, mock_error, mock_open):
        mock_open.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            read_write_data.edit_contexts_main(self.test_syntax_file)

        mock_error.assert_called_with(
            '[Errno %d] %s: %r',
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            self.test_syntax_file,
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch.object(read_write_data.logger, 'error')
    def test_edit_contexts_main_os_error(self, mock_error, mock_open):
        mock_open.side_effect = OSError

        with self.assertRaises(OSError):
            read_write_data.edit_contexts_main(self.test_syntax_file)

        mock_error.assert_called_with(
            '[Errno %d] %s: %r',
            errno.EACCES,
            os.strerror(errno.EACCES),
            self.test_syntax_file,
        )

    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'contexts:\n  main:\n    - include: some_other_include\n'
            '      apply_prototype: some_value\n'
        ),
    )
    @patch.object(read_write_data.logger, 'debug')
    def test_edit_contexts_main_with_scope(self, mock_debug, mock_open):
        file_path = 'ATest.yaml'
        scope = 'source.atest'
        read_write_data.edit_contexts_main(file_path, scope)

        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')

        expected_content = (
            'contexts:\n  main:\n    - include: scope:source.atest#prototype\n'
            '      include: scope:source.atest\n'
        )
        mock_open().write.assert_called_with(expected_content)

        mock_debug.assert_called_with('edited file %r contaxts main.', file_path)

    @patch(
        'builtins.open',
        new_callable=mock_open,
        read_data=(
            'contexts:\n  main:\n    - include: some_other_include\n      '
            'apply_prototype: some_value\n'
        ),
    )
    @patch.object(read_write_data.logger, 'debug')
    def test_edit_contexts_main_without_scope(self, mock_debug, mock_open):
        file_path = 'ATest.yaml'
        read_write_data.edit_contexts_main(file_path)

        mock_open.assert_any_call(file_path, 'r')
        mock_open.assert_any_call(file_path, 'w')

        expected_content = 'contexts:\n  main: []\n'
        mock_open().write.assert_called_with(expected_content)

        mock_debug.assert_called_with('edited file %r contaxts main.', file_path)
