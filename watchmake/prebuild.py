import os
import re

from cliglue.utils.files import set_workdir, script_real_dir, read_file, save_file
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
}

watchmaker_src_dir = '/media/user/data/ext/watchmaker'
pytools_src_dir = f'{watchmaker_src_dir}/modules/py-tools'


def prebuild_tools():
	# TODO change to storage watchmaker full repo
    workdir_watchmake()

    info(f'checking required files existence')
    assert os.path.exists('modules/dev-data/remotes.md')
    assert os.path.exists('/media/user/data/')
    assert os.path.exists(pytools_src_dir)
    assert os.path.exists(f'{pytools_src_dir}/lichking')
    assert os.path.exists(f'{pytools_src_dir}/regex-rename')
    assert os.path.exists(f'{pytools_src_dir}/differ')
    assert os.path.exists(f'{pytools_src_dir}/volumen')
    assert os.path.exists(watchmaker_src_dir)

    assert os.geteuid() != 0, 'This script must not be run as root'

    info('updating watchmaker tools itself')
    wrap_shell(f'mkdir -p ~/tools')
    wrap_shell(f'rsync -a {watchmaker_src_dir}/watchmake/ ~/tools/watchmake')
    wrap_shell(f'rsync -a {watchmaker_src_dir}/scripts/ ~/tools/scripts')
    wrap_shell(f'cp {watchmaker_src_dir}/modules/music/tubular.wav ~/Music/')
    wrap_shell(f'cp {watchmaker_src_dir}/modules/music/tubular.mp3 ~/Music/')

    info('updating py-tools')
    wrap_shell(f'rsync -a {pytools_src_dir}/lichking/ ~/tools/lichking')
    wrap_shell(f'rsync -a {pytools_src_dir}/regex-rename/ ~/tools/regex-rename')
    wrap_shell(f'rsync -a {pytools_src_dir}/differ/ ~/tools/differ')
    wrap_shell(f'rsync -a {pytools_src_dir}/volumen/ ~/tools/volumen')

    info('updating cliglue')
    wrap_shell(f'python3.6 -m pip install --upgrade cliglue')

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
    workdir_watchmake()

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


def workdir_watchmake():
    set_workdir(os.path.join(script_real_dir(), '..'))
