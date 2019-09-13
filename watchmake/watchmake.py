#!/usr/bin/env python3
from cliglue import CliBuilder, argument, flag, subcommand, parameter

import creator
import iso
import prebuild
import replicate
import resquash
import settings
from system import wrap_shell, ensure_root, confirm


def main():
    CliBuilder('Watchmaker OS tool', version='1.0.1').has(
        subcommand('create', run=create_os, help='flash Watchmaker OS to a drive').has(
            argument('disk', help='disk drive name (/dev/sdc)'),
            flag('skip-persistence', help='Skip creating persistence partition'),
        ),
        subcommand('prebuild', run=prebuild_tools, help='update current OS with latest tools').has(

        ),
        subcommand('resquash', run=resquash_os, help='rebuild squashed filesystem and swap it on the run').has(
            parameter('storage-path', help='temporary storage path for leaving a new squashed filesystem',
                      default='/media/user/data/ext/watchmaker/squash'),
            parameter('live-squash', help='target squashed filesytem to be replaced',
                      default='/media/user/boot/live/filesystem.squashfs'),
        ),
        subcommand('replicate', run=replicate_os, help='clone current OS itself to another drive').has(
            parameter('source-disk', help='source disk device name'),
            parameter('target-disk', help='target disk device name'),
        ),
        subcommand('iso', run=make_iso, help='make ISO from disk partitions').has(
            argument('source-disk', help='source disk device name'),
            argument('target-iso', help='target ISO filename'),
        ),
        flag('dry', help='dry run instead of invoking real shell commands'),
        flag('yes', help='skip confirmation'),
    ).run()


def create_os(dry: bool, yes: bool, disk: str, skip_persistence: bool):
    settings.DRY_RUN = dry
    ensure_root()
    wrap_shell('lsblk')
    confirm(yes, f'Are you sure, you want to create Wathmaker OS on {disk} disk?')
    creator.flash_disk(disk, not skip_persistence)


def prebuild_tools(dry: bool):
    settings.DRY_RUN = dry
    prebuild.prebuild_tools()


def resquash_os(dry: bool, yes: bool, storage_path: str, live_squash: str):
    settings.DRY_RUN = dry
    ensure_root()
    confirm(yes, f'Are you sure, you want to resquash filesystem?')
    resquash.resquash_os(storage_path, live_squash)


def replicate_os(dry: bool, yes: bool, source_disk: str, target_disk: str):
    settings.DRY_RUN = dry
    ensure_root()
    wrap_shell('lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT')
    confirm(yes, f'Are you sure, you want to replicate OS from {source_disk} to {target_disk}?')
    replicate.replicate_os(source_disk, target_disk)


def make_iso(dry: bool, yes: bool, source_disk: str, target_iso: str):
    settings.DRY_RUN = dry
    ensure_root()
    iso.make_iso(yes, source_disk, target_iso)


if __name__ == '__main__':
    main()
