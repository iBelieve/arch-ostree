import os.path

from .utils import put
from .helpers import systemd_nspawn


class Chroot(object):
    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, cmd, workdir=None):
        if workdir:
            if isinstance(cmd, list):
                cmd = ' '.join(cmd)
            cmd = 'cd {} && {}'.format(workdir, cmd)
            cmd = (['bash', '-cil', cmd])
        systemd_nspawn(self.workdir, cmd)

    def put(self, filename, text):
        filename = os.path.join(self.workdir, filename)

        put(filename, text, sudo=True)

    def enable_service(self, service):
        self.run(['systemctl', 'enable', service])

    def disable_service(self, service):
        self.run(['systemctl', 'disable', service])

    def enable_sudo_access(self):
        self.run(['sed', '-i',
                  's/# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/',
                  '/etc/sudoers'])

    def install_aur(self, packages):
        if len(packages) == 0:
            return

        self.run(['mkdir', '/nobody'])
        self.run(['chmod', 'a+rw', '/nobody'])
        self.run(['bash', '-cil', 'echo "ALL ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers'])
        self.run(['sed', '-i', 's#nobody:x:99:99:nobody:/:/usr/bin/nologin#nobody:x:99:99:nobody:/nobody:/usr/bin/nologin#', '/etc/passwd'])

        self.run(['sudo', '-u', 'nobody', 'yaourt', '-S',
                  '--noconfirm'] + packages)

        self.run(['sed', '-i', '$ d', '/etc/sudoers'])
        self.run(['sed', '-i', 's#nobody:x:99:99:nobody:/nobody:/usr/bin/nologin#nobody:x:99:99:nobody:/:/usr/bin/nologin#', '/etc/passwd'])
        self.run(['rm', '-rf', '/nobody'])
