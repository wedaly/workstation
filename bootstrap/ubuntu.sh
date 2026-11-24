#!/usr/bin/env sh

set -e

echo "updating system"
sudo apt update
sudo apt upgrade

echo "installing chezmoi"
sudo apt install chezmoi

echo "initializing chezmoi"
chezmoi init https://github.com/wedaly/workstation && chezmoi apply
