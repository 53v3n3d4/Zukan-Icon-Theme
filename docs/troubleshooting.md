## Icons not showing correct

Since icons collections are growing, there are cases where icons do not prompt show correct.  

- If there is no change in installed icons themes, a package rebuild or upgrade, will be done with no need to restart ST  
- ST command `refresh_folder_list` do not refresh `icon_file_type`  

For reference, when we say icon theme, icon syntax and icon preference. It is about files in Zukan package.

## Cases

As of now, the case below usually have the same solution, restart ST.

We display an dialog message about restart in these cases.  

If you do not want it, you can turn off. Go to menu `Sublime Text > Settings > Package Settings > Zukan Icon Theme > Settings` and change `zukan_restart_message` to `false`.  

### First install via sublime-package (zip) or clone repo

It seems to affect only the current theme. If change to another installed theme, icons shows correct.

```
**Solution:** 
Restart fix. 

Or, if installed via clone repo, duplicante a folder with 5 files or more, seems to force reload.
```

### Delete one or all icons themes

When delete one or all themes, an icon can still show, even deleted, or an error not found image (red blur image).

They will be no error in console. If deleted only one theme, others themes seems to be working fine. Even if after new buidls.

```
**Solution:** 
Restart fix. 

Or, if installed via clone repo, duplicante a folder with 5 files or more, seems to force reload.
```

### Install new theme

If theme package has more than one theme. Usually this affect only the current theme when icons is being built.

This also may happen when a specific theme that do not have icon theme, and run command `Zukan Icon Theme: Install Theme` in `Command Palette...` with this theme selected.

```
**Solution:** 
Restart fix. 

Or, if installed via clone repo, duplicante a folder with 5 files or more, seems to force reload.
```


### Current Theme or another icon package is overriding Zukan Theme

ST seems to apply plugins in order, read first starting with `Installed Packages` in alphabetical order then go to `Packages`.  

So if a theme has its own tmPreferences and sublime-syntax file, Zukan icons will usually complete with icons that do not exist.  

`A File Icon` package will also override our icons. They have the first position in `Installed Packages` (A File Icon) and the last in `Packages` (zzz A File Icon zzz).  

It is same situation, Zukan icons will complete with icons that do not exist.

```
**Solution**
If user is using a theme or another icon package, and install Zukan icons.

The solution is to use Zukan icon for an icon that do not exist.

Overiding other packages icons in these situations is not possible currently, as explained above, without changing other packages.
```
