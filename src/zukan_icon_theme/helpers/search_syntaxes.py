import sublime

from .read_write_data import read_pickle_data
from ..utils.zukan_paths import (
    ZUKAN_ICONS_DATA_FILE,
    # ZUKAN_SYNTAXES_DATA_FILE,
)
from ruamel.yaml import YAML


class UserSyntax:
    def __init__(self, path, name, scope, hidden):
        self.path = path
        self.name = name
        self.scope = scope
        self.hidden = hidden


def visible_syntaxes_only() -> set:
    """
    Create a list of user ST installed syntaxes, visible only.

    Returns:
    syntaxes_list_visible (set) -- list of user ST installed syntaxes, excluded
    hidden syntaxes.
    """
    syntaxes_list_visible = set()
    all_syntaxes = sublime.list_syntaxes()
    for s in all_syntaxes:
        if s.hidden is False:
            # print(s.name, s.path)
            syntaxes_list_visible.add(s)
    return syntaxes_list_visible


def compare_scopes() -> list:
    """
    Compare scopes from user ST installed syntaxes and zukan icon syntaxes.

    Returns:
    list_scopes_to_remove (list) -- scopes list that are present in both, user ST
    installed syntaxes and zukan icon syntaxes.
    """
    list_scopes_to_remove = []
    zukan_icons_syntaxes = read_pickle_data(ZUKAN_ICONS_DATA_FILE)
    user_syntaxes = visible_syntaxes_only()
    for x in zukan_icons_syntaxes:
        if x.get('syntax') is not None:
            for s in x['syntax']:
                for y in user_syntaxes:
                    if s['scope'] == y.scope:
                        # print(s['scope'])
                        list_scopes_to_remove.append(s)
    return list_scopes_to_remove


def list_syntax_to_dump():
    """
    Print syntax that will be dumped. Used for testing only,
    """
    zukan_icons_syntaxes = read_pickle_data(ZUKAN_SYNTAXES_DATA_FILE)
    for x in zukan_icons_syntaxes:
        if x not in compare_scopes():
            print(x)


def replace_tabs(file_info: str) -> str:
    """
    Replace tabs for double spaces. Used by 'list_user_syntaxes_file_ext' for
    testing only.

    Parameters:
    file (str) -- info of data file.

    Returns:
    str -- text with tabs converted to double spaces if found.
    """
    return file_info.replace('\t', '  ')


def list_user_syntaxes_file_ext():
    """
    List file_extensions in sublime-syntaxes installed. Used for testing only.
    """
    user_file_extensions = []
    list_syntaxes = UserSyntax.visible_syntaxes_only()
    for s in list_syntaxes:
        # print('syntax name:' + s.name + '-> path:' + s.path + '-> scope:' + s.scope)
        syntax_content = replace_tabs(sublime.load_resource(s.path))
        # syntax_content = sublime.load_binary_resource(s.path)
        # print(syntax_content)
        # this is slow
        yaml = YAML(typ='rt')
        file_data = yaml.load(syntax_content)
        # There are sublime-syntaxes with no key 'file_extensions'.
        # Also, not all are sublime-syntaxes, there is/are tmLanguage.
        if 'file_extensions' in file_data:
            # print(file_data['file_extensions'])
            user_file_extensions.append(file_data['file_extensions'])
    return user_file_extensions


# https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
def flatten(xss):
    """
    Flast list of lists. Used for testing only.
    """
    return [x for xs in xss for x in xs]


# reloading python 3.3 plugin Zukan-Icon-Theme.main
# [['sty', 'cls'], ['cljs', 'cljc'], ['sql', 'ddl', 'dml'], ['css'], ['rd'], ['ruby.rail', 'rxml', 'builder', 'arb'], ['ts'], ['js', 'mjs', 'cjs', 'htc'], ['py', 'py3', 'pyw', 'pyi', 'pyx', 'pyx.in', 'pxd', 'pxd.in', 'pxi', 'pxi.in', 'rpy', 'cpy', 'gyp', 'gypi', 'vpy', 'smk', 'wscript', 'bazel', 'bzl'], ['tsx'], ['groovy', 'gvy', 'gradle'], ['gitconfig'], ['js.php'], ['vbs'], ['tsx'], ['diff', 'patch'], ['go'], ['eex'], ['adp'], ['d', 'di'], ['html.eex', 'html.leex'], ['erl', 'hrl', 'escript'], ['mll'], ['c', 'h'], ['md', 'mdown', 'mdwn', 'markdown', 'markdn'], ['tcl'], ['css.erb'], ['re'], ['pas', 'p', 'dpr'], ['css.php'], ['html', 'htm', 'shtml', 'xhtml'], [], ['js', 'jsx', 'es6', 'babel'], ['toml', 'tml', 'Cargo.lock', 'Gopkg.lock', 'Pipfile', 'poetry.lock'], ['lhs'], ['lisp', 'cl', 'clisp', 'l', 'mud', 'el', 'scm', 'ss', 'lsp', 'fasl', 'sld'], ['gohtml', 'go.html'], ['gitattributes'], ['mk', 'mak', 'make'], ['xsd', 'xsl', 'xslt'], ['tex', 'ltx'], ['yaml', 'yml', 'sublime-syntax'], ['rst', 'rest'], ['jsx'], ['sface'], ['mly'], ['dot', 'gv'], ['dtd', 'ent', 'mod'], ['heex'], ['java', 'bsh'], ['properties'], ['gomd', 'go.md', 'hugo'], ['ex.sql'], ['scala', 'sbt', 'sc'], ['bib'], ['clj', 'cljc', 'edn'], ['sass'], ['gocss', 'go.css'], ['jsp', 'jspf', 'jspx', 'jstl'], ['ex.eex', 'exs.eex'], ['matlab'], ['gojs', 'go.js'], ['asp', 'asa'], ['php', 'php3', 'php4', 'php5', 'php7', 'php8', 'phps', 'phpt', 'phtml'], ['R'], ['gitignore'], ['m', 'h'], ['mm', 'M', 'h'], ['sh', 'bash', 'bashrc', 'ash', 'zsh'], ['sql.erb', 'erbsql'], ['json', 'jsonc', 'sublime-build', 'sublime-color-scheme', 'sublime-commands', 'sublime-completions', 'sublime-keymap', 'sublime-macro', 'sublime-menu', 'sublime-mousemap', 'sublime-project', 'sublime-settings', 'sublime-theme', 'sublime-workspace', 'ipynb', 'gltf', 'avsc'], ['gitlog'], ['ex', 'exs'], ['applescript', 'script editor'], ['ml', 'mli'], ['xml', 'tld', 'dtml', 'rng', 'rss', 'opml', 'svg', 'xaml'], ['rb', 'rbi', 'rbx', 'rjs', 'rabl', 'rake', 'capfile', 'jbuilder', 'gemspec', 'podspec', 'irbrc', 'pryrc', 'prawn', 'thor'], ['hs', 'hs-boot', 'hsig'], ['jsx'], ['yaws'], ['textile'], ['cpp', 'cc', 'cp', 'cxx', 'c++', 'C', 'h', 'hh', 'hpp', 'hxx', 'h++', 'inl', 'ipp', 'ixx', 'cppm'], ['haml'], ['scss'], ['rails', 'rhtml', 'erb', 'html.erb'], ['bat', 'cmd'], ['js.erb'], ['js', 'mjs', 'cjs', 'htc'], ['lua'], ['as'], ['mailmap'], ['rs'], ['.git'], ['cs', 'csx'], ['pl', 'pc', 'pm', 'pmc', 'pod', 't'], ['CODEOWNERS'], ['cabal', 'cabal.project'], ['ts'], ['git-blame-ignore-revs']]
# Function time_listing, Time 11.73568606376648
# reloading python 3.3 plugin Zukan-Icon-Theme.main
# ['sty', 'cls', 'cljs', 'cljc', 'sql', 'ddl', 'dml', 'css', 'rd', 'ruby.rail', 'rxml', 'builder', 'arb', 'ts', 'js', 'mjs', 'cjs', 'htc', 'py', 'py3', 'pyw', 'pyi', 'pyx', 'pyx.in', 'pxd', 'pxd.in', 'pxi', 'pxi.in', 'rpy', 'cpy', 'gyp', 'gypi', 'vpy', 'smk', 'wscript', 'bazel', 'bzl', 'tsx', 'groovy', 'gvy', 'gradle', 'gitconfig', 'js.php', 'vbs', 'tsx', 'diff', 'patch', 'go', 'eex', 'adp', 'd', 'di', 'html.eex', 'html.leex', 'erl', 'hrl', 'escript', 'mll', 'c', 'h', 'md', 'mdown', 'mdwn', 'markdown', 'markdn', 'tcl', 'css.erb', 're', 'pas', 'p', 'dpr', 'css.php', 'html', 'htm', 'shtml', 'xhtml', 'js', 'jsx', 'es6', 'babel', 'toml', 'tml', 'Cargo.lock', 'Gopkg.lock', 'Pipfile', 'poetry.lock', 'lhs', 'lisp', 'cl', 'clisp', 'l', 'mud', 'el', 'scm', 'ss', 'lsp', 'fasl', 'sld', 'gohtml', 'go.html', 'gitattributes', 'mk', 'mak', 'make', 'xsd', 'xsl', 'xslt', 'tex', 'ltx', 'yaml', 'yml', 'sublime-syntax', 'rst', 'rest', 'jsx', 'sface', 'mly', 'dot', 'gv', 'dtd', 'ent', 'mod', 'heex', 'java', 'bsh', 'properties', 'gomd', 'go.md', 'hugo', 'ex.sql', 'scala', 'sbt', 'sc', 'bib', 'clj', 'cljc', 'edn', 'sass', 'gocss', 'go.css', 'jsp', 'jspf', 'jspx', 'jstl', 'ex.eex', 'exs.eex', 'matlab', 'gojs', 'go.js', 'asp', 'asa', 'php', 'php3', 'php4', 'php5', 'php7', 'php8', 'phps', 'phpt', 'phtml', 'R', 'gitignore', 'm', 'h', 'mm', 'M', 'h', 'sh', 'bash', 'bashrc', 'ash', 'zsh', 'sql.erb', 'erbsql', 'json', 'jsonc', 'sublime-build', 'sublime-color-scheme', 'sublime-commands', 'sublime-completions', 'sublime-keymap', 'sublime-macro', 'sublime-menu', 'sublime-mousemap', 'sublime-project', 'sublime-settings', 'sublime-theme', 'sublime-workspace', 'ipynb', 'gltf', 'avsc', 'gitlog', 'ex', 'exs', 'applescript', 'script editor', 'ml', 'mli', 'xml', 'tld', 'dtml', 'rng', 'rss', 'opml', 'svg', 'xaml', 'rb', 'rbi', 'rbx', 'rjs', 'rabl', 'rake', 'capfile', 'jbuilder', 'gemspec', 'podspec', 'irbrc', 'pryrc', 'prawn', 'thor', 'hs', 'hs-boot', 'hsig', 'jsx', 'yaws', 'textile', 'cpp', 'cc', 'cp', 'cxx', 'c++', 'C', 'h', 'hh', 'hpp', 'hxx', 'h++', 'inl', 'ipp', 'ixx', 'cppm', 'haml', 'scss', 'rails', 'rhtml', 'erb', 'html.erb', 'bat', 'cmd', 'js.erb', 'js', 'mjs', 'cjs', 'htc', 'lua', 'as', 'mailmap', 'rs', '.git', 'cs', 'csx', 'pl', 'pc', 'pm', 'pmc', 'pod', 't', 'CODEOWNERS', 'cabal', 'cabal.project', 'ts', 'git-blame-ignore-revs']
# Function time_listing, Time 11.709559917449951


# syntax name:TeX-> path:Packages/LaTeX/TeX.sublime-syntax-> scope:text.tex
# ['sty', 'cls']
# syntax name:ClojureScript-> path:Packages/Clojure/ClojureScript.sublime-syntax-> scope:source.clojure.clojurescript
# ['cljs', 'cljc']
# syntax name:SQL-> path:Packages/SQL/SQL.sublime-syntax-> scope:source.sql
# ['sql', 'ddl', 'dml']
# syntax name:CSS-> path:Packages/CSS/CSS.sublime-syntax-> scope:source.css
# ['css']
# syntax name:Rd (R Documentation)-> path:Packages/R/Rd (R Documentation).sublime-syntax-> scope:text.tex.latex.rd
# ['rd']
# syntax name:Ruby (Rails)-> path:Packages/Rails/Ruby (Rails).sublime-syntax-> scope:source.ruby.rails
# ['ruby.rail', 'rxml', 'builder', 'arb']
# syntax name:TS-> path:Packages/User/TS.sublime-syntax-> scope:source.ts
# ['ts']
# syntax name:Git Rebase Todo-> path:Packages/Git Formats/Git Rebase.sublime-syntax-> scope:text.git.rebase
# syntax name:JavaScript-> path:Packages/JavaScript/JavaScript.sublime-syntax-> scope:source.js
# ['js', 'mjs', 'cjs', 'htc']
# syntax name:Python-> path:Packages/Python/Python.sublime-syntax-> scope:source.python
# ['py', 'py3', 'pyw', 'pyi', 'pyx', 'pyx.in', 'pxd', 'pxd.in', 'pxi', 'pxi.in', 'rpy', 'cpy', 'gyp', 'gypi', 'vpy', 'smk', 'wscript', 'bazel', 'bzl']
# syntax name:TSX-> path:Packages/JavaScript/TSX.sublime-syntax-> scope:source.tsx
# ['tsx']
# syntax name:Groovy-> path:Packages/Groovy/Groovy.sublime-syntax-> scope:source.groovy
# ['groovy', 'gvy', 'gradle']
# syntax name:Git Config-> path:Packages/Git Formats/Git Config.sublime-syntax-> scope:text.git.config
# ['gitconfig']
# syntax name:JavaScript (PHP)-> path:Packages/PHP/JavaScript (PHP).sublime-syntax-> scope:source.js.php
# ['js.php']
# syntax name:ASP-> path:Packages/ASP/ASP.sublime-syntax-> scope:source.asp
# ['vbs']
# syntax name:TSX2-> path:Packages/User/TSX2.sublime-syntax-> scope:source.tsx
# ['tsx']
# syntax name:Git Commit Message-> path:Packages/Git Formats/Git Commit Message.sublime-syntax-> scope:text.git.commit-message
# syntax name:Diff-> path:Packages/Diff/Diff.sublime-syntax-> scope:source.diff
# ['diff', 'patch']
# syntax name:Go-> path:Packages/Go/Go.sublime-syntax-> scope:source.go
# ['go']
# syntax name:EEx-> path:Packages/ElixirSyntax/syntaxes/EEx.sublime-syntax-> scope:text.eex
# ['eex']
# syntax name:HTML (Tcl)-> path:Packages/TCL/HTML (Tcl).sublime-syntax-> scope:text.html.tcl
# ['adp']
# syntax name:D-> path:Packages/D/D.sublime-syntax-> scope:source.d
# ['d', 'di']
# syntax name:Plain Text-> path:Packages/Text/Plain text.tmLanguage-> scope:text.plain
# syntax name:HTML (EEx)-> path:Packages/ElixirSyntax/syntaxes/HTML (EEx).sublime-syntax-> scope:text.html.eex
# ['html.eex', 'html.leex']
# syntax name:Erlang-> path:Packages/Erlang/Erlang.sublime-syntax-> scope:source.erlang
# ['erl', 'hrl', 'escript']
# syntax name:OCamllex-> path:Packages/OCaml/OCamllex.sublime-syntax-> scope:source.ocamllex
# ['mll']
# syntax name:C-> path:Packages/C++/C.sublime-syntax-> scope:source.c
# ['c', 'h']
# syntax name:Markdown-> path:Packages/Markdown/Markdown.sublime-syntax-> scope:text.html.markdown
# ['md', 'mdown', 'mdwn', 'markdown', 'markdn']
# syntax name:Tcl-> path:Packages/TCL/Tcl.sublime-syntax-> scope:source.tcl
# ['tcl']
# syntax name:CSS (Rails)-> path:Packages/Rails/CSS (Rails).sublime-syntax-> scope:source.css.rails
# ['css.erb']
# syntax name:Regular Expression-> path:Packages/Regular Expressions/RegExp.sublime-syntax-> scope:source.regexp
# ['re']
# syntax name:Pascal-> path:Packages/Pascal/Pascal.sublime-syntax-> scope:source.pascal
# ['pas', 'p', 'dpr']
# syntax name:CSS (PHP)-> path:Packages/PHP/CSS (PHP).sublime-syntax-> scope:source.css.php
# ['css.php']
# syntax name:HTML-> path:Packages/HTML/HTML.sublime-syntax-> scope:text.html.basic
# ['html', 'htm', 'shtml', 'xhtml']
# syntax name:camlp4-> path:Packages/OCaml/camlp4.sublime-syntax-> scope:source.camlp4.ocaml
# syntax name:R Console-> path:Packages/R/R Console.sublime-syntax-> scope:source.r-console
# []
# syntax name:JavaScript (Babel)-> path:Packages/Babel/JavaScript (Babel).sublime-syntax-> scope:source.js
# ['js', 'jsx', 'es6', 'babel']
# syntax name:TOML-> path:Packages/TOML/TOML.sublime-syntax-> scope:source.toml
# ['toml', 'tml', 'Cargo.lock', 'Gopkg.lock', 'Pipfile', 'poetry.lock']
# syntax name:Literate Haskell-> path:Packages/Haskell/Literate Haskell.sublime-syntax-> scope:text.tex.latex.haskell
# ['lhs']
# syntax name:Lisp-> path:Packages/Lisp/Lisp.sublime-syntax-> scope:source.lisp
# ['lisp', 'cl', 'clisp', 'l', 'mud', 'el', 'scm', 'ss', 'lsp', 'fasl', 'sld']
# syntax name:HTML (Go)-> path:Packages/Go/HTML (Go).sublime-syntax-> scope:text.html.go
# ['gohtml', 'go.html']
# syntax name:Git Attributes-> path:Packages/Git Formats/Git Attributes.sublime-syntax-> scope:text.git.attributes
# ['gitattributes']
# syntax name:Makefile-> path:Packages/Makefile/Makefile.sublime-syntax-> scope:source.makefile
# ['mk', 'mak', 'make']
# syntax name:XSL-> path:Packages/XML/XSL.sublime-syntax-> scope:text.xml.xsl
# ['xsd', 'xsl', 'xslt']
# syntax name:LaTeX-> path:Packages/LaTeX/LaTeX.sublime-syntax-> scope:text.tex.latex
# ['tex', 'ltx']
# syntax name:YAML-> path:Packages/YAML/YAML.sublime-syntax-> scope:source.yaml
# ['yaml', 'yml', 'sublime-syntax']
# syntax name:reStructuredText-> path:Packages/RestructuredText/reStructuredText.sublime-syntax-> scope:text.restructuredtext
# ['rst', 'rest']
# syntax name:JSX-> path:Packages/JavaScript/JSX.sublime-syntax-> scope:source.jsx
# ['jsx']
# syntax name:HTML (Surface)-> path:Packages/ElixirSyntax/syntaxes/HTML (Surface).sublime-syntax-> scope:text.html.surface
# ['sface']
# syntax name:OCamlyacc-> path:Packages/OCaml/OCamlyacc.sublime-syntax-> scope:source.ocamlyacc
# ['mly']
# syntax name:Graphviz (DOT)-> path:Packages/Graphviz/DOT.sublime-syntax-> scope:source.dot
# ['dot', 'gv']
# syntax name:DTD-> path:Packages/XML/DTD.sublime-syntax-> scope:text.xml.dtd
# ['dtd', 'ent', 'mod']
# syntax name:HTML (HEEx)-> path:Packages/ElixirSyntax/syntaxes/HTML (HEEx).sublime-syntax-> scope:text.html.heex
# ['heex']
# syntax name:Java-> path:Packages/Java/Java.sublime-syntax-> scope:source.java
# ['java', 'bsh']
# syntax name:Java Properties-> path:Packages/Java/JavaProperties.sublime-syntax-> scope:source.java-props
# ['properties']
# syntax name:Markdown (Go)-> path:Packages/Go/Markdown (Go).sublime-syntax-> scope:text.html.markdown.go
# ['gomd', 'go.md', 'hugo']
# syntax name:SQL (Elixir)-> path:Packages/ElixirSyntax/syntaxes/SQL (Elixir).sublime-syntax-> scope:source.ex.sql
# ['ex.sql']
# syntax name:Scala-> path:Packages/Scala/Scala.sublime-syntax-> scope:source.scala
# ['scala', 'sbt', 'sc']
# syntax name:BibTeX-> path:Packages/LaTeX/Bibtex.sublime-syntax-> scope:text.bibtex
# ['bib']
# syntax name:LaTeX Log-> path:Packages/LaTeX/LaTeX Log.sublime-syntax-> scope:text.log.latex
# syntax name:Clojure-> path:Packages/Clojure/Clojure.sublime-syntax-> scope:source.clojure
# ['clj', 'cljc', 'edn']
# syntax name:Sass-> path:Packages/Sass/Syntaxes/Sass.sublime-syntax-> scope:source.sass
# ['sass']
# syntax name:CSS (Go)-> path:Packages/Go/CSS (Go).sublime-syntax-> scope:source.css.go
# ['gocss', 'go.css']
# syntax name:HTML (JSP)-> path:Packages/Java/HTML (JSP).sublime-syntax-> scope:text.html.jsp
# ['jsp', 'jspf', 'jspx', 'jstl']
# syntax name:Elixir (EEx)-> path:Packages/ElixirSyntax/syntaxes/Elixir (EEx).sublime-syntax-> scope:source.elixir.eex
# ['ex.eex', 'exs.eex']
# syntax name:MATLAB-> path:Packages/Matlab/Matlab.sublime-syntax-> scope:source.matlab
# ['matlab']
# syntax name:JavaScript (Go)-> path:Packages/Go/JavaScript (Go).sublime-syntax-> scope:source.js.go
# ['gojs', 'go.js']
# syntax name:NAnt Build File-> path:Packages/C#/Build.sublime-syntax-> scope:source.nant-build
# syntax name:HTML (ASP)-> path:Packages/ASP/HTML (ASP).sublime-syntax-> scope:text.html.asp
# ['asp', 'asa']
# syntax name:PHP-> path:Packages/PHP/PHP.sublime-syntax-> scope:embedding.php
# ['php', 'php3', 'php4', 'php5', 'php7', 'php8', 'phps', 'phpt', 'phtml']
# syntax name:R-> path:Packages/R/R.sublime-syntax-> scope:source.r
# ['R']
# syntax name:Git Ignore-> path:Packages/Git Formats/Git Ignore.sublime-syntax-> scope:text.git.ignore
# ['gitignore']
# syntax name:Objective-C-> path:Packages/Objective-C/Objective-C.sublime-syntax-> scope:source.objc
# ['m', 'h']
# syntax name:Objective-C++-> path:Packages/Objective-C/Objective-C++.sublime-syntax-> scope:source.objc++
# ['mm', 'M', 'h']
# syntax name:Git Commit-> path:Packages/Git Formats/Git Commit.sublime-syntax-> scope:text.git.commit
# syntax name:Bash-> path:Packages/ShellScript/Bash.sublime-syntax-> scope:source.shell.bash
# ['sh', 'bash', 'bashrc', 'ash', 'zsh']
# syntax name:SQL (Rails)-> path:Packages/Rails/SQL (Rails).sublime-syntax-> scope:source.sql.rails
# ['sql.erb', 'erbsql']
# syntax name:JSON-> path:Packages/JSON/JSON.sublime-syntax-> scope:source.json
# ['json', 'jsonc', 'sublime-build', 'sublime-color-scheme', 'sublime-commands', 'sublime-completions', 'sublime-keymap', 'sublime-macro', 'sublime-menu', 'sublime-mousemap', 'sublime-project', 'sublime-settings', 'sublime-theme', 'sublime-workspace', 'ipynb', 'gltf', 'avsc']
# syntax name:Git Log-> path:Packages/Git Formats/Git Log.sublime-syntax-> scope:text.git.log
# ['gitlog']
# syntax name:Elixir-> path:Packages/ElixirSyntax/syntaxes/Elixir.sublime-syntax-> scope:source.elixir
# ['ex', 'exs']
# syntax name:AppleScript-> path:Packages/AppleScript/AppleScript.sublime-syntax-> scope:source.applescript
# ['applescript', 'script editor']
# syntax name:OCaml-> path:Packages/OCaml/OCaml.sublime-syntax-> scope:source.ocaml
# ['ml', 'mli']
# syntax name:XML-> path:Packages/XML/XML.sublime-syntax-> scope:text.xml
# ['xml', 'tld', 'dtml', 'rng', 'rss', 'opml', 'svg', 'xaml']
# syntax name:Ruby-> path:Packages/Ruby/Ruby.sublime-syntax-> scope:source.ruby
# ['rb', 'rbi', 'rbx', 'rjs', 'rabl', 'rake', 'capfile', 'jbuilder', 'gemspec', 'podspec', 'irbrc', 'pryrc', 'prawn', 'thor']
# syntax name:Haskell-> path:Packages/Haskell/Haskell.sublime-syntax-> scope:source.haskell
# ['hs', 'hs-boot', 'hsig']
# syntax name:JSX2-> path:Packages/User/JSX2.sublime-syntax-> scope:source.jsx
# ['jsx']
# syntax name:HTML (Erlang)-> path:Packages/Erlang/HTML (Erlang).sublime-syntax-> scope:text.html.erlang
# ['yaws']
# syntax name:Textile-> path:Packages/Textile/Textile.sublime-syntax-> scope:text.html.textile
# ['textile']
# syntax name:C++-> path:Packages/C++/C++.sublime-syntax-> scope:source.c++
# ['cpp', 'cc', 'cp', 'cxx', 'c++', 'C', 'h', 'hh', 'hpp', 'hxx', 'h++', 'inl', 'ipp', 'ixx', 'cppm']
# syntax name:HAML-> path:Packages/Rails/HAML.sublime-syntax-> scope:text.haml
# ['haml']
# syntax name:SCSS-> path:Packages/Sass/Syntaxes/SCSS.sublime-syntax-> scope:source.scss
# ['scss']
# syntax name:HTML (Rails)-> path:Packages/Rails/HTML (Rails).sublime-syntax-> scope:text.html.rails
# ['rails', 'rhtml', 'erb', 'html.erb']
# syntax name:Batch File-> path:Packages/Batch File/Batch File.sublime-syntax-> scope:source.dosbatch
# ['bat', 'cmd']
# syntax name:JavaScript (Rails)-> path:Packages/Rails/JavaScript (Rails).sublime-syntax-> scope:source.js.rails
# ['js.erb']
# syntax name:JS-> path:Packages/User/JS.sublime-syntax-> scope:source.js
# ['js', 'mjs', 'cjs', 'htc']
# syntax name:Lua-> path:Packages/Lua/Lua.sublime-syntax-> scope:source.lua
# ['lua']
# syntax name:ActionScript-> path:Packages/ActionScript/ActionScript.sublime-syntax-> scope:source.actionscript.2
# ['as']
# syntax name:Git Mailmap-> path:Packages/Git Formats/Git Mailmap.sublime-syntax-> scope:text.git.mailmap
# ['mailmap']
# syntax name:Rust-> path:Packages/Rust/Rust.sublime-syntax-> scope:source.rust
# ['rs']
# syntax name:Git Link-> path:Packages/Git Formats/Git Link.sublime-syntax-> scope:text.git.link
# ['.git']
# syntax name:MultiMarkdown-> path:Packages/Markdown/MultiMarkdown.sublime-syntax-> scope:text.html.markdown.multimarkdown
# syntax name:C#-> path:Packages/C#/C#.sublime-syntax-> scope:source.cs
# ['cs', 'csx']
# syntax name:Perl-> path:Packages/Perl/Perl.sublime-syntax-> scope:source.perl
# ['pl', 'pc', 'pm', 'pmc', 'pod', 't']
# syntax name:Git Code Owners-> path:Packages/Git Formats/Git Code Owners.sublime-syntax-> scope:text.git.codeowners
# ['CODEOWNERS']
# syntax name:Cabal-> path:Packages/Haskell/Cabal.sublime-syntax-> scope:source.cabal
# ['cabal', 'cabal.project']
# syntax name:TypeScript-> path:Packages/JavaScript/TypeScript.sublime-syntax-> scope:source.ts
# ['ts']
# syntax name:Git Blame Ignore Revisions-> path:Packages/Git Formats/Git Blame Ignore Revisions.sublime-syntax-> scope:text.git.blame.ignorerevs
# ['git-blame-ignore-revs']
