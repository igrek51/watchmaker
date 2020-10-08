#!/bin/bash

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# provide mounted partition name, not device
export OF=/dev/sdc1
# disks info
lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT
df .
CURRENT_PARTITION=$(df . | awk 'END{print $1}')
echo "Current partition: ${CURRENT_PARTITION}"

read -p "[WARNING] Attempting to test disk speed on $OF. Are you sure?"

echo "Testing write speed..."
sync && echo "BS=8k..."
dd if=/dev/zero of=$OF bs=8k count=8192 oflag=direct conv=fdatasync | grep bytes
sync && echo "BS=1M..."
dd if=/dev/zero of=$OF bs=1M count=64 oflag=direct conv=fdatasync | grep bytes
sync && echo "BS=64M..."
dd if=/dev/zero of=$OF bs=64M count=1 oflag=direct conv=fdatasync | grep bytes

echo "Testing read speed..."
sync && echo "BS=8k..."
dd if=$OF of=/dev/null bs=8k count=8192 iflag=direct | grep bytes
sync
dd if=$OF of=/dev/null bs=8k count=8192 iflag=direct | grep bytes
sync && echo "BS=1M..."
dd if=$OF of=/dev/null bs=1M count=64 iflag=direct | grep bytes
sync
dd if=$OF of=/dev/null bs=1M count=64 iflag=direct | grep bytes
sync && echo "BS=64M..."
dd if=$OF of=/dev/null bs=64M count=1 iflag=direct | grep bytes
sync
dd if=$OF of=/dev/null bs=64M count=1 iflag=direct | grep bytes

# clean up
#rm $OF
sync
echo "done"
