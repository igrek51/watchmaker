import datetime
import hashlib
import os

from nuclear.utils.files import set_workdir
from nuclear.sublog import log
from nuclear.utils.time import time2str

from system import wrap_shell


def resquash_os(storage_path: str, live_squash: str, exclude_file: str):
    today = today_stamp()
    squashfs_storage_path = f'{storage_path}/filesystem.squashfs'
    tagged_squashfs_path = f'{storage_path}/filesystem-{today}.squashfs'
    exclude_file_abs = os.path.abspath(exclude_file)

    set_workdir('/')

    # ensure mount points are mounted
    log.info(f'checking mount points')
    assert os.path.exists(storage_path), f'storage path does not exist: {storage_path}'
    assert os.path.exists(live_squash), f'live squash file does not exist: {live_squash}'
    assert os.path.exists(exclude_file_abs), f'exclude file does not exist: {exclude_file_abs}'

    log.info('removing old filesystem copy on storage')
    wrap_shell(f'sudo rm -f {squashfs_storage_path}')
    wrap_shell('sync')

    log.info('squashing filesystem...')
    wrap_shell(f'''
sudo mksquashfs \
    /bin /boot /dev /etc /home /lib /lib64 /media /mnt /opt /proc /run /root /sbin /srv /sys /tmp /usr /var \
    /initrd.img /initrd.img.old /vmlinuz /vmlinuz.old \
    {squashfs_storage_path} \
    -regex -ef {exclude_file_abs} \
    -comp gzip -b 512k \
    -keep-as-directory
    ''')

    log.info(f'creating tagged copy: {tagged_squashfs_path}...')
    wrap_shell(f'sudo cp {squashfs_storage_path} {tagged_squashfs_path}')
    wrap_shell('sync')

    log.info(f'cheking current squashfs size')
    live_squash_mib = os.path.getsize(live_squash) / 1024 ** 2

    log.info(f'[!] Putting Live system at risk')
    log.info(f'[!] removing current Live squashfs: {live_squash}')
    wrap_shell(f'sudo rm -f {live_squash}')

    log.info('[!] replacing with newest squashfs')
    wrap_shell(f'sudo rsync -ah --progress --no-perms --no-owner --no-group {squashfs_storage_path} {live_squash}')
    wrap_shell('sync')
    log.info(f'[!] Live system is functional again')

    log.info(f'calculating checksum {squashfs_storage_path}')
    cksum1 = checksum_file(squashfs_storage_path)
    log.info(f'calculating checksum {live_squash}')
    cksum2 = checksum_file(live_squash)
    assert cksum1 == cksum2
    log.info(f'checksums are valid')
    tagged_squashfs_mib = os.path.getsize(tagged_squashfs_path) / 1024 ** 2
    squash_size_diff = tagged_squashfs_mib - live_squash_mib

    log.info(f'Success. '
         f'Resquashed {live_squash}. '
         f'Filesystem snaposhot dumped to {tagged_squashfs_path}',
         size=f'{tagged_squashfs_mib}MiB',
         size_diff=f'{squash_size_diff}MiB')


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
