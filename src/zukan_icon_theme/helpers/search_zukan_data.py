def list_data_names(zukan_icons_data: list) -> list:
    """
    Returns:
    list_data_names (list) -- list of data names.
    """
    list_data_names = [d['name'] for d in zukan_icons_data]

    return list_data_names
