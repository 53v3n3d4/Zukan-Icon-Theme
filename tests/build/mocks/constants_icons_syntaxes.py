TEST_SUBLIME_SYNTAX_DICT = {
    'name': 'Binary (Audio)',
    'scope': 'binary.audio',
    'hidden': True,
    'file_extensions': [
        'aac',
        'aiff',
        'au',
        'flac',
        'm4a',
        'm4p',
        'mp3',
        'mp+',
        'mpc',
        'mpp',
        'oga',
        'opus',
        'ra',
        'rm',
        'wav',
        'wma',
    ],
    'contexts': {'main': []},
}

TEST_SUBLIME_SYNTAXES_CREATED_MESSAGE = 'created.'

TEST_SUBLIME_SYNTAXES_DICT = [
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
        'contexts': {'main': [{'include': 'scope:source.js', 'apply_prototype': True}]},
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
        'contexts': {'main': [{'include': 'scope:source.ts', 'apply_prototype': True}]},
    },
]

TEST_SUBLIME_SYNTAXES_FILE = 'sublime-syntax.sublime-syntax'
