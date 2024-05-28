from collections import OrderedDict

# TEMPLATE_JSON = [
#     {'class': 'icon_file_type', 'layer0.tint': None, 'content_margin': [9, 8]}
# ]
TEMPLATE_JSON = [
    OrderedDict(
        [('class', 'icon_file_type'), ('layer0.tint', None), ('content_margin', [9, 8])]
    )
]

# TEMPLATE_JSON_WITH_OPACITY = [
#     {
#         'class': 'icon_file_type',
#         'layer0.tint': None,
#         'layer0.opacity': 0.8,
#         'content_margin': [9, 8],
#     },
#     {
#         'class': 'icon_file_type',
#         'parents': [{'class': 'tree_row', 'attributes': ['hover']}],
#         'layer0.opacity': 1.0,
#     },
#     {
#         'class': 'icon_file_type',
#         'parents': [{'class': 'tree_row', 'attributes': ['selected']}],
#         'layer0.opacity': 1.0,
#     },
# ]
TEMPLATE_JSON_WITH_OPACITY = [
    OrderedDict(
        [
            ('class', 'icon_file_type'),
            ('layer0.tint', None),
            ('layer0.opacity', 0.8),
            ('content_margin', [9, 8]),
        ]
    ),
    OrderedDict(
        [
            ('class', 'icon_file_type'),
            (
                'parents',
                [OrderedDict([('class', 'tree_row'), ('attributes', ['hover'])])],
            ),
            ('layer0.opacity', 1.0),
        ]
    ),
    OrderedDict(
        [
            ('class', 'icon_file_type'),
            (
                'parents',
                [OrderedDict([('class', 'tree_row'), ('attributes', ['selected'])])],
            ),
            ('layer0.opacity', 1.0),
        ]
    ),
]
