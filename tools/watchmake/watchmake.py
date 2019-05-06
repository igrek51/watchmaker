#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from glue import *
import os

DRY_RUN = False


def wrap_shell(cmd, *args):
    if args:
        cmd = cmd.format(*args)
    cmd = cmd.strip()
    debug('> ' + cmd)
    if not DRY_RUN:
        shell(cmd)


def flash_disk(disk):
    warn('writing to disk {}'.format(disk))
    wrap_shell('df {}', disk)

    info('creating MBR')
    wrap_shell('''
wipefs {}
    ''', disk)
    wrap_shell('''
parted --script {} \\
    mklabel msdos
    ''', disk)

    info('creating partitions space')
    wrap_shell('''
parted --script {} \\
    mkpart primary fat32 1MiB 4608MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 4608MiB 4813MiB \\
    set 2 esp on \\
    mkpart primary ext4 4813MiB 6349MiB \\
    mkpart primary ext4 6349MiB 100%
    ''', disk)

    wrap_shell('sync')

    info('making boot partition filesystem')
    wrap_shell('''
mkfs.fat -F32 {}1
    ''', disk)
    info('making EFI partition filesystem')
    wrap_shell('''
mkfs.fat -F32 {}2
    ''', disk)
    info('making persistence partition filesystem')
    wrap_shell('''
mkfs.ext4 -F {}3
    ''', disk)
    info('making usb-data partition filesystem')
    wrap_shell('''
mkfs.ext4 -F {}4
    ''', disk)

    wrap_shell('sync')

    info('setting partition names')
    wrap_shell('''
mlabel -i {}1 ::boot
mlabel -i {}2 ::EFI
e2label {}3 persistence
e2label {}4 usb-data
    ''', disk, disk, disk, disk)

    wrap_shell('sync')

    info('mounting partitions')
    wrap_shell('''
mkdir -p /mnt/watchmaker
mkdir -p /mnt/watchmaker/boot
mkdir -p /mnt/watchmaker/efi
mkdir -p /mnt/watchmaker/persistence
mkdir -p /mnt/watchmaker/usb-data
mount {}1 /mnt/watchmaker/boot
mount {}2 /mnt/watchmaker/efi
mount {}3 /mnt/watchmaker/persistence
mount {}4 /mnt/watchmaker/usb-data
    ''', disk, disk, disk, disk)

    info('installing GRUB EFI bootloaders')
    wrap_shell('''
grub-install \\
    --target=i386-efi \\
    --efi-directory=/mnt/watchmaker/boot \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell('''
grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/boot \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell('''
grub-install \\
    --target=i386-efi \\
    --efi-directory=/mnt/watchmaker/efi \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell('''
grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/efi \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')

    info('installing GRUB i386-pc bootloader')
    wrap_shell('''
grub-install \\
    --target=i386-pc \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --recheck \\
    {}
    ''', disk)

    wrap_shell('sync')

    info('making EFI Microsoft workaround')
    wrap_shell('''
mkdir -p /mnt/watchmaker/efi/EFI/Microsoft
mkdir -p /mnt/watchmaker/boot/EFI/Microsoft
cp -r /mnt/watchmaker/efi/EFI/BOOT /mnt/watchmaker/efi/EFI/Microsoft/
cp -r /mnt/watchmaker/boot/EFI/BOOT /mnt/watchmaker/boot/EFI/Microsoft/
    ''')

    info('GRUB config')
    wrap_shell('''
cp content/grub/grub.cfg /mnt/watchmaker/boot/boot/grub/
cp content/grub/background.png /mnt/watchmaker/boot/boot/grub/
cp content/grub/font.pf2 /mnt/watchmaker/boot/boot/grub/
cp content/grub/loopback.cfg /mnt/watchmaker/boot/boot/grub/
cp content/grub/GRUB_FINDME /mnt/watchmaker/boot/
    ''')

    info('Boot base files')
    wrap_shell('''
cp -r content/boot-files/[BOOT] /mnt/watchmaker/boot/
cp -r content/boot-files/d-i /mnt/watchmaker/boot/
cp -r content/boot-files/dists /mnt/watchmaker/boot/
cp -r content/boot-files/live /mnt/watchmaker/boot/
cp -r content/boot-files/pool /mnt/watchmaker/boot/
cp -r content/boot-files/.disk /mnt/watchmaker/boot/
    ''')
    wrap_shell('''
cp -r content/boot-files/[BOOT] /mnt/watchmaker/efi/
cp -r content/boot-files/dists /mnt/watchmaker/efi/
cp -r content/boot-files/live /mnt/watchmaker/efi/
cp -r content/boot-files/pool /mnt/watchmaker/efi/
cp -r content/boot-files/.disk /mnt/watchmaker/efi/
    ''')

    info('Persistence configuration')
    wrap_shell('''
cp -r content/persistence/persistence.conf /mnt/watchmaker/persistence/
    ''')

    info('Copying squash filesystem')
    wrap_shell('''
cp squash/filesystem.squashfs /mnt/watchmaker/boot/live/
    ''')

    info('Copying base usb-data modules')
    wrap_shell('''
cp -r modules/dev-data /mnt/watchmaker/usb-data/
    ''')
    wrap_shell('''
mkdir -p /mnt/watchmaker/usb-data/modules
    ''')
    wrap_shell('''
cp -r modules/init /mnt/watchmaker/usb-data/modules/
    ''')
    info('make usb-data writable to non-root user')
    wrap_shell('''
chown igrek /mnt/watchmaker/usb-data -R
    ''')

    info('unmounting')
    wrap_shell('sync')
    wrap_shell('''
umount /mnt/watchmaker/boot
umount /mnt/watchmaker/efi
umount /mnt/watchmaker/persistence
umount /mnt/watchmaker/usb-data
    ''')

    info('done')
    print_modules()


def action_flash(ap: ArgsProcessor):
    global DRY_RUN
    DRY_RUN = ap.is_flag_set('dry')

    set_workdir(os.path.join(script_real_dir(), '..', '..'))

    if os.geteuid() != 0:
        raise PermissionError('This script must be run as root')

    disk = ap.get_param('disk', required=True)
    shell('lsblk')

    if not ap.is_flag_set('yes'):
        warn('Are you sure, you want to write to {} disk?'.format(disk))
        while input_required('[yes/no]... ') != 'yes':
            pass
    flash_disk(disk)


def print_modules():
    info('Optional modules:')
    modules = [
        'android-sdk - /mnt/data/ext/watchmaker/modules/android-sdk.zip',
        'android-studio - /mnt/data/ext/watchmaker/modules/android-studio.zip',
        'dev-data',
        'init',
        'factorio - /mnt/games/linux-games/factorio',
        'aoe2 - /mnt/data/ext/live-games/aoe2',
        'heroes3-hota - /mnt/data/ext/live-games/heroes3-hota',
        'warcraft-3-pl - /mnt/data/ext/live-games/warcraft-3-pl',
        'pycharm - /mnt/data/ext/watchmaker/modules/pycharm',
    ]
    for module in modules:
        info('- ' + module)


def main():
    ap = ArgsProcessor(app_name='Watchmaker Creator', version='1.0.1')
    ap.add_subcommand('flash', action=action_flash, help='flash watchmaker to a drive')
    ap.add_param('disk', help='disk drive name (/dev/sdc)')
    ap.add_flag('yes', help='skip confirmation')
    ap.add_flag('dry', help='dry run instead of invoking real shell commands')

    ap.process()


if __name__ == '__main__':
    main()
