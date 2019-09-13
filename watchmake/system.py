import os

from cliglue.utils.output import debug
from cliglue.utils.shell import shell

import settings


def wrap_shell(cmd):
    cmd = cmd.strip()
    debug(f'> {cmd}')
    if not settings.DRY_RUN:
        shell(cmd)


def ensure_root():
    if os.geteuid() != 0:
        raise PermissionError('This script must be run as root')
