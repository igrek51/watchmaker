import datetime
import hashlib
import os

from cliglue.utils.files import set_workdir
from cliglue.utils.output import info
from cliglue.utils.time import time2str

from system import wrap_shell


def resquash_os(storage_path: str, live_squash: str, exclude_file: str):
    today = today_stamp()
    squashfs_storage_path = f'{storage_path}/filesystem.squashfs'
    tagged_squashfs_path = f'{storage_path}/filesystem-{today}.squashfs'
    exclude_file_abs = os.path.abspath(exclude_file)

    set_workdir('/')

    # ensure mount points are mounted
    info(f'checking mount points')
    assert os.path.exists(storage_path), f'storage path does not exist: {storage_path}'
    assert os.path.exists(live_squash), f'live squash file does not exist: {live_squash}'
    assert os.path.exists(exclude_file_abs), f'exclude file does not exist: {exclude_file_abs}'

    info('removing old filesystem copy on storage')
    wrap_shell(f'sudo rm -f {squashfs_storage_path}')
    wrap_shell('sync')

    info('squashing filesystem...')
    wrap_shell(f'''
sudo mksquashfs \
    /bin /boot /dev /etc /home /lib /lib64 /media /mnt /opt /proc /run /root /sbin /srv /sys /tmp /usr /var \
    /initrd.img /initrd.img.old /vmlinuz /vmlinuz.old \
    {squashfs_storage_path} \
    -regex -ef {exclude_file_abs} \
    -comp gzip -b 512k \
    -keep-as-directory
    ''')

    info(f'creating tagged copy: {tagged_squashfs_path}...')
    wrap_shell(f'sudo cp {squashfs_storage_path} {tagged_squashfs_path}')
    wrap_shell('sync')

    info(f'[!] Putting Live system at risk')
    info(f'[!] removing current Live squashfs: {live_squash}')
    wrap_shell(f'sudo rm -f {live_squash}')

    info('[!] replacing with newest squashfs')
    wrap_shell(f'sudo rsync -ah --progress --no-perms --no-owner --no-group {squashfs_storage_path} {live_squash}')
    wrap_shell('sync')
    info(f'[!] Live system is functional again')

    info(f'calculating checksum {squashfs_storage_path}')
    cksum1 = checksum_file(squashfs_storage_path)
    info(f'calculating checksum {live_squash}')
    cksum2 = checksum_file(live_squash)
    assert cksum1 == cksum2
    info(f'checksums are valid')
    tagged_squashfs_mib = os.path.getsize(tagged_squashfs_path) / 1024 ** 2

    info(f'Success. '
         f'Resquashed {live_squash}. '
         f'Filesystem snaposhot dumped to {tagged_squashfs_path} ({tagged_squashfs_mib}MiB)')


def today_stamp() -> str:
    return time2str(datetime.datetime.now(), '%Y-%m-%d')


def checksum_file(path: str) -> str:
    blocksize = 2 ** 20  # 1MB
    m = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()
