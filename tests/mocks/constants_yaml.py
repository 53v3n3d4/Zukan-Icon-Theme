from collections import OrderedDict


TEST_YAML_CONTENT = """%YAML 1.2
---
name: Vitest
preferences:
scope: source.js.vitest, source.ts.vitest
settings:
icon: vitest
syntax:
- name: JavaScript (Vitest)
scope: source.js.vitest
hidden: true
file_extensions:
  - vitest.config.js
  - vitest.config.cjs
  - vitest.config.mjs
  - vitest.workspace
contexts:
  main:
    - include: scope:source.js
      apply_prototype: true
- name: TypeScript (Vitest)
scope: source.ts.vitest
hidden: true
file_extensions:
  - vitest.config.ts
  - vitest.config.cts
  - vitest.config.mts
contexts:
  main:
    - include: scope:source.ts
      apply_prototype: true
"""

TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITH_SCOPES = """%YAML 1.2
---
name: JSON (Lerna)
scope: source.json.lerna
hidden: true
file_extensions:
- lerna.json
contexts:
  main:
  - include: scope:source.json#prototype
  - include: scope:source.json
"""

TEST_YAML_CONTENT_EDIT_CONTEXTS_MAIN_WITHOUT_SCOPES = """%YAML 1.2
---
name: JSON (Lerna)
scope: source.json.lerna
hidden: true
file_extensions:
- lerna.json
contexts:
  main: []
"""

TEST_YAML_DICT = {
    'name': 'Binary (Affinity Designer)',
    'scope': 'binary.afdesign',
    'hidden': True,
    'file_extensions': ['afdesign'],
    'contexts': {'main': []},
}

TEST_YAML_EMPTY_FILE = ''

TEST_YAML_EXPECTED = {
    'name': 'Vitest',
    'preferences': {
        'scope': 'source.js.vitest, source.ts.vitest',
        'settings': {'icon': 'vitest'},
    },
    'syntax': [
        {
            'name': 'JavaScript (Vitest)',
            'scope': 'source.js.vitest',
            'hidden': True,
            'file_extensions': [
                'vitest.config.js',
                'vitest.config.cjs',
                'vitest.config.mjs',
                'vitest.workspace',
            ],
            'contexts': {
                'main': [{'include': 'scope:source.js', 'apply_prototype': True}]
            },
        },
        {
            'name': 'TypeScript (Vitest)',
            'scope': 'source.ts.vitest',
            'hidden': True,
            'file_extensions': [
                'vitest.config.ts',
                'vitest.config.cts',
                'vitest.config.mts',
            ],
            'contexts': {
                'main': [{'include': 'scope:source.ts', 'apply_prototype': True}]
            },
        },
    ],
}

TEST_YAML_FILE = 'tests/foo/bar.yaml'

TEST_YAML_ORDERED_DICT = OrderedDict([('a', 1), ('b', 2), ('c', 3)])

TEST_YAML_ORDERED_DICT_EDIT_CONTEXTS_MAIN = OrderedDict(
    [
        ('name', 'JSON (Lerna)'),
        ('scope', 'source.json.lerna'),
        ('hidden', True),
        ('file_extensions', ['lerna.json']),
        (
            'contexts',
            OrderedDict(
                [
                    (
                        'main',
                        [
                            OrderedDict(
                                [
                                    ('include', 'scope:source.json'),
                                    ('apply_prototype', True),
                                ]
                            )
                        ],
                    )
                ]
            ),
        ),
    ]
)
