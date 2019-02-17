#!/bin/bash
export TARGET_DISK=/dev/sdc
export MBR_FILE=watchmaker-mbr.img

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

sudo fdisk -l $SOURCE_DISK

lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT

read -p "[WARNING] Attempting to write MBR $MBR_FILE to disk $TARGET_DISK. Are you sure?"

echo "Writing $MBR_FILE to $TARGET_DISK..."
dd if=$MBR_FILE of=$TARGET_DISK bs=446 count=1
echo "Syncing..."
sync
echo "done"
