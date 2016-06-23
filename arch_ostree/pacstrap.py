import os
import os.path
from .helpers import systemd_nspawn
from .utils import run

__author__ = 'Michael Spencer'


class Pacstrap(object):
    def __init__(self, workdir, arch):
        self.workdir = workdir
        self.arch = arch

    def create(self, packages, conf_file=None):
        if os.path.exists(self.workdir):
            # TODO: Update and install packages
            return

        os.makedirs(self.workdir)

        if conf_file:
            command = ['pacstrap', '-cdC', conf_file, self.workdir, 'base', 'base-devel'] + packages
        else:
            command = ['pacstrap', '-cd', self.workdir, 'base', 'base-devel'] + packages

        # TODO: Make install_dir first
        run(command, arch=self.arch, capture_stdout=False)

    def run(self, cmd, workdir=None):
        if workdir:
            if isinstance(cmd, list):
                cmd = ' '.join(cmd)
            cmd = 'cd {} && {}'.format(workdir, cmd)
            cmd = (['bash', '-cil', cmd])
        systemd_nspawn(self.workdir, cmd)
