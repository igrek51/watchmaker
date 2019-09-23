import os
import psutil
from typing import List

from cliglue.utils.files import set_workdir, script_real_dir
from cliglue.utils.output import info, warn

from system import wrap_shell, confirm

# raw directory name or zip archive
optional_modules = {
    'android-sdk': '/mnt/data/ext/watchmaker/modules/android-sdk.zip',
    'android-studio': '/mnt/data/ext/watchmaker/modules/android-studio.zip',
    'factorio': '/mnt/games/linux-games/factorio',
    'aoe2': '/mnt/data/ext/live-games/aoe2',
    'heroes3-hota': '/mnt/data/ext/live-games/heroes3-hota',
    'warcraft-3-pl': '/mnt/data/ext/live-games/warcraft-3-pl',
    'pycharm': '/mnt/data/ext/watchmaker/modules/pycharm.zip',
    'wine': '/mnt/data/ext/watchmaker/modules/wine.zip',
    'dev-data': '/mnt/data/ext/watchmaker/modules/dev-data',
}


def add_modules(yes: bool, modules: List[str]):
    set_workdir(os.path.join(script_real_dir(), '..'))

    info(f'checking required files existence')
    assert os.path.exists('squash/filesystem.squashfs')
    assert os.path.exists('content/boot-files')
    assert os.path.exists('content/grub')
    assert os.path.exists('modules/init')
    assert os.path.exists('modules/dev-data')

    target_path = find_usb_data_partition()
    assert os.path.exists(target_path), 'module target path not found'

    confirm(yes, f'Attepmting to install modules {modules} to {target_path}. Are you sure?')

    info(f'Adding optional modules: {modules}')
    for module in modules:
        add_module(module, target_path)


def find_usb_data_partition() -> str:
    candidates = list(
        filter(lambda m: m.endswith('/watchmodules'),
               map(lambda p: p.mountpoint,
                   psutil.disk_partitions()))
    )
    if not candidates:
        warn('cant find any mounted watchmodules partition')
        return '/mnt/watchmaker/watchmodules'
    assert len(candidates) <= 1, f'there are more than one partitions matching watchmodules: {candidates}'
    return candidates[0]


def add_module(module: str, target_path):
    info(f'Adding module {module}')
    assert module in optional_modules
    module_src_path = optional_modules[module]
    assert os.path.exists(module_src_path), 'module src path not found'
    if os.path.isdir(module_src_path):
        dirname = os.path.basename(os.path.normpath(module_src_path))
        info(f'Copying module {module_src_path} to {target_path}/{dirname}')
        wrap_shell(f'mkdir -p {target_path}/{dirname}')
        wrap_shell(f'rsync -a {module_src_path}/ {target_path}/{dirname}/')
    else:
        assert module_src_path.endswith('.zip'), 'supporting .zip only'
        info(f'Extracting module from {module_src_path} to {target_path}')
        wrap_shell(f'unzip {module_src_path} -d {target_path}/')
    wrap_shell(f'sync')
