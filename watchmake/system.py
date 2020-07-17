import os

from nuclear.sublog import log
from nuclear.utils.shell import shell
from nuclear.utils.input import input_required

import settings


def wrap_shell(cmd):
    cmd = cmd.strip()
    log.debug(f'> {cmd}')
    if not settings.DRY_RUN:
        shell(cmd)


def ensure_root():
    if os.geteuid() != 0:
        raise PermissionError('This script must be run as root')


def confirm(yes: bool, msg: str):
    if not yes:
        log.warn(msg)
        while input_required('[yes/no]... ') != 'yes':
            pass
