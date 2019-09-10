#!/usr/bin/env python3

from cliglue import CliBuilder, argument, flag, subcommand, parameter
from cliglue.utils.input import input_required
from cliglue.utils.output import warn

from system import wrap_shell, ensure_root, workdir_root
import settings
import creator
import resquash


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

        ),
        subcommand('make-iso', run=make_iso, help='create ISO from disk OS installation').has(

        ),
        flag('dry', help='dry run instead of invoking real shell commands'),
        flag('yes', help='skip confirmation'),
    ).run()


def create_os(dry: bool, yes: bool, disk: str, skip_persistence: bool):
    settings.DRY_RUN = dry
    ensure_root()
    workdir_root()

    wrap_shell('lsblk')

    confirm(yes, f'Are you sure, you want to write to {disk} disk?')

    creator.flash_disk(disk, not skip_persistence)


def prebuild_tools(dry: bool):
    settings.DRY_RUN = dry
    # TODO update py-tools:
    # watchmaker tools
    # EXCLUDE_FILE
    # lichking
    # regex-rename
    # differ
    # volumen
    # update tips, cheatsheet
    # update live dev-data repos
    # update .osversion
    pass


def resquash_os(dry: bool, yes: bool, storage_path: str, live_squash: str):
    settings.DRY_RUN = dry
    ensure_root()
    workdir_root()
    confirm(yes, f'Are you sure, you want to resquash filesystem?')
    resquash.resquash_os(storage_path, live_squash)


def replicate_os():
    pass


def make_iso():
    pass


def confirm(yes: bool, msg: str):
    if not yes:
        warn(msg)
        while input_required('[yes/no]... ') != 'yes':
            pass


if __name__ == '__main__':
    main()
