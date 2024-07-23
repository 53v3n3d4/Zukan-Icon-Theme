from ..helpers.read_write_data import read_pickle_data
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
)


def list_data_names():
    """
    list of data names.
    """
    zukan_icons = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
    list_data_names = [d['name'] for d in zukan_icons]

    return list_data_names
