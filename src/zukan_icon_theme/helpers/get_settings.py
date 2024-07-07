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
