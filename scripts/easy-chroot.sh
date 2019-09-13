#!/bin/bash
export CHDIR=/mnt/chroot
mkdir -p $CHDIR

#mount /dev/sda3 $CHDIR

#mkdir -p $CHDIR/proc
#mkdir -p $CHDIR/sys
#mkdir -p $CHDIR/dev

mount --bind /proc $CHDIR/proc
mount --bind /dev $CHDIR/dev
mount --bind /dev/pts $CHDIR/dev/pts
#mount --bind /sys $CHDIR/sys

# Networking problem
#cp /etc/hosts ${CHDIR}/etc/hosts
#cp /etc/resolv.conf ${CHDIR}/etc/resolv.conf

echo "[WARN] Diving into the /mnt/chroot..."
chroot $CHDIR /bin/bash
echo "[WARN] chroot exited."

umount ${CHDIR}/dev/pts
umount ${CHDIR}/dev
umount ${CHDIR}/proc
#umount ${CHDIR}/sys
