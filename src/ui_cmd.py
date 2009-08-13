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

from common import (_, runCommand, copyPisiPackage, createConfigFile, getMounted)
from common import (HOME, NAME, SHARE)

class Create:
    def __init__(self, src, dst):
        if self.__checkSource(src) and self.__checkDestination(dst):
            self.__createImage(src, dst)

        else:
            print(_("An error occured. Check the parameters please."))

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
            print(self.__printDiskInfo(dst))
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

    def __printDiskInfo(self, dst):
        from common import getDiskInfo

        (capacity, available, used) = getDiskInfo(str(dst))

        output = """\
USB disk informations:
    Capacity  : %d
    Available : %d
    Used      : %d""" % (capacity, available, used)

        return output

    def __createImage(self, src, dst):
        # create a directory for mounting iso image.
        dirname = "%s/iso_mount_dir" % HOME
        os.mkdir(dirname)

        print(_("Mounting %s.." % src))

        cmd = "mount -o loop %s %s" % (src, dirname)
        if runCommand(cmd):
            print(_("Could not mounted CD image."))

            return False

        else:
            # copy image to usb disk
            print(_("Copying CD image.."))
            self.__copyImage(dirname, dst)

            # unmount and remove dirname
            print(_("Unmounting %s.." % dirname))
            cmd = "umount %s" % dirname

            if runCommand(cmd):
                print(_("Could not unmounted CD image."))

                return False

            print(_("Copying syslinux files.."))
            createConfigFile(dst)

            # install syslinux and create mbr
            print(_("Creating ldlinux.sys.."))
            cmd = "syslinux %s" % getMounted(dst)

            if runCommand(cmd):
                print(_("Could not create, ldlinux.sys."))

                return False

            device = os.path.split(getMounted(dst))[1][:3]
            print(_("Concatenating MBR to %s" % device))
            cmd = 'cat /usr/lib/syslinux/mbr.bin > /dev/%s' % device

            if runCommand(cmd):
                print(_("Could not concatenate, MBR."))

                return False

            print(_("MBR written, USB disk is ready for Pardus installation."))

            return True

    def __copyImage(self, src, dst):
        os.mkdir('%s/repo' % dst)

        for file in glob.glob('%s/repo/*' % src):
            pisi = os.path.split(file)[1]
            print(_("Copying %s.." % copyPisiPackage(file, dst, pisi)))

        print(_("\nCreated \"boot\" directory in %s." % dst))
        os.mkdir('%s/boot' % dst)
        for file in glob.glob('%s/boot/*' % src):
            if not os.path.isdir(file):
                file_name = os.path.split(file)[1]
                print(_("Copying %s.." % file_name))
                shutil.copy(file, '%s/boot/%s' % (dst, file_name))

        print(_("\nAnd copying pardus.img to %s.." % dst))
        shutil.copy('%s/pardus.img' % src, '%s/pardus.img' % dst)

