# update initrfs
update-initramfs -u -k all

# create respin fs
sudo respin clean
sudo respin dist cdfs

# 'persistence' ext4 partition
echo / union > persistence.conf

# show sync progress
sync
watch -n 1 grep -e Dirty: -e Writeback: /proc/meminfo

# install primary bootloader on MBR
dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/mbr/mbr.bin of=/dev/sdc

# install grub on usb
grub-install --removable --boot-directory=/media/igrek/os/boot /dev/sdx
grub-install --target=i386-pc --boot-directory=/media/igrek/os/boot /dev/sdx

# test: boot usb
qemu-system-x86_64 -hda /dev/sdc


# Making live BIOS/UEFI x86_64/i386 USB
- read disk id (fdisk -l / lsblk):
	export disk=/dev/sdc
- create MBR partition table (gnome-disks / gparted)
- create 1. FAT32 partition (512 MB) named 'efi' (gnome-disks / gparted)
- create 2. ext4 partition (~4 GB) named 'live' with 'boot' flag (gnome-disks / gparted)
- create 3. ext4 partition (remaining space) named 'persistence' (gnome-disks / gparted)
- write primary MBR bootloader:
	dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/mbr/mbr.bin of=${disk}
- mount partitions:
	mount ${disk}1 /mnt/efi
	mount ${disk}2 /mnt/usb
- write VBR bootloaders:
	grub-install --target=x86_64-efi --efi-directory=/mnt/efi --boot-directory=/mnt/usb/boot --removable --recheck
	grub-install --target=i386-efi --efi-directory=/mnt/efi --boot-directory=/mnt/usb/boot --removable --recheck
	grub-install --target=i386-pc --boot-directory=/mnt/usb/boot --recheck $disk
- copy GRUB config (/mnt/usb/boot/grub/grub.cfg)
- copy live OS files (/mnt/usb)
- copy data to 'persistence' partition
- sync:
	sync
	watch -n 1 grep -e Dirty: -e Writeback: /proc/meminfo
- unmount disks
	umount ${disk}1
	umount ${disk}2