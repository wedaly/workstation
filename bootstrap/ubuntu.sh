#!/usr/bin/env sh

set -e

echo "updating system"
sudo apt update
sudo apt upgrade

echo "installing chezmoi"
export CHEZMOI_VERSION=2.15.0
(cd /tmp && wget https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}/chezmoi_${CHEZMOI_VERSION}_linux_amd64.deb && apt install ./chezmoi_${CHEZMOI_VERSION}_linux_amd64.deb)

echo "initializing chezmoi"
chezmoi upgrade && chezmoi init https://github.com/wedaly/workstation && chezmoi apply
