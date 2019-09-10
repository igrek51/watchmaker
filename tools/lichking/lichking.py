#!/usr/bin/env python3
import os
import sys
from random import randint

from cliglue.utils.shell import shell, shell_output, shell_error_code
from cliglue.utils.files import script_real_dir, list_dir, set_workdir, read_file
from cliglue.utils.strings import nonempty_lines, split_to_tuples
from cliglue.utils.regex import regex_filter_list, regex_replace_list

from cliglue.utils.output import info, fatal, error, debug, warn
from cliglue.utils.input import input_required
from cliglue import CliBuilder, argument, arguments, flag, parameter, subcommand

WARCRAFT_DIR = '/mnt/usb-data/modules/warcraft-3-pl/'
AOE2_DIR = '/mnt/usb-data/modules/aoe2/'
HOMM3_DIR = '/mnt/usb-data/modules/heroes3-hota/'
VERSION = '1.19.0'


def play_wav(path):
    shell('aplay %s' % path)


def play_mp3(path):
    shell('mplayer "%s" 1>/dev/null' % path)


def play_mp3_infinitely(path):
    try:
        shell('mpg123 --loop -1 --no-control -q "%s"' % path)
    except KeyboardInterrupt:
        shell('pkill mpg123')


def play_voice(voice_name):
    if not voice_name.endswith('.wav'):
        voice_name = voice_name + '.wav'
    voice_path = os.path.join(script_real_dir(), 'voices/', voice_name)
    if not os.path.isfile(voice_path):
        error('no voice file named %s' % voice_name)
    else:
        play_wav(voice_path)


def list_voices(subdir=''):
    voices_dir = os.path.join(script_real_dir(), 'voices/', subdir)
    voices = list_dir(voices_dir)
    voices = filter(lambda file: os.path.isfile(voices_dir + file), voices)
    voices = filter(lambda file: file.endswith('.wav'), voices)
    return list(map(lambda file: subdir + file[:-4], voices))


def random_item(a_list):
    return a_list[randint(0, len(a_list) - 1)]


def play_random_voice(subdir=''):
    if subdir and not subdir.endswith('/'):
        subdir += '/'
    # populate voices list
    voices = list_voices(subdir)
    # draw random voice
    if not voices:
        fatal('no voice available')
    random_voice = random_item(voices)
    info('Playing voice %s...' % random_voice)
    play_voice(random_voice)


def test_sound():
    info('testing audio...')
    try:
        while True:
            play_random_voice()
    except KeyboardInterrupt:
        pass


def test_network():
    info('Useful Linux commands: ifconfig, ping, nmap, ip')
    info('available network interfaces (up):')
    ifconfig = shell_output('sudo ifconfig')
    lines = nonempty_lines(ifconfig)
    lines = regex_filter_list(lines, r'^([a-z0-9]+).*')
    lines = regex_replace_list(lines, r'^([a-z0-9]+).*', '\\1')
    if not lines:
        fatal('no available network interfaces')
    for interface in lines:
        print(interface)
    info('testing IPv4 global DNS connectivity...')
    shell('ping 8.8.8.8 -c 4')
    info('testing global IP connectivity...')
    shell('ping google.pl -c 4')


def test_graphics():
    info('testing GLX (OpenGL for X Window System)...')
    error_code = shell_error_code('glxgears')
    debug('glxgears error code: %d' % error_code)


def test_wine():
    info('testing wine...')
    shell('wine --version')
    debug('launching notepad...')
    error_code = shell_error_code('wine notepad')
    debug('error code: %d' % error_code)


def network_disable_ipv6():
    debug('sudo sysctl -p')
    shell('sudo sysctl -p')
    info('IPv6 has been disabled')


def list_screens():
    # list outputs
    xrandr = shell_output('xrandr 2>/dev/null')
    lines = nonempty_lines(xrandr)
    lines = regex_filter_list(lines, r'^([a-zA-Z0-9\-]+) connected')
    lines = regex_replace_list(lines, r'^([a-zA-Z0-9\-]+) connected[a-z ]*([0-9]+)x([0-9]+).*', '\\1\t\\2\t\\3')
    if not lines:
        fatal('no xrandr outputs - something\'s fucked up')
    return split_to_tuples(lines, attrs_count=3, splitter='\t')


def set_screen_primary(screen_name):
    shell('xrandr --output %s --primary' % screen_name)
    info('%s set as primary' % screen_name)


def set_largest_screen_primary():
    largest_screen = None
    largest_size = 0
    for screen_name2, w, h in list_screens():
        size = int(w) * int(h)
        if size >= largest_size:  # when equal - the last one
            largest_size = size
            largest_screen = screen_name2
    if not largest_screen:
        fatal('largest screen not found')
    info('setting largest screen "%s" as primary...' % largest_screen)
    set_screen_primary(largest_screen)


def select_audio_output_device():
    info('select proper output device by disabling profiles in "Configuration" tab')
    shell('pavucontrol &')
    debug('playing test audio indefinitely...')
    sample_path = os.path.join(script_real_dir(), 'data/illidan-jestem-slepy-a-nie-gluchy.mp3')
    play_mp3_infinitely(sample_path)


def action_run_war3():
    set_workdir(WARCRAFT_DIR)
    # taunt on startup
    play_random_voice()
    error_code = shell_error_code('./wine.sh')
    debug('wine error code: %d' % error_code)
    # taunt on shutdown
    play_random_voice('war-close')


def action_play_voice(voice_name):
    if voice_name:
        play_voice(voice_name)
    else:
        # list available voices - default
        action_list_voices()


def completer_voices_list():
    return list_voices()


def action_play_voices_group(group):
    play_random_voice(group)


def action_play_random_voice():
    play_random_voice()


def action_list_voices():
    info('Available voices:')
    for voice_name in list_voices():
        print(voice_name)


def action_tips_dota():
    shell('sublime %swar-info/dota-info.md' % WARCRAFT_DIR)


def action_tips_age():
    shell('sublime %sTaunt/cheatsheet.md' % get_aoe2_dir())


def action_set_screen_primary(screen_name):
    if screen_name:
        info(f'setting screen "{screen_name}" as primary...')
        set_screen_primary(screen_name)
    else:
        action_list_screen()


def action_list_screen():
    info('Available screens:')
    for screenName2, w, h in list_screens():
        print(screenName2)


def completer_screen_list():
    return list(map(lambda s: s[0], list_screens()))


def action_vsync_set(state):
    if state == 'on':
        shell('export vblank_mode=3')
        os.environ['vblank_mode'] = '3'
        info('please execute in parent shell process: export vblank_mode=3')
    elif state == 'off':
        os.environ['vblank_mode'] = '0'
        shell('export vblank_mode=0')
        info('please execute in parent shell process: export vblank_mode=0')
    else:
        raise CliSyntaxError('unknown state: %s' % state)


def action_memory_clear():
    info('syncing...')
    shell('sync')
    info('memory (before):')
    shell('free -h')
    info('clearing PageCache, dentries and inodes (3)...')
    shell('sync; echo 3 | sudo tee /proc/sys/vm/drop_caches')
    info('cache / buffer memory dropped (after):')
    shell('free -h')


def action_memory_watch():
    shell('watch -n 1 cat /proc/meminfo')


def get_aoe2_dir():
	if os.path.isdir(AOE2_DIR):
		return AOE2_DIR
	else:
		return './'

def action_run_aoe2():
    aoe_stachu_version = read_file(get_aoe2_dir() + 'version.md')
    info('Running Age of Empires 2 - %s...' % aoe_stachu_version)
    play_wav(os.path.join(script_real_dir(), 'data/stachu-2.wav'))
    set_workdir(get_aoe2_dir() + 'age2_x1/')
    error_code = shell_error_code('./wine.sh')
    debug('wine error code: %d' % error_code)
    play_wav(os.path.join(script_real_dir(), 'data/stachu-8.wav'))


def action_aoe_taunt_list():
    info('Available taunts:')
    taunt_list_file = get_aoe2_dir() + 'Taunt/cheatsheet.md'
    taunts_cheatsheet = read_file(taunt_list_file)
    print(taunts_cheatsheet)


def completer_taunts_list():
    return list(map(lambda num: str(num), range(1, 43)))


def action_aoe_taunt(taunt_number):
    if taunt_number:
        # play selected taunt
        # preceding zero
        if len(taunt_number) == 1:
            taunt_number = '0' + taunt_number
        # find taunt by number
        taunts_dir = get_aoe2_dir() + 'Taunt/'
        taunts = list_dir(taunts_dir)
        taunts = list(filter(lambda file: os.path.isfile(taunts_dir + file), taunts))
        taunts = list(filter(lambda file: file.startswith(taunt_number), taunts))
        taunts = list(filter(lambda file: file.endswith('.mp3'), taunts))
        if not taunts:
            fatal('Taunt with number %s was not found' % taunt_number)
        if len(taunts) > 1:
            warn('too many taunts found')
        play_mp3(taunts_dir + taunts[0])
    else:  # list available taunts - default
        action_aoe_taunt_list()


def get_homm3_dir():
    if os.path.isdir(HOMM3_DIR):
        return HOMM3_DIR
    else:
        return './'


def action_run_homm3():
    set_workdir(get_homm3_dir())
    info('Running Heroes of Might & Magic 3...')
    error_code = shell_error_code('./wine.sh')
    debug('wine error code: %d' % error_code)



def main():
    set_workdir(script_real_dir())

    CliBuilder('lichking', version=VERSION, help='LichKing tool').has(
        subcommand('war', 'go', run=action_run_war3, help='run Warcraft3 using wine'),
        subcommand('age', 'aoe', run=action_run_aoe2, help='run AOE2 using wine'),
        subcommand('heroes', 'homm3', run=action_run_homm3, help='run HOMM3 using wine'),
        subcommand('test').has(
            subcommand('audio', run=test_sound, help='perform continuous audio test'),
            subcommand('graphics', run=test_graphics, help='perform graphics tests'),
            subcommand('network', run=test_network, help='perform network tests'),
            subcommand('wine', run=test_wine, help='perform wine tests'),
        ),
        subcommand('screen', run=action_set_screen_primary, help='set screen as primary').has(
            argument('screen_name', required=False, choices=completer_screen_list),
            subcommand('list', run=action_list_screen, help='list available screens'),
            subcommand('largest', run=set_largest_screen_primary, help='automatically set largest screen as primary'),
        ),
        subcommand('network').has(
            subcommand('noipv6', run=network_disable_ipv6, help='disable IPv6 (IPv4 only)'),
        ),
        subcommand('audio').has(
            subcommand('select-output', run=select_audio_output_device, help='select audio output device'),
        ),
        subcommand('vsync', run=action_vsync_set, help='enable / disable VSync').has(
            argument('state', choices=['on', 'off']),
        ),
        subcommand('voice', run=action_play_voice, help='play selected voice sound').has(
            argument('voice_name', choices=completer_voices_list, required=False),
            subcommand('list', run=action_list_voices, help='list available voices'),
            subcommand('random', run=action_play_random_voice, help='play random voice sound'),
            subcommand('group', run=action_play_voices_group, help='play random voice from a group').has(
                argument('group', choices=['startup', 'war-close', 'war-launch']),
            ),
        ),
        subcommand('info').has(
            subcommand('dota', run=action_tips_dota, help='open Dota cheatsheet'),
            subcommand('age', run=action_tips_age, help='open AOE2 Taunts cheatsheet'),
        ),
        subcommand('taunt', run=action_aoe_taunt, help='play AOE2 Taunt').has(
                argument('taunt_number', choices=completer_taunts_list, required=False),
                subcommand('list', run=action_aoe_taunt_list, help='list available AOE2 Taunts'),
        ),
        subcommand('memory').has(
            subcommand('clear', run=action_memory_clear, help='clear cache / buffer RAM memory'),
            subcommand('watch', run=action_memory_watch, help='watch memory cache / buffers / sections size'),
        ),
    ).run()


if __name__ == '__main__':
    main()
