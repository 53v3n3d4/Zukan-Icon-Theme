import sublime


def get_settings(file_settings: str, option: str = None):
    """
    Load sublime-settings, and get options.

    Parameters:
    file_settings (str) -- sublime-settings file.
    option (str) -- get option value.
    """
    if option is not None:
        return sublime.load_settings(file_settings).get(option)
    if option is None:
        return sublime.load_settings(file_settings)


def set_save_settings(file_settings: str, option: str, value: list):
    """
    Modify and save settings options.

    Parameters:
    file_settings (str) -- sublime-settings file.
    option (str) -- set option key.
    value (list) --  option vslue.
    """
    sublime.load_settings(file_settings).set(option, value)
    sublime.save_settings(file_settings)
