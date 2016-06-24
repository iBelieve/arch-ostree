#!/bin/bash

#
# Archbuild - Buildbot configuration for Papyros
#
# Copyright (C) 2015 Michael Spencer <sonrisesoftware@gmail.com>
# Copyright (C) 2015 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

set -e
set -x

os_dir=$1
OSNAME=$2
arch=$3

# Set up the kernel/boot files

kernel_version=$(pacman -r "$os_dir" -Q linux | cut -d' ' -f 2)-ARCH

linux${arch} systemd-nspawn -D "$os_dir" \
    mkinitcpio -c /etc/ostree-mkinitcpio.conf -g /boot/initramfs-linux.img \
        -k $kernel_version -S autodetect

boot_dir="$os_dir"/boot

rm -f "$boot_dir"/initramfs-linux-fallback.img

checksum=$(cat "$boot_dir"/initramfs-* "$boot_dir"/vmlinuz-* | \
           sha256sum | cut -d' ' -f 1)

mv "$boot_dir"/initramfs-*.img "$boot_dir"/initramfs-$checksum
mv "$boot_dir"/vmlinuz-* "$boot_dir"/vmlinuz-$checksum

# Clean up the directory structure

# Doesn't seem to be needed any more...
rm "$os_dir"/etc/pacman.d/gnupg/S.gpg-agent

mkdir -p "$os_dir"/usr/etc/
mkdir -p "$os_dir"/sysroot
mkdir -p "$os_dir"/var/mnt
mkdir -p "$os_dir"/var/srv
mkdir -p "$os_dir"/var/opt

rsync -av "$os_dir"/etc "$os_dir"/usr/etc/
rm -rf "$os_dir"/{home,opt,root,mnt,etc}

ln -s sysroot/ostree "$os_dir"/ostree
ln -s sysroot/tmp "$os_dir"/tmp
ln -s var/home "$os_dir"/home
ln -s var/opt "$os_dir"/opt
ln -s var/srv "$os_dir"/srv
ln -s var/mnt "$os_dir"/mnt
ln -s var/local "$os_dir"/usr/local
ln -s var/roothome "$os_dir"/root

chmod a+rX "$os_dir"/{bin,boot,lib,sysroot,usr,var,opt,srv,mnt}

# cat << EOF > "$os_dir"/usr/etc/fstab
# LABEL=$OSNAME-boot /boot ext4 rw,relatime,data=ordered 0 2
# LABEL=$OSNAME-root / ext4 rw,relatime,data=ordered 0 1
# EOF

cat << EOF > "$os_dir"/usr/lib/tmpfiles.d/ostree.conf
d /var/log/journal 0755 root root -
L /var/home - - - - ../sysroot/home
d /var/opt 0755 root root -
d /var/srv 0755 root root -
d /var/roothome 0700 root root -
d /var/local 0755 root root -
d /var/local/bin 0755 root root -
d /var/local/etc 0755 root root -
d /var/local/games 0755 root root -
d /var/local/include 0755 root root -
d /var/local/lib 0755 root root -
d /var/local/man 0755 root root -
d /var/local/sbin 0755 root root -
d /var/local/share 0755 root root -
d /var/local/src 0755 root root -
d /var/mnt 0755 root root -
d /run/media 0755 root root -
EOF
