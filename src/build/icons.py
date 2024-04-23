# import errno
import os

from cairosvg import svg2png
from src.build.helpers.color import Color
from src.build.helpers.read_write_data import read_yaml_data
from src.build.helpers.special_chars import special_chars
from src.build.utils.build_dir_paths import (
    DATA_PATH,
    ICONS_PNG_TEST_PATH,
    ICONS_TEST_PATH,
    ICONS_TEST_NOT_EXIST_PATH,
)
from src.build.utils.file_extensions import PNG_EXTENSION, SVG_EXTENSION
from src.build.utils.png_details import png_details

# ICONS_TEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../donotexist')

# file_test = os.path.join(DATA_PATH, 'test_no_icon_file.yaml')
# file_test = os.path.join(ICONS_TEST_PATH, 'file_type_afdesign.svg')
# file_test = os.path.join(DATA_PATH, 'c++.yaml')
# file_test = os.path.join(DATA_PATH, 'afdesign.yaml')
# file_test = os.path.join(DATA_PATH, 'test_js.yaml')
file_test = os.path.join(DATA_PATH, 'c#.yaml')
# file_test = os.path.join(DATA_PATH, 'afdesign_not_exist.yaml')


class IconPNG:
    """
    Transform icon SVG to PNG.

    It will create or save if file exist.
    """

    def svg_to_png(icon_data: str, dir_origin: str, dir_destiny: str):
        """
        Generate PNG file from SVG.

        Create PNG icons in 3 sizes, Size and suffix details comes from
        png_details.py.
        Sizes:
        - icon-name.png: 18px x 16px
        - icon-name@2x.png: 36px x 32px
        - icon-name@3x.png: 54px x 48px

        The file name will be name of icon stored in file data, Preferences >
        Settings > Icon. Info is stored in src/data directory.

        It will be also the name of sublime-syntax and tmPreferences generated.

        Parameters:
        icon_data(str) -- path to data file.
        dir_origin (str) -- path to SVG file.
        dir_destiny (str) -- path destination of PNG file.
        """
        try:
            # YAML
            if icon_data.endswith('.yaml') and os.path.exists(icon_data):
                data = read_yaml_data(icon_data)
                if data is None:
                    print(
                        f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                        f'{ Color.END } yaml file is empty.'
                    )
                # Check if preferences not exist. Or if icon key exist
                # but value empty error.
                elif (
                    not any('preferences' in d for d in data)
                    or data['preferences']['settings'].get('icon') is None
                ):
                    print(
                        f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                        f'{ Color.END } key icon is not defined or is None.'
                    )
                else:
                    svgfile = (
                        f'{ data["preferences"]["settings"]["icon"] }'
                        f'{ SVG_EXTENSION }'
                    )
                    # Do not allow PNG file name with certain special chars.
                    if special_chars(svgfile):
                        print(
                            f'{ Color.RED }[!] { os.path.basename(icon_data) }:'
                            f'{ Color.END } icon value { Color.RED }(filename '
                            f'would be c#.svg){ Color.END }  can not contain '
                            f'special characters.'
                        )
                    # print(svgfile)
                    svgfile_path = os.path.join(dir_origin, svgfile)
                    # print(svgfile_path)
                    pngfile_base = data['preferences']['settings']['icon']
                    # print(pngfile_base)
                    if not os.path.exists(dir_destiny):
                        os.makedirs(dir_destiny)
                    pngfile_path_base = os.path.join(dir_destiny, pngfile_base)
                    if svgfile.endswith('.svg') and os.path.exists(svgfile_path):
                        for attribute in png_details:
                            svg2png(
                                url=svgfile_path,
                                write_to=f'{ pngfile_path_base }{ attribute["suffix"] }'
                                f'{ PNG_EXTENSION }',
                                output_width=attribute['width'],
                                output_height=attribute['height'],
                            )
                            print(
                                f'{ Color.CYAN }[!] { os.path.basename(icon_data) } '
                                f'[{ svgfile }]{ Color.END } -> { Color.YELLOW }'
                                f'{ pngfile_base }{ attribute["suffix"] }'
                                f'{ PNG_EXTENSION }{ Color.END } done.'
                            )
                    elif not svgfile.endswith('.svg'):
                        print(
                            f'{ Color.RED }{ svgfile }{ Color.END }: file extension '
                            f'is not svg.'
                        )
                    elif not os.path.exists(svgfile_path):
                        # Ansi color not working
                        raise FileNotFoundError(
                            f'[!] {svgfile}: origin directory { dir_origin } or file '
                            f'does not exist.'
                        )
                    else:
                        raise ValueError(
                            f'{ Color.RED }{ svgfile }{ Color.END }: icon svg file '
                            f'does not exist.'
                        )
            elif not icon_data.endswith('.yaml'):
                print(
                    f'{ Color.PURPLE }[!] { os.path.basename(icon_data) }'
                    f'{ Color.END }: file extension is not yaml.'
                )
            else:
                raise ValueError('Yaml file do not exist.')
        except OSError as error:
            # log here
            print(error.args)
        except FileNotFoundError as error:
            # log here
            print(error.args, 'Icons Error')
            # print(errno.ENOENT, os.strerror(errno.ENOENT), icon_data)

    def svg_to_png_all(dir_icon_data: str, dir_origin: str, dir_destiny: str):
        """
        Generate all icons PNGs files from data files.

        Parameters:
        dir_icon_data(str) -- path to directory with data files.
        dir_origin (str) -- path to svgs files directory.
        dir_destiny (str) -- path destination of PNGs files.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            # print(isinstance(files_in_dir, list))
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                IconPNG.svg_to_png(icon_data_path, dir_origin, dir_destiny)
            return files_in_dir
        except FileNotFoundError as error:
            # log here
            print(error.args, 'Icons error')


# IconPNG.svg_to_png(file_test, ICONS_TEST_NOT_EXIST_PATH, ICONS_PNG_TEST_PATH)
# IconPNG.svg_to_png(file_test, ICONS_TEST_PATH, ICONS_PNG_TEST_PATH)
# IconPNG.svg_to_png_all(DATA_PATH, ICONS_TEST_NOT_EXIST_PATH, ICONS_PNG_TEST_PATH)
# IconPNG.svg_to_png_all(DATA_PATH, ICONS_TEST_PATH, ICONS_PNG_TEST_PATH)
