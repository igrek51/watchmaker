#!/bin/bash
set -ex

DATE=`date +%Y-%m-%d`

export SQUASH_STORAGE_PATH=/media/user/data/ext/watchmaker/squash
export SQUASH_FS_STORAGE_PATH=$SQUASH_STORAGE_PATH/filesystem.squashfs
export TAGGED_SQUASH_PATH=$SQUASH_STORAGE_PATH/filesystem-${DATE}.squashfs
export TARGET_SQUASH=/media/user/boot/live/filesystem.squashfs

# root only
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# ensure mount points are mounted
test -d $SQUASH_STORAGE_PATH
test -f $TARGET_SQUASH

cd /

rm -f $SQUASH_FS_STORAGE_PATH
sync

echo "squashing filesystem..."
mksquashfs \
	/bin /boot /dev /etc /home /lib /lib64 /media /mnt /opt /proc /run /root /sbin /srv /sys /tmp /usr /var \
	/initrd.img /initrd.img.old /vmlinuz /vmlinuz.old \
	$SQUASH_FS_STORAGE_PATH \
	-regex -ef $SQUASH_STORAGE_PATH/EXCLUDE_FILE \
	-comp gzip -b 512k \
	-keep-as-directory

echo "creating tagged copy: $TAGGED_SQUASH_PATH..."
cp $SQUASH_FS_STORAGE_PATH $TAGGED_SQUASH_PATH
sync

echo "removing old squashfs: $TARGET_SQUASH"
rm -f $TARGET_SQUASH

echo "rsync"
rsync -ah --progress $SQUASH_FS_STORAGE_PATH $TARGET_SQUASH
echo "Syncing..."
sync

echo "source checksum:"
cksum $SQUASH_FS_STORAGE_PATH
echo "target checksum:"
cksum $TARGET_SQUASH

echo "done"
