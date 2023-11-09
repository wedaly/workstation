# workstation
configure a workstation!

I use these to quickly set up new development environments for myself. They probably won't be useful for anyone else.

After bootstrapping an environment (see below), use [chezmoi](https://github.com/twpayne/chezmoi) to synchronize dotfiles.

# Bootstrap

## Fedora

Run the bootstrap script:
```
cd /tmp
curl https://raw.githubusercontent.com/wedaly/workstation/main/bootstrap/fedora.sh > bootstrap.sh
chmod +x bootstrap.sh
./bootstrap.sh
```

To use an existing Yubikey:
```
# pcscd fights with opensc on Fedora 34/35
# https://bugzilla.redhat.com/show_bug.cgi?id=1941346
sudo dnf remove opensc
sudo systemctl restart pcscd

# Workaround for "no keyserver available" error.
gpgconf --kill dirmngr

export KEYID=0xC1CAD9CDB82E69DE
gpg --keyserver pgp.mit.edu --recv-key $KEYID

# Select all keys, then "trust", then choose "ultimate"
gpg --edit-key $KEYID

gpg --card-status
gpg --list-secret-keys
```

Workaround for issue with Firefox:
```
# Add this to /usr/share/p11-kit/modules/opensc.module
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1892137
disable-in: firefox
```

## Ubuntu

Run the bootstrap script:
```
cd /tmp
curl https://raw.githubusercontent.com/wedaly/workstation/main/bootstrap/ubuntu.sh > bootstrap.sh
chmod +x bootstrap.sh
./bootstrap.sh
```

## Ubuntu on WSL2

1. Download an image like `ubuntu-22.04-server-cloudimg-amd64-root.tar.xz` from [https://cloud-images.ubuntu.com/releases/](https://cloud-images.ubuntu.com/releases/).

2. Decompress the `.xz` file.

3. In Powershell, create a new WSL distribution:
```
wsl.exe --import ubuntu-22.04-wsl .\Documents\ubuntu-22.04-wsl .\Downloads\ubuntu-22.04-server-cloudimg-amd64-root.tar
```

3. Run the bootstrap script:
```
wsl.exe -d ubuntu-22.04-wsl
cd /tmp
curl https://raw.githubusercontent.com/wedaly/workstation/main/bootstrap/wsl-ubuntu.sh > bootstrap.sh
chmod +x bootstrap.sh
./bootstrap.sh
```

4. Restart:
```
wsl.exe --shutdown ubuntu-22.04-wsl
wsl.exe -d ubuntu-22.04-wsl
```
