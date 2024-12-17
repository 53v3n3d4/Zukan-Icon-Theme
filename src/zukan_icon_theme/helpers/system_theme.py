import platform
import subprocess

# Linux
# apt — Ubuntu, Debian
# pacman — Arch
# yum — CentOS
# dnf — Fedora
# zypper — openSUSE

# Windows


def macos_theme():
    """
    Code from
    https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python
    """
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    return bool(p.communicate()[0])


def system_theme() -> bool:
    # Linux
    if platform.system() == 'Linux':
        print('Linux')
        # Returning only for testing
        return True

    # macOS
    if platform.system() == 'Darwin':
        if macos_theme():
            return True

    # Windows
    if platform.system() == 'Windows':
        print('Windows')
        # Returning only for testing
        return True
