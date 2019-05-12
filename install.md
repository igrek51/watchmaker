# Making USB
```bash
su
cd /mnt/data/ext/watchmaker
```

## find dev disk name
```bash
# check which one of the disks is your USB stick
lsblk
fdisk -l

export disk=/dev/sdc
```

## Create MBR
```bash
parted --script $disk \
    mklabel msdos
```

## Create partitions
(Using gnome-disks or gparted)
1. GRUB boot - Primary partition: FAT32, boot + lba flag, 4.5GiB, label: boot
2. EFI - Primary partition: FAT32, esp flag, 200MiB, label: EFI
3. Persistence - Primary partition: ext4, 1.5GiB, label: persistence
4. USB data - Primary partition: ext4, 100%, label: usb-data

or parted (then need to mkfs partition filesystems)
```bash
parted --script $disk \
	mkpart primary fat32 1MiB 4.5GiB \
	set 1 lba on \
	set 1 boot on \
	mkpart primary fat32 4.5GiB 4.7GiB \
	set 2 esp on \
	mkpart primary ext4 4.7GiB 6.2GiB \
	mkpart primary ext4 6.2GiB 100%
```

## Mount partitions
```bash
# mount
mkdir -p /mnt/boot
mkdir -p /mnt/efi
mkdir -p /mnt/persistence
mkdir -p /mnt/usb-data
mount ${disk}1 /mnt/boot
mount ${disk}2 /mnt/efi
mount ${disk}3 /mnt/persistence
mount ${disk}4 /mnt/usb-data
```

## Grub bootloader
```bash
# Install grub EFI
grub-install \
	--target=i386-efi \
	--efi-directory=/mnt/boot \
	--boot-directory=/mnt/boot/boot \
	--removable --recheck
grub-install \
	--target=x86_64-efi \
	--efi-directory=/mnt/boot \
	--boot-directory=/mnt/boot/boot \
	--removable --recheck
grub-install \
	--target=i386-efi \
	--efi-directory=/mnt/efi \
	--boot-directory=/mnt/boot/boot \
	--removable --recheck
grub-install \
	--target=x86_64-efi \
	--efi-directory=/mnt/efi \
	--boot-directory=/mnt/boot/boot \
	--removable --recheck
# Install Grub for i386-pc booting.
grub-install \
	--target=i386-pc \
	--boot-directory=/mnt/boot/boot \
	--recheck \
	$disk

sync
```

## EFI Microsoft workaround
```
mkdir -p /mnt/efi/EFI/Microsoft
mkdir -p /mnt/boot/EFI/Microsoft
cp -r /mnt/efi/EFI/BOOT /mnt/efi/EFI/Microsoft/
cp -r /mnt/boot/EFI/BOOT /mnt/boot/EFI/Microsoft/
```

## GRUB config
```bash
cp content/grub/grub.cfg /mnt/boot/boot/grub/
cp content/grub/background.png /mnt/boot/boot/grub/
cp content/grub/font.pf2 /mnt/boot/boot/grub/
cp content/grub/loopback.cfg /mnt/boot/boot/grub/
cp content/grub/GRUB_FINDME /mnt/boot/
```

## Boot base files
```bash
cp -r content/boot-files/[BOOT] /mnt/boot/
cp -r content/boot-files/d-i /mnt/boot/
cp -r content/boot-files/dists /mnt/boot/
cp -r content/boot-files/live /mnt/boot/
cp -r content/boot-files/pool /mnt/boot/
cp -r content/boot-files/.disk /mnt/boot/

cp -r content/boot-files/[BOOT] /mnt/efi/
cp -r content/boot-files/dists /mnt/efi/
cp -r content/boot-files/live /mnt/efi/
cp -r content/boot-files/pool /mnt/efi/
cp -r content/boot-files/.disk /mnt/efi/
```

## Persistence configuration
```bash
cp -r content/persistence/persistence.conf /mnt/persistence/
```

## Copy squash filesystem
```bash
cp squash/filesystem.squashfs /mnt/boot/live/
```

## Copy usb-data modules
```bash
# dev-data
cp -r modules/dev-data /mnt/usb-data/

mkdir -p /mnt/usb-data/modules
# make it writable to user
sudo chown igrek /mnt/usb-data -R

cp -r modules/init /mnt/usb-data/modules/
cp -r modules/android-sdk /mnt/usb-data/modules/
cp -r modules/android-studio /mnt/usb-data/modules/
cp -r modules/aoe2 /mnt/usb-data/modules/
cp -r modules/heroes3-hota /mnt/usb-data/modules/
cp -r modules/warcraft-3-pl /mnt/usb-data/modules/
```

## unmount
```bash
sync
umount /mnt/boot
umount /mnt/efi
umount /mnt/persistence
umount /mnt/usb-data
```


# Updating filesystem
On live system (live or toRAM), making new squashing new filesystem

## New version number
```bash
cat << 'EOF' > ~/.osversion
v2.11
EOF
```

## pre-clean:
```bash
sudo apt clean
sudo apt autoremove

rm -r ~/.cache
sudo rm -r /root/.cache
```

## build squash
1. mount /media/user/data
2. cd /home/user/tools/squash
3. su
4. ./build-squash.sh

## Replace filesystem.squashfs:
```bash
cp squash/filesystem.squashfs /mnt/boot/live/
sync
```
or on live (toRAM):
```bash
#!/bin/bash
export SOURCE_SQUASH=/media/user/data/ext/watchmaker/squash/filesystem.squashfs
export TARGET_SQUASH=/media/user/boot/live/filesystem.squashfs

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo "source checksum:"
cksum $SOURCE_SQUASH

read -p "[WARNING] Attempting to replace squash from $SOURCE_SQUASH to $TARGET_SQUASH. Are you sure?"

echo "removing old squashfs: $TARGET_SQUASH"
rm -f $TARGET_SQUASH

echo "rsync"
rsync -ah --progress $SOURCE_SQUASH $TARGET_SQUASH

echo "Syncing..."
sync

echo "source checksum:"
cksum $SOURCE_SQUASH
echo "target checksum:"
cksum $TARGET_SQUASH

echo "done"
```


# Making ISO
```bash
export SOURCE_DISK=/dev/sdc
export VERSION=v2.5
export TARGET_ISO=iso/watchmaker-base-amd64-${VERSION}.iso

lsblk
fdisk -l $SOURCE_DISK

echo "Units: sectors of 1 * 512 = __bs__ bytes"
export BS_SIZE=512
read -p "unit size: bs=$BS_SIZE, OK?"

echo "Device     Boot   Start      End Sectors  Size Id Type"
echo "/dev/sdc3        8595456  __END__ 1048576  512M 83 Linux"
export END_SECTOR=13533183
read -p "end sector: count=$END_SECTOR, OK?"

lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT

read -p "[WARNING] Attempting to write $SOURCE_DISK to $TARGET_ISO. Are you sure?"

echo "Writing $SOURCE_DISK to $TARGET_ISO..."
dd if=$SOURCE_DISK of=$TARGET_ISO bs=$BS_SIZE count=$END_SECTOR conv=noerror,sync status=progress
echo "Syncing..."
sync
```


# Reference Links
https://willhaley.com/blog/custom-debian-live-environment/
