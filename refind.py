#! /usr/bin/env python3
import sys
import re
import os

template = '''menuentry "{name}" {{
        icon     /EFI/BOOT/icons/os_arch.png
        volume   {volume}
        loader  {prefix}{loader}
        initrd  {prefix}{initrd}
        options "{options}"
}}'''


with open('/boot/efi/EFI/BOOT/refind.conf') as f:
    refind = f.read()


def find(key, text):
    match = re.findall(r'{}\s+(.+)'.format(key), text)

    if len(match) == 0:
        print('Error: not found: ' + key)
        sys.exit(-1)

    return match[0]


def save():
    # print(refind)
    with open('/boot/efi/EFI/BOOT/refind.conf', 'w') as f:
        f.write(refind)


def update_entry(ostree_entry, volume):
    global refind

    with open(ostree_entry) as f:
        loader_text = f.read()
        name = find('title', loader_text)
        initrd = find('initrd', loader_text)
        options = find('options', loader_text)
        loader = find('linux', loader_text)

    entry = template.format(name=name, volume=volume, loader=loader,
                            initrd=initrd, options=options, prefix='/boot')

    regex = r'menuentry "{}" {{.*}}'.format(name)

    if len(re.findall(regex, refind, flags=re.DOTALL)) == 0:
        refind += '\n\n' + entry
    else:
        refind = re.sub(regex, entry, refind, flags=re.DOTALL)

if __name__ == '__main__':
    volume = sys.argv[1]

    for entry in os.listdir('/boot/loader/entries'):
        update_entry('/boot/loader/entries/' + entry, volume)

    save()

    print('rEFInd config updated!')
