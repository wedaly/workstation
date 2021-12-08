# workstation
configure a workstation!

I use these to quickly set up new development environments for myself. They probably won't be useful for anyone else.

After bootstrapping an environment (see below), use [chezmoi](https://github.com/twpayne/chezmoi) to synchronize dotfiles.

# Bootstrap

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
