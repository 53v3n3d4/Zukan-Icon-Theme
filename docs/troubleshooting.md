## Icons not showing correct

Since icons collections are growing, there are cases where icons do not prompt show correct.  

- If there is no change in installed icons themes, a package rebuild or upgrade, will be done with no need to restart ST  
- ST command `refresh_folder_list` do not refresh `icon_file_type`  

For reference, when we say icon theme, icon syntax and icon preference. It is about files in Zukan package.

## Cases

As of now, the cases below usually have the same solution, restart ST.

We display an dialog message about restart in these cases.  

If you do not want it, you can turn off. Go to menu `Sublime Text > Settings > Package Settings > Zukan Icon Theme > Settings` and change `zukan_restart_message` to `false`.  

### First install via sublime-package (zip) or clone repo

It seems to affect only the current theme. If change to another installed theme, icons shows correct.

**Solution**
```
Restart fix. 

Or, if installed via clone repo, duplicate a folder with 5 files or more, 
seems to force reload.
```

### Delete one or all icons themes

When delete one or all themes, an icon can still show, even deleted, or an error not found image (red blur image).  

They will be no error in console. If deleted only one theme, others themes seems to be working fine.  

**Solution**
```
Restart fix. 

Or, if installed via clone repo, duplicate a folder with 5 files or more, 
seems to force reload.
```

### Install new theme

If theme package has more than one theme. Usually, this affect only the current theme, when icons is being built.

This also may happen, when a specific theme that do not have icon theme, is followed by run command `Zukan Icon Theme: Install Theme` in `Command Palette...`. This theme may not prompt show icons correct.  

**Solution**
```
Restart fix. 

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

### Error exception when disable zukan package and enable with `theme` setting `auto`

This error occurr when zukan package is in `ignored_package` and enabling it with `theme` setting `auto`.

```
Exception in thread Thread-6:
Traceback (most recent call last):
  File "/Users/xxxx/Library/Application Support/Sublime Text/Installed Packages/Zukan Icon Theme.sublime-package/src/zukan_icon_theme/lib/icons_preferences.py", line 69, in build_icons_preferences
  File "/Users/xxxx/Library/Application Support/Sublime Text/Installed Packages/Zukan Icon Theme.sublime-package/src/zukan_icon_theme/lib/icons_preferences.py", line 317, in create_icons_preferences
IndexError: list index out of range

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "./python3.8/threading.py", line 932, in _bootstrap_inner
  File "./python3.8/threading.py", line 870, in run
  File "/Users/xxxx/Library/Application Support/Sublime Text/Installed Packages/Zukan Icon Theme.sublime-package/src/zukan_icon_theme/events/install.py", line 56, in install_batch
  File "/Users/xxxx/Library/Application Support/Sublime Text/Installed Packages/Zukan Icon Theme.sublime-package/src/zukan_icon_theme/lib/icons_preferences.py", line 72, in build_icons_preferences
  File "/Users/xxxx/Library/Application Support/Sublime Text/Installed Packages/Zukan Icon Theme.sublime-package/src/zukan_icon_theme/lib/icons_preferences.py", line 581, in delete_plist_tags
UnboundLocalError: local variable 'p' referenced before assignment
```

**Solution**
```
Select a theme before enabling zukan, the build seems to happen with no errors.

If already enabled with 'auto'. Change to a theme and restart ST. This will build files.
```