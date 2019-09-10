#!/bin/bash
export SQUASH_PATH=/media/user/data/ext/watchmaker/squash
export FS_SQUASH_PATH=$SQUASH_PATH/filesystem.squashfs
DATE=`date +%Y-%m-%d`
export TAGGED_SQUASH_PATH=$SQUASH_PATH/filesystem-${DATE}.squashfs

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cd /

rm -f $FS_SQUASH_PATH

mksquashfs \
	/bin /boot /dev /etc /home /lib /lib64 /media /mnt /opt /proc /run /root /sbin /srv /sys /tmp /usr /var \
	/initrd.img /initrd.img.old /vmlinuz /vmlinuz.old \
	$FS_SQUASH_PATH \
	-regex -ef $SQUASH_PATH/EXCLUDE_FILE \
	-comp gzip -b 512k \
	-keep-as-directory

unsquashfs -l $FS_SQUASH_PATH

echo "creating tagged copy: $TAGGED_SQUASH_PATH..."
cp $FS_SQUASH_PATH $TAGGED_SQUASH_PATH

sync

echo "done"