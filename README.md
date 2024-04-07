## File type icons

![file type icons](assets/screenshot.png "Screenshot")

> Icons from v0.1.0

This is a slow work in progress (WIP).  

File type icons for Sublime Text editor.  

This package uses tmPreferences and sublime-syntax files.  

## Theme

![treble with file type icons](assets/treble-light-screenshot.png "Treble Light Screenshot")

Currently, only Treble theme suported.  

- [Treble Adaptive](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Adaptive.sublime-theme)
- [Treble Dark](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Dark.sublime-theme)
- [Treble Light](https://github.com/53v3n3d4/file-type-icons/blob/main/icons/Treble%20Light.sublime-theme)

To add new theme:
- Duplicate one of the Treble files above inside icons folder
- Rename it with new theme name, e.g. Default.sublime-theme
- Maybe restart needed

If your theme do not have settings for icon_file_type, the settings below has a hover and select effects.
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

If your theme does have setting for icon_file_type, the setting below is enough.  
```
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

The icons bellow will work if you rename `file-type-icons` folder to `zz-file-type-icons` and make it the last folder in `Packages` directory.
- Svg
- sublime-theme, sublime-color-scheme, sublime-settings (Few json sublime extensions like `hidden-theme` works with no need to rename folder)

The icons bellow will not work even if you rename `file-type-icons` folder to `zzz-file-type-icons`
- xml

## Notes
- If rename `file-type-icons` to `v-file-type-icons`, and make the last folder in `Packages` directory, sublime icons will work
- If rename `file-type-icons` to `z-file-type-icons`, and make the last folder in `Packages` directory, is not enough for svg icon to work. It was needed `zz-file-type-icons` to make svg icon work

## File icon packages :alien:

- [A File Icon](https://github.com/SublimeText/AFileIcon)
- [FileIcons](https://github.com/braver/FileIcons)

## License

MIT license ([LICENSE-MIT](LICENSE))
