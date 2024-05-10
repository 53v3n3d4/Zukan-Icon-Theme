from collections import OrderedDict


# OrderedDict only necessary if using python 3.3
# Python 3.8, dict read ordered.
def nested_ordered_dict(d: dict) -> OrderedDict:
    """
    Convert recursively to OrderedDict, before saving pickle file.

    Parameters:
    d (dict) -- sublime-syntaxes dict.

    Returns:
    (OrderedDict) -- OrderedDict to preserve dict order.
    """
    if isinstance(d, dict):
        for k, v in d.items():
            d[k] = nested_ordered_dict(v)
            od = OrderedDict(d)

        # od = OrderedDict((k, nested_ordered_dict(v)) for k, v in d.items())

        return od
    elif isinstance(d, list):
        # od = []
        # for i in d:
        #     od = nested_ordered_dict(i)

        od = [nested_ordered_dict(i) for i in d]
        # od = [*map(nested_ordered_dict, d)]
        return od
    else:
        return d
    return d
