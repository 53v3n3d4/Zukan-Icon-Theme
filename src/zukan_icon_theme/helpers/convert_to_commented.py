from collections import OrderedDict
from ruamel.yaml.comments import CommentedMap


# OrderedDict only necessary if using python 3.3
# Python 3.8, dict read ordered.
# From https://stackoverflow.com/questions/53874345/how-do-i-dump-an-ordereddict-out-as-a-yaml-file
def convert_to_commented(d: dict) -> dict:
    """
    Convert OrderedDict to a ruamel CommentedMap before yaml dump.

    Parameters:
    d (dict) -- OrderedDict to be converted.

    Returns:
    (dict) -- dict with preserving order.
    """
    if isinstance(d, OrderedDict):
        od = CommentedMap()
        for k, v in d.items():
            od[k] = convert_to_commented(v)

        # od = CommentedMap((k, convert_to_commented(v)) for k, v in d.items())
        # print(od)

        return od
    elif isinstance(d, list):
        # od = []
        # for i in d:
        #     od = convert_to_commented(i)

        od = [convert_to_commented(i) for i in d]
        return od
    else:
        return d
    # print(d)
    return d
