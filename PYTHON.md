# Python Notes

> Sublime Text 4 uses python 3.8 and Sublime Text 3 uses Python 3.3  
Link https://www.sublimetext.com/docs/porting_guide.html#python-3-3  

> Build package uses python 3.8.19, probably will try upgrade to latest later.

> Plugin follow ST python versions.

```
Package
├── src
|   ├── build # generate icons PNGs, syntaxes and preferences files
|   ├── data
|   ├── icons
│   └── zukan_icon_theme # plugin install files
├── tests
├── .coveragerc
├── .python.version
├── dependencies.json
├── main.py
├── pyproject.toml
├── pytest.ini
└── ruff.toml
```

## Install

```sh
# use specific python version
$ poetry env use path-to-python/3.8.19/bin/python
$ poetry env use /Users/xxxxx/.pyenv/versions/3.8.19/bin/python
$ poetry env info
Virtualenv
Python:         3.8.19
Implementation: CPython

# Check if .python-version file has correct version. Important for poetry install.
# It could be 3.3 or 3.8 because Sublime Text interpreter.
$ cat .python-version
3.8.19

# install
$ poetry install
```

## Poetry notes

- If package do not install using `poetry add <package>` or during `poetry install`, use `pip install <package>`  


## Tests

```sh
# Environment need to be activated
$ pytest
```
Or
```
$ poetry run pytest
```

To disable coverage (pytest-cov)  
```
# pytest.ini
# Comment line below to disable coverage
;addopts = --cov=src

# Pass other arguments
# See https://docs.pytest.org/en/8.0.x/reference/customize.html
addopts = -ra -q
```

## Build

Scripts used to generate icons files: pngs, syntaxes and preferences.  

See [build.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/build.md)

## Plugin

See [plugin.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/plugin.md)
