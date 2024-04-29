import collections.abc
import os
import pytest

from build.clean_svg import CleanSVG, _replace_line
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch


unused_list = {
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
    ' xmlns:serif="http://www.serif.com/"',
}

file_all_unused = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" xmlns:serif="http://www.serif.com/" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub1" serif:id="afpub"></g>
</svg>"""

file_partial_unused = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" xmlns:serif="http://www.serif.com/" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
</svg>"""

file_almost_clean = """
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" xmlns:serif="http://www.serif.com/" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub1" serif:id="afpub"></g>
</svg>"""

file_cleaned = """
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub"></g>
</svg>"""


class TestClean:
    @pytest.mark.parametrize('a, expected', [(file_all_unused, file_cleaned)])
    def test_clean_svg(self, a, expected):
        result = CleanSVG.clean_svg(a, unused_list)
        return result
        assert result == file_cleaned

    @pytest.mark.parametrize('a, expected', [(file_all_unused, file_cleaned)])
    def test_clean_all_svgs(self, a, expected):
        result = CleanSVG.clean_all_svgs(a, unused_list)
        return result
        assert result == file_cleaned

    @pytest.fixture(autouse=True)
    def test_load_svg_file_error(self, caplog):
        caplog.clear()
        with patch('build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            CleanSVG.clean_svg('tests/build/files/svg.svg', unused_list)
        # This is capturing nothing, but expect a 13 Permission Error
        assert caplog.record_tuples == []

    @pytest.fixture(autouse=True)
    def test_load_svgs_oserror(self, caplog):
        caplog.clear()
        with patch('build.clean_svg.open') as mock_open:
            mock_open.side_effect = FileNotFoundError
            CleanSVG.clean_all_svgs('tests/build/files/svg.svg', unused_list)
        # This is capturing nothing, but expect a 13 Permission Error
        assert caplog.record_tuples == []

    @pytest.fixture(autouse=True)
    def test_load_svgs_filenotfound_error(self, caplog):
        caplog.clear()
        with patch('build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            CleanSVG.clean_all_svgs('tests/build/files/svg.svg', unused_list)
        # This is capturing nothing, but expect a 13 Permission Error
        assert caplog.record_tuples == []

    @pytest.fixture(autouse=True)
    def test_write_svg_file_error(self, caplog):
        caplog.clear()
        with patch('build.clean_svg.open') as mock_open:
            mock_open.side_effect = OSError
            CleanSVG.clean_svg('tests/build/files/svg.svg', unused_list)
        # This is capturing nothing, but expect a 13 Permission Error
        assert caplog.record_tuples == []

    def test_replace_line(self):
        test_line = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        test_removed = ''
        result = _replace_line('', test_line)
        assert result == test_removed

    def test_replace_line_not_remove(self):
        test_line = 'Text not unused'
        test_removed = ''
        result = _replace_line('Text', test_line)
        assert result != test_removed


class TestCleanSVG(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.fake_fs().create_file('icons/file_type_afdesign.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afphoto.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_afpub.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_ai.svg', contents='test')
        cls.fake_fs().create_file('icons/file_type_angular.svg', contents='test')

    def test_file_exist(self):
        CleanSVG.clean_svg('icons/file_type_ai.svg', unused_list)
        self.assertTrue(os.path.exists('icons/file_type_ai.svg'))

    def test_file_not_found(self):
        CleanSVG.clean_svg('icons/file_type_babel.svg', unused_list)
        self.assertFalse(os.path.exists('icons/file_type_babel.svg'))

    def test_params_clean_svg(self):
        CleanSVG.clean_svg('icons/file_type_ai.svg', unused_list)
        self.assertTrue(isinstance('icons/file_type_ai.svg', str))
        self.assertTrue(isinstance(unused_list, collections.abc.Set))
        self.assertFalse(isinstance('icons/file_type_ai.svg', int))
        self.assertFalse(isinstance('icons/file_type_ai.svg', list))
        self.assertFalse(isinstance('icons/file_type_ai.svg', bool))
        self.assertFalse(isinstance(unused_list, int))
        self.assertFalse(isinstance(unused_list, list))
        self.assertFalse(isinstance(unused_list, bool))

    def test_params_clean_all_svgs(self):
        CleanSVG.clean_all_svgs('icons', unused_list)
        self.assertTrue(isinstance('icons', str))
        self.assertTrue(isinstance(unused_list, collections.abc.Set))
        self.assertFalse(isinstance('icons', int))
        self.assertFalse(isinstance('icons', list))
        self.assertFalse(isinstance('icons', bool))
        self.assertFalse(isinstance(unused_list, int))
        self.assertFalse(isinstance(unused_list, list))
        self.assertFalse(isinstance(unused_list, bool))
