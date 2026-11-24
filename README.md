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

## Ubuntu

Run the bootstrap script:
```
cd /tmp
curl https://raw.githubusercontent.com/wedaly/workstation/main/bootstrap/ubuntu.sh > bootstrap.sh
chmod +x bootstrap.sh
./bootstrap.sh
```

## macOS

1. Install [homebrew](https://docs.brew.sh/Installation)
2. Change shell to bash: `chsh -s /bin/bash`
3. Install chezmoi: `brew install chezmoi`
4. Apply config: `chezmoi init https://github.com/wedaly/workstation.git && chezmoi apply`
