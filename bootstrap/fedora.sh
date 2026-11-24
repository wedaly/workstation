#!/usr/bin/env sh

echo "installing chezmoi"
sudo dnf install chezmoi

echo "initializing chezmoi"
chezmoi init https://github.com/wedaly/workstation && chezmoi apply
