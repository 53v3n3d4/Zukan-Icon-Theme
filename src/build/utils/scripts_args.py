import argparse

from src.build.helpers.color import Color
from src.build.utils.build_dir_paths import (
    DATA_PATH,
    ICON_THEME_TEST_PATH,
    ICONS_DATA_PATH,
    ICONS_DATA_PRIMARY_ICONS_PATH,
    ICONS_PNG_PATH,
    ICONS_SVG_PATH,
    ZUKAN_ICONS_DATA_FILE,
)
from src.build.utils.svg_unused_list import (
    UNUSED_LIST,
)

# Args opts sequence
# (opt short, opt long, action, default, help, required, type)
COMMANDS = {
    'clean': {
        'help': f'{Color.YELLOW}Clean unused SVGs tags and attributes.{Color.END}',
        'args': [
            (
                '-a',
                '--all',
                # BooleanOptionalAction added on 3.9
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Clean all SVGs from src/icons folder.{Color.END}',
                False,
            ),
            (
                '-d',
                '--directory',
                'store',
                None,
                f'{Color.YELLOW}Path to SVGs folder.{Color.END}',
                False,
                str,
            ),
            (
                '-f',
                '--file',
                'store',
                None,
                f'{Color.YELLOW}Path to SVG file.{Color.END}',
                False,
                str,
            ),
            (
                '-l',
                '--list',
                'store',
                UNUSED_LIST,
                f'{Color.YELLOW}List(str) of unused tags to be removed.{Color.END}',
                False,
                str,
            ),
        ],
    },
    'concat': {
        'help': f'{Color.YELLOW}Concat icons SVGs.{Color.END}',
        'args': [
            (
                '-a',
                '--all',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Concat SVG file with all icons.{Color.END}',
                False,
            ),
            (
                '-cf',
                '--concatfile',
                'store',
                None,
                f'{Color.YELLOW}Path to concat SVG file.{Color.END}',
                False,
                str,
            ),
            (
                '-d',
                '--data',
                'store',
                DATA_PATH,
                f'{Color.YELLOW}Path to folder data.{Color.END}',
                False,
                str,
            ),
            (
                '-i',
                '--icon',
                'store',
                ICONS_SVG_PATH,
                f'{Color.YELLOW}Path to icons SVGs folder.{Color.END}',
                False,
                str,
            ),
            (
                '-ipr',
                '--iconsperrow',
                'store',
                5,
                f'{Color.YELLOW}Icons per row in concat SVG.{Color.END}',
                False,
                int,
            ),
            (
                '-pf',
                '--prefericon',
                'store',
                'dark',
                f'{Color.YELLOW}Prefer icon options: dark, light or all.{Color.END}',
                False,
                str,
            ),
            (
                '-mh',
                '--maxheight',
                'store',
                2000,
                f'{Color.YELLOW}Max height of concat SVG file.{Color.END}',
                False,
                int,
            ),
            (
                '-sa',
                '--sample',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Concat SVG file from random selection.{Color.END}',
                False,
            ),
            (
                '-sano',
                '--samplenumbers',
                'store',
                30,
                f'{Color.YELLOW}Number of icons in random sample.{Color.END}',
                False,
                int,
            ),
        ],
    },
    'icon-theme': {
        'help': f'{Color.YELLOW}Create icons PNGs and zukan icons data file.{Color.END}',
        'args': [
            (
                '-a',
                '--all',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Create all PNGs, zukan preferences and syntaxes files.{Color.END}',
                False,
            ),
            (
                '-d',
                '--data',
                'store',
                None,
                f'{Color.YELLOW}Path to folder data.{Color.END}',
                False,
                str,
            ),
            (
                '-f',
                '--file',
                'store',
                None,
                f'{Color.YELLOW}Path to icon data file.{Color.END}',
                False,
                str,
            ),
            (
                '-i',
                '--icon',
                'store',
                ICONS_SVG_PATH,
                f'{Color.YELLOW}Path to icons SVGs folder.{Color.END}',
                False,
                str,
            ),
            (
                '-id',
                '--icondata',
                'store',
                ICONS_DATA_PATH,
                f'{Color.YELLOW}Path to destiny for icons data file.{Color.END}',
                False,
                str,
            ),
            (
                '-if',
                '--iconfile',
                'store',
                ZUKAN_ICONS_DATA_FILE,
                f'{Color.YELLOW}Path to icons data file.{Color.END}',
                False,
                str,
            ),
            (
                '-p',
                '--png',
                'store',
                ICONS_PNG_PATH,
                f'{Color.YELLOW}Path to destiny for PNGs.{Color.END}',
                False,
                str,
            ),
            (
                '-pp',
                '--pngprimary',
                'store',
                ICONS_DATA_PRIMARY_ICONS_PATH,
                f'{Color.YELLOW}Path to destiny for primary icons PNGs.{Color.END}',
                False,
                str,
            ),
        ],
    },
    'png': {
        'help': f'{Color.YELLOW}Generate icon PNGs.{Color.END}',
        'args': [
            (
                '-a',
                '--all',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Generate all PNGs in icons folder.{Color.END}',
                False,
            ),
            (
                '-d',
                '--data',
                'store',
                None,
                f'{Color.YELLOW}Path to folder data.{Color.END}',
                False,
                str,
            ),
            (
                '-f',
                '--file',
                'store',
                None,
                f'{Color.YELLOW}Path to icon data file.{Color.END}',
                False,
                str,
            ),
            (
                '-i',
                '--icon',
                'store',
                ICONS_SVG_PATH,
                f'{Color.YELLOW}Path to icons SVGs folder.{Color.END}',
                False,
                str,
            ),
            (
                '-p',
                '--png',
                'store',
                ICONS_PNG_PATH,
                f'{Color.YELLOW}Path to destiny for PNGs.{Color.END}',
                False,
                str,
            ),
            (
                '-pp',
                '--pngprimary',
                'store',
                ICONS_DATA_PRIMARY_ICONS_PATH,
                f'{Color.YELLOW}Path to destiny for primary icons PNGs.{Color.END}',
                False,
                str,
            ),
        ],
    },
    'test-icon-theme': {
        'help': f'{Color.YELLOW}Create icons theme test files.{Color.END}',
        'args': [
            (
                '-a',
                '--all',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Create all icons test files in tests_icon_theme folder.{Color.END}',
                False,
            ),
            (
                '-d',
                '--data',
                'store',
                None,
                f'{Color.YELLOW}Path to folder data.{Color.END}',
                False,
                str,
            ),
            (
                '-f',
                '--file',
                'store',
                None,
                f'{Color.YELLOW}Path to icon data file.{Color.END}',
                False,
                str,
            ),
            (
                '-tp',
                '--testspath',
                'store',
                ICON_THEME_TEST_PATH,
                f'{Color.YELLOW}Path to destiny for sublime-syntaxes files.{Color.END}',
                False,
                str,
            ),
        ],
    },
    'zukan-icon': {
        'help': f'{Color.YELLOW}Create zukan icons data file.{Color.END}',
        'args': [
            (
                '-r',
                '--read',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Print zukan icons data file.{Color.END}',
                False,
            ),
            (
                '-id',
                '--icondata',
                'store',
                ICONS_DATA_PATH,
                f'{Color.YELLOW}Path to destiny for icons data file.{Color.END}',
                False,
                'str',
            ),
            (
                '-if',
                '--iconfile',
                'store',
                ZUKAN_ICONS_DATA_FILE,
                f'{Color.YELLOW}Path to icons data file.{Color.END}',
                False,
                'str',
            ),
            (
                '-w',
                '--write',
                argparse.BooleanOptionalAction,
                False,
                f'{Color.YELLOW}Dump zukan icons data file.{Color.END}',
                False,
            ),
        ],
    },
}
