import os

from ..helpers.read_write_data import dump_yaml_data, read_pickle_data
from ..utils.zukan_dir_paths import (
    ASSETS_PATH,
    ZUKAN_SYNTAXES_DATA_FILE,
)


class ZukanSyntax:
    def create_icons_syntaxes():
        zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
        # zukan_icons_syntaxes = dict(zukan_icons_syntaxes)
        for s in zukan_icons_syntaxes:
            filename = s['name'] + '.sublime-syntax'
            test_path = os.path.join(ASSETS_PATH, 'test')
            syntax_file_path = os.path.join(test_path, filename)
            # print(syntax_file_path)
            dump_yaml_data(s, syntax_file_path)
        return zukan_icons_syntaxes


# def sort_dict(zukan_list):
#     """
#     Re ordering syntax keys.

#     Python 3.3 is reading unordered dict. ST Python 3.8, reads ordered.
#     """
#     for s in zukan_list:
#         syntax_order = ['name', 'scope', 'hidden', 'file_extensions', 'contexts']
#         s = sorted(s.items(), key=lambda i:syntax_order.index(i[0]))
#         print(s)
#     return zukan_list
