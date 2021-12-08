#!/usr/bin/env sh

set -e

echo "creating user"
read -p "Enter username: " USERNAME
if [ -z "$USERNAME" ]; then echo "username is required"; exit 1; fi
useradd -m -G sudo -s /bin/bash "$USERNAME"
passwd "$USERNAME"
tee /etc/wsl.conf <<_EOF
[user]
default=$USERNAME
_EOF

echo "updating system"
apt update
apt upgrade

echo "installing chezmoi"
export CHEZMOI_VERSION=2.9.2
(cd /tmp && wget https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}/chezmoi_${CHEZMOI_VERSION}_linux_amd64.deb && apt install ./chezmoi_${CHEZMOI_VERSION}_linux_amd64.deb)

echo "initializing chezmoi"
su $USERNAME --pty -c "chezmoi init https://github.com/wedaly/workstation && chezmoi apply"
