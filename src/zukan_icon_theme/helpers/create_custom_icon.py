import logging
import os

from ..helpers.load_save_settings import get_settings
from ..utils.file_extensions import (
    PNG_EXTENSION,
)
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_PATH,
)
from collections import OrderedDict

logger = logging.getLogger(__name__)


def data(d: dict):
    # Preference only
    # No 'syntax_name' and 'file_extensions'
    if ('synttax_name' and 'file_extensions') not in d:
        return OrderedDict(
            {
                'name': d['name'],
                'preferences': OrderedDict(
                    {'scope': d['scope'], 'settings': OrderedDict({'icon': d['icon']})}
                ),
            }
        )

    # Syntax only
    # No icon argument -> no preferences, only create syntax
    if 'icon' not in d:
        if 'contexts_scope' not in d:
            return OrderedDict(
                {
                    'name': d['name'],
                    'syntax': [
                        OrderedDict(
                            {
                                'name': d['syntax_name'],
                                'scope': d['scope'],
                                'hidden': True,
                                'file_extensions': d['file_extensions'],
                                'contexts': OrderedDict({'main': []}),
                            }
                        )
                    ],
                }
            )
        if 'contexts_scope' in d:
            scope = 'scope:' + d['contexts_scope']
            return OrderedDict(
                {
                    'name': d['name'],
                    'syntax': [
                        OrderedDict(
                            {
                                'name': d['syntax_name'],
                                'scope': d['scope'],
                                'hidden': True,
                                'file_extensions': d['file_extensions'],
                                'contexts': OrderedDict(
                                    {
                                        'main': [
                                            OrderedDict(
                                                {
                                                    'include': scope,
                                                    'apply_prototype': True,
                                                }
                                            )
                                        ]
                                    }
                                ),
                            }
                        )
                    ],
                }
            )

    # Preference and Syntax
    if (
        d.get('icon') is not None
        and ('icon' and 'syntax_name' and 'scope' and 'file_extensions') in d
    ):
        if 'contexts_scope' not in d:
            return OrderedDict(
                {
                    'name': d['name'],
                    'preferences': OrderedDict(
                        {
                            'scope': d['scope'],
                            'settings': OrderedDict({'icon': d['icon']}),
                        }
                    ),
                    'syntax': [
                        OrderedDict(
                            {
                                'name': d['syntax_name'],
                                'scope': d['scope'],
                                'hidden': True,
                                'file_extensions': d['file_extensions'],
                                'contexts': OrderedDict({'main': []}),
                            }
                        )
                    ],
                }
            )
        if 'contexts_scope' in d:
            scope = 'scope:' + d['contexts_scope']
            return OrderedDict(
                {
                    'name': d['name'],
                    'preferences': OrderedDict(
                        {
                            'scope': d['scope'],
                            'settings': OrderedDict({'icon': d['icon']}),
                        }
                    ),
                    'syntax': [
                        OrderedDict(
                            {
                                'name': d['syntax_name'],
                                'scope': d['scope'],
                                'hidden': True,
                                'file_extensions': d['file_extensions'],
                                'contexts': OrderedDict(
                                    {
                                        'main': [
                                            OrderedDict(
                                                {
                                                    'include': scope,
                                                    'apply_prototype': True,
                                                }
                                            )
                                        ]
                                    }
                                ),
                            }
                        )
                    ],
                }
            )


def create_custom_icon() -> list:
    create_custom_icon = get_settings(ZUKAN_SETTINGS, 'create_custom_icon')
    if not isinstance(create_custom_icon, list):
        logger.warning('create_custom_icon option malformed, need to be a string list')

    list_od = []

    if create_custom_icon:
        for c in create_custom_icon:
            # Check if PNG exist
            if 'icon' in c and not os.path.exists(
                os.path.join(ZUKAN_PKG_ICONS_PATH, c['icon'] + PNG_EXTENSION)
            ):
                logger.warning('%s%s not found', c['icon'], PNG_EXTENSION)
            if 'name' in c:
                od = data(c)
                list_od.append(od)
            if 'name' not in c:
                logger.warning('%s do not have key "name", it is required', c)

    logger.debug('create_custom_icon od list %s', list_od)
    return list_od
