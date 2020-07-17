import os
from typing import List

from nuclear.utils.files import set_workdir, script_real_dir
from nuclear.sublog import log

import install_module
from system import wrap_shell

efi_part_size = 270  # MiB
persistence_part_size = 1536  # MiB


def flash_disk(disk: str, persistence: bool, boot_storage_surplus: int, modules: List[str], skip_fs: bool):
    set_workdir(os.path.join(script_real_dir(), '..'))

    log.info(f'checking required files existence')
    assert os.path.exists('squash/filesystem.squashfs')
    assert os.path.exists('content/boot-files')
    assert os.path.exists('content/grub')
    assert os.path.exists('modules/init')

    # TODO unmount disk partitions

    log.warn(f'writing to disk {disk}')
    wrap_shell(f'df {disk}')

    log.info('creating MBR')
    wrap_shell(f'''sudo wipefs {disk}''')
    wrap_shell(f'''sudo dd if=/dev/zero of={disk} seek=1 count=2047''')
    wrap_shell(f'''
sudo parted --script {disk} \\
    mklabel msdos
    ''')

    log.info('calculating partitions size')
    # depend on filesystem.squash size, expand by some surplus (for storage)
    squashfs_size = os.path.getsize('squash/filesystem.squashfs')
    boot_part_min_size = squashfs_size + dir_size('content/boot-files') + dir_size('content/grub')
    boot_part_end_mib = boot_part_min_size / 1024 ** 2 + boot_storage_surplus
    efi_part_end_mib = boot_part_end_mib + efi_part_size
    persistence_part_end_mib = efi_part_end_mib + persistence_part_size
    log.info(f'boot partition size: {boot_part_end_mib}MiB ({boot_storage_surplus}MiB surplus)')

    log.info('creating partitions space')
    if persistence:
        wrap_shell(f'''
sudo parted --script {disk} \\
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
sudo parted --script {disk} \\
    mkpart primary fat32 1MiB {boot_part_end_mib}MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 {boot_part_end_mib}MiB {efi_part_end_mib}MiB \\
    set 2 esp on \\
    mkpart primary ext4 {efi_part_end_mib}MiB 100%
        ''')
    wrap_shell('sync')

    log.info('making boot partition filesystem')
    wrap_shell(f'''sudo mkfs.fat -F32 {disk}1''')
    log.info('making EFI partition filesystem')
    wrap_shell(f'''sudo mkfs.fat -F32 {disk}2''')
    if persistence:
        log.info('making persistence partition filesystem')
        wrap_shell(f'''sudo mkfs.ext4 -F {disk}3''')
        log.info('making watchmodules partition filesystem')
        wrap_shell(f'''sudo mkfs.ext4 -F {disk}4''')
    else:
        log.info('making watchmodules partition filesystem')
        wrap_shell(f'''sudo mkfs.ext4 -F {disk}3''')
    wrap_shell('sync')

    log.info('setting partition names')
    if persistence:
        wrap_shell(f'''
sudo mlabel -i {disk}1 ::boot
sudo mlabel -i {disk}2 ::EFI
sudo e2label {disk}3 persistence
sudo e2label {disk}4 watchmodules
        ''')
    else:
        wrap_shell(f'''
sudo mlabel -i {disk}1 ::boot
sudo mlabel -i {disk}2 ::EFI
sudo e2label {disk}3 watchmodules
        ''')
    wrap_shell('sync')

    log.info('mounting partitions')
    wrap_shell(f'''sudo mkdir -p /mnt/watchmaker''')
    wrap_shell(f'''
sudo mkdir -p /mnt/watchmaker/boot
sudo mount {disk}1 /mnt/watchmaker/boot
        ''')
    wrap_shell(f'''
sudo mkdir -p /mnt/watchmaker/efi
sudo mount {disk}2 /mnt/watchmaker/efi
        ''')

    wrap_shell(f'''sudo mkdir -p /mnt/watchmaker/watchmodules''')
    if persistence:
        wrap_shell(f'''
sudo mkdir -p /mnt/watchmaker/persistence
sudo mount {disk}3 /mnt/watchmaker/persistence
        ''')
        wrap_shell(f'''sudo mount {disk}4 /mnt/watchmaker/watchmodules''')
    else:
        wrap_shell(f'''sudo mount {disk}3 /mnt/watchmaker/watchmodules''')

    log.info('installing GRUB EFI bootloaders')
    wrap_shell(f'''
sudo grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/boot \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')
    wrap_shell(f'''
sudo grub-install \\
    --target=x86_64-efi \\
    --efi-directory=/mnt/watchmaker/efi \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --removable --recheck
    ''')

    log.info('installing GRUB i386-pc bootloader')
    wrap_shell(f'''
sudo grub-install \\
    --target=i386-pc \\
    --boot-directory=/mnt/watchmaker/boot/boot \\
    --recheck \\
    {disk}
    ''')

    wrap_shell('sync')

    log.info('Fixing GRUB EFI by replacing with Debian GRUB')
    wrap_shell(f'''
sudo rm /mnt/watchmaker/efi/EFI/BOOT/*
sudo cp -r content/efi/* /mnt/watchmaker/efi/EFI/BOOT/
sudo rm /mnt/watchmaker/boot/EFI/BOOT/*
sudo cp -r content/efi/* /mnt/watchmaker/boot/EFI/BOOT/
sudo cp -r /mnt/watchmaker/efi/EFI/BOOT /mnt/watchmaker/efi/EFI/debian
sudo cp -r /mnt/watchmaker/boot/EFI/BOOT /mnt/watchmaker/boot/EFI/debian

sudo cp -r content/grub/x86_64-efi /mnt/watchmaker/boot/boot/grub/
    ''')

    log.info('making EFI Microsoft workaround')
    wrap_shell(f'''
sudo cp -r /mnt/watchmaker/efi/EFI/BOOT /mnt/watchmaker/efi/EFI/Microsoft
sudo cp -r /mnt/watchmaker/boot/EFI/BOOT /mnt/watchmaker/boot/EFI/Microsoft
    ''')

    log.info('GRUB config')
    wrap_shell(f'''
sudo cp content/grub/grub.cfg /mnt/watchmaker/boot/boot/grub/
sudo cp content/grub/background.png /mnt/watchmaker/boot/boot/grub/
sudo cp content/grub/font.pf2 /mnt/watchmaker/boot/boot/grub/
sudo cp content/grub/loopback.cfg /mnt/watchmaker/boot/boot/grub/
sudo cp content/grub/GRUB_FINDME /mnt/watchmaker/boot/
    ''')

    log.info('Boot base files')
    wrap_shell(f'''
sudo cp -r content/boot-files/[BOOT] /mnt/watchmaker/boot/
sudo cp -r content/boot-files/d-i /mnt/watchmaker/boot/
sudo cp -r content/boot-files/dists /mnt/watchmaker/boot/
sudo cp -r content/boot-files/live /mnt/watchmaker/boot/
sudo cp -r content/boot-files/pool /mnt/watchmaker/boot/
sudo cp -r content/boot-files/.disk /mnt/watchmaker/boot/
    ''')
    wrap_shell(f'''sudo mkdir -p /mnt/watchmaker/boot/storage''')

    log.info('EFI base files')
    wrap_shell(f'''
    sudo cp -r content/boot-files/[BOOT] /mnt/watchmaker/efi/
    sudo cp -r content/boot-files/d-i /mnt/watchmaker/efi/
    sudo cp -r content/boot-files/dists /mnt/watchmaker/efi/
    sudo cp -r content/boot-files/live /mnt/watchmaker/efi/
    sudo cp -r content/boot-files/pool /mnt/watchmaker/efi/
    sudo cp -r content/boot-files/.disk /mnt/watchmaker/efi/
        ''')

    if persistence:
        log.info('Persistence configuration')
        wrap_shell(f'''sudo cp -r content/persistence/persistence.conf /mnt/watchmaker/persistence/''')

    log.info('Copying squash filesystem')
    if not skip_fs:
        wrap_shell(f'''sudo cp squash/filesystem.squashfs /mnt/watchmaker/boot/live/''')

    log.info('Adding init module')
    wrap_shell(f'''sudo cp -r modules/init /mnt/watchmaker/watchmodules/''')
    log.info('Adding dev module')
    wrap_shell(f'''sudo mkdir -p /mnt/watchmaker/watchmodules/dev''')

    log.info('make watchmodules writable to non-root user')
    wrap_shell(f'''sudo chown igrek /mnt/watchmaker/watchmodules -R''')

    if modules:
        log.info(f'Adding optional modules: {modules}')
        target_path = '/mnt/watchmaker/watchmodules'
        for module in modules:
            install_module.add_module(module, target_path)

    log.info('unmounting')
    wrap_shell('sync')
    wrap_shell(f'''sudo umount /mnt/watchmaker/boot''')
    wrap_shell(f'''sudo umount /mnt/watchmaker/efi''')
    wrap_shell(f'''sudo umount /mnt/watchmaker/watchmodules''')
    if persistence:
        wrap_shell(f'''sudo umount /mnt/watchmaker/persistence''')
    wrap_shell('sync')

    log.info('Success')


def dir_size(dir_path: str) -> int:
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
