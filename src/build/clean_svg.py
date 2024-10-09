import errno
import os
import logging
import random
import re
import string

from collections.abc import Set
from src.build.helpers.color import Color
from src.build.helpers.print_message import print_message

# from src.build.utils.build_dir_paths import (
#     ICONS_TEST_PATH,
#     ICONS_TEST_NOT_EXIST_PATH,
#     ICONS_SVG_PATH,
# )
from src.build.utils.svg_common_ids import AFDESIGNER_COMMON_IDS_NAMES
# from src.build.utils.svg_unused_list import UNUSED_LIST

# file_test = os.path.join(ICONS_SVG_PATH, 'rvm.svg')
# file_test = os.path.join(ICONS_SVG_PATH, 'cassandra.svg')

# file_test = os.path.join(ICONS_TEST_PATH, 'file_type_sql.svg')
# file_test = os.path.join(ICONS_TEST_PATH, 'file_type_sql_npt_found.svg')
# file_test = os.path.join(TEST_PATH, 'file_type_afdesign.svg')

logger = logging.getLogger(__name__)


class CleanSVG:
    """
    Clean unused tags, ids and attributes in SVG.

    Affinity Designer program, used to  export SVGs, produce them with unsed tags
    that needs to be deleted. Error can raise depending on lib used.

    The tags and attributes below will be deleted:
    1- <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    2- <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    3- Inside svg tag, delete attribute xmlns:serif="http://www.serif.com/"
    4- Regex clean serif:id="text" attribute
    There are files that do not have item 4. Example: angular.svg

    Affinity Designer use common ids names indexed that conflict when concat SVGs.
    These names are renamed when clean is used.

    Common id names: _clip, _Effect, _Linear, _Gradient and Path_.
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
                            # clean_file = clean_file.replace(line, '')
                            clean_file = _replace_line(clean_file, line)
                            print_message(
                                basename_svgfile,
                                f'line { Color.YELLOW }{ line }{ Color.END } '
                                f'found and being deleted.',
                                color=f'{ Color.CYAN }',
                                color_end=f'{ Color.END }',
                            )
                        else:
                            print_message(
                                basename_svgfile,
                                f'line { Color.YELLOW }{ line }{ Color.END } not found.',
                                color=f'{ Color.RED }',
                                color_end=f'{ Color.END }',
                            )
                    # Regex to remove all serif:id="<text>".
                    # If left, svg file may not read in lib, also in finder(macOS)
                    # svgs will be flaged with error notice.
                    word = 'serif:id'
                    if word in clean_file:
                        clean_file = re.sub(
                            r'\s+serif:id=".*?"', '', clean_file, flags=re.DOTALL
                        )
                        print_message(
                            basename_svgfile,
                            f'attribute { Color.YELLOW }{ word }{ Color.END } '
                            f'found and being deleted.',
                            color=f'{ Color.CYAN }',
                            color_end=f'{ Color.END }',
                        )
                    else:
                        print_message(
                            basename_svgfile,
                            f'attribute { Color.YELLOW }{ word }{ Color.END } not found.',
                            color=f'{ Color.RED }',
                            color_end=f'{ Color.END }',
                        )
                    # Clean Affinity Designer common id names.
                    # They conflict between icons, messing gradient, clips and effects
                    # colors when concat them together.
                    clean_file = CleanSVG.edit_svg_id(clean_file, basename_svgfile)
                with open(svgfile, 'w') as f:
                    f.write(clean_file)
            else:
                print_message(
                    basename_svgfile,
                    'file extension is not svg.',
                    color=f'{ Color.PURPLE }',
                    color_end=f'{ Color.END }',
                )
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), svgfile
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), svgfile
            )

    def clean_all_svgs(dir_svg: str, replace_list: Set):
        """
        Clean a list of unused tags and attributes from SVGs files in a directory.

        Parameters:
        dir_svg (str) -- path to directory with SVGs files.
        replace_list (Set) -- list of unused strings to be replaced.
        """
        try:
            svgs_in_dir = os.listdir(dir_svg)
            for svg in svgs_in_dir:
                svg = os.path.join(dir_svg, svg)
                CleanSVG.clean_svg(svg, replace_list)
                # print(svg)
            # print(svgs_in_dir)
            return svgs_in_dir
        except FileNotFoundError:
            logger.error(
                '[Errno %d] %s: %r', errno.ENOENT, os.strerror(errno.ENOENT), dir_svg
            )
        except OSError:
            logger.error(
                '[Errno %d] %s: %r', errno.EACCES, os.strerror(errno.EACCES), dir_svg
            )

    def edit_svg_id(clean_file: str, basename_svgfile: str):
        """
        Edit common ids names from Affinity Designer. They conflict each other when
        concat SVG.

        New name id needs to be unique to avoid change SVG everytime clean is done,
        otherwise will generate unnecessary commits.

        Common id names: _clip, _Effect, _Linear, _Gradient and Path_.

        Affinity Designer enumerates them starting with 1 and up, one index for all.

        Example: '_clip83', '_Effect84', '_Linear85', '_Linear86', '_Gradient87',
        'Path_88'.
        """
        alphabet = string.ascii_lowercase + string.digits

        for s in AFDESIGNER_COMMON_IDS_NAMES:
            if s in clean_file:
                # The max i found in SVG is llvm-1, i = 297
                # rvm.svg has i = 85.
                for i in range(300):
                    name_id = f'{ s }{ i }'
                    # print(name_id)
                    if name_id in clean_file:
                        # print(name_id)
                        s_uuid = ''.join(random.choices(alphabet, k=7))
                        new_name_id = f'{ s }-{ s_uuid }'
                        # Rename 'Path_' to 'Path'
                        if new_name_id.startswith('Path_'):
                            changed_name_id = new_name_id.replace('Path_', 'Path')
                        if not new_name_id.startswith('Path_'):
                            changed_name_id = new_name_id
                        # Change name id number with shortuuid.
                        # Check if, e.g., '_Linear1' is not '_Linear11'.
                        # Regex 'name_id' followed by ')' or '"'
                        clean_file = re.sub(
                            rf'({ name_id })(ˆ?+["|)])',
                            rf'{ changed_name_id }\2',
                            clean_file,
                        )
                        print_message(
                            basename_svgfile,
                            f'id { Color.YELLOW }{ name_id }{ Color.END } '
                            f'found and being renamed.',
                            color=f'{ Color.CYAN }',
                            color_end=f'{ Color.END }',
                        )
                else:
                    print_message(
                        basename_svgfile,
                        f'id { Color.YELLOW }{ s }{ Color.END } already renamed.',
                        color=f'{ Color.RED }',
                        color_end=f'{ Color.END }',
                    )
            else:
                print_message(
                    basename_svgfile,
                    f'id { Color.YELLOW }{ s }{ Color.END } not found.',
                    color=f'{ Color.RED }',
                    color_end=f'{ Color.END }',
                )

        # print(clean_file)
        return clean_file


def _replace_line(file_info: str, line: str) -> str:
    """
    Remove unwanted line from tmPreference file.

    Parameters:
    file_info (str) -- info of data file.

    Returns:
    str -- text with line removed if found.
    """
    return file_info.replace(line, '')


# CleanSVG.clean_svg(file_test, UNUSED_LIST)
# print(file_test)

# CleanSVG.clean_all_svgs(ICONS_TEST_NOT_EXIST_PATH, UNUSED_LIST)
# CleanSVG.clean_all_svgs(ICONS_TEST_PATH, UNUSED_LIST)
# print(all_svgs)
