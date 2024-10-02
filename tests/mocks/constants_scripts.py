from src.build.utils.build_dir_paths import (
    DATA_PATH,
    ICON_THEME_TEST_PATH,
    ICONS_DATA_PATH,
    ICONS_DATA_PRIMARY_ICONS_PATH,
    ICONS_PNG_PATH,
    ICONS_SVG_PATH,
    ICONS_SYNTAXES_PATH,
    ICONS_PREFERENCES_PATH,
    # ZUKAN_ICONS_DATA_FILE,
)
from src.build.utils.svg_unused_list import (
    UNUSED_LIST,
)
from tests.mocks.constants_pickle import TEST_PICKLE_ZUKAN_FILE
from tests.mocks.constants_svg import TEST_SVG_FILE


COMMANDS_ARGS_PATH_P2 = [
    (
        'src.build.helpers.read_write_data.read_pickle_data',
        ['zukan-icon', '--read'],
    ),
]

COMMANDS_ARGS_PATH_P3 = [
    # Command zukan-icon
    (
        'src.build.helpers.read_write_data.read_pickle_data',
        ['zukan-icon', '--read', '--iconfile', TEST_PICKLE_ZUKAN_FILE],
        TEST_PICKLE_ZUKAN_FILE,
    ),
]

COMMANDS_ARGS_PATH_P4 = [
    # Command clean
    (
        'src.build.clean_svg.CleanSVG.clean_all_svgs',
        ['clean', '--directory', ICONS_SVG_PATH],
        ICONS_SVG_PATH,
        UNUSED_LIST,
    ),
    (
        'src.build.clean_svg.CleanSVG.clean_all_svgs',
        ['clean', '--all'],
        ICONS_SVG_PATH,
        UNUSED_LIST,
    ),
    (
        'src.build.clean_svg.CleanSVG.clean_svg',
        ['clean', '--file', TEST_SVG_FILE],
        TEST_SVG_FILE,
        UNUSED_LIST,
    ),
    # Command preference
    (
        'src.build.helpers.icons_preferences.Preference.preferences_all',
        ['preference', '--data', DATA_PATH, '--tmpreference', ICONS_PREFERENCES_PATH],
        DATA_PATH,
        ICONS_PREFERENCES_PATH,
    ),
    (
        'src.build.helpers.icons_preferences.Preference.preferences_all',
        ['preference', '--all'],
        DATA_PATH,
        ICONS_PREFERENCES_PATH,
    ),
    (
        'src.build.helpers.icons_preferences.Preference.preferences',
        [
            'preference',
            '--file',
            'src/data/afdesing.yaml',
            '--tmpreference',
            ICONS_PREFERENCES_PATH,
        ],
        'src/data/afdesing.yaml',
        ICONS_PREFERENCES_PATH,
    ),
    # Command syntax
    (
        'src.build.helpers.icons_syntaxes.IconSyntax.icons_syntaxes',
        ['syntax', '--data', DATA_PATH, '--syntax', ICONS_SYNTAXES_PATH],
        DATA_PATH,
        ICONS_SYNTAXES_PATH,
    ),
    (
        'src.build.helpers.icons_syntaxes.IconSyntax.icons_syntaxes',
        ['syntax', '--all'],
        DATA_PATH,
        ICONS_SYNTAXES_PATH,
    ),
    (
        'src.build.helpers.icons_syntaxes.IconSyntax.icon_syntax',
        ['syntax', '--file', 'src/data/afdesing.yaml', '--syntax', ICONS_SYNTAXES_PATH],
        'src/data/afdesing.yaml',
        ICONS_SYNTAXES_PATH,
    ),
    # Command test-icon-theme
    (
        'src.build.helpers.create_test_icon_theme.TestIconTheme.create_icons_files',
        ['test-icon-theme', '--data', DATA_PATH, '--testspath', ICON_THEME_TEST_PATH],
        DATA_PATH,
        ICON_THEME_TEST_PATH,
    ),
    (
        'src.build.helpers.create_test_icon_theme.TestIconTheme.create_icons_files',
        ['test-icon-theme', '--all'],
        DATA_PATH,
        ICON_THEME_TEST_PATH,
    ),
    (
        'src.build.helpers.create_test_icon_theme.TestIconTheme.create_icon_file',
        [
            'test-icon-theme',
            '--file',
            'src/data/afdesign.yaml',
            '--testspath',
            ICON_THEME_TEST_PATH,
        ],
        'src/data/afdesign.yaml',
        ICON_THEME_TEST_PATH,
    ),
]

COMMANDS_ARGS_PATH_P5 = [
    # Command icon-theme
    # icon-theme combine png and zukan-icon
    # Comment 2 tuples below to speed tests
    (
        'src.build.zukan_icons.ZukanIcon.write_icon_data',
        [
            'icon-theme',
            '--all',
            '--icondata',
            ICONS_DATA_PATH,
            '--iconfile',
            TEST_PICKLE_ZUKAN_FILE,
        ],
        DATA_PATH,
        ICONS_DATA_PATH,
        TEST_PICKLE_ZUKAN_FILE,
    ),
    (
        'src.build.zukan_icons.ZukanIcon.write_icon_data',
        [
            'icon-theme',
            '--data',
            DATA_PATH,
            '--icondata',
            ICONS_DATA_PATH,
            '--iconfile',
            TEST_PICKLE_ZUKAN_FILE,
        ],
        DATA_PATH,
        ICONS_DATA_PATH,
        TEST_PICKLE_ZUKAN_FILE,
    ),
    # Command zukan-icon
    (
        'src.build.zukan_icons.ZukanIcon.write_icon_data',
        [
            'zukan-icon',
            '--write',
            '--icondata',
            ICONS_DATA_PATH,
            '--iconfile',
            TEST_PICKLE_ZUKAN_FILE,
        ],
        DATA_PATH,
        ICONS_DATA_PATH,
        TEST_PICKLE_ZUKAN_FILE,
    ),
    # (
    #     'src.build.helpers.read_write_data.read_pickle_data',
    #     ['zukan-icon', '--read', '--icondata', ICONS_DATA_PATH, '--iconfile', TEST_PICKLE_ZUKAN_FILE],
    #     DATA_PATH,
    #     ICONS_DATA_PATH,
    #     TEST_PICKLE_ZUKAN_FILE,
    # ),
]

COMMANDS_ARGS_PATH_P6 = [
    # Command icon-theme
    # icon-theme combine png and zukan-icon
    (
        'src.build.icons.IconPNG.svg_to_png_all',
        ['icon-theme', '--all'],
        DATA_PATH,
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
    (
        'src.build.icons.IconPNG.svg_to_png_all',
        [
            'icon-theme',
            '--data',
            DATA_PATH,
            '--icon',
            ICONS_SVG_PATH,
            '--png',
            ICONS_PNG_PATH,
            '--pngprimary',
            ICONS_DATA_PRIMARY_ICONS_PATH,
        ],
        DATA_PATH,
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
    (
        'src.build.icons.IconPNG.svg_to_png',
        [
            'icon-theme',
            '--file',
            'src/data/afdesign.yaml',
            '--icon',
            ICONS_SVG_PATH,
            '--png',
            ICONS_PNG_PATH,
            '--pngprimary',
            ICONS_DATA_PRIMARY_ICONS_PATH,
        ],
        'src/data/afdesign.yaml',
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
    # Command png
    (
        'src.build.icons.IconPNG.svg_to_png_all',
        ['png', '--all'],
        DATA_PATH,
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
    (
        'src.build.icons.IconPNG.svg_to_png_all',
        [
            'png',
            '--data',
            DATA_PATH,
            '--icon',
            ICONS_SVG_PATH,
            '--png',
            ICONS_PNG_PATH,
            '--pngprimary',
            ICONS_DATA_PRIMARY_ICONS_PATH,
        ],
        DATA_PATH,
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
    (
        'src.build.icons.IconPNG.svg_to_png',
        [
            'png',
            '--file',
            'src/data/afdesign.yaml',
            '--icon',
            ICONS_SVG_PATH,
            '--png',
            ICONS_PNG_PATH,
            '--pngprimary',
            ICONS_DATA_PRIMARY_ICONS_PATH,
        ],
        'src/data/afdesign.yaml',
        ICONS_SVG_PATH,
        ICONS_PNG_PATH,
        ICONS_DATA_PRIMARY_ICONS_PATH,
    ),
]

COMMANDS_ARGS_PATH_P9 = [
    # Command concat
    (
        'src.build.helpers.concat_svgs.ConcatSVG.write_concat_svgs',
        [
            'concat',
            '--data',
            DATA_PATH,
            '--icon',
            ICONS_SVG_PATH,
            '--sample',
            '--samplenumbers',
            str(40),
            '--iconsperrow',
            str(8),
            '--concatfile',
            TEST_SVG_FILE,
            '--maxheight',
            str(1000),
        ],
        DATA_PATH,
        ICONS_SVG_PATH,
        TEST_SVG_FILE,
        True,
        40,
        8,
        1000,
    ),
    (
        'src.build.helpers.concat_svgs.ConcatSVG.write_concat_svgs',
        [
            'concat',
            '--data',
            DATA_PATH,
            '--icon',
            ICONS_SVG_PATH,
            '--all',
            '--iconsperrow',
            str(8),
            '--concatfile',
            TEST_SVG_FILE,
            '--maxheight',
            str(2000),
        ],
        DATA_PATH,
        ICONS_SVG_PATH,
        TEST_SVG_FILE,
        False,
        30,
        8,
        2000,
    ),
]
