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

    info('setting partition names')
    wrap_shell('''
mlabel -i {}1 ::boot
mlabel -i {}2 ::EFI
e2label {}3 persistence
e2label {}4 usb-data
    ''', disk, disk, disk, disk)


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


def main():
    ap = ArgsProcessor(app_name='Watchmaker Creator', version='1.0.1')
    ap.add_subcommand('flash', action=action_flash, help='flash watchmaker to a drive')
    ap.add_param('disk', help='disk drive name (/dev/sdc)')
    ap.add_flag('yes', help='skip confirmation')
    ap.add_flag('dry', help='dry run instead of invoking real shell commands')

    ap.process()


if __name__ == '__main__':
    main()
