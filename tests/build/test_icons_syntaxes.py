import os
import pytest

from pyfakefs.fake_filesystem_unittest import TestCase
from src.build.helpers.icons_syntaxes import IconSyntax
from src.build.helpers.read_write_data import dump_yaml_data, read_yaml_data
from tests.mocks.constants_icons_syntaxes import (
    TEST_STDOUT_SYNTAXES,
)
from tests.mocks.tests_paths import (
    DIR_DATA,
    DIR_DATA_NOT_FOUND,
    DIR_DESTINY,
)
from unittest.mock import patch


class TestCreateFile:
    @pytest.fixture
    def sample_yaml_file(self, tmpdir):
        data = {
            'syntax': [
                {'name': 'TestIcon1'},
                {'name': 'TestIcon2'},
            ]
        }
        yaml_file = tmpdir.join('test_data.yaml')
        dump_yaml_data(data, str(yaml_file))
        return str(yaml_file)

    @pytest.fixture
    def temp_dir(self, tmpdir):
        return str(tmpdir)

    def test_icon_syntax_creates_files(self, sample_yaml_file, temp_dir):
        IconSyntax.icon_syntax(sample_yaml_file, temp_dir)
        assert os.path.exists(os.path.join(temp_dir, 'TestIcon1.sublime-syntax'))
        assert os.path.exists(os.path.join(temp_dir, 'TestIcon2.sublime-syntax'))

    def test_icon_syntax_no_syntax(self, sample_yaml_file, temp_dir):
        no_syntax_data = {'no_syntax_key': 'value'}
        yaml_file_no_syntax = sample_yaml_file.replace(
            'test_data.yaml', 'no_syntax.yaml'
        )
        dump_yaml_data(no_syntax_data, yaml_file_no_syntax)

        result = IconSyntax.icon_syntax(yaml_file_no_syntax, temp_dir)
        assert result == read_yaml_data(yaml_file_no_syntax)

    def test_icon_syntax_file_not_found(self, temp_dir):
        with pytest.raises(TypeError):
            result = IconSyntax.icon_syntax('non_existent_file.yaml', temp_dir)
            assert result is None  # Or any specific behavior you want to check

    def test_icons_syntaxes_creates_multiple_files(self, sample_yaml_file, temp_dir):
        IconSyntax.icons_syntaxes(os.path.dirname(sample_yaml_file), temp_dir)
        assert os.path.exists(os.path.join(temp_dir, 'TestIcon1.sublime-syntax'))
        assert os.path.exists(os.path.join(temp_dir, 'TestIcon2.sublime-syntax'))


class TestSyntax:
    # @pytest.mark.parametrize('a, b, expected', [(DIR_DATA, DIR_DESTINY, TEST_DATA_DIR)])
    # def test_icons_syntaxes(self, a, b, expected):
    #     result = IconSyntax.icons_syntaxes(a, b)
    #     assert result == TEST_DATA_DIR

    @pytest.fixture(autouse=True)
    def test_create_syntax_file(self, capfd):
        IconSyntax.icon_syntax('tests/mocks/yaml.yaml', DIR_DESTINY)

        out, err = capfd.readouterr()
        assert (
            out
            == '\x1b[36m[!] yaml.yaml\x1b[0m -> \x1b[93mJavaScript (Vitest).sublime-syntax\x1b[0m created.\n'
            '\x1b[36m[!] yaml.yaml\x1b[0m -> \x1b[93mTypeScript (Vitest).sublime-syntax\x1b[0m created.\n'
        )

    @pytest.fixture(autouse=True)
    def test_create_all_syntaxes_file(self, capfd):
        IconSyntax.icons_syntaxes(DIR_DATA, DIR_DESTINY)

        out, err = capfd.readouterr()
        assert out == TEST_STDOUT_SYNTAXES

    @pytest.fixture(autouse=True)
    def test_syntax_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_syntaxes.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            IconSyntax.icon_syntax(
                'tests/mocks/not_found_yaml.yaml',
                DIR_DESTINY,
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.icons_syntaxes',
                40,
                "[Errno 2] No such file or directory: 'tests/mocks/not_found_yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_syntax_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_syntaxes.open') as mock_open:
            mock_open.side_effect = OSError
            IconSyntax.icon_syntax(
                'tests/build/yaml.yaml',
                DIR_DESTINY,
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.icons_syntaxes',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_syntaxes_filenotfounderror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_syntaxes.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            IconSyntax.icons_syntaxes(
                DIR_DATA_NOT_FOUND,
                DIR_DESTINY,
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.icons_syntaxes',
                40,
                "[Errno 2] No such file or directory: 'tests/build/mocks_not_found/'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_syntaxes_oserror(self, caplog):
        caplog.clear()
        with patch('src.build.helpers.icons_syntaxes.open') as mock_open:
            mock_open.side_effect = OSError
            IconSyntax.icons_syntaxes(
                'tests/build/yaml.yaml',
                DIR_DESTINY,
            )
        assert caplog.record_tuples == [
            (
                'src.build.helpers.icons_syntaxes',
                40,
                "[Errno 13] Permission denied: 'tests/mocks/yaml.yaml'",
            )
        ]

    @pytest.fixture(autouse=True)
    def test_not_have_syntax_yaml_file(self, capfd):
        IconSyntax.icon_syntax('yaml.yaml', DIR_DESTINY)

        out, err = capfd.readouterr()
        assert out == '[!] yaml.yaml: file does not have any syntax.\n'


class TestIconSyntax(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('data/afdesign.yaml')
        cls.fake_fs().create_file('data/afphoto.yaml')
        cls.fake_fs().create_file('data/afpub.yaml')
        cls.fake_fs().create_file('data/ai.yaml')
        cls.fake_fs().create_file('data/angular.yaml')
        cls.fake_fs().create_file('./yaml.yaml')
        cls.fake_fs().create_file('data/Binary (Affinity Publisher.sublime-syntax)')

    def test_syntax_exist(self):
        IconSyntax.icon_syntax('data/ai.yaml', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/ai.yaml'))

    def test_syntaxes_exist(self):
        IconSyntax.icons_syntaxes('data', DIR_DESTINY)
        self.assertTrue(os.path.exists('data/afdesign.yaml'))

    def test_params_syntax(self):
        IconSyntax.icon_syntax('data/afdesign.yaml', DIR_DESTINY)
        self.assertTrue(isinstance('data/afdesign.yaml', str))
        self.assertFalse(isinstance('data/afdesign.yaml', int))
        self.assertFalse(isinstance('data/afdesign.yaml', list))
        self.assertFalse(isinstance('data/afdesign.yaml', bool))
        self.assertFalse(isinstance('data/afdesign.yaml', dict))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertFalse(isinstance(DIR_DESTINY, dict))

    def test_params_syntaxes(self):
        IconSyntax.icons_syntaxes('data/', DIR_DESTINY)
        self.assertTrue(isinstance('data/', str))
        self.assertFalse(isinstance('data/', int))
        self.assertFalse(isinstance('data/', list))
        self.assertFalse(isinstance('data/', bool))
        self.assertFalse(isinstance('data/', dict))
        self.assertTrue(isinstance(DIR_DESTINY, str))
        self.assertFalse(isinstance(DIR_DESTINY, int))
        self.assertFalse(isinstance(DIR_DESTINY, list))
        self.assertFalse(isinstance(DIR_DESTINY, bool))
        self.assertFalse(isinstance(DIR_DESTINY, dict))
