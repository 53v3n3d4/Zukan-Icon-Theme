TEMPLATE_JSON = """[
    {
        "class": "icon_file_type",
        "layer0.tint": null,
        "content_margin": [9, 8]
    }
]"""

TEMPLATE_JSON_WITH_OPACITY = """[
    {
        "class": "icon_file_type",
        "layer0.tint": null,
        "layer0.opacity": 0.8,
        "content_margin": [9, 8],
    },
    {
        "class": "icon_file_type",
        "parents": [{"class": "tree_row", "attributes": ["hover"]}],
        "layer0.opacity": 1.0,
    },
    {
        "class": "icon_file_type",
        "parents": [{"class": "tree_row", "attributes": ["selected"]}],
        "layer0.opacity": 1.0,
    }
]"""
