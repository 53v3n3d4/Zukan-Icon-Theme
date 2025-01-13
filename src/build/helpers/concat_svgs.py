import errno
import logging
import os
import random

from collections.abc import Set
from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_created_message,
    print_message,
)
from src.build.helpers.read_write_data import read_yaml_data
from src.build.utils.file_extensions import (
    SVG_EXTENSION,
)
from src.build.utils.svg_element_attributes import (
    SVG_ELEMENTS_ATTRIBUTES_LIST,
)
from src.build.utils.prefer_icons import (
    PREFER_ICONS,
)
from xml.etree import ElementTree


logger = logging.getLogger(__name__)


class ConcatSVG:
    """
    Concat all icons SVGs or a random sample.

    SVGs are concat side by side, orientation horizontally. By default, it places
    5 icons in each row.

    Two lists mode: all icons sorted by name. Name is the key name in data file, not
    SVG file name.

    The other list mode is sample, used in README. By default 30 icons are randomly
    selected.

    When writing the concat file, it does not re calculate positions after putting all
    icons, rects and texts together into new position. It only inserts SVG inside SVG.

    A few links with info about transforming and flattening:
    - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform-origin
    - https://stackoverflow.com/questions/5149301/baking-transforms-into-svg-path-element-commands
    - https://codepen.io/herrstrietzel/pen/MWzZLPP
    """

    def create_element_svg(self, svg_attributes: dict):
        """
        Create 'svg' element. Used to create the main svg, and, also, the 'svg' for icon
        sticker. Sticker means the group made of an icon, text and rect.

        Example:
        Main -- <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 470 300">
        Sticker -- <svg width="79" height="77" viewBox="0 0 79 77" x="12" y="8">

        Paramenters:
        svg_attributes (dict) -- 'svg' element attributes. Currently, apppending, only
        'height', 'viewbox', 'width', 'x' and  'y'.

        Returns:
        svg_tag - return an ElementTree instance.
        """
        svg_tag = ElementTree.Element(
            'svg',
        )
        logger.debug('%r', svg_attributes)

        for k, v in svg_attributes.items():
            if k in SVG_ELEMENTS_ATTRIBUTES_LIST:
                svg_tag.set(k, v)

        return svg_tag

    def create_rounded_rect(self, svg_tag: str):
        """
        Create sticker rounded rect, sub element of 'svg' element.

        Paramenters:
        svg_tag (str) -- 'svg' element tag.

        Returns:
        sticker_rect - return an ElementTree instance.
        """
        sticker_rect = ElementTree.SubElement(
            svg_tag,
            'g',
            transform='matrix(0.79,0,0,0.77,0,0)',
        )
        ElementTree.SubElement(
            sticker_rect,
            'path',
            d='M100,6.494L100,93.506C100,97.09 97.164,100 93.671,100L6.329,'
            '100C2.836,100 0,97.09 0,93.506L0,6.494C0,2.91 2.836,0 6.329,0L93.671,'
            '0C97.164,0 100,2.91 100,6.494Z',
            style='fill:rgba(235,235,235,1);',
        )

        return sticker_rect

    def write_icon_name(self, svg_tag: str, sticker_name: str, svgfile_name: str):
        """
        Write icon name text, sub element of 'svg' element.

        Paramenters:
        svg_tag (str) -- 'svg' element tag.
        sticker_name (str) -- key name in data file. Not the icon SVG
        file name.
        svgfile_name (str) -- SVG file name.

        Returns:
        sticker_text - return an ElementTree instance.
        """
        sticker_text = ElementTree.SubElement(
            svg_tag,
            'g',
            transform='matrix(1,0,0,1,20,55)',
        )
        sticker_text_tag = ElementTree.SubElement(
            sticker_text,
            'text',
            style='font-family:"ArialMT", "Arial", sans-serif;font-size:8px;',
            # dominant-baseline = 'middle',
            # text-anchor = 'middle',
            dy='0',
        )
        sticker_text_tag.set('dominant-baseline', 'middle')
        sticker_text_tag.set('text-anchor', 'middle')
        title = ElementTree.SubElement(
            sticker_text_tag,
            'tspan',
            x='19',
            dy='.6em',
        )
        # print(len(sticker_name))
        title.text = sticker_name
        description = ElementTree.SubElement(
            sticker_text_tag,
            'tspan',
            x='19',
            dy='1.6em',
            style='font-family:"ArialMT", "Arial", sans-serif;font-size:6px;'
            'fill:rgb(155,155,155)',
        )
        description.text = svgfile_name

        return sticker_text

    def edit_icon_svg(self, svgfile_path: str):
        """
        Edit icon SVG size and position, sub element of 'svg' element.

        Paramenters:
        svgfile_path (str) -- path to SVG file.

        Returns:
        icon_svg_tag - return an ElementTree instance.
        """
        # Avoid auto insert namespace. Example 'ns0:'
        ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

        svg_data = ElementTree.parse(svgfile_path)

        icon_svg_tag = svg_data.getroot()
        icon_svg_tag.set('width', '32')
        icon_svg_tag.set('height', '28.4')
        icon_svg_tag.set('viewbox', '0 0 32 28.4')
        icon_svg_tag.set('x', '23')
        icon_svg_tag.set('y', '17')

        logger.debug('%r', icon_svg_tag.attrib)

        return icon_svg_tag

    def create_icon_sticker(
        self, svgfile_path: str, x: str, y: str, sticker_name: str, svgfile_name: str
    ):
        """
        Create sticker, sub element of 'svg' element.

        Sticker is made of an icon, text and rect.

        Paramenters:
        svgfile_path (str) -- path to SVG file.
        x (str) -- 'svg' attribute x. A string(int)
        x (str) -- 'svg' attribute y. A string(int)
        sticker_name (str) -- icon name is the key name in data file. Not the
        icon SVG file name.
        svgfile_name (str) -- SVG file name.

        Returns:
        sticker - return an ElementTree instance.
        """
        sticker = self.create_element_svg(
            {
                'width': '79',
                'height': '77',
                'viewbox': '0 0 79 77',
                'x': x,
                'y': y,
            }
        )
        self.create_rounded_rect(sticker)
        self.write_icon_name(sticker, sticker_name, svgfile_name)
        icon = self.edit_icon_svg(svgfile_path)
        sticker.append(icon)

        return sticker

    def add_to_list_svgs(
        self, icon_name: str, sticker_name: str, dir_origin: str, list_svgs: Set
    ) -> Set:
        """
        Add to SVGs list.

        Paramenters:
        icon_name (str) -- icon name.
        sticker_name (str) -- key name in data file. Not the icon SVG
        file name.
        dir_origin (str) -- path to SVG file.
        list_svgs (Set) -- list with icon name and icon svg file path.

        Returns:
        (Set) - list with icon name and icon svg file path.
        """
        svgfile = f'{icon_name}{SVG_EXTENSION}'
        svgfile_path = os.path.join(dir_origin, svgfile)

        if os.path.exists(svgfile_path):
            icon_svg = (sticker_name, svgfile_path, svgfile)
            list_svgs.add(icon_svg)

    def select_prefer_icon(
        self,
        icon_name: str,
        sticker_name: str,
        dir_origin: str,
        list_svgs: Set,
        prefer_icon: str,
    ) -> Set:
        """
        Select icons versions. Options are: 'dark', 'light' or
        'all'.

        Paramenters:
        icon_name (str) -- icon name.
        sticker_name (str) -- key name in data file. Not the icon SVG
        file name.
        dir_origin (str) -- path to SVG file.
        list_svgs (Set) -- list with icon name and icon svg file path.
        prefer_icon (str) -- choose 'dark', 'light' or 'all'. Default is 'dark'.

        Returns:
        (Set) - list with icon name and icon svg file path.
        """
        # Prefer icon - options dark
        if prefer_icon == 'dark' and not icon_name.endswith('-light'):
            self.add_to_list_svgs(
                icon_name,
                sticker_name,
                dir_origin,
                list_svgs,
            )

        # Prefer icon - options light
        if prefer_icon == 'light' and not icon_name.endswith('-dark'):
            self.add_to_list_svgs(
                icon_name,
                sticker_name,
                dir_origin,
                list_svgs,
            )

        # Prefer icon - options all
        if prefer_icon not in PREFER_ICONS or prefer_icon == 'all':
            self.add_to_list_svgs(
                icon_name,
                sticker_name,
                dir_origin,
                list_svgs,
            )

    def sorted_icons_list(
        self, dir_icon_data: str, dir_origin: str, prefer_icon: str = 'Dark'
    ) -> Set:
        """
        Read icon data files, and create a list with name, svg path and svgfile.

        Paramenters:
        dir_icon_data (str) -- path to directory with data files.
        dir_origin (str) -- path to SVG file.
        prefer_icon (str) -- choose 'dark', 'light' or 'all'. Default is 'dark'.

        Returns:
        sorted_list (Set) - list with icon name and icon svg file path.
        """
        try:
            list_svgs = set()
            files_in_dir = os.listdir(dir_icon_data)

            for file_data in files_in_dir:
                icon_data = os.path.join(dir_icon_data, file_data)
                data = read_yaml_data(icon_data)

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
                elif icon_data.endswith('.yaml'):
                    self.select_prefer_icon(
                        data['preferences']['settings']['icon'],
                        data['name'],
                        dir_origin,
                        list_svgs,
                        prefer_icon,
                    )

                    # Icons options. I.e. nodejs-1
                    if any('icons' in d for d in data) and data['icons'] is not None:
                        for i in data['icons']:
                            self.select_prefer_icon(
                                i,
                                data['name'],
                                dir_origin,
                                list_svgs,
                                prefer_icon,
                            )

            sorted_list = sorted(list_svgs, key=lambda d: d[0].upper())
            logger.debug('%r', sorted_list)

            return sorted_list

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

    def max_icons_per_file(
        self, row_height: int, icons_per_row: int, max_height: int
    ) -> int:
        """
        Calculate max icons per file, given a max height.

        GitHub Markdown viewer seems to cut after 21 row, in pixels would be 1932px.
        The 22 line display only part of. If row height is 92px. Seems limited to 2000px.

        Parameters:
        row_height (int) -- row height of concat SVG file.
        icons_per_row (int) -- number of icons per row.
        max_height (int) --  max height of concat SVG file.

        Returns:
        icons_per_list (int) - max number of icons per file.
        """
        icons_per_list = (max_height // row_height) * icons_per_row
        return icons_per_list

    def write_concat_svgs(
        self,
        dir_icon_data: str,
        dir_origin: str,
        concat_svgfile: str,
        is_sample: bool = False,
        sample_no: int = 30,
        icons_per_row: int = 5,
        max_height: int | None = 2000,
        prefer_icon: str = 'dark',
    ):
        """
        Write concat SVG file, all icons or a sample of icons.

        Orientation: horizontal.

        Max height is for GitHub README, currently, it cut SVG after around
        2000px.

        Paramenters:
        dir_icon_data (str) -- path to directory with data files.
        dir_origin (str) -- path to SVG file.
        concat_svgfile (str) -- path to concat SVG file.
        is_sample (Optional[bool]) -- True for create the sample icons file. Default
        is False.
        sample_no (Optional[int]) -- numbers of SVGs in concat sample file. Default
        is 30.
        icons_per_row (Optional[int]) -- number of icons per row. Default is 5.
        max_height (Optional[int]) -- max concat SVG height. Default is 2000.
        prefer_icon (str) -- choose 'dark', 'light' or 'all'. Default is 'dark'.
        """
        # sticker_size = (77, 79)
        row_height = 92
        column_width = 91

        if is_sample is False:
            print('Write concat SVGs mode all icons')
            icons_list = self.sorted_icons_list(dir_icon_data, dir_origin, prefer_icon)

        if is_sample is True:
            print('Write concat SVGs mode sample icons')
            icons_list_full = self.sorted_icons_list(
                dir_icon_data, dir_origin, prefer_icon
            )
            icons_list = random.sample(icons_list_full, sample_no)

        # Will be added to concat file name, if more than one file saved.
        chunk_counter = 0

        max_range = self.max_icons_per_file(row_height, icons_per_row, max_height)
        logger.debug('max number of icons per list is %d', max_range)

        # Split list based on given height.
        for items in range(0, len(icons_list), max_range):
            chunk = icons_list[items : items + max_range]
            logger.debug('items in list: %s', chunk)

            concat_svg_width = column_width * icons_per_row
            concat_svg_height = round(len(chunk) / icons_per_row) * row_height
            print(f'SVG file size is: {str(concat_svg_width)}x{str(concat_svg_height)}')

            # Main 'svg' element, root.
            concat_svgs_content = self.create_element_svg(
                {
                    'viewbox': f'0 0 {concat_svg_width} {concat_svg_height}',
                }
            )

            # Insert stickers
            icon_sticker_position = {'x': 12, 'y': 8}

            for i, icon in enumerate(chunk):
                logger.debug('svg path %s', icon[1])
                icon_sticker = self.create_icon_sticker(
                    icon[1],
                    str(icon_sticker_position['x']),
                    str(icon_sticker_position['y']),
                    icon[0],
                    icon[2],
                )
                concat_svgs_content.append(icon_sticker)
                print_created_message(
                    icon[2],
                    icon[0],
                    'added to concat SVG file.',
                )

                # Next position in row.
                icon_sticker_position['x'] += column_width

                counter = i + 1

                # After n numbers of stickers, start new row.
                if counter % icons_per_row == 0:
                    icon_sticker_position['x'] = 12
                    icon_sticker_position['y'] += row_height

            if chunk_counter == 0:
                svgfile_path = concat_svgfile

            if chunk_counter > 0:
                file_name, file_extension = os.path.splitext(concat_svgfile)
                svgfile_path = file_name + '-' + str(chunk_counter) + file_extension

            with open(svgfile_path, 'w') as f:
                f.write(ElementTree.tostring(concat_svgs_content).decode('utf-8'))

            chunk_counter += 1
