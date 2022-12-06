## File type icons

![file type icons](https://github.com/53v3n3d4/file-type-icons/blob/main/assets/screenshot.png "Screenshot")

**This is a slow work in progress (WIP).**  

*File type icons for Sublime Text editor.*  

***This package uses tmPreferences and sublime-syntax files.***  

*[Treble Adaptive](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Adaptive.sublime-theme)*  
**[Treble Dark](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Dark.sublime-theme)**  
***[Treble Light](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Light.sublime-theme)***  

<ins>Underline text</ins>
<u>Underline text</u>
text here <span style="text-decoration: underline">underlined text</span> other text

| all users | user | login shell  | interactive shell | scripts | Terminal.app |
|-----------|------|--------------|-------------------|---------|--------------|
| /etc/zprofile | .zprofile | √ | x | x | √ |
| /etc/zshrc  | .zshrc  | √ | √ | x | √ |

## Theme

![treble with file type icons](https://github.com/53v3n3d4/file-type-icons/blob/main/assets/treble-light-screenshot.png "Treble Light Screenshot")

Currently, only Treble theme suported.  

- [Treble Adaptive](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Adaptive.sublime-theme)
- [Treble Dark](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Dark.sublime-theme)
- [Treble Light](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Light.sublime-theme)

To add new theme:
- Duplicate one of the Treble files above inside icons folder
- Rename it with new theme name, e.g. Default.sublime-theme
- Maybe restart needed

If your theme do not have settings for file_type_icon, the settings below has a hover and select effects.
```
[
  {
    "class": "icon_file_type",
    "layer0.tint": null,
    "layer0.opacity": 0.8,
    "content_margin": [9, 8]
  },
  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["hover"]}],
    "layer0.opacity": 0.6
  },
  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["selected"]}],
    "layer0.opacity": 1.0
  }
]
```

If your theme does have setting for file_type_icon, the setting below is enough.  
```json
[
  {
    "class": "icon_file_type",
    "layer0.tint": null,
    "content_margin": [9, 8]
  }
]
```

## Install

The only way to install this icons now is manually.

To install manually,
- Download the [latest release](https://github.com/53v3n3d4/file-type-icons/releases) or clone this repo.
- Menu `Sublime Text > Preferences > Browse packages...` to open destination folder
- Then unzip `file-type-icons zip file` inside `Packages` folder. Or clone the repo inside `Packages`folder.

## Uninstall

To uninstall manually, go to your Sublime Text folder.
- Menu `Sublime Text > Preferences > Browse packages...`
- Then delete `file-type-icons` inside `Packages` folder

## Icons not working

- Svg
- xml
- sublime-theme, sublime-color-scheme, sublime-settings

## File icon packages :alien:

- [A File Icon](https://github.com/SublimeText/AFileIcon)
- [FileIcons](https://github.com/braver/FileIcons)

## License

MIT license ([LICENSE-MIT](LICENSE))
