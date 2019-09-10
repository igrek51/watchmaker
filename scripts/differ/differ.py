#!/usr/bin/python
import time
import difflib
import subprocess
import sys


def shell_error_code(cmd):
    return subprocess.call(cmd, shell=True)


def shell(cmd):
    err_code = shell_error_code(cmd)
    if err_code != 0:
        fatal('failed executing: %s' % cmd)


def shell_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = process.communicate()
    return output.decode('utf-8')


GREEN = '\033[32m'
RED = '\033[31m'
BLUE = '\033[34m'
RESET = '\033[0m'


def color_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield GREEN + line + RESET
        elif line.startswith('-'):
            yield RED + line + RESET
        elif line.startswith('^'):
            yield BLUE + line + RESET
        else:
            yield line


def get_cmd():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    else:
        return 'date'

cmd = get_cmd()
output_0 = shell_output(cmd)

try:
    while(True):
        shell('tput reset')

        output_now = shell_output(cmd)

        diff = difflib.ndiff(output_0.splitlines(1), output_now.splitlines(1))
        diff = [d for d in diff if d[0] != ' ']
        diff = color_diff(diff)
        print(''.join(diff))

        time.sleep(1)
except KeyboardInterrupt:
    print
