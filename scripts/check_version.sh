#!/bin/sh

# Check package version in files before release.
version_in_settings=$(perl -nle'print $& while 
  m{(?<="version": ")[^"\\]*(?:\\.[^"\\]*)*}g' sublime/Zukan\ Icon\ Theme.sublime-settings)
# version_in_settings=0.3.10

version_in_pyproject=$(perl -nle'print $& while 
  m{(?<=version = ")[^"\\]*(?:\\.[^"\\]*)*}g' pyproject.toml)
# version_in_pyproject=0.3.3

version_in_changelog=$(awk -F '[][]' 'FNR == 3 { print $2 }' CHANGELOG.md)
# version_in_changelog=0.3.5

CYAN=$(tput setaf 123) #6
GRAY=$(tput setaf 255)
NORMAL=$(tput sgr0)
RED=$(tput setaf 203) #1
YELLOW=$(tput setaf 228) #3

# Code adapted from 
# https://www.unix.com/shell-programming-and-scripting/
# 186383-how-compare-version-values-shell-script.html
# @(#) user4	Compare version numbers of form a.b.c.
# Adapted from post # 10.
# https://www.unix.com/unix-dummies-questions-answers/
# 93739-comparing-version-numbers.html#post302269675

pe() {
  for _i; do printf "%s" "$_i"; done
  printf "\n"
}

# compare version numbers
# usage: vercmp <versionnr1> <versionnr2>
#         with format for versions xxx.xxx.xxx
# returns: 0 if versionnr1 equal or greater
#          1 if versionnr1 lower

vercmp()
{
  local a1 b1 c1 a2 b2 c2
  # echo|read succeeds in ksh, but fails in bash.
  # bash alternative is "set --"
  v1=$1
  v2=$2

  set -- $( echo "$v1" | sed 's/\./ /g' )
  a1=$1 b1=$2 c1=$3
  set -- $( echo "$v2" | sed 's/\./ /g' )
  a2=$1 b2=$2 c2=$3

  ret=$(( (a1-a2)*1000000+(b1-b2)*1000+c1-c2 ))

  if [ $ret -lt 0 ]; then
    v=-1
  elif [ $ret -eq 0 ]; then
    v=0
  else
    v=1
  fi
  printf "%d" $v
  return
}

pe
pe "Comparing version strings in files:"
pe "${YELLOW}- Zukan Icon Theme.sublime-settings -> $version_in_settings
- pyproject.toml -> $version_in_pyproject
- CHANGELOG.MD -> $version_in_changelog${NORMAL}"
pe

v=$( vercmp $version_in_settings $version_in_pyproject )
v1=$( vercmp $version_in_pyproject $version_in_changelog )

if [[ $v -eq 0 && $v1 -eq 0 ]]; then
  pe "${CYAN}Versions are equal${NORMAL}"
else
  pe "${RED}Versions are not equal${NORMAL}"
fi
pe

exit 0
