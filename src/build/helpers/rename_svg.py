import os

from src.build.helpers.color import Color
from src.build.helpers.print_message import (
    print_created_message,
    print_filenotfounderror,
    print_message,
    print_oserror,
)
# from src.build.utils.build_dir_paths import ICONS_TEST_PATH, ICONS_TEST_NOT_EXIST_PATH


class RenameSVG:
    def rename_svg(name: str, dir_origin: str, dir_destiny: str):
        """
        Rename svg file from file_type_(name).svg to (name).svg

        Parameters:
        name(str) -- svg file name to be renamed.
        dir_origin (str) -- path to svg file.
        dir_destiny (str) -- path destination of svg renamed file.
        """
        try:
            if name.endswith('.svg'):
                previous_name = os.path.join(dir_origin, name)
                # print(previous_name)
                new_name = os.path.join(
                    dir_destiny, previous_name.replace('file_type_', '')
                )
                # print(new_name)
                os.rename(previous_name, new_name)
                print_created_message(
                    name,
                    new_name,
                    '.',
                )
            else:
                print_message(
                    name,
                    'file extension is not svg.',
                    color=f'{ Color.PURPLE }',
                    color_end=f'{ Color.END }',
                )
        except FileNotFoundError:
            print_filenotfounderror(name)
        except OSError:
            print_oserror(name)

    def rename_svgs_in_dir(dir_origin: str, dir_destiny: str):
        """
        Rename all svgs files, that starts with file_type_, inside
        a directiory.

        Parameters:
        dir_origin (str) -- path to svgs files directory.
        dir_destiny (str) -- path destination of svgs renamed files.
        """
        try:
            files_in_dir = os.listdir(dir_origin)
            for name in files_in_dir:
                RenameSVG.rename_svg(name, dir_origin, dir_destiny)
            return files_in_dir
        except FileNotFoundError:
            print_filenotfounderror(dir_origin)
        except OSError:
            print_oserror(dir_origin)


# RenameSVG.rename_svg('file_type_afdesign.svg', ICONS_TEST_PATH, ICONS_TEST_PATH)
# RenameSVG.rename_svgs_in_dir(ICONS_TEST_PATH, ICONS_TEST_PATH)
# RenameSVG.rename_svgs_in_dir(ICONS_TEST_NOT_EXIST_PATH, ICONS_TEST_PATH)
