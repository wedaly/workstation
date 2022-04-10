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
# pcscd fights with another daemon on Fedora 34/35, so disable it.
sudo systemctl disable pcscd
sudo systemctl stop pcscd

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

## Ubuntu on WSL2

1. Download an image like `ubuntu-20.04-server-cloudimg-amd64-wsl.rootfs.tar.gz` from [https://cloud-images.ubuntu.com/releases/](https://cloud-images.ubuntu.com/releases/).

2. In Powershell, create a new WSL distribution:
```
wsl.exe --import ubuntu-20.04-wsl .\Documents\ubuntu-20.04-wsl .\Downloads\ubuntu-20.04-server-cloudimg-amd64-wsl.rootfs.tar.gz
```

3. Run the bootstrap script:
```
wsl.exe -d ubuntu-20.04-wsl
cd /tmp
curl https://raw.githubusercontent.com/wedaly/workstation/main/bootstrap/wsl-ubuntu.sh > bootstrap.sh
chmod +x bootstrap.sh
./bootstrap.sh
```

4. Restart:
```
wsl.exe --shutdown ubuntu-20.04-wsl
wsl.exe -d ubuntu-20.04-wsl
```

## macOS

1. Install [homebrew](https://docs.brew.sh/Installation)
2. Change shell to bash: `chsh -s /bin/bash`
3. Install chezmoi: `brew install chezmoi`
4. Apply config: `chezmoi init http://github.com/wedaly/workstation.git && chezmoi apply`
