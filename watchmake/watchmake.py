#!/usr/bin/env python3
import sys
from typing import List

from cliglue import CliBuilder, argument, flag, subcommand, parameter
from cliglue.utils.shell import shell_error_code

import creator
import iso
import prebuild
import replicate
import resquash
import settings
from system import wrap_shell, ensure_root, confirm


def main():
    CliBuilder('Watchmaker OS tool', version='1.1.0').has(
        subcommand('create', run=create_os, help='flash Watchmaker OS to a drive').has(
            argument('disk', help='disk drive name (/dev/sdc)'),
            flag('skip-persistence', help='Skip creating persistence partition'),
            parameter('boot-surplus', help='Boot partition storage surplus (MiB)', type=int, default=300),
            parameter('--module', name='modules', help='Add optional module', multiple=True,
                      choices=creator.optional_modules.keys(), strict_choices=True),
        ),
        subcommand('prebuild', run=prebuild_tools, help='update current OS with latest tools').has(
            parameter('watchmaker-repo', help='a path to full watchmaker repository',
                      default='/media/user/data/ext/watchmaker'),
        ),
        subcommand('resquash', run=resquash_os, help='rebuild squashed filesystem and swap it on the run').has(
            parameter('storage-path', help='storage path for dumping new squashed filesystem snapshot',
                      default='/media/user/data/ext/watchmaker/squash'),
            parameter('exclude-file', help='EXCLUDE_FILE path for squashfs',
                      default='./EXCLUDE_FILE'),
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


def create_os(dry: bool, yes: bool, disk: str, skip_persistence: bool, boot_surplus: int, modules: List[str]):
    settings.DRY_RUN = dry
    ensure_root()
    wrap_shell('lsblk')
    confirm(yes, f'Attempting to create Wathmaker OS on {disk} disk. Are you sure?')
    creator.flash_disk(disk, not skip_persistence, boot_surplus, modules)


def prebuild_tools(dry: bool, watchmaker_repo: str):
    settings.DRY_RUN = dry
    prebuild.prebuild_tools(watchmaker_repo)


def resquash_os(dry: bool, yes: bool, storage_path: str, live_squash: str, exclude_file: str):
    settings.DRY_RUN = dry
    ensure_root()
    confirm(yes, f'Attepmting to resquash filesystem. Are you sure?')
    resquash.resquash_os(storage_path, live_squash, exclude_file)


def replicate_os(dry: bool, yes: bool, source_disk: str, target_disk: str):
    settings.DRY_RUN = dry
    ensure_root()
    wrap_shell('lsblk -o NAME,TYPE,RM,RO,FSTYPE,SIZE,VENDOR,MODEL,LABEL,MOUNTPOINT')
    confirm(yes, f'Attepmting to replicate OS from {source_disk} to {target_disk}. Are you sure?')
    replicate.replicate_os(source_disk, target_disk)


def make_iso(dry: bool, yes: bool, source_disk: str, target_iso: str):
    settings.DRY_RUN = dry
    ensure_root()
    iso.make_iso(yes, source_disk, target_iso)


def ensure_python():
    # ensure it's Python 3.6+
    if sys.version_info.major == 3 and sys.version_info.minor >= 6:
        return
    args = ' '.join(sys.argv)
    if shell_error_code('/usr/bin/env python3.7 --version > /dev/null') == 0:
        shell_error_code('/usr/bin/env python3.7 ' + args)
        exit(0)
    shell_error_code('/usr/bin/env python3.6 ' + args)
    exit(0)


if __name__ == '__main__':
    ensure_python()
    main()
