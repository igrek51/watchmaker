from cliglue.utils.output import info

from system import wrap_shell


def replicate_os(source_disk: str, target_disk: str):
    info(f'Cloning {source_disk} to {target_disk}...')
    wrap_shell(f'sudo dd if={source_disk} of={target_disk} bs=64K conv=noerror,sync status=progress')
    wrap_shell('sync')
