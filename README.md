Watchmaker Linux
================
Watchmaker is a portable Live Linux Sytem with persistence features.

The Watchmaker system is based on Debian and runs pretty well on USB pendrives, that's how it's intended to be used.
Its bootloader works with both BIOS and UEFI devices as well.

Watchmaker OS doesn't even need hard drive presence on the machine, because the base system image is loaded on the fly from USB disk to RAM using `overlayfs`, thus the sytem runs very fast regarding base system applications.
Other user-specific components (programs, games, data, etc), which requires changes persistence, can be stored on separate partition with write permissions.
Although, the writing speed performance may be slower, depending on USB device.

Watchmaker OS can be used in both manners:
- as a portable system with all the programs and needed data on a USB stick.
- as a tool for diagnosing and repairing other broken machines (that's why it's named `Watchmaker`).

Watchmaker can be booted in 3 different modes:
* **Live mode** - The base Linux system is loaded on the fly to RAM (not the entire, but only required components when necessary). Any change in the system is not persistent, but only separate `watchmodules` partition is fully persistent (can be modified).
* **Persistent mode** - like Live mode, but any modified system file is copied on write and stored on separate `persitence` partition. Although, this might be slow due to many writing operations on USB disk. On boot both RW and RO images are joined in the union FS.
* **Full RAM mode** - All the required system files are loaded to RAM, so it's even allowed to eject the USB from machine, leaving fully efficient running system.

It also has Debian installer on the board (as one of the booting options).

# Making USB with Live OS
In order to install Watchmaker on the USB stick, you need to download the squashed filesystem image. It's not included in the git repository, cause it's huge (about 3GB).
The latest one can be downloaded from [here](https://drive.google.com/drive/folders/1dM3Hzds_2qhJ9KLAo6CgsyE4K_-yaj75?usp=sharing). Save it to `squash/filesystem.squashfs`.

Check your disk device name (e.g. `/dev/sdd`) using `lsblk` or `sudo fdisk -l` command.

Then run `watchmake.py` script which will create all the partitions, bootloaders and save all the needed files:
```bash
./watchmake/watchmake.py create /dev/sdd
```

For more commands, see `./watchmake/watchmake.py --help`.

# Adding modules
Optional modules & custom data can be copied to `watchmodules` partition.

Some pre-defined modules are available [here](https://drive.google.com/drive/folders/12vn14uRO9fMJdfilrou3U5jd4cLzadAZ?usp=sharing).
For instance download `wine.zip` and save it to `modules/wine.zip`. Then run:
```bash
./watchmake/watchmake.py module wine
```

# Resquashing filesystem
If you need to make the applied changes persistent, you can rebuild `filesystem.squashfs` and swap it on the run on the USB drive.
1. Boot OS in Live RAM mode (making `filesystem.squashfs` writable)
2. Apply your changes
3. Update current OS with latest tools
```bash
watchmake prebuild
```
4. Rebuild squashed filesystem and swap it on the run
```bash
watchmake resquash
```
or
```bash
./watchmake/watchmake.py resquash --storage-path=/media/user/data/ext/watchmaker/squash
```

# Custom squashed filesystem
In order to run live OS you need squashed filesystem placed in `squash/filesystem.squashfs`.
You can either download latest [Watchmaker filesystem image](https://drive.google.com/drive/folders/1dM3Hzds_2qhJ9KLAo6CgsyE4K_-yaj75?usp=sharing) or start it from scratch by getting base image and applying custom changes on it:

1. Get [Debian Live CD ISO](https://www.debian.org/CD/live/)
2. Open ISO with archive manager and extract `live/filesystem.squashfs` from there.
3. Create Live USB using `watchmake create` and replace `live/filesystem.squashfs` with base Debian filesystem image.
4. Apply your custom changes in live system (checkout [postinstall.md](https://github.com/igrek51/watchmaker/blob/master/scripts/postinstall.md))
5. Use `watchmake resquash` to generate new filesystem, persist changes and replace image on the run.

# Software Prerequisites
* Python 3.6+
* Before running any of `watchmake.py` commands, install required packages. For Debian-based systems:
```bash
python3 -m pip install -r watchmake/requirements.txt
sudo apt install `cat watchmake/pkg-requirements.txt`
```

# Hardware Requirements
- USB stick with the Watchmaker Linux should have at least 8GB disk space.
- The machine running Watchmaker should have at least 4GB of RAM.

# Reference links
https://willhaley.com/blog/custom-debian-live-environment/
