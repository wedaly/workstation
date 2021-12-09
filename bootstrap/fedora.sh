#!/usr/bin/env sh

echo "installing chezmoi"
export CHEZMOI_VERSION=2.9.2
(cd /tmp && wget https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}/chezmoi-${CHEZMOI_VERSION}-x86_64.rpm)
sudo dnf install /tmp/chezmoi-${CHEZMOI_VERSION}-x86_64.rpm

echo "initializing chezmoi"
chezmoi init https://github.com/wedaly/workstation && chezmoi apply
