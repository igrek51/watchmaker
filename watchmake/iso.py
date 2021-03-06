import os
import re

from nuclear.sublog import log
from nuclear.utils.shell import shell_output

from system import wrap_shell, confirm


def make_iso(yes: bool, source_disk: str, target_iso: str):
    log.info(f'checking required files existence')
    assert os.path.exists(os.path.abspath(os.path.join(target_iso, os.pardir)))

    fdisk_output = shell_output(f'sudo fdisk -l {source_disk}')
    print(fdisk_output)

    block_size_line = [line for line in fdisk_output.splitlines() if line.startswith('Units: sectors of')][0]
    block_size_matcher = re.compile(r'= ([0-9]+) bytes$')
    match = block_size_matcher.search(block_size_line)
    assert match
    block_size = int(match.group(1))

    end_sector_line = fdisk_output.splitlines()[-1]
    end_sector_matcher = re.compile(f'^{source_disk}[a-z0-9]*\\s+[0-9]+\\s+([0-9]+)\\s+[0-9]+')
    match = end_sector_matcher.search(end_sector_line)
    assert match
    end_sector = int(match.group(1))

    log.info(f'block size: {block_size}')
    log.info(f'end sector: {end_sector}')
    confirm(yes, f'Attempting to dump partitions from {source_disk} to {target_iso}. Are you sure?')

    log.info(f'Writing {source_disk} to {target_iso}')
    wrap_shell(
        f'sudo dd if={source_disk} of={target_iso} bs={block_size} count={end_sector} conv=noerror,sync status=progress')
    wrap_shell('sync')
