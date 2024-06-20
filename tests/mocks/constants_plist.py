TEST_PLIST_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>scope</key>
<string>binary.afdesign</string>
<key>settings</key>
<dict>
	<key>icon</key>
	<string>afdesign</string>
</dict>
</dict>
</plist>
"""

TEST_PLIST_DICT = {
    'name': 'Affinity Designer',
    'preferences': {'scope': 'binary.afdesign', 'settings': {'icon': 'afdesign'}},
    'syntax': [
        {
            'name': 'Binary (Affinity Designer)',
            'scope': 'binary.afdesign',
            'hidden': True,
            'file_extensions': ['afdesign'],
            'contexts': {'main': []},
        }
    ],
}

TEST_PLIST_DICT_PLUGIN = {
    'scope': 'source.js.vitest, source.ts.vitest',
    'settings': {'icon': 'vitest'},
}

TEST_PLIST_EXPECTED = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>scope</key>
<string>binary.afdesign</string>
<key>settings</key>
<dict>
	<key>icon</key>
	<string>afdesign</string>
</dict>
</dict>
</plist>
"""

# Tab identantion important to assertEqual in test_clean_data.
TEST_PLIST_EXPECTED_PLUGIN = """<?xml version="1.0" encoding="UTF-8"?>
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

TEST_PLIST_FILE = 'tests/bar.plist'

TEST_PLIST_FILE_PLUGIN = 'plist.plist'
