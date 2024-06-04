import sys


# Used by dump_plist_data for compat.
# Python 3.3 is plistlib.writePlist
# Python 3.8 is plistlib.dump
PYTHON_VERSION = float(
    '{a}.{i}'.format(a=sys.version_info.major, i=sys.version_info.minor)
)
