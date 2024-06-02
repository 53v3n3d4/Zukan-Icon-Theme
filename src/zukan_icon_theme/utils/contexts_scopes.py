CONTEXTS_MAIN = {'contexts': {'main': []}}

# Scopes used in 'contexts', sublime-syntax files. In case, syntax not installed
# or disable, this needs to be removed. Or user receive an error message in console,
# about syntax not found.
# Contexts main are important for highlighting while also keep icon showing.
CONTEXTS_SCOPES = [
    {'scope': 'source.css', 'startsWith': 'CSS ('},
    {'scope': 'source.groovy', 'startsWith': 'Groovy ('},
    {'scope': 'source.ini', 'startsWith': 'INI ('},
    {'scope': 'source.js', 'startsWith': 'JavaScript ('},
    {'scope': 'source.json', 'startsWith': 'JSON ('},
    {'scope': 'source.jsx', 'startsWith': 'JSX ('},
    {'scope': 'source.makefile', 'startsWith': 'Makefile ('},
    {'scope': 'source.python', 'startsWith': 'Python ('},
    {'scope': 'source.ruby', 'startsWith': 'Ruby ('},
    {'scope': 'source.scala', 'startsWith': 'Scala ('},
    {'scope': 'source.shell', 'startsWith': 'Shell ('},
    {'scope': 'source.toml', 'startsWith': 'TOML ('},
    {'scope': 'source.ts', 'startsWith': 'TypeScript ('},
    {'scope': 'source.tsx', 'startsWith': 'TSX ('},
    {'scope': 'source.webidl', 'startsWith': 'IDL ('},
    {'scope': 'source.yaml', 'startsWith': 'YAML ('},
    {'scope': 'text.bibtex', 'startsWith': 'BibTeX ('},
    {'scope': 'text.git.ignore', 'startsWith': 'Git ('},
    {'scope': 'text.html.basic', 'startsWith': 'HTML ('},
    {'scope': 'text.html.markdown', 'startsWith': 'Markdown ('},
    # {'scope': 'text.plain', 'startsWith': 'Plain Text ('},
    {'scope': 'text.xml', 'startsWith': 'XML ('},
    # Specific file
    {'scope': 'source.clojure', 'startsWith': 'Babashka'},
    {'scope': 'source.clojure', 'startsWith': 'ClojureDart'},
    {'scope': 'source.clojure', 'startsWith': 'ClojureScript'},
    {'scope': 'source.css', 'startsWith': 'Less'},
    {'scope': 'source.css', 'startsWith': 'SCSS'},
    {'scope': 'source.js', 'startsWith': 'UnitTest (JavaScript)'},
    {'scope': 'source.jsx', 'startsWith': 'UnitTest (JSX)'},
    {'scope': 'source.tsx', 'startsWith': 'UnitTest (TSX)'},
    {'scope': 'source.ts', 'startsWith': 'UnitTest (TypeScript)'},
    {'scope': 'text.html.basic', 'startsWith': 'XML (SVG)'},
    {'scope': 'text.tex.latex', 'startsWith': 'Literate Haskell'},
]