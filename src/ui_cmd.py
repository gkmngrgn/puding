#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import glob
import sys
import shutil
import subprocess

from main import (createImage, getDiskInfo)
from common import (app_launch_name, _)

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

    return parts[disk_path]

def getDiskInfo(disk_path):
    command_df = subprocess.Popen('df -h'.split(), stdout = subprocess.PIPE)

    grep = 'grep %s' % getMounted(disk_path)
    command_grep = subprocess.Popen(grep.split(), stdin = command_df.stdout,
                                                  stdout = subprocess.PIPE)

    disk_info = command_grep.stdout.read()

    filesystem, size, used, avail, use, mounted_on = disk_info.split()

    output = """\
Usb disk informations:
    Filesystem : %s
    Mounted On : %s
    Size       : %s
    Used       : %s
    Available  : %s
    Use Rating : %s""" % (filesystem, mounted_on, size, used, avail, use)

    return output

def runCommand(cmd):
    proc = subprocess.call(cmd, shell = True)

    return proc

def copyImage(src, dst):
    print(_("\nCreated \"repo\" directory in %s." % dst))
    os.mkdir('%s/repo' % dst)
    for file in glob.glob('%s/repo/*' % src):
        file_name = os.path.split(file)[1]
        print(_("Copying %s.." % file_name))
        shutil.copy(file, '%s/repo/%s' % (dst, file_name))

    print(_("\nCreated \"boot\" directory in %s." % dst))
    os.mkdir('%s/boot' % dst)
    for file in glob.glob('%s/boot/*' % src):
        if not os.path.isdir(file):
            file_name = os.path.split(file)[1]
            print(_("Copying %s.." % file_name))
            shutil.copy(file, '%s/boot/%s' % (dst, file_name))

    print(_("\nAnd copying pardus.img to %s.." % dst))
    shutil.copy('%s/pardus.img' % src, '%s/pardus.img' % dst)

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

def createConfigFile(dst):
    # Syslinux'un kurulu olup olmadigina bakmiyor. Pisi paketine syslinux
    # bagimliligi yazdim zaten. Asagidaki bilgileri su betikten ogrendim:
    # /usr/lib/pardus/pisi/cli/info.py
    from pisi.api import info_name

    # Kurmadan da uygulamanin calismasi icin
    if os.path.exists('/usr/share/%s' % app_launch_name):
        DATA_DIR = '/usr/share/%s' % app_launch_name

    else:
        DATA_DIR = 'datas'

    SYSLINUX_DIR = '/usr/lib/syslinux'
    GFXTHEME_DIR = '/usr/share/gfxtheme/'

    # True parametresi ne ise yarar bilmiyorum henuz.
    metadata = info_name('syslinux', True)[0]
    version = metadata.package.version

    # Her seyden once syslinux dizinini olusturmak gerek
    os.mkdir('%s/boot/syslinux' % dst)

    # Bu nasil calisiyor ki, string kiyaslamasi yapiyorum =/
    if not checkVersion(version, '3.74'):
        syslinux_conf_file = '%s/syslinux.cfg.old' % DATA_DIR

    else:
        syslinux_conf_file = '%s/syslinux.cfg.new' % DATA_DIR

        shutil.copy('%s/gfxboot.com' % SYSLINUX_DIR,
                    '%s/boot/syslinux/gfxboot.com' % dst)

        shutil.copy('%s/hdt.c32' % SYSLINUX_DIR,
                    '%s/boot/syslinux/hdt.c32' % dst)

    for file in glob.glob('%s/pardus/boot/*' % GFXTHEME_DIR):
        file_name = os.path.split(file)[1]
        shutil.copy(file, '%s/boot/syslinux/%s' % (dst, file_name))

    shutil.copy(syslinux_conf_file, '%s/boot/syslinux/syslinux.cfg' % dst)

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

        print(_("Copying syslinux files.."))
        createConfigFile(dst)

        # install syslinux and create mbr
        if createMBR(dst):
            print(_("MBR written, USB disk is ready for Pardus installation."))

            return True

        else:
            print(_("Could not write MBR to USB disk."))

            return False

def checkVersion(src, dst):
    src_ver = map(int, src.split('.'))
    dst_ver = map(int, dst.split('.'))

    # Syslinux'un 4.* surumu cikarsa diye..
    if src_ver[0] > dst_ver[0]:
        return True

    # src_ver, dst_ver'den buyuk degilse, esittir buyuk olasilikla.
    else:
        if src_ver[1] < dst_ver[1]:
            return False

        else:
            return True

class Create:
    def __init__(self, src, dst):
        # Yetkiyi kontrol etme isi simdilik burada yer alsin. Yeni ara-
        # yuzler yazildiginda puic.py dosyasina tasiriz.
        if not os.getuid() == 0:
            print(_("You need superuser permissions to run this application."))

            sys.exit(0)

        else:
            # Yollar soruluyor, bilgiler dogruysa imaj olusturma islemi
            # baslatiliyor.
            if self.__checkSource(src) and self.__checkDestination(dst):
                createImage(src, dst)

            else:
                print(_("An error occured. Check the parameters please."))

                sys.exit(1)

    def __checkSource(self, src):
        if not os.path.isfile(src):
            print(_("Path to the source file is invalid, try again."))

            return False

        else:
            try:
                iso_extension = os.path.splitext(src)[1] == ".iso"

                if not iso_extension:
                    print(_("The file you have specified is not an ISO image. If you think it's an ISO image, change the extension to \".iso\""))

                    return False

                else:
                    print(_("\nCD image: %s" % src))

                    return True

            except IndexError:
                print(_("The file you have specified is invalid. It's a CD image, use \".iso\" extension. e.g. Pardus_2009_Prealpha3.iso"))

                return False

    def __checkDestination(self, dst):
        if os.path.isdir(dst) and os.path.ismount(dst):
            print(getDiskInfo(dst))
            print(_("Please double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?"))

            answer = raw_input(_("Please type CONFIRM to continue: "))

            if answer in (_('CONFIRM'), _('confirm')):
                print(_("Writing CD image data to USB stick!"))

                return True

            else:
                print(_("You did not type CONFIRM. Exiting.."))

                return False

        else:
            print(_("The path you have typed is invalid. If you think the path is valid, make sure you have mounted USB stick to the path you gave. To check the path, you can use: mount | grep %s" % dst))

            return False
