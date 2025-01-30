import logging

from ..helpers.load_save_settings import get_create_custom_icon_settings
from ..helpers.remove_empty_dict import remove_empty_dict
from ..helpers.search_zukan_data import list_data_names

logger = logging.getLogger(__name__)


def data(d: dict):
    # Syntax scope if multiple scopes, separated by commas.
    syntax_scope = d['scope'].split(',', 1)[0]
    # Preference only
    # No 'syntax_name' and 'file_extensions'
    if 'syntax_name' not in d and 'file_extensions' not in d:
        return {
            'name': d['name'],
            'preferences': {
                'scope': d['scope'],
                'settings': {'icon': d['icon']},
            },
        }

    # Syntax only
    # No icon argument -> no preferences, only create syntax
    if 'icon' not in d and 'syntax_name' in d:
        if 'contexts_scope' not in d:
            return {
                'name': d['name'],
                'syntax': [
                    {
                        'name': d['syntax_name'],
                        'scope': syntax_scope,
                        'hidden': True,
                        'file_extensions': d['file_extensions'],
                        'contexts': {'main': []},
                    }
                ],
            }
        if 'contexts_scope' in d:
            scope = 'scope:' + d['contexts_scope']
            return {
                'name': d['name'],
                'syntax': [
                    {
                        'name': d['syntax_name'],
                        'scope': syntax_scope,
                        'hidden': True,
                        'file_extensions': d['file_extensions'],
                        'contexts': {
                            'main': [
                                {
                                    'include': scope,
                                    'apply_prototype': True,
                                }
                            ]
                        },
                    }
                ],
            }

    # Preference and Syntax
    if (
        d.get('icon') is not None
        and 'icon' in d
        and 'syntax_name' in d
        and 'scope' in d
        and 'file_extensions' in d
    ):
        if 'contexts_scope' not in d:
            return {
                'name': d['name'],
                'preferences': {
                    'scope': d['scope'],
                    'settings': {'icon': d['icon']},
                },
                'syntax': [
                    {
                        'name': d['syntax_name'],
                        'scope': syntax_scope,
                        'hidden': True,
                        'file_extensions': d['file_extensions'],
                        'contexts': {'main': []},
                    }
                ],
            }
        if 'contexts_scope' in d:
            scope = 'scope:' + d['contexts_scope']
            return {
                'name': d['name'],
                'preferences': {
                    'scope': d['scope'],
                    'settings': {'icon': d['icon']},
                },
                'syntax': [
                    {
                        'name': d['syntax_name'],
                        'scope': syntax_scope,
                        'hidden': True,
                        'file_extensions': d['file_extensions'],
                        'contexts': {
                            'main': [
                                {
                                    'include': scope,
                                    'apply_prototype': True,
                                }
                            ]
                        },
                    }
                ],
            }


def generate_custom_icon(zukan_icons: list) -> list:
    create_custom_icon = get_create_custom_icon_settings()
    dict_list = []

    if create_custom_icon:
        for c in create_custom_icon:
            if 'name' in c and c['name'] not in list_data_names(zukan_icons):
                od = data(remove_empty_dict(c))
                dict_list.append(od)
            if 'name' not in c:
                logger.warning('%s do not have key "name", it is required', c)
            if 'name' in c and c['name'] in list_data_names(zukan_icons):
                logger.warning(
                    '%s key "name" already exists, it should be unique. Excluding from build.',
                    c['name'],
                )

    logger.debug('create_custom_icon od list %s', dict_list)
    return dict_list
