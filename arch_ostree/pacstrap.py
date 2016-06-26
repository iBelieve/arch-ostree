import os
import os.path
from .chroot import Chroot
from .utils import run

__author__ = 'Michael Spencer'


class Pacstrap(Chroot):
    def __init__(self, workdir, arch):
        super().__init__(workdir)
        self.arch = arch

    def create(self, packages, conf_file=None):
        if os.path.exists(self.workdir):
            # TODO: Update and install packages
            return

        os.makedirs(self.workdir)

        if conf_file:
            command = ['pacstrap', '-cdC', conf_file, self.workdir, 'base',
                       'base-devel'] + packages
        else:
            command = ['pacstrap', '-cd', self.workdir, 'base',
                       'base-devel'] + packages

        # TODO: Make install_dir first
        run(command, arch=self.arch, capture_stdout=False, sudo=True)
