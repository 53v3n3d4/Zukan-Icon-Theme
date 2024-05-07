from src.build.helpers.special_chars import special_chars


def test_special_chars_true():
    filename = 'c#.png'
    assert special_chars(filename) is True


def test_special_chars_false():
    filename = 'csharp.png'
    assert special_chars(filename) is False
