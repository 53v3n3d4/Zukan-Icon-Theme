# Plugin

If installed using Package Control, plugin create a 'Zukan Icon Theme' folder in 'Packages'.  

We need this folder, to create, edit or delete, icons sublime-themes, icons tmPreferences and icons sublime-syntax files. And `Installed Packages` uses a zip file.  

## Install

You may need to `Package Control: Satisfy Libraries` to install dependencies.  

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

## Commands

They can be accessed through `Tools > Command Palette...`. Type `zukan` to see the commands available.  

### Delete Preference

It delete a tmPreference file from a list of created preferences.  

### Delete Preferences

It delete all created tmPreferences files in `preferences` folder.  

### Delete Syntax

It delete a sublime-syntax file from a list of created syntaxes.  

### Delete Syntaxes

It delete all created sublime-syntax files in `icons_syntaxes` folder.  

### Delete Theme

It delete a sublime-theme file from a list of created themes.  

### Delete Themes

It delete all created sublime-theme files in `icons` folder.  

### Install Preference

It install a tmPreferences file from zukan preferences list, excluding already installed in plugin.  

### Install Syntax

It install a sublime-syntax file from zukan icons syntaxes list, excluding already installed in plugin or ST.  

### Install Theme

It install a sublime-theme file from a list of user installed themes, excluding already installed in plugin.  

### Install Themes

It install all sublime-theme files from a list of user installed themes.  

### Rebuild Preferences

It remove all previous tmPreferences files in `preferences`, before install all zukan icons preferences.  

### Rebuild Syntaxes

It remove all previous sublime-syntax files in `icons_syntaxes`, before install all zukan icons syntaxes, excluding user installed syntaxes.  
