import os
from typing import List

from cliglue.utils.files import set_workdir, script_real_dir
from cliglue.utils.output import info, warn

import install_module
from system import wrap_shell

efi_part_size = 205  # MiB
persistence_part_size = 1536  # MiB


def flash_disk(disk: str, persistence: bool, boot_storage_surplus: int, modules: List[str]):
    set_workdir(os.path.join(script_real_dir(), '..'))

    info(f'checking required files existence')
    assert os.path.exists('squash/filesystem.squashfs')
    assert os.path.exists('content/boot-files')
    assert os.path.exists('content/grub')
    assert os.path.exists('modules/init')
    assert os.path.exists('modules/dev-data')

    warn(f'writing to disk {disk}')
    wrap_shell(f'df {disk}')

    info('creating MBR')
    wrap_shell(f'''wipefs {disk}''')
    wrap_shell(f'''
parted --script {disk} \\
    mklabel msdos
    ''')

    info('calculating partitions size')
    # depend on filesystem.squash size, expand by some surplus (for storage)
    squashfs_size = os.path.getsize('squash/filesystem.squashfs')
    boot_part_min_size = squashfs_size + dir_size('content/boot-files') + dir_size('content/grub')
    boot_part_end_mib = boot_part_min_size / 1024 ** 2 + boot_storage_surplus
    efi_part_end_mib = boot_part_end_mib + efi_part_size
    persistence_part_end_mib = efi_part_end_mib + persistence_part_size
    info(f'boot partition size: {boot_part_end_mib}MiB ({boot_storage_surplus}MiB surplus)')

    info('creating partitions space')
    if persistence:
        wrap_shell(f'''
parted --script {disk} \\
    mkpart primary fat32 1MiB {boot_part_end_mib}MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 {boot_part_end_mib}MiB {efi_part_end_mib}MiB \\
    set 2 esp on \\
    mkpart primary ext4 {efi_part_end_mib}MiB {persistence_part_end_mib}MiB \\
    mkpart primary ext4 {persistence_part_end_mib}MiB 100%
        ''')
    else:
        wrap_shell(f'''
parted --script {disk} \\
    mkpart primary fat32 1MiB {boot_part_end_mib}MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 {boot_part_end_mib}MiB {efi_part_end_mib}MiB \\
    set 2 esp on \\
    mkpart primary ext4 {efi_part_end_mib}MiB 100%
        ''')
    wrap_shell('sync')

    info('making boot partition filesystem')
    wrap_shell(f'''mkfs.fat -F32 {disk}1''')
    info('making EFI partition filesystem')
    wrap_shell(f'''mkfs.fat -F32 {disk}2''')
    if persistence:
        info('making persistence partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}3''')
        info('making watchmodules partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}4''')
    else:
        info('making watchmodules partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}3''')
    wrap_shell('sync')

    info('setting partition names')
    if persistence:
        wrap_shell(f'''
mlabel -i {disk}1 ::boot
mlabel -i {disk}2 ::EFI
e2label {disk}3 persistence
e2label {disk}4 watchmodules
        ''')
    else:
        wrap_shell(f'''
mlabel -i {disk}1 ::boot
mlabel -i {disk}2 ::EFI
e2label {disk}3 watchmodules
        ''')
    wrap_shell('sync')

    info('mounting partitions')
    wrap_shell(f'''mkdir -p /mnt/watchmaker''')
    wrap_shell(f'''
mkdir -p /mnt/watchmaker/boot
mount {disk}1 /mnt/watchmaker/boot
        ''')
    wrap_shell(f'''
mkdir -p /mnt/watchmaker/efi
mount {disk}2 /mnt/watchmaker/efi
        ''')

    wrap_shell(f'''mkdir -p /mnt/watchmaker/watchmodules''')
    if persistence:
        wrap_shell(f'''
mkdir -p /mnt/watchmaker/persistence
mount {disk}3 /mnt/watchmaker/persistence
        ''')
        wrap_shell(f'''mount {disk}4 /mnt/watchmaker/watchmodules''')
    else:
        wrap_shell(f'''mount {disk}3 /mnt/watchmaker/watchmodules''')

    info('installing GRUB EFI bootloaders')
    wrap_shell(f'''
grub-install \\
    --target=i386-efi \\
    --efi-directory=/mnt/watchmaker/boot \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell(f'''
grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/boot \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell(f'''
grub-install \\
    --target=i386-efi \\
    --efi-directory=/mnt/watchmaker/efi \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell(f'''
grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/efi \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')

    info('installing GRUB i386-pc bootloader')
    wrap_shell(f'''
grub-install \\
    --target=i386-pc \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --recheck \\
    {disk}
    ''')

    wrap_shell('sync')

    info('making EFI Microsoft workaround')
    wrap_shell(f'''
mkdir -p /mnt/watchmaker/efi/EFI/Microsoft
mkdir -p /mnt/watchmaker/boot/EFI/Microsoft
cp -r /mnt/watchmaker/efi/EFI/BOOT /mnt/watchmaker/efi/EFI/Microsoft/
cp -r /mnt/watchmaker/boot/EFI/BOOT /mnt/watchmaker/boot/EFI/Microsoft/
    ''')

    info('GRUB config')
    wrap_shell(f'''
cp content/grub/grub.cfg /mnt/watchmaker/boot/boot/grub/
cp content/grub/background.png /mnt/watchmaker/boot/boot/grub/
cp content/grub/font.pf2 /mnt/watchmaker/boot/boot/grub/
cp content/grub/loopback.cfg /mnt/watchmaker/boot/boot/grub/
cp content/grub/GRUB_FINDME /mnt/watchmaker/boot/
    ''')

    info('Boot base files')
    wrap_shell(f'''
cp -r content/boot-files/[BOOT] /mnt/watchmaker/boot/
cp -r content/boot-files/d-i /mnt/watchmaker/boot/
cp -r content/boot-files/dists /mnt/watchmaker/boot/
cp -r content/boot-files/live /mnt/watchmaker/boot/
cp -r content/boot-files/pool /mnt/watchmaker/boot/
cp -r content/boot-files/.disk /mnt/watchmaker/boot/
    ''')
    wrap_shell(f'''
cp -r content/boot-files/[BOOT] /mnt/watchmaker/efi/
cp -r content/boot-files/dists /mnt/watchmaker/efi/
cp -r content/boot-files/live /mnt/watchmaker/efi/
cp -r content/boot-files/pool /mnt/watchmaker/efi/
cp -r content/boot-files/.disk /mnt/watchmaker/efi/
    ''')
    wrap_shell(f'''mkdir -p /mnt/watchmaker/boot/storage''')

    if persistence:
        info('Persistence configuration')
        wrap_shell(f'''cp -r content/persistence/persistence.conf /mnt/watchmaker/persistence/''')

    info('Copying squash filesystem')
    wrap_shell(f'''cp squash/filesystem.squashfs /mnt/watchmaker/boot/live/''')

    info('Adding init module')
    wrap_shell(f'''cp -r modules/init /mnt/watchmaker/watchmodules/''')
    info('Adding dev-data module')
    wrap_shell(f'''cp -r modules/dev-data /mnt/watchmaker/watchmodules/''')

    if modules:
        info(f'Adding optional modules: {modules}')
        target_path = '/mnt/watchmaker/watchmodules'
        for module in modules:
            install_module.add_module(module, target_path)

    info('make watchmodules writable to non-root user')
    wrap_shell(f'''chown igrek /mnt/watchmaker/watchmodules -R''')

    info('unmounting')
    wrap_shell('sync')
    wrap_shell(f'''umount /mnt/watchmaker/boot''')
    wrap_shell(f'''umount /mnt/watchmaker/efi''')
    wrap_shell(f'''umount /mnt/watchmaker/watchmodules''')
    if persistence:
        wrap_shell(f'''umount /mnt/watchmaker/persistence''')

    info('Success')


def dir_size(dir_path: str) -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
