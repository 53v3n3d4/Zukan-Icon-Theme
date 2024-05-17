## Repository and files/folders renamed

https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository
```
$ git remote set-url origin https://github.com/53v3n3d4/Zukan-Icon-Theme.git


```

Files and folders that has been renamed, or is going to be, in version v0.2.0.
| previous | new |
|-----------|------|
| file_type_(name).tmPreferences | (name).tmPreferences  |
| file_type_(name).svg | (name).svg  |
| file_type_(name).png | (name).png  |
| /aliases | /icons_syntaxes |

## Zukan Icon Theme

![file type icons](assets/screenshot.png "Screenshot")

> Icons from v0.1.0

This is a slow work in progress (WIP).  

Icon theme for Sublime Text editor.  

## Install

The only way to install this icons now is manually.  

To install manually,  
- Download the [latest release](https://github.com/53v3n3d4/Zukan-Icon-Theme/releases) or clone this repo.  
- Menu `Sublime Text > Preferences > Browse packages...` to open destination folder  
- Then unzip `zukan-icon-theme zip file` inside `Packages` folder. Or clone the repo inside `Packages`folder.  

> You may see a console message, regarding `ruamel-yaml` dependecy, when first install this package. ST may install it and inform that a restart is needed.

> `ruamel-yaml` is/will be used to create icons sublime-sytnaxes files in `icon-syntaxes` folder.

### Theme

To make icon theme works with your theme, you can use `Tools > Command Palette`. Type `zukan` and select `Zukan Icon Theme: Install Themes`.  

This command install for all existing themes in your ST.

If you prefer to create manually, see [theme.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/theme.md).  

## Uninstall

To uninstall manually, go to your Sublime Text folder.  
- Menu `Sublime Text > Preferences > Browse packages...`  
- Then delete `Zukan-Icon-Theme` inside `Packages` folder  

## Icons that works depending on folder position

- Poetry  
- SVG  
- sublime-theme, sublime-color-scheme, sublime-settings... mostly sublime (Exceptions like `hidden-theme` works not depending on this condition)  

## Icons that do not work

- Photoshop. ST use `file_type_image` icon  
- XML. ST use `file_type_markup` icon  

## Notes
- This package uses tmPreferences and sublime-syntax files, it is heavily based on how [`A File Icon`](https://github.com/SublimeText/AFileIcon) package make icons work  
- `file-type-icons` is old project name  
- If rename `file-type-icons` to `v-file-type-icons`, and make the last folder in `Packages` directory, sublime icons will work  
- If rename `file-type-icons` to `z-file-type-icons`, and make the last folder in `Packages` directory, is not enough for svg icon to work. It was needed `zz-file-type-icons` to make svg icon work  

## Limitations
- If you use a theme that has sublime-syntax and tmPreferences, only icons, not present on theme, might show.  


## File icon packages :alien:

- [A File Icon](https://github.com/SublimeText/AFileIcon)  
- [FileIcons](https://github.com/braver/FileIcons)  

## License

MIT license ([LICENSE-MIT](LICENSE))  