import logging

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

    change_icon_file_extension_dict = {}
    for d in change_icon_file_extension:
        for e in d['file_extensions']:
            if e not in change_icon_file_extension_dict:
                change_icon_file_extension_dict[e] = d['scope']

    scope_file_extensions_dict = {}
    for d in SCOPES_FILE_EXTENSIONS:
        for e in d['file_extensions']:
            if e not in scope_file_extensions_dict:
                scope_file_extensions_dict[e] = d['scope']

    # Remove items from scope_file_extensions_dict if file extension is
    # in change_icon_file_extension_dict
    for d in change_icon_file_extension_dict:
        if d in scope_file_extensions_dict:
            del scope_file_extensions_dict[d]

    file_extensions_dict = {
        **scope_file_extensions_dict,
        **change_icon_file_extension_dict,
    }
    # print(file_extensions_dict)

    syntax_file_extensions = [
        i
        for i in syntax_file_extensions
        if i not in file_extensions_dict or file_extensions_dict[i] == syntax_scope
    ]

    # print(syntax_file_extensions)

    return syntax_file_extensions
