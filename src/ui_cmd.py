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
from common import PartitionUtils
from constants import (HOME, NAME, SHARE)

class Utils:
    def colorize(self, output, color = "white"):
        colors = {'red'                : "\033[31m",
                  'green'              : "\033[32m",
                  'yellow'             : "\033[33m",
                  'blue'               : "\033[34m",
                  'purple'             : "\033[35m",
                  'cyan'               : "\033[36m",
                  'white'              : "\033[37m",
                  'brightred'          : "\033[01;31m",
                  'brightgreen'        : "\033[01;32m",
                  'brightyellow'       : "\033[01;33m",
                  'brightblue'         : "\033[01;34m",
                  'brightcyan'         : "\033[01;36m",
                  'brightwhite'        : "\033[01;37m",
                  'default'            : "\033[0m"  }

        return colors[color] + output + colors["default"]

    def cprint(self, output, color, no_wrap = False):
        if no_wrap:
            print(self.colorize(_(output), color)),

        else:
            print(self.colorize(_(output), color))

class Create:
    def __init__(self, src):
        self.utils = Utils()
        self.partutils = PartitionUtils()

        if not self.partutils.detectRemovableDrives():
            self.utils.cprint("USB device not found.", "red")
            
            sys.exit()

        else:
            self.__askDestination()

        # FIX ME: is __checkDestination really required?
        if self.__checkSource(src) and self.__checkDestination(dst):
            self.__createImage(src, dst)

        else:
            self.utils.cprint("An error occured. Check the parameters please.", "red")

    def __checkSource(self, src):
        if not os.path.isfile(src):
            self.utils.cprint("Path to the source file is invalid, try again.", "red")

            return False

        else:
            try:
                iso_extension = os.path.splitext(src)[1] == ".iso"

                if not iso_extension:
                    self.utils.cprint("The file you have specified is not an ISO image. If you think it's an ISO image, change the extension to \".iso\"", "red")

                    return False

                else:
                    self.utils.cprint("\nCD image: %s" % src)

                    return True

            except IndexError:
                self.utils.cprint("The file you have specified is invalid. It's a CD image, use \".iso\" extension. e.g. Pardus_2009_Prealpha3.iso", "red")

                return False

    def __askDestination(self):
        drives = self.partutils.returnDrives()
        
        if len(drives):
            # FIX ME: If disk is unmounted, you should mount it before return process!
            # It returns mount point directory.
            return drives[drives.keys()[0]]["mount"]

        else:
            drive_no = 0

            self.utils.cprint("Devices:", "brightwhite")

            for drive in drives:
                drive_no += 1

                # FIX ME: Bad coding..
                self.utils.cprint("\n%d) %s:" % (drive_no, drive), "brightwhite")
                self.utils.cprint("    Label\t\t:", "green", True)
                self.utils.cprint(drives[drive]["label"], "yellow")

                self.utils.cprint("    Parent\t\t:", "green", True)
                self.utils.cprint(str(drives[drive]["parent"]), "yellow")

                self.utils.cprint("    Mount Point\t\t:", "green", True)
                self.utils.cprint(drives[drive]["mount"], "yellow")

                self.utils.cprint("    Unmount\t\t:", "green", True)
                self.utils.cprint(drives[drive]["unmount"], "yellow")

                self.utils.cprint("    UUID\t\t:", "green", True)
                self.utils.cprint(drives[drive]["uuid"], "yellow")

                self.utils.cprint("    File System Version\t:", "green", True)
                self.utils.cprint(drives[drive]["fsversion"], "yellow")

                self.utils.cprint("    File System Type\t:", "green", True)
                self.utils.cprint(drives[drive]["fstype"], "yellow")

            # Birden fazla USB bölümü bulunursa seçmeler olacak.
            try:
                answer = int(raw_input("Birden fazla USB aygıtı veya bölümü bulundu, birini seçin: "))

            except ValueError:
                self.cprint("You must enter a number between 0 - %d!" % drive_no + 1, "red")

        sys.exit()

    def __checkDestination(self, dst):
        if os.path.isdir(dst) and os.path.ismount(dst):
            print(self.__printDiskInfo(dst))
            self.utils.cprint("Please double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?")

            answer = raw_input(_("Please type CONFIRM to continue: "))

            if answer in (_('CONFIRM'), _('confirm')):
                self.utils.cprint("Writing CD image data to USB stick!", "green")

                return True

            else:
                self.utils.cprint("You did not type CONFIRM. Exiting..", "red")

                return False

        else:
            # FIX ME: is it required?
            self.utils.cprint("The path you have typed is invalid. If you think the path is valid, make sure you have mounted USB stick to the path you gave. To check the path, you can use: mount | grep %s" % dst, "red")

            return False

    def __printDiskInfo(self, dst):
        from common import getDiskInfo

        (capacity, available, used) = getDiskInfo(str(dst))

        output = """\
USB disk informations:
    Capacity  : %dG
    Available : %dG
    Used      : %dG
        """ % (capacity, available, used)

        return output

    def __createImage(self, src, dst):
        # create a directory for mounting iso image.
        dirname = "%s/iso_mount_dir" % HOME
        os.mkdir(dirname)

        self.utils.cprint("Mounting %s.." % src, "green")

        cmd = "mount -o loop %s %s" % (src, dirname)
        if runCommand(cmd):
            self.utils.cprint("Could not mounted CD image.", "red")

            return False

        else:
            self.__copyImage(dirname, dst)

            self.utils.cprint("\nUnmounting %s.." % dirname, "green")
            cmd = "umount %s" % dirname

            if runCommand(cmd):
                self.utils.cprint("Could not unmounted CD image.", "red")

                return False

            self.utils.cprint("Copying syslinux files..", "yellow")
            createConfigFile(dst)

            self.utils.cprint("Creating ldlinux.sys..", "yellow")
            cmd = "syslinux %s" % getMounted(dst)

            if runCommand(cmd):
                self.utils.cprint("Could not create, ldlinux.sys.", "red")

                return False

            device = os.path.split(getMounted(dst))[1][:3]
            self.utils.cprint("Concatenating MBR to %s" % device, "yellow")
            cmd = "cat /usr/lib/syslinux/mbr.bin > /dev/%s" % device

            if runCommand(cmd):
                self.utils.cprint("Could not concatenate, MBR.", "red")

                return False

            self.utils.cprint("MBR written, USB disk is ready for Pardus installation.", "brightgreen")

            return True

    def __copyImage(self, src, dst):
        os.mkdir("%s/repo" % dst)

        for file in glob.glob("%s/repo/*" % src):
            pisi = os.path.split(file)[1]
            self.utils.cprint("Copying: ", "green") + self.utils.colorize(copyPisiPackage(file, dst, pisi), "brightyellow")

        self.utils.cprint("\nCreated \"boot\" directory in %s." % dst, "green")
        os.mkdir("%s/boot" % dst)
        for file in glob.glob("%s/boot/*" % src):
            if not os.path.isdir(file):
                file_name = os.path.split(file)[1]
                self.utils.cprint("Copying: ", "green") + self.utils.colorize(file_name, "cyan")

                shutil.copy(file, "%s/boot/%s" % (dst, file_name))

        self.utils.cprint("And copying pardus.img to %s.." % dst, "green")
        shutil.copy('%s/pardus.img' % src, '%s/pardus.img' % dst)
