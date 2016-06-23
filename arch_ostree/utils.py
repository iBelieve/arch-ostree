import os.path
import re
import subprocess

import yaml

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def bits(arch):
    return '32' if arch == 'i686' else '64'


def run(cmd, workdir=None, capture_stdout=True, sudo=False, arch=None):
    if arch:
        cmd = ['linux' + bits(arch)] + cmd
    if sudo:
        cmd = ['sudo'] + cmd
    print(' '.join(cmd))
    if capture_stdout:
        completion = subprocess.run(cmd, cwd=workdir, check=True, universal_newlines=True,
                                    stdout=subprocess.PIPE)
        return completion.stdout.strip()
    else:
        return subprocess.run(cmd, cwd=workdir, check=True)


def helper(name, args, workdir, sudo=False):
    return run([os.path.join(base_dir, 'helpers', name)] + args, workdir=workdir, sudo=sudo)


def load_yaml(fileName):
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    stream = open(fileName, "r")
    return yaml.load(stream, Loader=Loader)


def save_yaml(fileName, data):
    with open(fileName, 'w') as file:
        file.write(yaml.dump(data, default_flow_style=False))


def flatten(outer_list):
    return [item for inner_list in outer_list for item in inner_list]


def append_to_file(filename, text):
    if isinstance(text, list):
        text = '\n'.join(text)
    with open(filename, 'a') as file:
        file.write(text)


def replace_in_file(filename, regex, replacement):
    regex = re.compile(regex)

    lines = []
    with open(filename) as infile:
        for line in infile:
            line = regex.sub(replacement, line)
            lines.append(line)
    with open(filename, 'w') as outfile:
        for line in lines:
            outfile.write(line)
