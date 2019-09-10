#!/bin/bash
export SOURCE_DISK=/dev/sdc
export TARGET_ISO=../iso/watchmaker-base-amd64-v2.5.iso

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

lsblk

sudo fdisk -l $SOURCE_DISK

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
echo "done"

#mkisofs
