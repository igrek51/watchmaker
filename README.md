Watchmaker Linux
================
Watchmaker is a portable Live Linux Sytem with persistence features.

The Watchmaker system is based on Debian and runs pretty well on USB pendrives.
Its bootloader works with both BIOS and UEFI devices.
It doesn't even need hard drive presence on the machine, because the base system image is loaded on the fly from USB disk to RAM using `overlayfs`, so the sytem is very fast.
Other components (programs, games, data, etc), which requires changes persistence, might be stored on separate partition with write permissions.
Although, the writing speed performance may be slow, depending on USB device.

It can be used as a portable system with all the programs and data you need on a USB stick.

It also has tools for diagnosing and repairing other broken machines (that's why it's named `Watchmaker`).

Watchmaker can be booted in 3 different modes:
* **Live mode** - The base Linux system is loaded on the fly to RAM (not the entire, but only required components when necessary). Any change in the system is not persistent, only separate `data` partition is fully persistent (can be modified).
* **Persistent mode** - like Live mode, but any modified system file is copied on write and stored on separate `persitence` partition. This might be slow due to many writing operations on USB disk. On boot both RW and RO images are joined in the union FS.
* **full RAM mode** - All the required system files are loaded to RAM, so it's even allowed to eject the USB from machine, leaving fully efficient running system.

It also has Debian installer on the board (as one of the booting options).

# Making USB
In order to install Watchmaker on the USB stick, you need to download the squashed filesystem image. It's not included in the git repository, cause it's huge (about 3.5GB).
It can be downloaded from [here](https://drive.google.com/drive/folders/1FbVHMHunX0wT5GI0DPFMLswnBw5EHA7S?usp=sharing). Save it to `squash/filesystem.squashfs`.

Check the disk device name (`/dev/sdd`) with `lsblk` or `sudo fdisk -l` command.

Then run `watchmake.py` script which will create all the partitions and save all the needed files:
```bash
tools/watchmake/watchmake.py flash /dev/sdd
```

Optional modules can be copied to `usb-data` partition.

# Requirements
- USB stick with the Watchmaker Linux should have at least 8GB disk space.
- The machine running Watchmaker should have at least 4GB of RAM.
