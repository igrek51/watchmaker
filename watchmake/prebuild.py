import os
import re

from cliglue.utils.files import set_workdir, read_file, save_file
from cliglue.utils.output import info

from system import wrap_shell

# Put your own develop repositories here
repo_remotes = {
    'android-songbook': 'https://github.com/igrek51/android-songbook.git',
    'py-tools': 'https://github.com/igrek51/py-tools.git',
    'linux-helpers': 'https://igrek51@bitbucket.org/igrek51/linux-helpers.git',
    'feedback_gateway': 'https://igrek51@bitbucket.org/igrek51/feedback_gateway.git',
    'django_chords': 'https://igrek51@bitbucket.org/igrek51/django_chords.git',
    'crypto-encoder': 'https://igrek51@bitbucket.org/igrek51/crypto-encoder.git',
    'cliglue': 'https://github.com/igrek51/cliglue.git',
    'dirty-monitor': 'https://github.com/igrek51/dirty-monitor',
}


def prebuild_tools(watchmaker_repo: str):
    set_workdir(watchmaker_repo)
    pytools_src_dir = f'{watchmaker_repo}/modules/py-tools'
    home = '/home/user'

    info(f'checking required files existence')
    assert os.path.exists(watchmaker_repo)
    assert os.path.exists(f'{watchmaker_repo}/modules/dev-data/remotes.md')
    assert os.path.exists(pytools_src_dir)
    assert os.path.exists(f'{pytools_src_dir}/lichking')
    assert os.path.exists(f'{pytools_src_dir}/regex-rename')
    assert os.path.exists(f'{pytools_src_dir}/differ')
    assert os.path.exists(f'{pytools_src_dir}/volumen')

    assert os.geteuid() != 0, 'This script must not be run as root'

    info('updating watchmaker tools itself')
    wrap_shell(f'mkdir -p ~/tools')
    wrap_shell(f'rsync -a {watchmaker_repo}/watchmake/ ~/tools/watchmake')
    wrap_shell(f'rsync -a {watchmaker_repo}/scripts/ ~/tools/scripts')
    wrap_shell(f'cp {watchmaker_repo}/modules/music/tubular.wav ~/Music/')
    wrap_shell(f'cp {watchmaker_repo}/modules/music/tubular.mp3 ~/Music/')

    info('updating cliglue')
    wrap_shell(f'sudo python3 -m pip install --upgrade cliglue')

    info('updating py-tools')
    wrap_shell(f'rsync -a {pytools_src_dir}/lichking/ ~/tools/lichking')
    wrap_shell(f'rsync -a {pytools_src_dir}/regex-rename/ ~/tools/regex-rename')
    wrap_shell(f'rsync -a {pytools_src_dir}/differ/ ~/tools/differ')
    wrap_shell(f'rsync -a {pytools_src_dir}/volumen/ ~/tools/volumen')
    wrap_shell(f'rsync -a {watchmaker_repo}/modules/dirty-monitor/ ~/tools/dirty-monitor')

    info('recreating links & autocompletion for tools')
    wrap_shell(f'sudo rm -f /usr/bin/{{lichking,king,lich,regex-rename,differ,dirty-monitor}}')
    wrap_shell(f'sudo rm -f /etc/bash_completion.d/cliglue_*')

    wrap_shell(f'sudo {home}/tools/lichking/lichking.py --bash-install lichking')
    wrap_shell(f'sudo {home}/tools/lichking/lichking.py --bash-install lich')
    wrap_shell(f'sudo {home}/tools/lichking/lichking.py --bash-install king')
    wrap_shell(f'sudo {home}/tools/dirty-monitor/dirty_monitor.py --bash-install dirty-monitor')
    wrap_shell(f'sudo {home}/tools/watchmake/watchmake.py --bash-install watchmake')

    wrap_shell(f'sudo ln -s {home}/tools/differ/differ.py /usr/bin/differ')
    wrap_shell(f'sudo ln -s {home}/tools/regex-rename/regex-rename.py /usr/bin/regex-rename')

    info('updating live dev-data repos')
    wrap_shell(f'rm -rf ~/dev-live')
    wrap_shell(f'mkdir -p ~/dev-live')
    wrap_shell(f'cp modules/dev-data/remotes.md ~/dev-live/')
    for repo_name, url in repo_remotes.items():
        info(f'initializing live git repo {repo_name}')
        repo_path = f'/home/user/dev-live/{repo_name}'
        wrap_shell(f'mkdir -p {repo_path}')
        set_workdir(repo_path)
        wrap_shell(f'git init')
        wrap_shell(f'git remote add origin "{url}"')
    set_workdir(watchmaker_repo)

    info('clearing gradle cache')
    wrap_shell(f'rm -rf ~/.gradle/*')

    info('clearing apt cache')
    wrap_shell(f'sudo apt clean')

    version_file = '/home/user/.osversion'
    version_line = read_file(version_file).splitlines()[0]
    version_matcher = re.compile(r'^v([0-9]+)\.([0-9]+)$')
    match = version_matcher.match(version_line)
    assert match
    major_version = int(match.group(1))
    minor_version = int(match.group(2)) + 1
    new_version = f'v{major_version}.{minor_version}'
    info(f'updating new OS version {new_version}')
    save_file(version_file, new_version)
