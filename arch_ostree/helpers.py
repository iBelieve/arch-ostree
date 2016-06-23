from .utils import run

__author__ = 'Michael Spencer'


def arch_nspawn(workdir, cmd, bind_ro=None, bind_rw=None):
    if not bind_ro:
        bind_ro = []
    if not bind_rw:
        bind_rw = []
    bind_ro = ['--bind-ro=' + bind for bind in bind_ro]
    bind_rw = ['--bind=' + bind for bind in bind_rw]
    run(['arch-nspawn', workdir] + bind_ro + bind_rw + cmd, capture_stdout=False)


def systemd_nspawn(workdir, cmd):
    run(['systemd-nspawn', '-D', workdir] + cmd, capture_stdout=False)
