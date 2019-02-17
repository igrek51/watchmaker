#!/bin/bash
export TEST_PARTITION=/media/igrek/ext4
export TEST_FILE=SPEED_TEST

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

export OF=${TEST_PARTITION}/${TEST_FILE}
export OF=/dev/sdc
# disks info
lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT
df $TEST_PARTITION
CURRENT_PARTITION=$(df . | awk 'END{print $1}')
echo "Current partition: ${CURRENT_PARTITION}"

read -p "[WARNING] Attempting to test disk speed on $TEST_PARTITION. Are you sure?"

echo "Testing write speed..."
sync && echo "BS=8k..."
dd if=/dev/zero of=$OF bs=8k count=8192 oflag=direct conv=fdatasync 2>&1 | grep bytes
sync && echo "BS=1M..."
dd if=/dev/zero of=$OF bs=1M count=64 oflag=direct conv=fdatasync 2>&1 | grep bytes
sync && echo "BS=64M..."
dd if=/dev/zero of=$OF bs=64M count=1 oflag=direct conv=fdatasync 2>&1 | grep bytes

echo "Testing read speed..."
sync && echo "BS=8k..."
dd if=$OF of=/dev/null bs=8k count=8192 iflag=direct 2>&1 | grep bytes
sync
dd if=$OF of=/dev/null bs=8k count=8192 iflag=direct 2>&1 | grep bytes
sync && echo "BS=1M..."
dd if=$OF of=/dev/null bs=1M count=64 iflag=direct 2>&1 | grep bytes
sync
dd if=$OF of=/dev/null bs=1M count=64 iflag=direct 2>&1 | grep bytes
sync && echo "BS=64M..."
dd if=$OF of=/dev/null bs=64M count=1 iflag=direct 2>&1 | grep bytes
sync
dd if=$OF of=/dev/null bs=64M count=1 iflag=direct 2>&1 | grep bytes

# clean up
#rm $OF
sync
echo "done"
