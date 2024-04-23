# Delete this after testing renaming files and folders.
import os

from src.build.helpers.color import Color
from src.build.utils.build_dir_paths import ICONS_TEST_PATH, ICONS_TEST_NOT_EXIST_PATH


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
                print(
                    f'{ Color.CYAN }[!] { name }{ Color.END } ->'
                    f' { Color.YELLOW }{ new_name }{ Color.END }'
                )
            else:
                print(
                    f'{ Color.PURPLE }[!] { name }{ Color.END }: file '
                    f'extension is not svg.'
                )
        except FileNotFoundError as error:
            # log here
            # print('File could not be found.')
            print(error.args)

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
        except FileNotFoundError as error:
            # log here
            print(error.args)


# RenameSVG.rename_svg('file_type_afdesign.svg', ICONS_TEST_PATH, ICONS_TEST_PATH)
# RenameSVG.rename_svgs_in_dir(ICONS_TEST_PATH, ICONS_TEST_PATH)
# RenameSVG.rename_svgs_in_dir(ICONS_TEST_NOT_EXIST_PATH, ICONS_TEST_PATH)
