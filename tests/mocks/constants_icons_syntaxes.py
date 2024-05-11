TEST_STDOUT_SYNTAXES = """\x1b[92m[!] test_no_icon_file.yaml:\x1b[0m file does not have any syntax.
\x1b[35m[!] pickle.pkl:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_pickle.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.ts:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.mts:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.cts:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest.png:\x1b[0m file extension is not yaml.
\x1b[35m[!] plist.plist:\x1b[0m file extension is not yaml.
\x1b[35m[!] __pycache__:\x1b[0m file extension is not yaml.
\x1b[91m[!] test_empty_file.yaml:\x1b[0m yaml file is empty.
\x1b[92m[!] test_empty_file.yaml:\x1b[0m file does not have any syntax.
\x1b[35m[!] file_type_svg.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_yaml.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_svg.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_icons.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest.tmPreferences:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.js:\x1b[0m file extension is not yaml.
\x1b[35m[!] svg_unused_tags.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] svg.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest@2x.png:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest@3x.png:\x1b[0m file extension is not yaml.
\x1b[35m[!] audio.pkl:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.workspace:\x1b[0m file extension is not yaml.
\x1b[35m[!] preferences.tmPreferences:\x1b[0m file extension is not yaml.
\x1b[36m[!] yaml.yaml\x1b[0m -> \x1b[93mJavaScript (Vitest).sublime-syntax\x1b[0m created.
\x1b[36m[!] yaml.yaml\x1b[0m -> \x1b[93mTypeScript (Vitest).sublime-syntax\x1b[0m created.
\x1b[35m[!] JavaScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_icons_syntaxes.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_preferences.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_plist.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] zukan_syntaxes_data.pkl:\x1b[0m file extension is not yaml.
\x1b[35m[!] tests_paths.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] TypeScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.mjs:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.cjs:\x1b[0m file extension is not yaml.
"""

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
