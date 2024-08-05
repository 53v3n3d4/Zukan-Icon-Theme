#!/usr/bin/env python

import argparse
import sys

from src.build.clean_svg import CleanSVG
from src.build.helpers.color import Color
from src.build.helpers.concat_svgs import ConcatSVG
from src.build.helpers.create_test_icon_theme import TestIconTheme
from src.build.helpers.icons_preferences import Preference
from src.build.helpers.icons_syntaxes import IconSyntax
from src.build.helpers.logger import logging
from src.build.helpers.print_message import print_build_message, print_message
from src.build.helpers.read_write_data import read_pickle_data
from src.build.icons import IconPNG
from src.build.utils.build_dir_paths import (
    CONCAT_SVGS_FILE,
    CONCAT_SVGS_FILE_SAMPLE,
    DATA_PATH,
    ICON_THEME_TEST_PATH,
    ICONS_PNG_PATH,
    ICONS_SVG_PATH,
    ICONS_SYNTAXES_PATH,
    ICONS_PREFERENCES_PATH,
    ZUKAN_ICONS_DATA_FILE,
)
from src.build.utils.scripts_args import (
    COMMANDS,
)
from src.build.zukan_icons import ZukanIcon

logger = logging.getLogger(__name__)


def create_parser(commands_args: dict):
    """
    Create parser for each command.

    Parameters:
    commands_args (dict) -- sub-parser dict.

    Returns:
    parser -- return an ArgumentParser object.
    """
    # from https://gist.github.com/jirihnidek/3f5d36636198e852280f619847d22d9e
    # Create the top-level parser
    parser = argparse.ArgumentParser(prog=f'{ Color.CYAN }Build script{ Color.END }')
    # parser.add_argument('-d', '--debug', action=argparse.BooleanOptionalAction, help='debug flag')

    # Create sub-parser
    subparsers = parser.add_subparsers(dest='subparser_name', help='sub-command help')

    for cmd, opts in commands_args.items():
        subparser = subparsers.add_parser(cmd, help=opts['help'])
        for arg in opts['args']:
            if len(opts) > 6:
                subparser.add_argument(
                    arg[0],
                    arg[1],
                    action=arg[2],
                    default=arg[3],
                    help=arg[4],
                    required=arg[5],
                    type=arg[6],
                )
            if len(opts) < 6:
                subparser.add_argument(
                    arg[0],
                    arg[1],
                    action=arg[2],
                    default=arg[3],
                    help=arg[4],
                    required=arg[5],
                )

    # print(parser)
    return parser


def main():
    parser = create_parser(COMMANDS)

    # Namespaces
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    # Subparser - subcommands
    parser = args.subparser_name

    # Clean
    if parser == 'clean':
        if args.all and not (args.file or args.directory):
            print_build_message('🛠️  Cleaning all SVGs files: ', ICONS_SVG_PATH)
            CleanSVG.clean_all_svgs(ICONS_SVG_PATH, args.list)
        elif args.file and not (args.all or args.directory):
            print_build_message('🛠️  Cleaning SVG:', args.file)
            CleanSVG.clean_svg(args.file, args.list)
        elif args.directory and not (args.all or args.file):
            print_build_message('🛠️  Cleaning all SVGs:', args.directory)
            CleanSVG.clean_all_svgs(args.directory, args.list)
        else:
            _error_message()
    # Concat
    if parser == 'concat':
        if args.sample:
            print_build_message(
                '🛠️  Concatenating sample SVGs: ', CONCAT_SVGS_FILE_SAMPLE
            )
            if args.concatfile is None:
                args.concatfile = CONCAT_SVGS_FILE_SAMPLE
            ConcatSVG.write_concat_svgs(
                DATA_PATH,
                args.icon,
                args.concatfile,
                args.sample,
                int(args.samplenumbers),
                int(args.iconsperrow),
                int(args.maxheight),
            )
        elif not args.sample:
            print_build_message('🛠️  Concatenating all SVGs: ', CONCAT_SVGS_FILE)
            if args.concatfile is None:
                args.concatfile = CONCAT_SVGS_FILE
            ConcatSVG.write_concat_svgs(
                DATA_PATH,
                args.icon,
                args.concatfile,
                args.sample,
                int(args.samplenumbers),
                int(args.iconsperrow),
                int(args.maxheight),
            )
        else:
            _error_message()
    # Icon Theme
    elif parser == 'icon-theme':
        if args.all and not (args.file or args.data):
            print(
                f'{ Color.BLUE }[⚙] Starting building zukan icons data file and '
                f'all icons PNGs{ Color.END }'
            )
            print_build_message(
                '🛠️  Creating zukan icons data: ',
                ZUKAN_ICONS_DATA_FILE,
            )
            ZukanIcon.write_icon_data(DATA_PATH, args.icondata, args.iconfile)
            print_build_message('🛠️  Generating all icons PNGs: ', ICONS_PNG_PATH)
            IconPNG.svg_to_png_all(DATA_PATH, args.icon, args.png, args.pngprimary)
        elif args.file and not (args.all or args.data):
            print_build_message(
                '🛠️  Creating zukan icons data: ',
                ZUKAN_ICONS_DATA_FILE,
            )
            ZukanIcon.write_icon_data(DATA_PATH, args.icondata, args.iconfile)
            print_build_message('🛠️  Generating icon PNGs: ', args.png)
            IconPNG.svg_to_png(args.file, args.icon, args.png, args.pngprimary)
        elif args.data and not (args.all or args.file):
            print(
                f'{ Color.BLUE }[⚙] Starting building zukan icons data file and '
                f'all icons PNGs{ Color.END }'
            )
            print_build_message(
                '🛠️  Creating zukan icons data: ',
                ZUKAN_ICONS_DATA_FILE,
            )
            ZukanIcon.write_icon_data(DATA_PATH, args.icondata, args.iconfile)
            print_build_message('🛠️  Generating all icons PNGs: ', args.png)
            IconPNG.svg_to_png_all(args.data, args.icon, args.png, args.pngprimary)
        else:
            _error_message()
    # PNGs
    elif parser == 'png':
        if args.all and not (args.file or args.data):
            print_build_message('🛠️  Generating all icons PNGs:', ICONS_PNG_PATH)
            IconPNG.svg_to_png_all(DATA_PATH, args.icon, args.png, args.pngprimary)
        elif args.file and not (args.all or args.data):
            print_build_message('🛠️  Generating icon PNGs: ', args.png)
            IconPNG.svg_to_png(args.file, args.icon, args.png, args.pngprimary)
        elif args.data and not (args.all or args.file):
            print_build_message('🛠️  Generating all icons PNGs: ', args.png)
            IconPNG.svg_to_png_all(args.data, args.icon, args.png, args.pngprimary)
        else:
            _error_message()
    # tmPreferences
    elif parser == 'preference':
        if args.all and not (args.file or args.data):
            print_build_message(
                '🛠️  Creating all icons tmPreferences: ',
                ICONS_PREFERENCES_PATH,
            )
            Preference.preferences_all(DATA_PATH, args.tmpreference)
        elif args.file and not (args.all or args.data):
            print_build_message('🛠️  Creating icon tmPreferences: ', args.tmpreference)
            Preference.preferences(args.file, args.tmpreference)
        elif args.data and not (args.all or args.file):
            print_build_message(
                '🛠️  Creating all icons tmPreferences: ', args.tmpreference
            )
            Preference.preferences_all(args.data, args.tmpreference)
        else:
            _error_message()
    # Sublime-syntaxes
    elif parser == 'syntax':
        if args.all and not (args.file or args.data):
            print_build_message(
                '🛠️  Creating all icons sublime-syntaxes: ',
                ICONS_SYNTAXES_PATH,
            )
            IconSyntax.icons_syntaxes(DATA_PATH, args.syntax)
        elif args.file and not (args.all or args.data):
            print_build_message('🛠️  Creating icon sublime-syntaxes: ', args.syntax)
            IconSyntax.icon_syntax(args.file, args.syntax)
        elif args.data and not (args.all or args.file):
            print_build_message('🛠️  Creating all icons sublime-syntaxes: ', args.syntax)
            IconSyntax.icons_syntaxes(args.data, args.syntax)
        else:
            _error_message()
    # Tests icons themes
    elif parser == 'test-icon-theme':
        if args.all and not (args.file or args.data):
            print_build_message(
                '🛠️  Creating all icons tests files: ',
                ICON_THEME_TEST_PATH,
            )
            TestIconTheme.create_icons_files(DATA_PATH, args.testspath)
        elif args.file and not (args.all or args.data):
            print_build_message('🛠️  Creating icon test file: ', args.testspath)
            TestIconTheme.create_icon_file(args.file, args.testspath)
        elif args.data and not (args.all or args.file):
            print_build_message('🛠️  Creating all icons tests files: ', args.testspath)
            TestIconTheme.create_icons_files(args.data, args.testspath)
        else:
            _error_message()
    # Zukan icons
    elif parser == 'zukan-icon':
        if args.write and not args.read:
            print_build_message(
                '🛠️  Writing zukan icons data: ',
                ZUKAN_ICONS_DATA_FILE,
            )
            ZukanIcon.write_icon_data(DATA_PATH, args.icondata, args.iconfile)
        elif args.read and not args.write:
            print_build_message(
                '🛠️  Printing zukan icons data: ',
                ZUKAN_ICONS_DATA_FILE,
            )
            read_pickle_data(args.iconfile)
        else:
            _error_message()

    # If uncomment, this showing error message at the end of clean command.
    # It does not seem to get here when build with no argument.
    # else:
    #     _error_message()


def _error_message():
    print_message(
        'Error',
        'You need pass an argument. Use --help to see options.',
        color=f'{ Color.RED }',
        color_end=f'{ Color.END }',
    )


if __name__ == '__main__':
    main()
