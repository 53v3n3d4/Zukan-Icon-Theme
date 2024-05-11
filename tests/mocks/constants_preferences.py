TEST_TMPREFERENCES_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>scope</key>
    <string>source.js.vitest, source.ts.vitest</string>
    <key>settings</key>
    <dict>
        <key>icon</key>
        <string>vitest</string>
    </dict>
</dict>
</plist>
"""

TEST_TMPREFERENCES_CREATED_MESSAGE = 'created.'

TEST_TMPREFERENCES_DICT = {
    'preferences': {
        'scope': ['source.js.vitest', 'source.ts.vitest'],
        'settings': {'icon': 'vitest'},
    },
}

TEST_TMPREFERENCES_FILE = 'preferences.tmPreferences'
