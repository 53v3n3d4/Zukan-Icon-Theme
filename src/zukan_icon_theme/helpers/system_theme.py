import platform
import subprocess


# Linux
# apt — Ubuntu, Debian
# pacman — Arch
# yum — CentOS
# dnf — Fedora
# zypper — openSUSE


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


def windows_theme() -> bool:
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
        return True

    if platform.system() == 'Darwin':
        return macos_theme()

    if platform.system() == 'Windows':
        return windows_theme()
