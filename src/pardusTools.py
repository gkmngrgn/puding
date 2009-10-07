#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import comar
import glob

class Main:
    def __init__(self, src):
        self.file_list = self.getFileList(src)

    def getFileList(self, src):
        file_list = ["%s/pardus.img" % src]
        for i in glob.glob("%s/boot/*" % src):
            if os.path.isfile(i):
                file_list.append(i)
        file_list.extend(glob.glob("%s/repo/*" % src))

        return file_list

class Authorization:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()

    def mount(self, device, path):
        self.link.Disk.Manager["mudur"].mount(device, path)

    def umount(self, device):
        self.link.Disk.Manager["mudur"].umount(device)

    def createSyslinux(self, device):
        self.link.Disk.Manager["puding"].createSyslinux(device)

