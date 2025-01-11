from ..helpers.read_write_data import read_pickle_data
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
)


def list_data_names(zukan_icons: list) -> list:
    """
    Returns:
    list_data_names (list) -- list of data names.
    """
    list_data_names = [d['name'] for d in zukan_icons]

    return list_data_names
