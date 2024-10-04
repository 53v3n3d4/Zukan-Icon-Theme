# Python Notes

> Sublime Text 4 uses python 3.8 and Sublime Text 3 uses Python 3.3  
Link https://www.sublimetext.com/docs/porting_guide.html#python-3-3  

> Build package uses python 3.12.3.  

> Plugin follow ST python versions.  

```
Package
├── src
|   ├── build # generate icons PNGs and icons data file
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
├── ruff.toml
└── unittesting.json
```

## Install

### Build

```sh
# Use specific python version
$ poetry env use path-to-python/3.12.3/bin/python
$ poetry env use /Users/xxxxx/.pyenv/versions/3.12.3/bin/python
$ poetry env info
Virtualenv
Python:         3.12.3
Implementation: CPython

# Check if .python-version file has correct version. Important for 'poetry install'.
# It could be 3.3 or 3.8 because Sublime Text interpreter.
$ cat .python-version
3.12.3

# install
$ poetry install
```

### Plugin

You may need to `Package Control: Satisfy Libraries` to install dependencies.  

```
# Select ST python interpreter in '.python-version' file
# 3.3 or 3.8
$ cat .python-version
3.3
```

## Poetry notes

- If package do not install using `poetry add <package>` or during `poetry install`, use `pip install <package>`  


## Tests

### Build tests

```sh
# Environment activated
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

> `test_scripts icon-theme command` delay tests. If need, comment it in `tests/mocks/constants_scripts.py`.  

#### Note

If error below show, it is because of a `DS_Store` file that was created in `tests/mocks` folder. To see `DS_Store`, change ST settings `file_exclude_patterns`.  

```sh
FAILED tests/build/test_create_icon_theme.py::TestCreateIconTheme::test_create_test_icon_theme[tests/mocks-tests/mocks-expected0] - AssertionError: assert ['test_no_ico...S_Store', ...] == ['test_no_ico...emes.py', ...]
FAILED tests/build/test_icons_preferences.py::TestPreferences::test_preferences_all[tests/mocks-tests/mocks-expected0] - AssertionError: assert ['test_no_ico...S_Store', ...] == ['test_no_ico...emes.py', ...]
FAILED tests/build/test_zukan_icons.py::TestZukanIcon::test_write_icon_data[tests/mocks-tests/mocks-tests/mocks/zukan_icons_data.pkl-expected0] - AssertionError: assert ['test_no_ico...S_Store', ...] == ['test_no_ico...emes.py', ...]
```

### Plugin tests

Using ST package `UnitTesting`.  

Go to `Tools > Command Palette...` select `UnitTesting: Test Package` type `Zukan Icon Theme`.  

> Tests files are not bundled with releases. Need to clone repo.  

> `.python-version` needs to be 3.8. There is no `subTest` in 3.3.

```
# .coveragerc
; Comment [paths] to coverage plugin
; [paths]
; source = src
```

## Build

Scripts used to generate icons files: PNGs and icon data file.  

See [build.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/build.md).  

## Plugin

Install icons tmPreferences, sublime-theme and sublime-syntax files.  

See [plugin.md](https://github.com/53v3n3d4/Zukan-Icon-Theme/blob/main/docs/plugin.md).  
