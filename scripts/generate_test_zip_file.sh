#!/bin/sh

# Prepare and generate sublime-package for testing, similar to first install.
#
# Prepare steps:
# - Exclude folders, 'icons_preferences' and 'icons_syntaxes', and
#   settings files, 'user_ui_settings' and 'zukan_current_settings'
# - Create zip file
# - Move project folder to parent directory
# - Move zip file to 'Installed Packages'

folders=("icons_preferences" "icons_syntaxes")
files=("user_ui_settings.pkl" "zukan_current_settings.pkl")
sublime_dir="sublime"
project_name="Zukan Icon Theme"
installed_packages_dir="Installed Packages"

cd ../"$project_name"
# echo $PWD

echo "Deleting folders and files."

for i in "${folders[@]}"; do
  find . -name $i -type d -prune -exec rm -r "{}" +
done

for i in "${files[@]}"; do
  find $sublime_dir -name $i -type f -delete
done

zip -r 'Zukan Icon Theme.sublime-package' ./* -X '*.DS_Store'

echo "Zip file has been created."

# Move project foler to parent directory and zip file to 'Installed
# Packages'.
mkdir -p ../../"$project_name"
(shopt -s dotglob && mv * ../../"$project_name")

mv ../../"$project_name"/"$project_name".sublime-package ../../"$installed_packages_dir"

cd .. && rm -rf "$project_name"

echo "Zip file moved to 'Installed Packages'."
