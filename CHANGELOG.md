# Changelog

## [0.4.9] - 2025

### Icons, syntaxes and preferences 👽
- Add icon-theme: Fluent, Just, prefix.dev
- Change syntax: License, OpenFGA

### Plugin 🕹️
- Change icons_themes
- Fix issue with partial paths being replaced from `/` to `\` on Windows by removing `os.path.join`
- Fix user customized theme not being handled by `get_sidebar_background`
- Add `cache_theme_info` and `cache_theme_info_lifespan` settings

## [0.4.8] - 2025-01-29

### Plugin 🕹️
- Undo removal constant from `get_sidebar_bgcolor`
- Removal constant from `find_attributes_hidden_file`

## [0.4.7] - 2025-01-29

### Plugin 🕹️
- Fix compatibility issue with Zukan-icons-theme v0.4.5 and v0.4.6 (#1)

## [0.4.6] - 2025-01-26

### Icons, syntaxes and preferences 👽
- Add icon-theme: Zizmor
- Change syntax: Sublime

### Plugin 🕹️
- Change icons_preferences, improve build time
- Fix logger TypeError after enabling from `ignored_packages`, avoiding need to restart Sublime Text
- Fix listener and add_on_change not starting after enabling via '.sublime-package' during upgrade
- Fix TypeError, NoneType, caused by failing to load settings when enabling from `ignored_packages`, if using '.sublime-package'

## [0.4.5] - 2025-01-22

### Icons, syntaxes and preferences 👽
- Add icon-theme: Scheme, GBIF
- Add icon option: CSS
- Add syntax: Cedar
- Change icon: CSS
- Change syntax: Applescript, Eleventy, R, Sublime

### Plugin 🕹️
- Fix install theme command, creating ignored_theme
- Fix install syntax command, creating syntax for ignored_icon
- Fix install preference command, creating preference for ignored_icon
- Change syntax, icons_syntaxes and read_write_data, improve build time
- Remove plugin `ruamel-yaml` dependency. This version no longer requires the library
- Add is_enabled for Commands, when InputHandler list_items is None

## [0.4.4] - 2025-01-11

### Plugin 🕹️
- Fix missing argument get_list_icons_syntaxes
- Fix no attribute themes_path

## [0.4.3] - 2025-01-11
- Change some outline light icons to darker tone

### Icons, syntaxes and preferences 👽
- Add icon-theme: Black
- Add icon option: Binary, Source, Text
- Change icon: Audio, Binary, CAD, Cert. Authentication, Code of Conduct, Citation, Debug, Default, Diff, Favicon, Font, Image, License, Log, Markup, Plist, README, Settings, Shell, Source, SSH, SystemVerilog, Text, Video
- Change sublime-syntax: License, Rebar3

### Plugin 🕹️
- Change SchemeThemeListener, improve handle icon dark/light
- Rename theme_dark_light -> color_dark_light
- Add zukan_listener_enabled setting
- Add zukan_reporter
- Rename folder commands -> core
- Rename settings -> zukan_pref_settings
- Merge folder events -> core
- Move move_folders to helpers
- Move clean_comments to helpers
- Change search_syntax and edit_file_extension, improve build time
- Fix error upgrade_zukan_files and multiple rebuild_icon_files calls when upgrading through Package Control
- Add EventBus for upgrade_zukan_files and rebuild_icon_files.

## [0.4.2] - 2024-12-19

### Plugin 🕹️
- Fix package_size not working for file
- Add delete_unused
- Fix error when Preferences 'theme' is set to 'auto'
- Add system_theme: Linux, macOS and Windows
- Rename icon_dark_light -> theme_dark_light

## [0.4.1] - 2024-12-15

### Plugin 🕹️
- Undo extract_remove_folder -> extract_folder, 'ignored_packaged' delete zukan folder in Packages.
- Fix error new install sublime-package not entering new_install_pkg_control

## [0.4.0] - 2024-12-15

### Icons, syntaxes and preferences 👽
- Add icon-theme: Alire, Bicep, Cedar, ClickHouse, Fly.io, Hatch, MDsveX, Oxc, Rolldown
- Add sublime-syntax: Ada, Angular, Erlang, OpenFGA, Rebar3, Sass, Sublime, TailwindCSS
- Add icon option: Rust
- Add icon dark and light: Ada, Alire, AppleScript, Archive, Arrow, Audio, Batchfile, BibTeX, Binary, CAD, Cert, Cert-1, CircleCI, Cirrus, Citation, ClickHouse, Codacy, Code of Conduct, Crowdin, Crystal, Cypress, Debug, Default, Diff, DirectX, DUB, EJS, Erlang.mk, Favicon, Font,GitBook, Groovy, Image, Java, Jinja, Julia, Lerna, License, Log, Makefile, Markdown, Markup, Maven, mdBook, MkDocs, Mocha, MySQL, Nant, NuGet, Nx, OpenGL, OpenWRT, Parquet, Perl, PHPUnit, Pipenv, Plist, PostCSS, Pyre, README, Regular Expression, reStructuredText, Rust, Sentry, Settings, Shell, Solidity, Source, SQLAlchemy, SSH, Stylelint, SystemVerilog, Tex, Text, Toit, TOML, Video, Yaml
- Change icon: Docker, EJS, Less, Log, MDX
- Change sublime-syntax: Cassandra, Conda, EdgeDB, MySQL, PLSQL, pnpm, PostgreSQL, Redis, SQL, SQLAlchemy, SQLite, Sublime, TiDB, uv, Vue, Yugabyte, Zukan
- Rename sublime-syntax: Vue
- Remove icon-theme: SCSS

### Build 🛠️
- Change icons
- Change concat_svgs

### Plugin 🕹️
- Add install size to get_user_zukan_preferences (Debug)
- Add tag `database`
- Add prefer_icon setting
- Change get_user_theme
- Remove `add_on_change` and `clear_on_change` for User Preferences
- Add SchemeThemeListener event listener
- Rename commands and command_settings, add 'Command' word
- Change extract_folder -> extract_remove_folder
- Fix not copying icons and icons_data when upgrading sublime-package
- Add icon_dark_light
- Add auto_prefer_icon setting

## [0.3.4] - 2024-10-22
- Fix update version in settings

## [0.3.3] - 2024-10-22

### Icons, syntaxes and preferences 👽
- Add icon-theme: Airflow, Arrow, Casbin, Debug, EJS, Lunaria, Open Policy Agent, OpenFGA, Parquet, Protein Data Bank, Templ, TiDB, SolidJS, SSH
- Add icon option: Cert
- Add sublime-syntax: Angular, Cert, Clojure, JS, Python
- Change icon: Deno, Renovate
- Change sublime-syntax: Nuxt, Sublime Text
- Rename sublime-syntax file name: Cert

### Build 🛠️
- Update clean_svg with new common id 'Path_'

## [0.3.2] - 2024-10-02

### Icons, syntaxes and preferences 👽
- Add icon-theme: CircleCI, Copier, FastAPI, Package Control, Phoenix Framework, Podman, Setuptools, SQLAlchemy, Travis CI
- Add sublime-syntax: Cargo, GitHub, JS, Python, Rust
- Change icon: Audio, GitHub Dependabot
- Change sublime-syntax: GitHub Dependabot, SQLite, Sublime Text

### Build 🛠️
- Fix save primary icons PNGs in folder 'primary_icons'
- Remove zukan_syntaxes and zukan_preferences

### Plugin 🕹️
- Fix auto upgrade below 0.2.2 to ^0.3.1
- Add annotation to 'reset_icon' and 'reset_file_extension' lists
- Fix warning PNGs not found for file_type_image-1

## [0.3.1] - 2024-07-23

### Icons, syntaxes and preferences 👽
- Add icon-theme: CSpell, DirectX, Dune, EdgeDB, Fantomas, FSharpLint, OCamlPRO, opam, Paket, Pascal, Pip, Pkg.jl, Web IDL, XMake
- Add icon option: Angular, C#, Composer, Go, DirectX, Image, LLVM, Node.js, PHP, Python, Ruff, Rust, Sublime Text
- Add sublime-syntax: NAnt
- Change icon: FlatBuffers, Image, Video
- Change sublime-syntax: CUDA, Dart, Flutter, Lavarel, PDM, Poetry, Python, Smarty, tox, uv

### Plugin 🕹️
- Add change_icon setting
- Add change_icon_file_extension setting
- Remove command delete_preferences, delete_syntaxes, delete_themes, install_themes, rebuild_preferences, rebuild_syntaxes
- Add commands_settings
- Add create_custom_icon setting
- Add auto_rebuild_icon setting
- Setting file `zukan-version` depreciated in favor of `zukan_current_settings` 

## [0.3.0] - 2024-07-09

### Icons, syntaxes and preferences 👽
- Change syntax: AppleScript, Sublime LSP, Terraform
- Delete tag: Text

### Build 🛠️
- Add zukan_icons

### Plugin 🕹️
- Add ignored_icon setting
- Fix error creating current theme when delete_icon_themes

## [0.2.2] - 2024-07-07
- Change icon support rectangle round corner.

### Icons, syntaxes and preferences 👽
- Add icon-theme: Checkly, GCC, LLVM, Puppeteer, OpenWrt, Redwood, Sublime LSP, SublimeLinter
- Change icon: C#, Diff, YAML
- Rename sublime-syntax file name: Bazel, Makefile

### Plugin 🕹️
- Add ignored_theme setting

## [0.2.1] - 2024-06-30
- Fix old version in sublime-settings

## [0.2.0] - 2024-06-30
- Rename project to Zukan Icon Theme
- Rename folder aliases -> icons_syntaxes
- Rename files icons PNGs, SVGs, sublime-syntaxes and tmPreferences
- Add python setup: poetry, pytest, ruff
- Rename folder preferences -> icons_preferences

### Icons, syntaxes and preferences 👽
- Add icon-theme: ActionScript, Ada, Ansible, AppleScript, AppVeyor, archive, AsciiDoc, ASP, Astro, Avro, Azure, Babashka, Batch File, Bazel, Behat, BibTeX, Biome, Bitbucket, Cabal, Caddyserver, Cairo, Cap'n Proto, Cargo, Cassandra, Cert, Cirrus, Clojure, ClojureDart, ClojureScript, Codacy, commitlint, Composer, Conan, Conda, Crowdin, Crystal, Cucumber, CUDA, Cypress, D, Datadog, Deno, Dependabot, Dart, Diff, Dioxus, Django, Docusaurus, Drone, DUB, EditorConfig, Eleventy, Erlang.mk, esbuild, F#, Figma, Firebase, Fish, Flask, Flow, Flutter, Font, Fortran, GitBook, git-cliff, GitHub, GitLab, Gitpod, Gleam, glTF, GolangCI-Lint, Gradle, Graphviz (DOT), Groovy, Gulp, Haml, Handlebars, Haskell, Heft, Hex, Hugo, isort, Istanbul, Jasmine, Jenkins, Jinja, Julia, JUnit, Jupyter, Knip, Kong, LaTeX, Lavarel, Lerna, Liquid, Lisp, MATLAB, Maven, mdBook, Mergify, Mermaid, Meson, Mill, MkDocs, Mocha, Modern Web, mypy, MySQL, NAnt, Nest, Nim, Nitro, Nix, NSIS, NuGet, NumPy, Nunjucks, Nushell, Nuxt, Nx, OCaml, PDM, Perl, PHP CS Fixer, PHPStan, PHPUnit, Pine, Pipenv, Playwright, Plist, PLSQL, PostCSS, PostgreSQL, pre-commit, Prisma, Pug, Pylint, Pyre, Pyright, Qt, Quokka, R, Read the Docs, Rebar3, Redis, Regular Expression, Renovate, reStructuredText, Rspec, RuboCop, Rush, RVM, sbt, Scala, Scala Steward, Scalafix, Scalameta, Sentry, Serverless, Smarty, Snapcraft, Snyk, Solidity, SQLite, Stylelint, SVGO, Swagger, Symfony, SystemVerilog, Tailwind CSS, Tauri, Tcl, TeX, Textile, Terraform, tmux, Toit, tox, Twig, Typst, uv, Vercel, Vyper, Wallaby, Yaws, Yugabyte, Zig
- Add sublime-syntax: C++, C, Citation, CMake, C#, CSS, CSV, Elixir, Erlang, file type iimage, Git, Go, HTML, Java, Jest, JS, JSX, Lua, makefile, Markdown, PHP, Prettier, Protobuf, Python, Rails, reStructuredText, Ruby, Rust, Shell, SQL, Swift, TOML, TS, TSX, WebAssembly, Webpack, YAML
- Change icon: Audio, Kotlin, makefile, Node js, Rspack
- Change sublime-syntax: CAD, Docker, Flatbuffers, Node js, Prettier, Pyhton, Ruby, Sublime Text
- Change tmPreferences: Arduino, Citation, CMake, CSV, Flatbuffers, git, HTML, Java, JSX, Lua, MDX, PHP, Ruby
- Rename icons: Elixir, Fusion, TS, Unity, WebAssembly
- Rename sublime-syntax file name: Arduino, Code of Conduct, Docker, GraphQL, Kotlin, Less js, Next js, NGINX, Node js, OpenGL, pnpm, pytest, Protobuf, README, Sass, SCSS, Svelte, Test JSX, Test TSX, Unity, Vue, WebAssembly, WebGPU

### Build 🛠️
- Add data files
- Add clean_svg
- Add icons
- Add icons_syntaxes
- Add icons_preferences
- Add scripts
- Add create_test_icon_theme
- Add zukan_syntaxes
- Add logger
- Add zukan_preferences
- Add concat_svgs

### Plugin 🕹️
- Add icons_themes
- Add move_folders
- Add icons_sytanxes
- Add logger
- Add sublime-menu and sublime-commands
- Add icons_preferences
- Add sublime-settings

## [0.1.3] - 2024-04-22
- Add alias: codecov, netlify, nextjs, poetry, prettier, pytest, ruff, unocss, vitest, webgpu
- Add file type icons: codecov, netlify, nextjs, poetry, prettier, pytest, ruff, unocss, vitest, webgpu
- Add preferences: ai, codecov, netlify, nextjs, poetry, prettier, ps, pytest, ruff, unocss, vitest, webgpu
- Change alias: javascript jest, javascript vitest, json ts, toml bun, plain text svelte
- Remove alias: plain text swc 
- Change preferences: swc
- Change SVGs file type icons: c# -> csharp, test_js -> test-js, test_jsx -> test-jsx, test_ts -> test-ts, test_tsx -> test-tsx

## [0.1.2] - 2024-03-31
- Add alias: angular, citation, flatbuffers, lua, mdx, opengl, svelte, vite, vue, rollup, rspack, storybook
- Add file type icons: angular, flatbuffers, lua, mdx, opengl, svelte, vite, vue, storybook
- Add preferences: angular, flatbuffers, lua, mdx, opengl, svelte, vite, vue, storybook
- Change alias: citation, rollup, vite, rspack
- Change file type icons: test.tsx, tsx
- Change preferences: citation, rspack, test.tsx, tsx

## [0.1.1] - 2024-02-11
- Add alias: go, pnpm, turbo, typescript, rspack, swc, yarn
- Add file type icons: afphoto, afpub, bun, makefile, pnpm, turbo, rails, rspack, swc, webassembly -> wast
- Add preferences: pnpm, turbo, rails, rspack, swc
- Rename for compatibility webassemby to wast, A File Icon package 
- Change alias: ruby
- Change file type icon: settings, toml, afdesign, wast
- Change preferences: typescript, wast, ruby, yarn

## [0.1.0] - 2022-12-11
- Add file type icons: afdesing, ai, arduino, audio, babel, binary, blender, c#, c++, c, cad, citatuion, cmake, codeofconduct, css, csv, default, docker, erlang, eslint, ex, excel, f3d, go, graphql, html, image, java, jest, js, json, jsx, kotlin, less, license, log, markdown, markup, nginx, nodejs, npm, pdf, php, protobuf, psd, python, readme, rollup, ruby, rust, sass, settings, shell, source, sql, sublime, svg, swift, test_js, test_jsx, test_typescript, text, toml, tsx, typescript, unity3d, video, webpack, word, xml, yaml, yarn.
- Add tmPreferences and sublime-synthax for icons.
- Add source files, svg and afdesign file.
- Add examples.
- Add changelog, license and readme.
