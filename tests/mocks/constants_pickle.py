from collections import OrderedDict


TEST_PICKLE_AUDIO_FILE = 'tests/mocks/audio.pkl'

TEST_PICKLE_FILE = 'tests/foo/bar.pkl'

TEST_PICKLE_ZUKAN_FILE = 'tests/mocks/zukan_syntaxes_data.pkl'

TEST_PICKLE_NESTED_ORDERED_DICT = [
    OrderedDict(
        [
            ('name', 'JavaScript (Vitest)'),
            ('scope', 'source.js.vitest'),
            ('hidden', True),
            (
                'file_extensions',
                [
                    'vitest.config.js',
                    'vitest.config.cjs',
                    'vitest.config.mjs',
                    'vitest.workspace',
                ],
            ),
            (
                'contexts',
                OrderedDict(
                    [
                        (
                            'main',
                            [
                                OrderedDict(
                                    [
                                        ('include', 'scope:source.js'),
                                        ('apply_prototype', True),
                                    ]
                                )
                            ],
                        )
                    ]
                ),
            ),
        ]
    ),
    OrderedDict(
        [
            ('name', 'TypeScript (Vitest)'),
            ('scope', 'source.ts.vitest'),
            ('hidden', True),
            (
                'file_extensions',
                ['vitest.config.ts', 'vitest.config.cts', 'vitest.config.mts'],
            ),
            (
                'contexts',
                OrderedDict(
                    [
                        (
                            'main',
                            [
                                OrderedDict(
                                    [
                                        ('include', 'scope:source.ts'),
                                        ('apply_prototype', True),
                                    ]
                                )
                            ],
                        )
                    ]
                ),
            ),
        ]
    ),
]

TEST_PICKLE_ORDERED_DICT = OrderedDict(
    [
        ('name', 'Binary (Audio)'),
        ('scope', 'binary.audio'),
        ('hidden', True),
        (
            'file_extensions',
            [
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
        ),
        ('contexts', OrderedDict([('main', [])])),
    ]
)
