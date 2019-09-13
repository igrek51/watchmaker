#!/bin/bash
export SOURCE_DISK=/dev/sdx
export TARGET_DISK=/dev/sdy

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

sudo fdisk -l

lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT

read -p "[WARNING] Attempting to clone $SOURCE_DISK to $TARGET_DISK. Are you sure?"

echo "Cloning $SOURCE_DISK to $TARGET_DISK..."
dd if=$SOURCE_DISK of=$TARGET_DISK bs=64K conv=noerror,sync status=progress
echo "Syncing..."
sync
echo "done"
