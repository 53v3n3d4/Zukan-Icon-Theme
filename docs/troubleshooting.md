## OS

| OS         | PC Install | Rebuild Command | Upgrade | Auto prefer icon | Notes |
|------------|------------|-----------------|---------|------------------|-------|
| Linux Febora 41 | ✔ | ✔ | ✔ | ✔ | Auto prefer icon works, but could not make ST theme auto works in my setup yet.|
| Linux Ubuntu 24.04 | ✔ | ✔ | ✔ | ✔ | |
| macOS Sonoma 14.6.1 | ✔ | ✔ | ✔ | ✔ | |
| Windows 10 Home | ✔ | ✔ | ✔ | ✔ | Error unable to read all preferences when saving settings. I tested it a few times, and it worked. This error usually occurred when build files are called multiple times together.|

> Linux and Windows testing on VM.

## Icons not showing correct

Since icons collections are growing, there are cases where icons do not prompt show correct.  

- If there is no change in installed icons themes, a package rebuild or upgrade, will be done with no need to restart ST  
- ST command `refresh_folder_list` do not refresh `icon_file_type`  

For reference, when we say icon theme, icon syntax and icon preference. It is about files in Zukan package.

## Cases

As of now, the some of cases below usually have the same solution, restart ST.

We display an dialog message about restart in these cases.  

If you do not want it, you can turn off. Go to menu `Sublime Text > Settings > Package Settings > Zukan Icon Theme > Settings` and change `zukan_restart_message` to `false`.  

### First install via sublime-package (zip) or clone repo

It seems to affect only the current theme. If change to another installed theme, icons shows correct.

**Solution**
```
A restart will fix it. 

Or, if installed via clone repo, duplicate a folder with 5 files or more, 
seems to force reload.
```

### Delete one or all icons themes

When delete one or all themes, an icon can still show, even deleted, or an error not found image (red blur image).  

They will be no error in console. If deleted only one theme, others themes seems to be working fine.  

**Solution**
```
A restart will fix it. 

Or, if installed via clone repo, duplicate a folder with 5 files or more, 
seems to force reload.
```

### Install new theme

If theme package has more than one theme. Usually, this affect only the current theme, when icons is being built.

This also may happen, when a specific theme that do not have icon theme, is followed by run command `Zukan Icon Theme: Install Theme` in `Command Palette...`. This theme may not prompt show icons correct.  

**Solution**
```
A restart will fix it. 

Or, if installed via clone repo, duplicate a folder with 5 files or more, 
seems to force reload.
```

### Theme or another icon package is overriding Zukan icons

If a theme has its own tmPreferences and sublime-syntax files, Zukan icons will usually complete with icons that do not exist.  

ST seems to apply plugins in order, read first starting with `Installed Packages` in alphabetical order then go to `Packages`.  

`A File Icon` package will override our icons. They have the first position in `Installed Packages` (A File Icon) and the last in `Packages` (zzz A File Icon zzz).  

It is same situation, Zukan icons will complete with icons that do not exist.

**Solution**
```
If user is using a theme or another icon package, and install Zukan icons.

The solution is to use Zukan icons to complete with icons that do not exist.

Overiding other packages icons in these situations is not possible currently, 
as explained above.
```

### Error icon not replaced when switching between dark and light modes

Icon does not change from dark version to light or vice-versa, while all others do.

If is an issue with plugin you can check if the correct icon was applied.

- Go to  `Settings > Browse Packages...`
- If the icon is not a Primary Icon, go to `Packages/Zukan Icon Theme/icons_preferences` and check the icon used in tmPreferences file
- If the icon is a Primary Icon and does not have a tmPreferences file, go to `Packages/Zukan Icon Theme/icons` and check the icon PNG

**Solution**
```
If the correct icon is applied, a restart will fix it.
```


### Error loading syntax file (Markdown, YAML, JSON) when building files

When building syntax, icons syntaxes files are deleted first. So if there are files (Markdown, YAML, JSON) opened, ST will show dialogs errors messages.  

Others types do not seem to throw dialogs errors.   

Syntax build happens in cases of:  
- Installation
- Upgrade
- Change file extension
- Create custom icon
- Delete or install icon syntax

**Solution**
```
One way for this do not happen is to close these types of files before rebuilding
icons syntaxes files.
```

### Change between theme or color-scheme and icons do not change dark/light

Plugin tries not to build files when not necessary. E.g. when change between themes with light sidebar background. Or, when adaptive themes, change color-schemes with dark background.

**Solution**
```
A move from a dark to a light theme/color-scheme or vice-versa make build
files.
```


### Error unable to read preferences files

When raise a lot of dialog messages for all preferences files.

This error usually occurs when build files are called multiple times together, causing conflicts with files being deleted and created.

**Solution**
```
Force quit ST or close all dialog messages.

The setting option 'zukan_listener_enabled' can be an option since it turn off
listener and 'add_on_change'. So any change needed, will have to do manually using
Commands.
```

See info about [setting `zukan_listener_enabled`](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/plugin.md#setting-zukan_listener_enabled)

### Added a syntax and it is not highlighting

Plugin does not rebuild icons syntaxes files when a new syntax package is added.

E.g. Install package INI after Zukan package. To avoid console error messages, the icons syntaxes files are different when a syntax is installed and when is not.

So, a `.npmrc` (INI file), that was not highlighted before package INI install, will need to rebuild icons syntaxes files to highlight.

***Solution***
```
Build icons syntaxes using Commands.

Option 1:
- Go to 'Command Palette', type 'zukan'
- Select 'Zukan Icon Theme: Install Syntax'
- Click all to rebuild all icons syntaxes files

Option 2:
- Go to 'Settings > Package Settings > Zukan Icon Theme'
- Click on 'Rebuild files'. This will rebuild all files, not only icons syntaxes. It
is similar to first install or upgrade package

Also, there are actions where icons syntaxes are rebuilt:
- Package upgrade
- Move from an ignored theme
- Deleted folder 'icons_syntaxes' or all icons syntaxes files, then restart ST
```
