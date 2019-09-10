from cliglue.utils.output import info, warn

from system import wrap_shell


def flash_disk(disk: str, persistence: bool):
    warn(f'writing to disk {disk}')
    wrap_shell(f'df {disk}')

    info('creating MBR')
    wrap_shell(f'''wipefs {disk}''')
    wrap_shell(f'''
parted --script {disk} \\
    mklabel msdos
    ''')

    info('creating partitions space')
    if persistence:
        wrap_shell(f'''
parted --script {disk} \\
    mkpart primary fat32 1MiB 4608MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 4608MiB 4813MiB \\
    set 2 esp on \\
    mkpart primary ext4 4813MiB 6349MiB \\
    mkpart primary ext4 6349MiB 100%
        ''')
    else:
        wrap_shell(f'''
parted --script {disk} \\
    mkpart primary fat32 1MiB 4608MiB \\
    set 1 lba on \\
    set 1 boot on \\
    mkpart primary fat32 4608MiB 4813MiB \\
    set 2 esp on \\
    mkpart primary ext4 4813MiB 100%
        ''')

    wrap_shell('sync')

    info('making boot partition filesystem')
    wrap_shell(f'''mkfs.fat -F32 {disk}1''')
    info('making EFI partition filesystem')
    wrap_shell(f'''mkfs.fat -F32 {disk}2''')
    if persistence:
        info('making persistence partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}3''')
        info('making usb-data partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}4''')
    else:
        info('making usb-data partition filesystem')
        wrap_shell(f'''mkfs.ext4 -F {disk}3''')

    wrap_shell('sync')

    info('setting partition names')
    if persistence:
        wrap_shell(f'''
mlabel -i {disk}1 ::boot
mlabel -i {disk}2 ::EFI
e2label {disk}3 persistence
e2label {disk}4 usb-data
        ''')
    else:
        wrap_shell(f'''
mlabel -i {disk}1 ::boot
mlabel -i {disk}2 ::EFI
e2label {disk}3 usb-data
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

    wrap_shell(f'''mkdir -p /mnt/watchmaker/usb-data''')
    if persistence:
        wrap_shell(f'''
mkdir -p /mnt/watchmaker/persistence
mount {disk}3 /mnt/watchmaker/persistence
        ''')
        wrap_shell(f'''mount {disk}4 /mnt/watchmaker/usb-data''')
    else:
        wrap_shell(f'''mount {disk}3 /mnt/watchmaker/usb-data''')

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

    if persistence:
        info('Persistence configuration')
        wrap_shell(f'''
    cp -r content/persistence/persistence.conf /mnt/watchmaker/persistence/
        ''')

    info('Copying squash filesystem')
    wrap_shell(f'''
cp squash/filesystem.squashfs /mnt/watchmaker/boot/live/
    ''')

    info('Copying base usb-data modules')
    wrap_shell(f'''
cp -r modules/dev-data /mnt/watchmaker/usb-data/
    ''')
    wrap_shell(f'''
mkdir -p /mnt/watchmaker/usb-data/modules
    ''')
    wrap_shell(f'''
cp -r modules/init /mnt/watchmaker/usb-data/modules/
    ''')
    info('make usb-data writable to non-root user')
    wrap_shell(f'''
chown igrek /mnt/watchmaker/usb-data -R
    ''')

    info('unmounting')
    wrap_shell('sync')
    wrap_shell(f'''umount /mnt/watchmaker/boot''')
    wrap_shell(f'''umount /mnt/watchmaker/efi''')
    wrap_shell(f'''umount /mnt/watchmaker/usb-data''')
    if persistence:
        wrap_shell(f'''umount /mnt/watchmaker/persistence''')

    info('done')
    print_modules()


def print_modules():
    info('Optional modules:')
    modules = [
        'android-sdk - /mnt/data/ext/watchmaker/modules/android-sdk.zip',
        'android-studio - /mnt/data/ext/watchmaker/modules/android-studio.zip',
        'dev-data',
        'init',
        'factorio - /mnt/games/linux-games/factorio',
        'aoe2 - /mnt/data/ext/live-games/aoe2',
        'heroes3-hota - /mnt/data/ext/live-games/heroes3-hota',
        'warcraft-3-pl - /mnt/data/ext/live-games/warcraft-3-pl',
        'pycharm - /mnt/data/ext/watchmaker/modules/pycharm',
    ]
    for module in modules:
        info('- ' + module)
