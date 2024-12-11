# Initial list to try solve conflicts of same file extensions used by differents
# languages, libraries or packages.
# If leave two same file extensions in differents scopes, ST will use the last
# one in alphabet order.
# Example: fs file extension used by F# and OpenGL. OpenGL will prevail.
SCOPES_FILE_EXTENSIONS = [
    {'scope': 'source.arduino', 'file_extensions': ['ino', 'pde']},  # arduino.yaml
    {'scope': 'source.asp', 'file_extensions': ['vbs']},  # asp.yaml
    {'scope': 'source.bazel', 'file_extensions': ['bazel', 'bzl']},  # bazel.yaml
    {'scope': 'source.c++', 'file_extensions': ['h']},  # cuda.yaml
    {'scope': 'source.css', 'file_extensions': ['css']},  # django.yaml
    {'scope': 'source.css.postcss.sugarss', 'file_extensions': ['sss']},  # postcss.yaml
    {
        'scope': 'source.clojure.clojurescript',
        'file_extensions': ['cljc'],
    },  # clojure.yaml
    {'scope': 'source.clojure', 'file_extensions': ['edn']},  # clojure.yaml
    {
        'scope': 'source.cmake',
        'file_extensions': ['CMakeLists.txt'],
    },  # cmake.yaml
    {'scope': 'source.elixir', 'file_extensions': ['config.exs']},  # phoenix.yaml
    {'scope': 'source.env', 'file_extensions': ['.env']},  # fastapi.yaml
    {
        'scope': 'source.fortran',
        'file_extensions': ['f90', 'F90', 'f95', 'F95', 'f03', 'F03', 'f08', 'F08'],
    },  # fortran.yaml
    {'scope': 'source.glsl', 'file_extensions': ['fs']},  # fsharp.yaml
    {'scope': 'source.ini.python', 'file_extensions': ['setup.cfg']},
    {'scope': 'source.js', 'file_extensions': ['js']},  # applescript.ymal
    {
        'scope': 'source.pubspec',
        'file_extensions': ['pubspec.lock', 'pubspec.yaml'],
    },  # flutter.ymal
    {'scope': 'source.python.fastapi', 'file_extensions': ['config.py']},
    {'scope': 'source.ruby', 'file_extensions': ['rb']},  # rspec.yaml
    {'scope': 'source.shader', 'file_extensions': ['cginc', 'shader']},  # unity.yaml
    {'scope': 'source.tex', 'file_extensions': ['cls']},  # tex.yaml
    {'scope': 'source.toml', 'file_extensions': ['config.toml']},
    {'scope': 'source.toml.python', 'file_extensions': ['pyproject.toml']},
    # poetry, pip, tox, pdm
    {'scope': 'source.ts', 'file_extensions': ['app.config.ts']},
    # angular.yaml, nuxt.yaml, solidjs.yaml
    {'scope': 'source.yaml', 'file_extensions': ['config.yaml']},
    {'scope': 'text.ejs.percentsign', 'file_extensions': ['ejs']},  # ejs.yaml
    {'scope': 'text.gherkin.feature', 'file_extensions': ['feature']},  # behat.yaml
    {'scope': 'text.html.basic', 'file_extensions': ['html']},  # django.yaml
    {'scope': 'text.html.markdown', 'file_extensions': ['md']},  # mdsvex.yaml
    {'scope': 'text.plain', 'file_extensions': ['BUILD', 'WORKSPACE']},  # bazel.yaml
    {'scope': 'text.plain.debug', 'file_extensions': ['pdb']},  # wwpdb.yaml
    {'scope': 'text.plain.pip', 'file_extensions': ['requirements.txt']},  # uv.yaml
    {'scope': 'text.xml', 'file_extensions': ['xml']},  # django.yaml
    {
        'scope': 'text.xml.sublime.snippet',
        'file_extensions': ['Comments.tmPreferences'],
    },  # sublime.yaml
]

# Occurred cases
# - AppleScript: package AppleScript Extensions using js file extension.
# - Arduino: same 2 files, different scope, 2 files in syntax.
# - ASP: package VBScript has 2 conflicts ext. vbs and cls.
# - Bazel: used BUILD and WORKSPACE. Package Starlark uses bazel and bzl
# - Behat: it is Cucumber for PHP. And use feature as file extension too.
# - Clojure: Clojure and ClojureScript use cljc.
# - CMake: same file, different scope, only 1 file in syntax CMakeEditor.
# - Cuda: use h. C and C++ also used but, if not disabled or deleted, it does not
# have an icon syntax. Since they are ST packages. And C++ prevail.
# - Dart: pubspec is present in Dart and Flutter projects.
# - Django: package Django Syntax uses css, html and xml.
# - Fortran: package Fortran and Modern-Fortran use same file-extensions.
# - F#: fs extension is used by OpenGL.
# - PostCSS: Syntax Highlighting for PostCSS and Syntax Highlighting for SSS SugarSS use sss.
# - Sublime: Package Plist highlight tmPreferences, also ST XML
# - Unity: Package Unity Shader and Unity3D Shader Highlighter and Snippets same extensions.

# Config files
# .env: fastapi
# app.config.ts: ts, angular, nuxt, solid
# ci.yml: github
# config.exs: phoenix
# config.py: fastapi
# config.toml: pdm, tidb
# config.xml: clickhouse
# config.yml: circleci
# config.yaml: clickhouse, openfga
# dependencies.json: packagecontrol
# Manifest.tom: pkgjl
# messages.json: sublime
# model.conf: casbin
# policy.csv: casbin
# Project.toml: pkgjl
# pyproject.toml: python, hatch, pdm, pip, poetry, setuptools, tox
# requirements.txt: pip, uv
# setup.cfg: python, setuptools, tox
# unittestings.json: sublime
