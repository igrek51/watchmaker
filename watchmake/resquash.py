import datetime
import hashlib
import os

from cliglue.utils.files import set_workdir
from cliglue.utils.output import info

from system import wrap_shell
from cliglue.utils.time import time2str


def resquash_os(storage_path: str, live_squash: str):
    today = today_stamp()
    squashfs_storage_path = f'{storage_path}/filesystem.squashfs'
    tagged_squashfs_path = f'{storage_path}/filesystem-{today}.squashfs'

    set_workdir('/')

    # ensure mount points are mounted
    assert os.path.exists(squashfs_storage_path)
    assert os.path.exists(live_squash)

    info('removing old filesystem copy on storage')
    wrap_shell(f'rm -f {squashfs_storage_path}')
    wrap_shell('sync')

    info('squashing filesystem...')
    wrap_shell(f'''
mksquashfs \
    /bin /boot /dev /etc /home /lib /lib64 /media /mnt /opt /proc /run /root /sbin /srv /sys /tmp /usr /var \
    /initrd.img /initrd.img.old /vmlinuz /vmlinuz.old \
    {squashfs_storage_path} \
    -regex -ef {squashfs_storage_path}/EXCLUDE_FILE \
    -comp gzip -b 512k \
    -keep-as-directory
    ''')

    info(f'creating tagged copy: {tagged_squashfs_path}...')
    wrap_shell(f'cp {squashfs_storage_path} {tagged_squashfs_path}')
    wrap_shell('sync')

    info(f'removing current LIVE squashfs: {live_squash}')
    wrap_shell(f'rm -f {live_squash}')

    info('replacing with newest squashfs')
    wrap_shell(f'rsync -ah --progress {squashfs_storage_path} {live_squash}')
    wrap_shell('sync')

    info(f'calculating checksum {squashfs_storage_path}')
    cksum1 = checksum_file(squashfs_storage_path)
    info(f'calculating checksum {live_squash}')
    cksum2 = checksum_file(live_squash)
    assert cksum1 == cksum2


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
