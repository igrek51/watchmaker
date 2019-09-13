import os

from cliglue.utils.files import set_workdir, script_real_dir
from cliglue.utils.output import info

from system import wrap_shell

repo_remotes = {
    'android-songbook': 'https://github.com/igrek51/android-songbook.git',
    'py-tools': 'https://github.com/igrek51/py-tools.git',
    'linux-helpers': 'https://igrek51@bitbucket.org/igrek51/linux-helpers.git',
    'feedback_gateway': 'https://igrek51@bitbucket.org/igrek51/feedback_gateway.git',
    'django_chords': 'https://igrek51@bitbucket.org/igrek51/django_chords.git',
    'crypto-encoder': 'https://igrek51@bitbucket.org/igrek51/crypto-encoder.git',
    'cliglue': 'https://github.com/igrek51/cliglue.git',
}

pytools_src_dir = '/media/user/data/Igrek/python/py-tools'
linux_helpers_src_dir = '/media/user/data/Igrek/linux'
watchmaker_src_dir = '/media/user/data/ext/watchmaker'


def prebuild_tools():
    workdir_watchmake()

    info(f'checking required files existence')
    assert os.path.exists('modules/dev-data/remotes.md')
    assert os.path.exists('/media/user/data/')
    assert os.path.exists(pytools_src_dir)
    assert os.path.exists(watchmaker_src_dir)

    assert os.geteuid() == 0, 'This script must not be run as root'

    info('updating watchmaker tools itself')
    wrap_shell(f'rsync -a {watchmaker_src_dir}/watchmake/ ~/tools/watchmake')
    wrap_shell(f'rsync -a {watchmaker_src_dir}/scripts/ ~/tools/scripts')
    wrap_shell(f'cp {watchmaker_src_dir}/data/tubular.wav ~/Music/')
    wrap_shell(f'cp {watchmaker_src_dir}/data/tubular.mp3 ~/Music/')

    wrap_shell('updating py-tools')
    wrap_shell(f'rsync -a {pytools_src_dir}/lichking/ ~/tools/lichking')
    wrap_shell(f'rsync -a {pytools_src_dir}/regex-rename/ ~/tools/regex-rename')
    wrap_shell(f'rsync -a {pytools_src_dir}/differ/ ~/tools/differ')
    wrap_shell(f'rsync -a {pytools_src_dir}/volumen/ ~/tools/volumen')

    wrap_shell('updating tips, cheatsheet')
    wrap_shell(f'mkdir -p ~/tools/cheatsheet')
    wrap_shell(f'rsync -a {linux_helpers_src_dir}/cheatsheet/ ~/tools/cheatsheet')

    info('updating cliglue')
    wrap_shell(f'python3.6 -m pip install --upgrade cliglue')

    info('updating live dev-data repos')
    wrap_shell(f'rm -rf ~/dev-live')
    wrap_shell(f'mkdir -p ~/dev-live')
    wrap_shell(f'cp modules/dev-data/remotes.md ~/dev-live/')
    for repo_name, url in repo_remotes:
        info(f'initializing live git repo {repo_name}')
        repo_path = f'~/dev-live/{repo_name}'
        wrap_shell(f'mkdir -p {repo_path}')
        set_workdir(repo_path)
        wrap_shell(f'git init')
        wrap_shell(f'git remote add origin "{url}"')
    workdir_watchmake()

    info('clearing gradle cache')
    wrap_shell(f'rm -rf ~/.gradle/*')

    info('clearing apt cache')
    wrap_shell(f'sudo apt clean')

    # TODO update .osversion


def workdir_watchmake():
    set_workdir(os.path.join(script_real_dir(), '..'))
