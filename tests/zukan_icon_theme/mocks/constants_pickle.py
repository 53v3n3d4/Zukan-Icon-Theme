from collections import OrderedDict


TEST_PICKLE_AUDIO_FILE = 'tests/build/mocks/audio.pkl'

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
