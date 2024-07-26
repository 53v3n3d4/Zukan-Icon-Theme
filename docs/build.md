Build scripts used to create icons PNG and icons data file.  

```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py -h
# Poetry with env activated
$ build -h

# Env deactivated, with poetry
$ poetry run build -h
```

## Create icon theme
Create PNGs, zukan preferences and syntaxes files for icons.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py icon-theme --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py icon-theme -f src/data/afdesign.yaml
# Create PNGs, syntaxes and preferences files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py icon-theme --all
```

Using poetry scripts  
```sh
$ poetry run build icon-theme -f src/data/afdesign.yaml
# Create PNGs, syntaxes and preferences files
$ poetry run build icon-theme --all
```

## Create zukan icon data file
Create a data file, with all icons data, to be used by plugin.  

File will be created in `icons` folder.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py zukan-icon --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py zukan-icon --write
# Print file
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py zukan-icon --read
```

Using poetry scripts  
```sh
$ poetry run build zukan-icon --write
# Print file
$ poetry run build zukan-icon --read
```

## Clean SVG
Clean unused tags, ids and attributes in SVG.  

Affinity designer program, used to export SVGs, produce them with unsed tags that needs to be deleted. Error can raise depending on lib used.  

Also, exported SVGs use common ids names indexed that conflict when concat SVGs. These names are renamed when clean is used.  

Common id names: `_clip`, `_Effect`, `_Linear` and `_Gradient`.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean -f src/icons/afdesign.svg
# Clean all SVGs
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py clean --all
# After migrating all data files, this will data files instead of svg files.
```

Using poetry scripts  
```sh
$ poetry run build clean -f src/icons/afdesign.svg
# Clean all SVGs
$ poetry run build clean --all
```

## Concat SVG
Concat SVG file. It generates the SVG used in README and [file-icon.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/file-icon.md).  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py concat --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py concat -a
# Concat SVG file.
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py concat --all
# After migrating all data files, this will data files instead of svg files.
```

Using poetry scripts  
```sh
$ poetry run build concat -isa -isano 30
# Concat SVG file.
$ poetry run build concat --all --iconsperrow 6
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
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png -f src/data/afdesign.yaml
# Create all PNGs
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py png --all
```

Using poetry scripts  
```sh
$ poetry run build png -f src/data/afdesign.yaml
# Create all PNGs 
$ poetry run build png --all
```

## Create sublime-syntaxes
Create icons sublime-syntaxes.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax -f src/data/afdesign.yaml
# Create all sublime-syntax files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py syntax --all
```

Using poetry scripts  
```sh
$ poetry run build syntax -f src/data/afdesign.yaml
# Create all sublime-syntax files
$ poetry run build syntax --all
```

## Create tmPreferences
Create icons tmPreferences.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference -f src/data/afdesign.yaml
# Create all tnPreferences files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py preference --all
```

Using poetry scripts  
```sh
$ poetry run build preference -f src/data/afdesign.yaml
# Create all tnPreferences files
$ poetry run build preference --all
```

## Create test files extensions
Create icons themes files extensions.  

The test files will be created inside folder `tests_icon_theme`.  

Using argparse commands  
```sh
# Environment activated
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py test-icon-theme --help
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py test-icon-theme -f src/data/afdesign.yaml
# Create all test files extensions files
🚥 in ../Zukan-Icon-Theme$ python src/build/scripts.py test-icon-theme --all
```

Using poetry scripts  
```sh
$ poetry run build test-icon-theme -f src/data/afdesign.yaml
# Create all test files extensions files
$ poetry run build test-icon-theme --all
```

> Creating test files may raise parsing errors for files that ST use, like Sublime Text.sublime-syntax or Sublime Text.sublime-settings.
