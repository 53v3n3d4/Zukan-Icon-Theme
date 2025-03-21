# Plugin

If installed using Package Control, plugin create a `Zukan Icon Theme` folder in `Packages`.  

We need this folder, to create, edit or delete, icons sublime-themes, icons tmPreferences and icons sublime-syntax files. And `Installed Packages` uses a zip file.  

## Install

> The plugin `ruamel-yaml` dependency has been removed in version 0.4.5.  

If clone repo, for tags below v0.4.4, you may need to `Package Control: Satisfy Libraries` to install dependencies.  

## `.python-version`

Change ST python interpreter in `.python-version` file: 3.3 or 3.8.  

## Themes

To make an icon show on ST, a sublime-theme is created in `icons` folder.  

Plugin use two templates. One with, and another without, attributes for hover and selected effect.  

## Preferefences

Icon preferences files register the scopes and PNG for each icon. This is also important, for this package, to allow not show icons in a specific theme and icons customizations.  

## Syntaxes

Aside icons PNGs, tmPreferences and sublime-theme file, there are cases where the plugin use a sublime-syntax to show icons:  
- Show icons for a file extension, without syntax package installed  
- An icon for a library/package/application file. Example: tsconfig.json (json file)  
- An icon for a specific file. Example: a README.md (markdown file)  

## Icons

There is a list of icons that are not working in [`README.md`](https://github.com/53v3n3d4/Zukan-Icon-Theme?tab=readme-ov-file#icons-that-works-depending-on-folder-position).  

## Commands settings

They can be accessed through `Tools > Command Palette...`. Type `zukan` to see the commands available.  

It is the same, if go to menu `Sublime Text > Settings > Package Settings > Zukan Icon Theme > Settings`. And edit settings manually.  

### Change Icon

It changes icon being used, a few icons has more than one option. E.g. Angular, C#, Cert, Composer, DirectX, Go, Image, LLVM, Node.js, PHP, Python, Ruff, Rust, SolidJS, Sublime Text.  

See [file-icon.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/file-icon.md).  

> ST theme essentials icons only works with exact ST file name.  

> ST essentials icons: 'file_type_binary', 'file_type_default', 'file_type_image', 'file_type_markup' and 'file_type_source'.  

> Essentials icons options works because plugin renames them when build file.  

#### Example
- `Zukan Icon Theme: Change Icon`  
- type `Angular` hit <kbd>Enter</kbd>  
- type `angular-1` hit <kbd>Enter</kbd>  

```json
    "change_icon": {
        "Angular": "angular-1",
        "Binary": "file_type_binary-1-dark",
        "C#": "csharp-1",
        "Cert. Authentication": "cert-1-dark",
        "Composer": "composer-1",
        "Composer": "composer-2",
        "CSS": "css-1",
        "DirectX": "directx-1-dark",
        "Go": "go-1",
        "Image": "file_type_image-1",
        "LLVM": "llvm-1",
        "Node.js": "nodejs-1",
        "PHP": "php-1",
        "Python": "python-1",
        "Ruff": "ruff-1",
        "Rust": "rust-1",
        "Rust": "rust-2",
        "SolidJS": "solidstart",
        "Source": "file_type_source-1-dark",
        "Sublime Text": "sublime-1",
        "Text": "text-1-dark"
    },
```

### Disable Icon

It inserts an icon in `ignored_icon` setting. Ignored icons are excluded during build.  

A 'primary' tag is supported and will ignore ST theme essentials icons. Icons with tag 'primary':
- file_type_binary
- file_type_default
- file_type_image
- file_type_markup
- file_type_source

Tags supported: 'database' and 'primary'.

### Disable Theme

It inserts a theme in `ignored_theme` setting. Ignored themes are excluded during build.  

### Enable Icon

It removes an icon from `ignored_icon` setting.  

### Enable Theme

It removes a theme from `ignored_theme` setting.  

> To show file icons, need to create an icon theme. Use command InstallTheme.

### Reset Icon

If icon has been changed for another option. This command will reset to default icon, removing the changed icon from `change_icon` setting.  

### Change File Extension

This setting tries to solve issues, if icon is pointing to a not desired file extension, when:  
- languages or libraries use same file extension  
- packages use different scope  

It only removes file extension in existing icons syntaxes, excluding the one inserted.

> In cases, where icons syntaxes do not exist, when language syntaxes are installed. Using ST 'View >
Syntax > Open all with current extension as...' could fix see the desired icon.  

> E.g., Clojure and ClojureScript, cljc extension is in both, no icons syntaxes since they are ST 
package. ClojureScript syntax will prevail since ST reads it last.

Required parameters are: scope and file extensions.  

#### Example
- `Zukan Icon Theme: Change File Extension`  
- type `source.iot` hit <kbd>Enter</kbd>  
- type `ino, pde` hit <kbd>Enter</kbd>  

> Multiple file extensions can be inserted separated by commas.

```json
    "change_icon_file_extension": [
        { "scope": "feature.behat", "file_extensions": ["feature"] },
        { "scope": "source.bazel", "file_extensions": ["BUILD", "WORKSPACE"] },
        { "scope": "source.clojure", "file_extensions": ["cljc"] },
        { "scope": "source.clojure.clojure-common", "file_extensions": ["cljc"] },
        { "scope": "source.cmakeeditor", "file_extensions": ["CMakeLists.txt"] },
        { "scope": "source.cuda-c++", "file_extensions": ["h"] },
        { "scope": "source.edn", "file_extensions": ["edn"] },
        { "scope": "source.elixir", "file_extensions": ["dev.exs", "prod.exs", "prod.secret.exs", "test.exs"] },
        { "scope": "source.elixir.phoenix", "file_extensions": ["config.exs"] },
        { "scope": "source.env.fastapi", "file_extensions": [".env"] },
        { "scope": "source.fsharp", "file_extensions": ["fs"] },
        { "scope": "source.ini", "file_extensions": ["setup.cfg"] },
        { "scope": "source.ini.setuptools", "file_extensions": ["setup.cfg"] },
        { "scope": "source.ini.tox", "file_extensions": ["setup.cfg"] },
        { "scope": "source.iot", "file_extensions": ["ino", "pde"] },
        { "scope": "source.js.jxa", "file_extensions": ["js"] },
        { "scope": "source.json", "file_extensions": ["config.json"] },
        { "scope": "source.json", "file_extensions": ["dependencies.json"] },
        { "scope": "source.json", "file_extensions": ["messages.json"] },
        { "scope": "source.json", "file_extensions": ["unittesting.json"] },
        { "scope": "source.lisp", "file_extensions": ["scm", "ss"]},
        { "scope": "source.modern-fortran", "file_extensions": ["f90", "F90", "f95", "F95", "f03", "F03", "f08", "F08"] },
        { "scope": "source.python", "file_extensions": ["config.py"] },
        { "scope": "source.rspec", "file_extensions": ["rb"] },
        { "scope": "source.sss", "file_extensions": ["sss"] },
        { "scope": "source.starlark", "file_extensions": ["BUILD", "WORKSPACE", "bazel", "bzl"] },
        { "scope": "source.txtree", "file_extensions": ["txt"] },
        { "scope": "source.toml", "file_extensions": ["book.toml"] },
        { "scope": "source.toml.pdm", "file_extensions": ["config.toml"] },
        { "scope": "source.toml.pixi", "file_extensions": ["config.toml"] },
        { "scope": "source.toml.tidb", "file_extensions": ["config.toml"] },
        { "scope": "source.toml", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.black", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.hatch", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.pdm", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.pip", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.poetry", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.pixi", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.setuptools", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.tox", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.ts.angular", "file_extensions": ["app.config.ts"] },
        { "scope": "source.ts.nuxt", "file_extensions": ["app.config.ts"] },
        { "scope": "source.ts.solidjs", "file_extensions": ["app.config.ts"] },
        { "scope": "source.vbs", "file_extensions": ["cls", "vbs"] },
        { "scope": "source.unity_shader", "file_extensions": ["cginc", "shader"] },
        { "scope": "source.yaml", "file_extensions": ["ci.yml"] },
        { "scope": "source.yaml", "file_extensions": ["config.yml"] },
        { "scope": "source.yaml.flutter", "file_extensions": ["pubspec.lock", "pubspec.yaml"] },
        { "scope": "source.yaml.clickhouse", "file_extensions": ["config.yaml"] },
        { "scope": "source.yaml.huggingface", "file_extensions": ["config.yaml"] },
        { "scope": "source.yaml.openfga", "file_extensions": ["config.yaml"] },
        { "scope": "text.django", "file_extensions": ["css", "html", "xml"] },
        { "scope": "text.html.js", "file_extensions": ["ejs"] },
        { "scope": "text.html.markdown.mdsvex", "file_extensions": ["md"] },
        { "scope": "text.plain", "file_extensions": ["requirements.txt"] },
        { "scope": "text.plain.uv", "file_extensions": ["requirements.txt"] },
        { "scope": "text.plain.wwpdb", "file_extensions": ["pdb"] },
    ],
```

### Create Custom Icon

It can insert a custom icon or a file extension that does not exist. The PNGs files will have to be inserted manually in Zukan `icons` folder.  

PNGs icon file name should follow ST suffix policy:

| icon suffix | size (px) |
|-------------|------|
| (icon).png | 18x16 |
| (icon)@2x.png | 36x32 |
| (icon)@3x.png | 54x48 |

Currently, 3 options possible and a key `name` is required:  
1. Create an icon for a scope without file extension, fill icon and scope keys  
2. Insert a file_extension for a existing icon, ommit icon key  
3. Create a new icon with file_extension, keys icon, syntax_name, scope and file_extensions are necessary  

> See ST docs for more info about syntax and scopes [http://www.sublimetext.com/docs/index.html](http://www.sublimetext.com/docs/index.html).  

Sequence: `Zukan Icon Theme: Create Custom Icon` `name` `icon` `syntax_name` `scope` `file_extensions` `contexts_scope`.  

> Hit enter to leave key empty.  

> Required parameter is name.  

#### Example Option 1

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest` hit <kbd>Enter</kbd>
- type `atest` hit <kbd>Enter</kbd>
- `(leave empty)` hit <kbd>Enter</kbd>
- type `source.toml.atest, source.json.atest` hit <kbd>Enter</kbd>
- `(leave empty)` hit <kbd>Enter</kbd>
- `(leave empty)` hit <kbd>Enter</kbd>  

#### Example Option 2

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest-1` hit <kbd>Enter</kbd>
- `(leave empty)` hit <kbd>Enter</kbd>
- type `JSON (ATest-1)` hit <kbd>Enter</kbd>
- type `source.json.atest1` hit <kbd>Enter</kbd>
- type `atest1.config.json` hit <kbd>Enter</kbd>
- type `source.json` hit <kbd>Enter</kbd>  

#### Example Option 3

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest-3` hit <kbd>Enter</kbd>
- type `atest3` hit <kbd>Enter</kbd>
- type `ATest-3` hit <kbd>Enter</kbd>
- type `source.atest3` hit <kbd>Enter</kbd>
- type `abc, def` hit <kbd>Enter</kbd>
- type `source.atest2` hit <kbd>Enter</kbd>  

> If inserted more than one scope. And syntax_name present, the first scope will be used in icon syntax.  

> Key name should be unique, if exists in Zukan icons data or in `create_custom_icon`, will be excluded from building.

```json
    "create_custom_icon": [
       {
           "name": "ATest",
           "icon": "atest",
           "scope": "source.toml.atest, source.json.atest"
       },
       {
           "name": "ATest-1",
           "syntax_name": "JSON (ATest-1)",
           "scope": "source.json.atest1",
           "file_extensions": ["atest1.config.json"],
           "contexts_scope": "source.json"
       },
       {
           "name": "ATest-2",
           "icon": "atest2",
           "syntax_name": "ATest-2",
           "scope": "source.atest2",
           "file_extensions": ["xyz"]
       },
       {
           "name": "ATest-3",
           "icon": "atest3",
           "syntax_name": "ATest-3",
           "scope": "source.atest3",
           "file_extensions": ["abc", "def"],
           "contexts_scope": "source.atest2"
       }
    ],
```

#### GitHub example

We use scopes from `Package YamlPipelines` in GitHub and GitHub Dependabot icons.  

To change to Yaml syntax:
- Using command palette, disable icon GitHub or GitHub Dependabot. Or, manually, insert in `ignored_icon`
- Next, create a custom icon
- `Zukan Icon Theme: Create Custom Icon`
- type `GitHub 2` hit <kbd>Enter</kbd>
- type `github` hit <kbd>Enter</kbd>
- type `YAML (GitHub 2)` hit <kbd>Enter</kbd>
- type `source.yaml.github` hit <kbd>Enter</kbd>
- type `ci.yml` hit <kbd>Enter</kbd>
- type `source.yaml` hit <kbd>Enter</kbd>  

```json
    "create_custom_icon": [
       {
           "name": "GitHub 2",
           "icon": "github",
           "syntax_name": "YAML (GitHub 2)",
           "scope": "source.yaml.github",
           "file_extensions": ["ci.yml"],
           "contexts_scope": "source.yaml"
       }
    ]
```

### Delete Custom Icon

It deletes an icon from a list of customized icons, in `created_custom_icon` setting.  

### Remove Prefer Icon

It remove a preferred icon in `prefer_icon` setting.  


### Reset File Extension

It remove an icon file extension from a list of scopes,  in `change_icon_file_extension` setting.  

### Select Prefer Icon

It can select a dark or light icon for a theme,  in `prefer_icon` setting.  

> Not all icons have a dark and light icon.  

> This option overrides `change_icon`. Because `prefer_icon` runs after `change_icon`.  

## Commands

They can be accessed through `Tools > Command Palette...`. Type `zukan` to see the commands available.  

### Delete Preference

It deletes a tmPreference file from a list of created preferences.  

### Delete Syntax

It deletes a sublime-syntax file from a list of created syntaxes.  

### Delete Theme

It deletes a sublime-theme file from a list of created themes.  

### Install Preference

It installs a tmPreferences file from zukan preferences list, excluding already installed in plugin.  

### Install Syntax

It installs a sublime-syntax file from zukan icons syntaxes list, excluding already installed in plugin or ST.  

### Install Theme

It installs a sublime-theme file from a list of user installed themes, excluding already installed in plugin.  

## Setting `zukan_listener_enabled`

Option to not use the listener and `add_on_change`, so the icon files will not auto build under any circumstances.  

Any change needed, will have to do manually through Commands, to build files. The Commands are:
- Install/Delete Preferences
- Install/Delete Syntaxes
- Install/Delete Themes
- Rebuild Files

Plugin use listener to watch when a Theme or Color-scheme change. It is used to:
- Delete files when an ignored theme is selected
- Change icon dark or light

ST `add_on_change` is used to watch Zukan Preferences settings. And, if following settings change, it apply them to icons files:
- Change icon
- Change icon file extension
- Create custom icon
- Prefer icon
- Ignored icon
- Ignored theme

To turn off the listener and `add_on_change`:
- Go to `Settings > Package Settings > Zukan Icon Theme`
- Click on `Settings`
- Set `zukan_listener_enabled` to `false`
- A ST restart is needed

