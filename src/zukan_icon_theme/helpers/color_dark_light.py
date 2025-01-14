import logging
import math
import re

from ..utils.st_color_palette import (
    ST_COLOR_PALETTE,
)

logger = logging.getLogger(__name__)


def convert_to_rgb(bgcolor: str) -> list:
    """
    Convert color to RGB, and return a list with RGB numbers.

    Currently only convert Hex, HSL and RGB. Alpha channel when present will
    not be considered.

    Parameters:
    bgcolor (str) -- Hex, HSL or RGB color.

    Returns:
    (list) -- list with RGB numbers.
    """
    # Hex/ Hexa
    # Limitation, currently not taking in consideration Alpha channel.
    if bgcolor.startswith('#') and len(bgcolor) <= 9:
        # from code
        # https://stackoverflow.com/questions/214359/
        # converting-hex-color-to-rgb-and-vice-versa
        hex_color = bgcolor[:7].lstrip('#')
        lv = len(hex_color)

        rgb = list(int(hex_color[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

        return rgb

    # HSL/HSLA
    # Limitation, currently not taking in consideration Alpha channel.
    elif bgcolor.startswith('hsl') or bgcolor.startswith('hsla'):
        hsl = extract_numbers_from_hsl(bgcolor)
        # print(hsl)

        hue, sat, lum, *alpha = hsl
        if hue < 0 or hue > 360 or sat < 0 or sat > 100 or lum < 0 or lum > 100:
            logger.debug('HSL range values not valid.')

        # Using wikipedia formula
        # https://en.wikipedia.org/wiki/HSL_and_HSV#To_RGB
        hue = hue / 60
        c = (1 - abs(2 * lum / 100 - 1)) * sat / 100
        x = c * (1 - abs((hue % 2) - 1))
        m = lum / 100 - c / 2

        if 0 <= hue < 1:
            r, g, b = c, x, 0
        elif 1 <= hue < 2:
            r, g, b = x, c, 0
        elif 2 <= hue < 3:
            r, g, b = 0, c, x
        elif 3 <= hue < 4:
            r, g, b = 0, x, c
        elif 4 <= hue < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255

        # return list(int(r), int(g), int(b))
        return [r, g, b]

    # Extract rgb numbers
    elif bgcolor.startswith('rgb') or bgcolor.startswith('rgba'):
        # RGBA: exclude alpha channel
        rgb = extract_numbers_from_rgb(bgcolor)[:3]
        # print(rgb)

        return rgb

    else:
        logger.info('could not convert color to RGB.')


def st_colors_to_hex(var_name: str) -> str:
    for i in ST_COLOR_PALETTE:
        for k, v in i.items():
            if var_name == k:
                return v


def extract_numbers_from_hsl(color_hsl: str) -> tuple:
    """
    Extract numbers from HSL, with ou without percentages sign.

    Examples: hsl(255, 8.0%, 9.8%), hsla(3, 100%, 95%, 0.9)

    Parameters:
    color_hsl (str) -- HSL or HSLA color.

    Returns:
    (tuple) -- HSL or HSLA numbers.
    """
    # Regex for HSL and HSLA
    pattern = (
        r'hsla?\((\d+),\s*(-?\d*\.?\d+)%?,\s*(-?\d*\.?\d+)%?(?:,\s*(\d+(\.\d+)?))?\)'
    )
    result = re.search(pattern, color_hsl)

    if result:
        hue = int(result.group(1))
        sat = float(result.group(2))
        lum = float(result.group(3))

        if result.group(4):
            alpha = float(result.group(4))
            return (hue, sat, lum, alpha)
        else:
            return (hue, sat, lum)

    else:
        logger.info('HSL or HSLA not valid')
        return None


def extract_numbers_from_rgb(color_rgb: str) -> list:
    """
    Extract numbers from RGB color string.

    Examples: rgb(59, 39, 61), rgba(38, 40, 51, 0.8)

    Parameters:
    color_rgb (str) -- RGB or RGBA color.

    Returns:
    (list) - list with RGB numbers.
    """
    pattern = r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(\.\d+)?))?\)'
    result = re.search(pattern, color_rgb)

    if result:
        r = int(result.group(1))
        g = int(result.group(2))
        b = int(result.group(3))

        if result.group(4):
            a = float(result.group(4))
            return [r, g, b, a]
        else:
            return [r, g, b]

    else:
        logger.info('RGB or RGBA not valid')
        return None


def rgb_dark_light(rgb_color: list) -> str:
    """
    Code from
    https://stackoverflow.com/questions/22603510/
    is-this-possible-to-detect-a-colour-is-a-light-or-dark-colour

    Return 'dark' or 'light' for a RGB color.

    Used to select icon version, light or dark, if available, based
    on theme sidebar background color.

    Parameters:
    rgb_color (list) -- list with RGB numbers.

    Returns:
    (str) -- return 'dark' or 'light' for a RGB color.
    """
    [r, g, b] = rgb_color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))

    if hsp <= 127.5:
        logger.debug('HSP = %s, sidebar seems dark background.', hsp)
        # print(hsp)
        # dark background, use light icon
        return 'dark'

    elif hsp > 127.5:
        logger.debug('HSP = %s, sidebar seems light background.', hsp)
        # print(hsp)
        # light background, use dark icon
        return 'light'


def get_icon_dark_light(bgcolor: str) -> str:
    """
    Get icon dark if bgcolor is light. And vice-versa.

    Parameters:
    bgcolor (str) -- string 'dark' or 'light'.

    Returns:
    (str) -- return 'dark' or 'light'.
    """
    if bgcolor == 'dark':
        return 'light'
    else:
        return 'dark'


def hex_dark_light(hex_color: str) -> str:
    """
    Return 'dark' or 'light' for a Hex color.

    Parameters:
    hex_color (str) -- string Hex.

    Returns:
    (str) -- return 'dark' or 'light' for a Hex color.
    """
    return rgb_dark_light(convert_to_rgb(hex_color))
