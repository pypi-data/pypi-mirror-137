import os
from pathlib import Path


def check_path():
    config_file = f'{Path.home()}/.fdrc'
    if not Path(config_file).exists():
        ZSH_PATH = os.popen(
            '/bin/zsh -c \'source ~/.zshrc; echo $PATH\'').read().rstrip()
        BASH_PATH = os.popen(
            '/bin/bash -c \'source ~/.bashrc; echo $PATH\'').read().rstrip()
        os.environ['PATH'] = os.environ['PATH'] + ZSH_PATH + BASH_PATH
        with open(config_file, 'w') as f:
            f.write(shutil.which('fd'))

    with open(config_file) as rc:
        fd = rc.read()
    return fd
