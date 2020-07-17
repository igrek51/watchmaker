import os
import re

from nuclear.utils.files import set_workdir, read_file, save_file
from nuclear.sublog import log

from system import wrap_shell

# Put your own develop repositories here
repo_remotes = {
    'songbook': 'https://github.com/igrek51/songbook.git',
    'py-tools': 'https://github.com/igrek51/py-tools.git',
    'linux-helpers': 'https://igrek51@bitbucket.org/igrek51/linux-helpers.git',
    'feedback_gateway': 'https://igrek51@bitbucket.org/igrek51/feedback_gateway.git',
    'django_chords': 'https://igrek51@bitbucket.org/igrek51/django_chords.git',
    'crypto-encoder': 'https://igrek51@bitbucket.org/igrek51/crypto-encoder.git',
    'nuclear': 'https://github.com/igrek51/nuclear.git',
    'dirty-monitor': 'https://github.com/igrek51/dirty-monitor',
    'lichking': 'https://igrek51@bitbucket.org/igrek51/lichking.git',
    'volumen': 'https://github.com/igrek51/volumen.git',
}


def prebuild_tools(watchmaker_repo: str):
    set_workdir(watchmaker_repo)
    submodule_src_dir = f'{watchmaker_repo}/modules'
    home = '/home/user'

    log.info(f'checking required files existence')
    assert os.path.exists(watchmaker_repo)
    assert os.path.exists(submodule_src_dir)
    assert os.path.exists(f'{submodule_src_dir}/lichking')
    assert os.path.exists(f'{submodule_src_dir}/volumen')

    assert os.geteuid() != 0, 'This script must not be run as root'

    log.info('updating watchmaker tools itself')
    wrap_shell(f'mkdir -p {home}/tools')
    wrap_shell(f'rsync -a {watchmaker_repo}/watchmake/ {home}/tools/watchmake')
    wrap_shell(f'rsync -a {watchmaker_repo}/scripts/ {home}/tools/scripts')
    wrap_shell(f'cp {watchmaker_repo}/modules/music/tubular.wav {home}/Music/')
    wrap_shell(f'cp {watchmaker_repo}/modules/music/tubular.mp3 {home}/Music/')

    log.info('updating pip packages')
    wrap_shell(f'sudo python3 -m pip install --upgrade nuclear')
    wrap_shell(f'python3 -m pip install --upgrade diffs')
    wrap_shell(f'python3 -m pip install --upgrade copymon')
    wrap_shell(f'python3 -m pip install --upgrade regex-rename')
    wrap_shell(f'python3 -m pip install --upgrade trimmer')
    wrap_shell(f'python3 -m pip install --upgrade youtube-dl')

    log.info('updating py-tools')
    wrap_shell(f'rsync -a {submodule_src_dir}/lichking/ {home}/tools/lichking')
    wrap_shell(f'rsync -a {submodule_src_dir}/volumen/ {home}/tools/volumen')

    log.info('recreating links & autocompletion for tools')
    wrap_shell(f'sudo rm -f /usr/bin/lichking')
    wrap_shell(f'sudo rm -f /usr/bin/lich')
    wrap_shell(f'sudo rm -f /usr/bin/king')
    wrap_shell(f'sudo rm -f /usr/bin/volumen')
    wrap_shell(f'sudo rm -f /usr/bin/watchmake')
    wrap_shell(f'sudo rm -f /etc/bash_completion.d/cliglue_*')
    wrap_shell(f'sudo rm -f /etc/bash_completion.d/nuclear_*')

    wrap_shell(f'{home}/tools/lichking/lichking.py --install-bash lichking')
    wrap_shell(f'{home}/tools/lichking/lichking.py --install-bash lich')
    wrap_shell(f'{home}/tools/lichking/lichking.py --install-bash king')
    wrap_shell(f'{home}/tools/watchmake/watchmake.py --install-bash watchmake')
    wrap_shell(f'{home}/tools/volumen/volumen.py --install-bash volumen')

    wrap_shell(f'diffs --install-autocomplete')
    wrap_shell(f'copymon --install-autocomplete')
    wrap_shell(f'regex-rename --install-autocomplete')
    wrap_shell(f'trimmer --install-autocomplete')

    log.info('updating live dev repos')
    wrap_shell(f'rm -rf {home}/dev-live')
    wrap_shell(f'mkdir -p {home}/dev-live')
    for repo_name, url in repo_remotes.items():
        log.info(f'initializing live git repo {repo_name}')
        repo_path = f'{home}/dev-live/{repo_name}'
        wrap_shell(f'mkdir -p {repo_path}')
        set_workdir(repo_path)
        wrap_shell(f'git init')
        wrap_shell(f'git remote add origin "{url}"')
    set_workdir(watchmaker_repo)

    log.info('clearing gradle cache')
    wrap_shell(f'rm -rf {home}/.gradle/*')

    log.info('clearing apt cache')
    wrap_shell(f'sudo apt clean')

    version_file = '/home/user/.osversion'
    version_line = read_file(version_file).splitlines()[0]
    version_matcher = re.compile(r'^v([0-9]+)\.([0-9]+)$')
    match = version_matcher.match(version_line)
    assert match
    major_version = int(match.group(1))
    minor_version = int(match.group(2)) + 1
    new_version = f'v{major_version}.{minor_version}'
    log.info(f'updating new OS version {new_version}')
    save_file(version_file, new_version)
