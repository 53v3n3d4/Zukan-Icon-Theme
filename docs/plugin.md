# Plugin

If installed using Package Control, plugin create a 'Zukan Icon Theme' folder in 'Packages'.  

We need this folder, to create, edit or delete, icons sublime-themes, icons tmPreferences and icons sublime-syntax files. And `Installed Packages` uses a zip file.  

## Install

If clone repo, you may need to `Package Control: Satisfy Libraries` to install dependencies.  

More info about 3rd party dependencies, see [SO link](https://stackoverflow.com/questions/61196270/how-to-properly-use-3rd-party-dependencies-with-sublime-text-plugins).  

Plugin use [`ruamel-yaml`](https://packagecontrol.github.io) dependency.  

Plugin dependencies in [`dependencies.json`](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/dependencies.json).  

## `.python-version`

Change ST python interpreter in `.python-version` file: 3.3 or 3.8.  

## Themes

To make an icon show on ST, a sublime-theme is created in `icons` folder.  

Plugin use two templates. One with, and another without, attributes for hover and selected effect.  

## Preferefences

Icon preferences files register the scopes and PNG for each icon. This is also important, for this package, to allow not show icons in a specific theme and future icons customizations.  

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

It changes icon being used, a few icons has more than one option. E.g. Angular, C#, Composer, DirectX, Go, Image, LLVM, Node.js, PHP, Python, Ruff, Rust, Sublime Text.  

See [file-icon.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/file-icon.md).  

> ST theme essentials icons only works with exact ST file name.  

> ST essentials icons: 'file_type_binary', 'file_type_default', 'file_type_image', 'file_type_markup' and 'file_type_source'.  

Example: `Zukan Icon Theme: Change Icon` type `Angular` hit Enter, type `angular-1` hit Enter

```json
    "change_icon": {
        "Angular": "angular-1",
        "Composer": "composer-1",
        "Composer": "composer-2",
        "C#": "csharp-1",
        "DirectX": "directx-1",
        "Go": "go-1",
        // Image option works because plugin renames it when build file.
        "Image": "file_type_image-1",
        "LLVM": "llvm-1",
        "Node.js": "nodejs-1",
        "PHP": "php-1",
        "Python": "python-1",
        "Ruff": "ruff-1",
        "Rust": "rust-1",
        "Sublime Text": "sublime-1"
    },
```

### Disable Icon

It inserts an icon in `ignored_icon` setting. Ignored icons are excluded during build.  

### Disable Theme

It inserts a theme in `ignored_theme` setting. Ignored themes are excluded during build.  

### Enable Icon

It removes an icon from `ignored_icon` setting.  

### Enable Theme

It removes a theme from `ignored_theme` setting.  

### Reset Icon

If icon is changed for another option. Reset Icon can reset, removing it from `change_icon` setting.  

### Change File Extension

This setting tries to solve issues, if icon is pointing to a not desired file extension, when:  
- languages or libraries use same file extension  
- packages use different scope  

It only remove file extension in existing icons syntaxes, excluding the one inserted.

> In cases, where icons syntaxes do not exist, when language syntaxes are installed. Using ST 'View >
Syntax > Open all with current extension as...' could fix see the desired icon.  

> E.g., Clojure and ClojureScript, cljc extension is in both, no icons syntaxes since they are ST 
package. ClojureScript syntax will prevail since ST reads it last.

Required parameters are: scope and file extensions.  

Example: `Zukan Icon Theme: Change File Extension` type `source.iot` hit Enter, type `ino, pde` hit Enter.  

> Multiple file extensions can be inserted separated by commas.

```json
    "change_icon_file_extension": [
        { "scope": "source.js.jxa", "file_extensions": ["js"] },
        { "scope": "source.iot", "file_extensions": ["ino", "pde"] },
        { "scope": "source.vbs", "file_extensions": ["cls", "vbs"] },
        { "scope": "source.bazel", "file_extensions": ["BUILD", "WORKSPACE"] },
        { "scope": "source.starlark", "file_extensions": ["BUILD", "WORKSPACE", "bazel", "bzl"] },
        { "scope": "feature.behat", "file_extensions": ["feature"] },
        { "scope": "source.clojure", "file_extensions": ["cljc"] },
        { "scope": "source.cmakeeditor", "file_extensions": ["CMakeLists.txt"] },
        { "scope": "source.cuda-c++", "file_extensions": ["h"] },
        { "scope": "text.django", "file_extensions": ["css", "html", "xml"] },
        { "scope": "source.yaml.flutter", "file_extensions": ["pubspec.lock", "pubspec.yaml"] },
        { "scope": "source.modern-fortran", "file_extensions": ["f90", "F90", "f95", "F95", "f03", "F03", "f08", "F08"] },
        { "scope": "source.fsharp", "file_extensions": ["fs"] },
        { "scope": "source.sss", "file_extensions": ["sss"] },
        { "scope": "source.unity_shader", "file_extensions": ["cginc", "shader"] },
        { "scope": "source.toml", "file_extensions": ["config.toml"] },
        { "scope": "source.toml", "file_extensions": ["book.toml"] },
        { "scope": "source.toml", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.pdm", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.pip", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.poetry", "file_extensions": ["pyproject.toml"] },
        { "scope": "source.toml.tox", "file_extensions": ["pyproject.toml"] },
        { "scope": "text.plain", "file_extensions": ["requirements.txt"] },
        { "scope": "text.plain.uv", "file_extensions": ["requirements.txt"] },
    ],
```

### Create Custom Icon

It can insert an custom icon or a file extension that do not exist. The PNGs files will have to be inserted manually in Zuka 'icons' folder.  

PNGs icon file name should follow ST policy:

| icon suffix | size |
|-------------|------|
| (icon).png | 18x16 |
| (icon)@2x.png | 36x32 |
| (icon)@3x.png | 54x48 |

Currently, 3 options possible and a key 'name' is required:  
1. To create an icon for a scope without file extension, fill icon and scope keys  
2. To insert a file_extension for a existing icon, ommit icon key  
3. To create a new icon with file_extension, keys icon, syntax_name, scope and file_extensions are necessary  

> See ST docs for more info about syntax and scopes [http://www.sublimetext.com/docs/index.html](http://www.sublimetext.com/docs/index.html).  

Sequence: `Zukan Icon Theme: Create Custom Icon` `name` `icon` `syntax_name` `scope` `file_extensions` `contexts_scope`.  

> Hit enter to leave key empty.  

> Required parameter is name.  

#### Example Option 1

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest` hit Enter
- type `atest` hit Enter
- `(leave empty)` hit Enter
- type `source.toml.atest` hit Enter
- `(leave empty)` hit Enter
- `(leave empty)` hit Enter  

#### Example Option 2

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest-1` hit Enter
- `(leave empty)` hit Enter
- type `JSON (ATest-1)` hit Enter
- type `source.json.atest1` hit Enter
- type `atest1.config.json` hit Enter
- type `source.json` hit Enter  

#### Example Option 3

- `Zukan Icon Theme: Create Custom Icon`
- type `ATest-3` hit Enter
- type `atest3` hit Enter
- type `ATest-3` hit Enter
- type `source.atest3` hit Enter
- type `abc, def` hit Enter
- type `source.atest2` hit Enter  

> If inserted more than one scopes. And syntax_name present, the first scope will be used in icon syntax.  

> Key name should be unique, if exists in Zukan icons data or in `create_custom_icon`, will be excluded from building.

```json
    "create_custom_icon": [
       {
           "name": "ATest",
           "icon": "atest",
           "scope": "source.toml.atest, source.toml.atest"
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

### Delete Custom Icon

It deletes an icon from a list of customized icons, in `created_custom_icon` setting.  

### Reset File Extension

It remove an icon file extension from a list of scopes,  in `change_icon_file_extension` setting.  

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
