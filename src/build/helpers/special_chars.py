import re


# From https://stackoverflow.com/questions/19970532/how-to-check-a-string-for-a-special-character
def special_chars(filename: str) -> bool:
    """
    PNG file name can not contain special characters. This function will
    return a boolean value, true or false.

    Special chars allowed: '_'.

    Paramenters:
    filename (str) -- PNG file name.

    Returns:
    value (bool) -- condition if file name has or not special characters.
    """
    regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
    if regex.search(filename) is None:
        value = False
    else:
        value = True
    return value
