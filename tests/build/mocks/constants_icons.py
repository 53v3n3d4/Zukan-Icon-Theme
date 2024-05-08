STDOUT_PNG = """\x1b[91m[!] test_no_icon_file.yaml:\x1b[0m key icon is not defined or is None.
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
\x1b[91m[!] test_empty_file.yaml:\x1b[0m key icon is not defined or is None.
\x1b[35m[!] file_type_svg.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_yaml.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_svg.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest.tmPreferences:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.js:\x1b[0m file extension is not yaml.
\x1b[35m[!] svg_unused_tags.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] svg.svg:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest@2x.png:\x1b[0m file extension is not yaml.
\x1b[35m[!] vitest@3x.png:\x1b[0m file extension is not yaml.
\x1b[35m[!] audio.pkl:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.workspace:\x1b[0m file extension is not yaml.
\x1b[35m[!] preferences.tmPreferences:\x1b[0m file extension is not yaml.
\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest.png\x1b[0m done.
\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@2x.png\x1b[0m done.
\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@3x.png\x1b[0m done.\n'
\x1b[35m[!] constants_tmpreferences.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] JavaScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_icons_syntaxes.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] constants_plist.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] tests_paths.py:\x1b[0m file extension is not yaml.
\x1b[35m[!] TypeScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.mjs:\x1b[0m file extension is not yaml.
\x1b[35m[!] Vitest.vitest.config.cjs:\x1b[0m file extension is not yaml."""

# STDOUT_PNG == '\x1b[91m[!] test_no_icon_file.yaml:\x1b[0m key icon is not defined or is None.\n'\
# '\x1b[35m[!] pickle.pkl:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] vitest.svg:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] constants_pickle.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.ts:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.mts:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.cts:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] vitest.png:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] plist.plist:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] __pycache__:\x1b[0m file extension is not yaml.\n'\
# '\x1b[91m[!] test_empty_file.yaml:\x1b[0m yaml file is empty.\n'\
# '\x1b[91m[!] test_empty_file.yaml:\x1b[0m key icon is not defined or is None.\n'\
# '\x1b[35m[!] file_type_svg.svg:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] constants_yaml.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] constants_svg.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] vitest.tmPreferences:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.js:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] svg_unused_tags.svg:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] svg.svg:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] vitest@2x.png:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] vitest@3x.png:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] audio.pkl:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.workspace:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] preferences.tmPreferences:\x1b[0m file extension is not yaml.\n'\
# '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest.png\x1b[0m done.\n'\
# '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@2x.png\x1b[0m done.\n'\
# '\x1b[36m[!] yaml.yaml [vitest.svg]\x1b[0m -> \x1b[93mvitest@3x.png\x1b[0m done.\n'
# '\x1b[35m[!] constants_tmpreferences.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] JavaScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] constants_icons_syntaxes.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] constants_plist.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] tests_paths.py:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] TypeScript (Vitest).sublime-syntax:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.mjs:\x1b[0m file extension is not yaml.\n'\
# '\x1b[35m[!] Vitest.vitest.config.cjs:\x1b[0m file extension is not yaml.\n'\
