import errno
import logging
import os

from cairosvg import svg2png
from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_created_message,
    print_message,
    print_special_char,
)
from src.build.helpers.read_write_data import read_yaml_data
from src.build.helpers.special_chars import special_chars
from src.build.utils.build_dir_paths import (
    ICONS_PNG_PATH,
)
from src.build.utils.file_extensions import (
    PNG_EXTENSION,
    SVG_EXTENSION,
)
from src.build.utils.png_details import png_details
from src.build.utils.primary_icons import (
    PRIMARY_ICONS,
)

logger = logging.getLogger(__name__)


class IconPNG:
    """
    Transform icon SVG to PNG.

    It will create or save if file exist.
    """

    def svg_to_png(
        self,
        icon_data: str,
        dir_origin: str,
        dir_destiny: str,
        dir_destiny_primary: str,
    ):
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
        dir_destiny_primary (str) -- path destination of primary icon PNG file.
        """
        try:
            data = read_yaml_data(icon_data)
            # Check if preferences not exist. Or if icon key exist
            # but value empty error.

            if icon_data.endswith('.yaml') and (
                not any('preferences' in d for d in data)
                or data['preferences']['settings'].get('icon') is None
            ):
                print_message(
                    os.path.basename(icon_data),
                    'key icon is not defined or is None.',
                    color=f'{Color.RED}',
                    color_end=f'{Color.END}',
                )
                return data

            elif icon_data.endswith('.yaml'):
                self.generate_png(
                    data['name'],
                    data['preferences']['settings']['icon'],
                    icon_data,
                    dir_origin,
                    dir_destiny,
                )

                # Primary icons
                if data['name'] in PRIMARY_ICONS:
                    self.generate_png(
                        data['name'],
                        data['preferences']['settings']['icon'],
                        icon_data,
                        dir_origin,
                        dir_destiny_primary,
                    )

                # Icons options. I.e. nodejs-1
                if (
                    any('icons' in d for d in data)
                    and data['icons'] is not None
                    and data['name'] not in PRIMARY_ICONS
                ):
                    for i in data['icons']:
                        self.generate_png(
                            data['name'],
                            i,
                            icon_data,
                            dir_origin,
                            dir_destiny,
                        )

                # Primary icons options should save to 'icons_data/primary_icons'
                if (
                    any('icons' in d for d in data)
                    and data['icons'] is not None
                    and data['name'] in PRIMARY_ICONS
                ):
                    for i in data['icons']:
                        self.generate_png(
                            data['name'],
                            i,
                            icon_data,
                            dir_origin,
                            dir_destiny_primary,
                        )
                return data
            else:
                return icon_data
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), icon_data
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), icon_data
            )

    def svg_to_png_all(
        self,
        dir_icon_data: str,
        dir_origin: str,
        dir_destiny: str,
        dir_destiny_primary: str,
    ):
        """
        Generate all icons PNGs files from data files.

        Parameters:
        dir_icon_data(str) -- path to directory with data files.
        dir_origin (str) -- path to svgs files directory.
        dir_destiny (str) -- path destination of PNGs files.
        dir_destiny_primary (str) -- path destination of primary icon PNG file.
        """
        try:
            files_in_dir = os.listdir(dir_icon_data)
            # print(isinstance(files_in_dir, list))
            for file_data in files_in_dir:
                icon_data_path = os.path.join(dir_icon_data, file_data)
                # print(icon_data_path)
                self.svg_to_png(
                    icon_data_path, dir_origin, dir_destiny, dir_destiny_primary
                )
            return files_in_dir
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                dir_icon_data,
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r',
                errno.EACCES,
                os.strerror(errno.EACCES),
                dir_icon_data,
            )

    def generate_png(
        self,
        name: str,
        icon_name: str,
        icon_data: str,
        dir_origin: str,
        dir_destiny: str,
    ):
        """
        Generate PNGs.

        Parameters:
        name(str) -- data name.
        icon_name(str) -- icon name.
        icon_data(str) -- path to data file.
        dir_origin (str) -- path to svgs files directory.
        dir_destiny (str) -- path destination of PNGs files.
        """
        svgfile = f'{icon_name}{SVG_EXTENSION}'

        # Do not allow PNG file name with certain special chars.
        if special_chars(svgfile):
            print_special_char(
                os.path.basename(icon_data),
                icon_name,
            )

        svgfile_path = os.path.join(dir_origin, svgfile)

        # Rename Primary icons in 'icons' folder
        if name in PRIMARY_ICONS and dir_destiny == ICONS_PNG_PATH:
            if icon_name.endswith('-dark'):
                icon_name = icon_name[:-5]
            if icon_name.endswith('-light'):
                icon_name = icon_name[:-6]

        pngfile_base = icon_name

        if not os.path.exists(dir_destiny):
            os.makedirs(dir_destiny)
        pngfile_path_base = os.path.join(dir_destiny, pngfile_base)
        if svgfile.endswith('.svg') and os.path.exists(svgfile_path):
            for attribute in png_details:
                svg2png(
                    url=svgfile_path,
                    write_to=f'{pngfile_path_base}{attribute["suffix"]}{PNG_EXTENSION}',
                    output_width=attribute['width'],
                    output_height=attribute['height'],
                )
                print_created_message(
                    os.path.basename(icon_data),
                    pngfile_base,
                    'done.',
                    filename=f' [{svgfile}]',
                    suffix=f'{attribute["suffix"]}',
                    extension=f'{PNG_EXTENSION}',
                )
        else:
            raise FileNotFoundError(
                print_message(
                    svgfile,
                    'file or directory do not exist.',
                    color=f'{Color.RED}',
                    color_end=f'{Color.END}',
                )
            )
        # return data
