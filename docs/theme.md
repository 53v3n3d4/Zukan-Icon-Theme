## Installing theme manually

To manually add a theme, go to your Sublime Text folder.  
- Menu `Sublime Text > Preferences > Browse packages...`  
- Then add the theme file inside `Packages/Zukan Icon Theme/icons` folder  

Create new theme file:  
- Copy code below  
- Rename it with your theme name, e.g. Default.sublime-theme  
- Maybe restart needed  

If your theme do not have settings for `icon_file_type`, the settings below has a hover and selected effects.  
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
    "layer0.opacity": 1.0
  },
  {
    "class": "icon_file_type",
    "parents": [{"class": "tree_row", "attributes": ["selected"]}],
    "layer0.opacity": 1.0
  }
]
```

If your theme does have setting for `icon_file_type`, the setting below is enough.  
```
[
  {
    "class": "icon_file_type",
    "layer0.tint": null,
    "content_margin": [9, 8]
  }
]
```

## Deleting theme manually

If you do not want Zukan to display in one of your theme, follow steps below.  

To manually delete a theme, go to your Sublime Text folder.  
- Menu `Sublime Text > Preferences > Browse packages...`  
- Then delete the theme file inside `Packages/Zukan Icon Theme/icons` folder  