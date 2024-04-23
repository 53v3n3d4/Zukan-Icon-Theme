import os
import re

from collections.abc import Set
from src.build.helpers.color import Color

from src.build.utils.build_dir_paths import ICONS_TEST_PATH, ICONS_TEST_NOT_EXIST_PATH
from src.build.utils.svg_unused_list import UNUSED_LIST


# file_test = os.path.join(ICONS_TEST_PATH, 'file_type_sql.svg')
# file_test = os.path.join(ICONS_TEST_PATH, 'file_type_sql_npt_found.svg')
# file_test = os.path.join(TEST_PATH, 'file_type_afdesign.svg')


class CleanSVG:
    """
    Clean unused tags and attributes in SVG.

    Affinity designer program, used to  export SVGs, produce them with unsed tags
    that needs to be deleted. Error can raise depending on lib used.

    The tags and attributes below will be deleted:
    1- <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    2- <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    3- Inside svg tag, delete attribute xmlns:serif="http://www.serif.com/"
    4- Regex clean serif:id="text" attribute
    There are files that do not have item 4. Example: angular.svg
    """

    def clean_svg(svgfile: str, replace_list: Set):
        """
        Clean unused tags and attributes in SVG file, from a list of strings.

        Parameters:
        svg (str) -- SVG file path.
        replace_list (Set) -- list of unused strings to be replaced.
        """
        try:
            basename_svgfile = os.path.basename(svgfile)
            if svgfile.endswith('.svg'):
                with open(svgfile, 'r+') as f:
                    clean_file = f.read()
                    # replace string line from unused list
                    for line in replace_list:
                        if line in clean_file:
                            clean_file = clean_file.replace(line, '')
                            print(
                                f'{ Color.CYAN }[!] { basename_svgfile }'
                                f'{ Color.END }: line { Color.YELLOW }{ line } '
                                f'{ Color.END }found and being deleted.'
                            )
                        else:
                            print(
                                f'{ Color.RED }[!] { basename_svgfile }'
                                f'{ Color.END }: line { Color.YELLOW }{ line } '
                                f'{ Color.END }not found.'
                            )
                    # Regex to remove all serif:id="<text>".
                    # If left, svg file may not read in lib, also in finder(macOS)
                    # svgs will be flaged with error notice.
                    word = 'serif:id'
                    if word in clean_file:
                        clean_file = re.sub(
                            r'\s+serif:id=".*?"', '', clean_file, flags=re.DOTALL
                        )
                        print(
                            f'{ Color.CYAN }[!] { basename_svgfile }'
                            f'{ Color.END }: attribute { Color.YELLOW }{ word } '
                            f'{ Color.END }found and being deleted.'
                        )
                    else:
                        print(
                            f'{ Color.RED }[!] { basename_svgfile }'
                            f'{ Color.END }: attribute { Color.YELLOW }{ word } '
                            f'{ Color.END }not found.'
                        )
                with open(svgfile, 'w') as f:
                    f.write(clean_file)
            else:
                print(
                    f'{ Color.PURPLE }[!] { basename_svgfile }{ Color.END }: '
                    f'file extension is not svg.'
                )
        except FileNotFoundError as error:
            # log here
            print(error.args)

    def clean_all_svgs(foldername: str, replace_list: Set):
        """
        Clean a list of unused tags and attributes from SVGs files in a directory.

        Parameters:
        foldername (str) -- path to directory with SVGs files.
        replace_list (Set) -- list of unused strings to be replaced.
        """
        try:
            svgs_in_dir = os.listdir(foldername)
            for svg in svgs_in_dir:
                svg = os.path.join(foldername, svg)
                CleanSVG.clean_svg(svg, replace_list)
                # print(svg)
            # print(svgs_in_dir)
            return svgs_in_dir
        except FileNotFoundError as error:
            # log here
            print(error.args)


# CleanSVG.clean_svg(file_test, UNUSED_LIST)
# print(file_test)

# CleanSVG.clean_all_svgs(ICONS_TEST_NOT_EXIST_PATH, UNUSED_LIST)
# CleanSVG.clean_all_svgs(ICONS_TEST_PATH, UNUSED_LIST)
# print(all_svgs)
