Build scripts used to create icons pngs, sublime-syntaxes and tmPreferences.  

```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$  python src/build/scripts.py -h

# Or, with poetry
$ peotry run build -h
```

## Create icon theme
Create pngs, sublime-syntax and tmPreferences files for icon.  

Using argparse commands  
```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$  python src/build/scripts.py icon-theme -h
🚥 in ../Zukan-Icon-Theme$  python src/build/scripts.py icon-theme -f src/data/afdesign.yaml
# Create all pngs, sublime-syntax and tmPreferences
🚥 in ../Zukan-Icon-Theme$  python src/build/scripts.py icon-theme -a
# After doing all data files, this will data files instead of svg files.
```

Using argparse trough poetry scripts  
```sh
$ poetry run build icon-theme -f src/data/afdesign.yaml
# Create all pngs, sublime-syntax and tmPreferences
$ poetry run build icon-theme -a
```

## Clean SVG
Clean unused tags and attributes in SVG.  

Affinity designer program, used to export SVGs, produce them with unsed tags that needs to be deleted. Error can raise depending on lib used.  

Using argparse commands  
```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean -h
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean -f src/icons/afdesign.svg
# Clean all SVGs
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean -a
# After migrating all data files, this will data files instead of svg files.
```

Using argparse trough poetry scripts  
```sh
$ poetry run build clean -f src/icons/afdesign.svg
# Clean all SVGs
$ poetry run build clean -a
```

## Generate PNGs
Generate PNGs file from SVGs.  

Create PNG icons in 3 sizes, Size and suffix details comes from png_details.py.  

| name | sizes |
|-----------|------|
| (icon-name).png | 18px x 16px |
| (icon-name)@2x.png: | 36px x 32px |
| (icon-name)@3x.png: | 54px x 48px |

Using argparse commands  
```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png -h
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png -f src/data/afdesign.yaml
# Create all PNGs
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png -a
# After doing all data files, this will data files instead of svg files.
```

Using argparse trough poetry scripts  
```sh
$ poetry run build png -f src/data/afdesign.yaml
# Create all PNGs 
$ poetry run build png -a
```

## Create sublime-syntaxes
Create icons sublime-syntaxes.  

Using argparse commands  
```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax -h
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax -f src/data/afdesign.yaml
# Create all sublime-syntax files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax -a
# After doing all data files, this will data files instead of svg files.
```

Using argparse trough poetry scripts  
```sh
$ poetry run build syntax -f src/data/afdesign.yaml
# Create all sublime-syntax files
$ poetry run build syntax -a
```

## Create tmPreferences
Create icons tmPreferences.  

Using argparse commands  
```sh
# Environment need to be activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference -h
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference -f src/data/afdesign.yaml
# Create all sublime-syntax files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference -a
# After doing all data files, this will data files instead of svg files.
```

Using argparse trough poetry scripts  
```sh
$ poetry run build preference -f src/data/afdesign.yaml
# Create all sublime-syntax files
$ poetry run build preference -a
```

