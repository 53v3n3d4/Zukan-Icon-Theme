import json
import platform
import subprocess


# ST Theme 'auto' has an open issue
# https://github.com/sublimehq/sublime_text/issues/5194
def linux_theme() -> bool:
    """
    Code from
    https://github.com/smac89/autodark-sublime-plugin/blob/main/helpers.py

    Returns:
    (bool) -- True for 'dark' theme.
    """
    dark_light_dict = {1: 'dark', 2: 'light'}

    p = subprocess.check_output(
        [
            '/usr/bin/busctl',
            '--user',
            '--json=short',
            'call',
            'org.freedesktop.portal.Desktop',
            '/org/freedesktop/portal/desktop',
            'org.freedesktop.portal.Settings',
            'ReadOne',
            'ss',
            'org.freedesktop.appearance',
            'color-scheme',
        ],
        universal_newlines=True,
        stderr=subprocess.STDOUT,
    )

    result = json.loads(p)
    data = result.get('data', [])

    system_scheme = data[0].get('data', None)
    color_scheme = dark_light_dict.get(system_scheme)

    return color_scheme == 'dark'


def macos_theme() -> bool:
    """
    Code from
    https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python

    Returns:
    (bool) -- True for 'dark' theme.
    """
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    return bool(p.communicate()[0])


# Windows module only
def windows_theme() -> bool:  # pragma: no cover
    """
    Code from
    https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python

    Returns:
    (bool) -- True for 'dark' theme.
    """
    import winreg

    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

    reg_key = winreg.OpenKey(registry, reg_keypath)

    for i in range(1024):
        value_name, value, _ = winreg.EnumValue(reg_key, i)
        if value_name == 'AppsUseLightTheme':
            return value == 0


def system_theme() -> bool:
    """
    Returns:
    (bool) -- True for 'dark' theme.
    """
    if platform.system() == 'Linux':
        return linux_theme()

    if platform.system() == 'Darwin':
        return macos_theme()

    # Windows module only
    if platform.system() == 'Windows':  # pragma: no cover
        return windows_theme()
