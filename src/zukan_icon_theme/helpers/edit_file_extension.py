import logging

from ..helpers.load_save_settings import get_change_icon_settings
from ..utils.scopes_file_extensions import (
    SCOPES_FILE_EXTENSIONS,
)

logger = logging.getLogger(__name__)


def edit_file_extension(
    syntax_file_extensions: list, syntax_scope: str, change_icon_file_extension: list
) -> list:
    """
    Different packages can use same file extension. It could result in an icon
    pointing to a not desired file extension. This function remove file extension,
    in existing icon syntax, if scope is different from a list.

    The list comes from 2 different origins. One is default: SCOPES_FILE_EXTENSIONS.
    And the other is from user 'change_icon_file_extension' setting.

    Parameters:
    syntax_file_extensions (list) -- list of file extensions in a syntax data.
    syntax_scope (str) --  syntax scope.

    Retunrs:
    syntax_file_extensions (list) -- list of file extensions based on two lists:
    SCOPES_FILE_EXTENSIONS and 'change_icon_file_extension' setting.
    """

    file_extensions_list = []
    default_extensions = set()
    user_extensions = set()

    for f in SCOPES_FILE_EXTENSIONS:
        # change_icon_file_extension is empty
        if not change_icon_file_extension:
            file_extensions_list.append(
                {'scope': f['scope'], 'file_extensions': f['file_extensions']}
            )
        for e in change_icon_file_extension:
            # File extension present in both lists, keep user setting.
            if f['file_extensions'] == e['file_extensions']:
                file_extensions_list.append(
                    {'scope': e['scope'], 'file_extensions': e['file_extensions']}
                )
                # print(e['scope'])
            # Need to append the ones that are not present in list default
            # book.toml in 'change_icon_file_extension' example
            for i in e['file_extensions']:
                user_extensions.add(i)
                if i not in default_extensions:
                    # print(i)
                    file_extensions_list.append(
                        {'scope': e['scope'], 'file_extensions': e['file_extensions']}
                    )

            # Need to append the ones that are not present in user list
            for i in f['file_extensions']:
                default_extensions.add(i)
                if i not in user_extensions:
                    # print(i)
                    file_extensions_list.append(
                        {'scope': f['scope'], 'file_extensions': f['file_extensions']}
                    )

    # print(file_extensions_list)
    # Duplicating dicts from not present in lists, user_extensions and default_extensions.
    file_extensions_list_not_duplicated = []
    seen = set()

    for f in file_extensions_list:
        scope_file_extension_tuple = (f['scope'], tuple(f['file_extensions']))
        if scope_file_extension_tuple not in seen:
            file_extensions_list_not_duplicated.append(f)
            seen.add(scope_file_extension_tuple)
    # print(file_extensions_list_not_duplicated)

    for d in file_extensions_list_not_duplicated:
        for e in d['file_extensions']:
            if syntax_scope != d['scope']:
                # Remove file extension
                syntax_file_extensions = [
                    f for f in syntax_file_extensions if not f == e
                ]

    logger.debug('%s file extensions %s', syntax_scope, syntax_file_extensions)
    # print('{s} file extensions {f}'.format(s=syntax_scope,f=syntax_file_extensions))
    return syntax_file_extensions
