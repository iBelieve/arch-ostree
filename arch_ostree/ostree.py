import os.path
import time

from .pacstrap import Pacstrap
from .utils import helper, run, bits

__author__ = 'Michael Spencer'


class OSTree(Pacstrap):
    def __init__(self, name, workdir, arch):
        super(OSTree, self).__init__(workdir, arch)
        self.name = name

    def put(self, filename, text):
        filename = self.workdir + filename

        with open(filename, 'w') as f:
            f.write(text)

    def install_release(self, release):
        self.put('/etc/release', release)

    def prepare(self):
        helper('prepare.sh', [os.path.abspath(self.workdir), self.name,
                              bits(self.arch)],
               self.workdir)

    def commit(self, ostree_dir, branch, channel, build_number):
        if not os.path.exists(ostree_dir):
            run(['ostree', '--repo=' + ostree_dir, 'init', '--mode', 'archive-z2'])

        branch = '{name}/{branch}/{arch}/{channel}'.format(name=self.name, branch=branch,
                                                           arch=self.arch, channel=channel)
        commit_message = 'Build {} at {}'.format(build_number, time.strftime("%c"))

        run(['sudo', 'ostree', '--repo=' + ostree_dir, 'commit',
             '--tree=dir=' + self.workdir,
             '--branch=' + branch,
             '--subject', commit_message])

    def enable_service(self, service):
        self.run(['systemctl', 'enable', service])
