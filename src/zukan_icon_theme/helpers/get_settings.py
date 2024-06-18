import sublime


USER_SETTINGS = 'Preferences.sublime-settings'
ZUKAN_SETTINGS = 'Zukan Icon Theme.sublime-settings'
ZUKAN_VERSION = 'zukan-version.sublime-settings'


def load_settings(file_settings: str, option: str = None):
    if option is not None:
        return sublime.load_settings(file_settings).get(option)
    if option is None:
        return sublime.load_settings(file_settings).get(option)
