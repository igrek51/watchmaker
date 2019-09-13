#!/bin/bash
export SOURCE_SQUASH=/media/user/data/ext/watchmaker/squash/filesystem.squashfs
export TARGET_SQUASH=/media/user/live/live/filesystem.squashfs

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
