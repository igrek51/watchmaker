import os

from cliglue.utils.output import debug, warn
from cliglue.utils.shell import shell
from cliglue.utils.input import input_required

import settings


def wrap_shell(cmd):
    cmd = cmd.strip()
    debug(f'> {cmd}')
    if not settings.DRY_RUN:
        shell(cmd)


def ensure_root():
    if os.geteuid() != 0:
        raise PermissionError('This script must be run as root')


def confirm(yes: bool, msg: str):
    if not yes:
        warn(msg)
        while input_required('[yes/no]... ') != 'yes':
            pass
