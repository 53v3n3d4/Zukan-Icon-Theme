def remove_empty_dict(d):
    """
    Copied from
    https://stackoverflow.com/questions/12118695/
    efficient-way-to-remove-keys-with-empty-strings-from-a-dict/24893252#24893252

    Remove empty keys.

    Used in 'commands_settings > CreateCustomIcon', inputs can be empty.
    """
    if isinstance(d, dict):
        return dict(
            (k, remove_empty_dict(v))
            for k, v in d.items()
            if v and remove_empty_dict(v)
        )
    elif isinstance(d, list):
        return [remove_empty_dict(v) for v in d if v and remove_empty_dict(v)]
    else:
        return d
