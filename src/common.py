#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import dbus
import gettext
import glob
import os
import shutil
import subprocess

from releases import releases
from constants import (HOME, MOUNT_ISO, MOUNT_USB, \
                       NAME, LOCALE, SHARE, SYSLINUX)

t = gettext.translation(NAME, LOCALE, fallback = True)
_ = t.ugettext

def getDiskInfo(dst):
    from math import pow

    disk_info = os.statvfs(dst)
    capacity = int(disk_info.f_bsize * disk_info.f_blocks / pow(1024, 3))
    available = int(disk_info.f_bsize * disk_info.f_bavail / pow(1024, 3))
    used = int(disk_info.f_bsize * (disk_info.f_blocks - disk_info.f_bavail) / pow(1024, 3))

    return [capacity, available, used]

def getIsoSize(src):
    return os.stat(src).st_size

def getFilesSize(src):
    all_files = []
    all_files.extend(glob.glob("%s/repo/*" % src))
    boot_files = glob.glob("%s/boot/*" % src)
    for file in boot_files:
        if os.path.isfile(file):
            all_files.append(file)
    all_files.append("%s/pardus.img" % src)
    total_size = 0

    for file in all_files:
        size = os.stat(file).st_size
        total_size = total_size + size # LOL!

    return total_size

def verifyIsoChecksum(src):
    import hashlib

    checksum = hashlib.md5()
    isofile = file(src, "rb")
    bytes = 1024**2
    total = 0

    while bytes:
        data = isofile.read(bytes)
        checksum.update(data)
        bytes = len(data)
        total += bytes

    src_md5 = checksum.hexdigest()

    for release in releases:
        if src_md5 in release['md5']:
            return release['name'], release['md5'], release['url']

    return False

def runCommand(cmd):
    process = subprocess.call(cmd, shell = True)

    return process

def run(cmd):
    process = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               stdin = subprocess.PIPE)

    result = process.communicate()

    return process, result

def copyPisiPackage(file, dst, pisi):
    shutil.copy(file, "%s/repo/%s" % (dst, pisi))

    return pisi

def createConfigFile(dst):
    conf_dir = "%s/boot/syslinux" % dst
    conf_files = ["%s/gfxboot.com" % SYSLINUX, "%s/hdt.c32" % SYSLINUX]
    conf_files.extend(glob.glob("%s/gfxtheme/*" % SHARE))

    for file in conf_files:
        file_name = os.path.split(file)[1]
        if not os.path.exists("%s/%s" % (dst, file_name)):
            shutil.copy(file, "%s/%s" % (dst, file_name))

    syslinux_conf_file = "%s/syslinux.cfg" % conf_dir
    if not os.path.exists(syslinux_conf_file):
        shutil.copy("%s/syslinux.cfg.pardus" % SHARE, syslinux_conf_file)

def getMounted(disk_path):
    parts = {}
    for line in open("/proc/mounts"):
        if line.startswith("/dev/"):
            device, path, other = line.split(" ", 2)
            parts[path] = device

    return parts[disk_path]

def createDirs():
    if not os.path.exists(HOME):
        os.makedirs(MOUNT_ISO)
        os.mkdir(MOUNT_USB)

def createUSBDirs(dst):
    dirs = ("repo", "boot/syslinux")

    for d in dirs:
        path = "%s/%s" % (dst, d)
        if not os.path.exists(path):
            os.makedirs(path)

class PartitionUtils:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.drives = {}
        self.devices = []
        self.label = "PARDUS_USB"

    def returnDrives(self):
        return self.drives

    def formatDevice(self, dst):
        cmd = "mkfs.vfat -F 32 %s" % dst

        return runCommand(cmd)

    def getDevice(self, device):
        dev_obj = self.bus.get_object("org.freedesktop.Hal", device)

        return dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")

    def addDevice(self, dev, parent = None):
        mount = str(dev.GetProperty("volume.mount_point"))
        device = str(dev.GetProperty("block.device"))

        self.drives[device] = {
            "label" : str(dev.GetProperty("volume.label")).replace(" ", "_"),
            "fstype"   : str(dev.GetProperty("volume.fstype")),
            "fsversion": str(dev.GetProperty("volume.fsversion")),
            "uuid"     : str(dev.GetProperty("volume.uuid")),
            "mount"    : mount,
            "device"   : dev,
            "unmount"  : False,
            "device"   : device,
            "parent"   : parent.GetProperty("block.device")
            }

    def detectRemovableDrives(self):
        hal_obj = self.bus.get_object("org.freedesktop.Hal",
                                 "/org/freedesktop/Hal/Manager")
        hal = dbus.Interface(hal_obj, "org.freedesktop.Hal.Manager")

        devices = hal.FindDeviceByCapability("storage")

        for device in devices:
            dev = self.getDevice(device)

            if dev.GetProperty("storage.bus") == "usb":
                if dev.GetProperty("block.is_volume"):
                    self.addDevice(dev)

                    continue

                else:
                    children = hal.FindDeviceStringMatch("info.parent", device)

                    for child in children:
                        child = self.getDevice(child)

                        if child.GetProperty("block.is_volume"):
                            self.addDevice(child, parent = dev)


        if not len(self.drives):
            return False

        else:
            return True
