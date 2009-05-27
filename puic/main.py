#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import shutil
import subprocess

from puic import _

def getMounted(disk_path):
    # Bu fonksiyon biraz daha basitlestirilebilir gibime
    # geliyor. parts sozlugu olusturup, sonra buna ogeler
    # eklemek sirf return satirinda bize gerekeni dondur-
    # mek icin yapilan fazlaliklar. Bu tip tanimlamalar
    # olmadan dogrudan isteneni elde etmek daha saglikli
    # olacak..
    parts = {}
    for line in open('/proc/mounts'):
        if line.startswith('/dev/'):
            device, path, other = line.split(" ", 2)
            parts[path] = device

    try:
        return parts[disk_path]

    except KeyError:
        # Kullanicinin USB bellek dizini olarak /media/disk/ yazma ihti-
        # maline karsilik boyle onlem alabildim. Sondaki '/' karakterini
        # almamasi icin
        return parts[disk_path[:-1]]

def getDiskInfo(disk_path):
    command_df = subprocess.Popen('df -h'.split(), stdout = subprocess.PIPE)

    grep = 'grep %s' % getMounted(disk_path)
    command_grep = subprocess.Popen(grep.split(), stdin = command_df.stdout,
                                                  stdout = subprocess.PIPE)

    disk_info = command_grep.stdout.read()

    filesystem, size, used, avail, use, mounted_on = disk_info.split()

    print(_("USB disk infos:"))
    print(_("\tFilesystem : %s" % filesystem))
    print(_("\tMounted On : %s" % mounted_on))
    print(_("\tSize       : %s" % size))
    print(_("\tUsed       : %s" % used))
    print(_("\tAvailable  : %s" % avail))
    print(_("\tUse Rating : %s" % use))

def runCommand(cmd):
    proc = subprocess.call(cmd, shell = True)

    return proc

def copyImage(src, dst):
    # sembolik baglantilari dogru kopyalamiyor.
    # eheh allahtan sembolik baglanti yok..
    for sub in os.listdir(src):
        sub_src = os.path.join(src, sub)
        sub_dst = os.path.join(dst, sub)

        print(_("Copying %s.." % sub_src))

        if os.path.isdir(sub_src):
            shutil.copytree(sub_src, sub_dst)

        else:
            shutil.copy2(sub_src, sub_dst)

def configSyslinux(iso_cfg, sys_cfg):
    # Tum yapilandirma dosyasini bellege almak bu fonksiyonu biraz
    # hantallastiriyor. Daha kolay bir cozum yolu bulunmalı. Mesela
    # dosya icerigini satir satir okutmak gibi.. Bu is icin start-
    # swith fonksiyonu arastirilmali.
    old_file = open(iso_cfg)
    new_file = open(sys_cfg, 'w')

    new_file.write(old_file.read().replace('isolinux',
                                            'syslinux').replace('root=/dev/ram0',
                                                                'root=/dev/ram0 mudur=livedisk')),
    new_file.close()

    os.remove(iso_cfg)

def mountDisk(src, dst):
    print(_("Mounting %s.." % src))
    cmd = 'mount -o loop %s %s' % (src, dst)
    proc = subprocess.call(cmd, shell = True)

    return proc

def unmountDisk(dst):
    print(_("Unmounting %s.." % dst))
    cmd = 'umount %s' % dst
    proc = subprocess.call(cmd, shell = True)

    if not proc:
        os.removedirs(dst)

    else:
        print(_("Could not unmount, %s." % dst))

def createMBR(dst):
    print(_("Creating ldlinux.sys.."))
    cmd = 'syslinux %s' % getMounted(dst)

    if runCommand(cmd):
        print(_("Could not create, ldlinux.sys."))

        return False

    else:
        device = os.path.split(getMounted(dst))[1][:3]
        print(_("Concatenating MBR to %s" % device))
        cmd = 'cat /usr/lib/syslinux/mbr.bin > /dev/%s' % device

        if runCommand(cmd):
            print(_("Could not concatenate, MBR."))

            return False

        else:
            return True

def createImage(src, dst):
    dirname = '%s/.puic_iso_dir' % os.getenv('HOME')

    #create a directory for mounting iso image.
    os.mkdir(dirname)

    if mountDisk(src, dirname):
        print(_("Could not mounted CD image."))

        return False

    else:
        # copy image to usb disk
        print(_("Copying CD image.."))
        copyImage(dirname, dst)

        # unmount and remove dirname
        unmountDisk(dirname)

        # change directory name and create syslinux.cfg
        print(_("Renaming boot/isolinux to boot/syslinux.."))
        os.rename('%s/boot/isolinux' % dst,
                  '%s/boot/syslinux' % dst)

        print(_("Renaming boot/syslinux/isolinux.cfg to boot/syslinux/syslinux.cfg and configuring.."))
        configSyslinux('%s/boot/syslinux/isolinux.cfg' % dst,
                       '%s/boot/syslinux/syslinux.cfg' % dst)

        # install syslinux and create mbr
        if createMBR(dst):
            print(_("MBR written, USB disk is ready for Pardus installation."))

            return True

        else:
            print(_("Could not write MBR to USB disk."))

            return False
