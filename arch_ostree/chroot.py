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

    def enable_service(self, service):
        self.run(['systemctl', 'enable', service])

    def disable_service(self, service):
        self.run(['systemctl', 'disable', service])

    def install_aur(self, packages):
        if len(packages) == 0:
            return

        command = ['yaourt', '-S', '--noconfirm'] + packages

        self.run(command)
