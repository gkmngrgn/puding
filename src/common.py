#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import gettext
import subprocess

# General variables
# FIX ME: Remove unused variables.
app_launch_name = "puic"
NAME = "puic"
share_dir = "/usr/share/%s" % app_launch_name
HOME = "%s/.puic" % os.getenv("HOME")
SHARE = "/usr/share/%s" % NAME
SYSLINUX = "/usr/lib/syslinux"
GFXTHEME = "/usr/share/gfxtheme/"

if os.path.exists("locale"):
    localedir = "locale"

else:
    localedir = "/usr/share/locale"

t = gettext.translation(app_launch_name, localedir, fallback = True)
_ = t.ugettext

# General functions
def getDiskInfo(dst):
    from math import pow

    disk_info = os.statvfs(dst)
    capacity = int(disk_info.f_bsize * disk_info.f_blocks / pow(1024, 2))
    available = int(disk_info.f_bsize * disk_info.f_bavail / pow(1024, 2))
    used = int(disk_info.f_bsize * (disk_info.f_blocks - disk_info.f_bavail) / pow(1024, 2))
    
    return [capacity, available, used]

def runCommand(cmd):
    proc = subprocess.call(cmd, shell = True)

    return proc

def copyPisiPackage(file, dst, pisi):
    shutil.copy(file, "%s/repo/%s" % (dst, pisi))

    return pisi

def checkSyslinuxVersion(version, request):
    ver = map(int, version.split('.'))
    req = map(int, request.split('.'))

    # Syslinux'un 4.* surumu cikarsa diye..
    if ver[0] > req[0]:
        return True

    # src_ver, dst_ver'den buyuk degilse, esittir buyuk olasilikla.
    else:
        if ver[1] < req[1]:
            return False

        else:
            return True

def createConfigFile(dst):
    # FIX ME: This puic should be work in Windows or another distribution.
    # So you mustn't use pisi.api
    from pisi.api import info_name

    # True parametresi ne ise yarar bilmiyorum henuz.
    metadata = info_name('syslinux', True)[0]
    version = metadata.package.version

    # Her seyden once syslinux dizinini olusturmak gerek
    os.mkdir('%s/boot/syslinux' % dst)

    # Bu nasil calisiyor ki, string kiyaslamasi yapiyorum =/
    if not checkSyslinuxVersion(version, "3.74"):
        syslinux_conf_file = '%s/syslinux.cfg.old' % SHARE

    else:
        syslinux_conf_file = '%s/syslinux.cfg.new' % SHARE

        shutil.copy('%s/gfxboot.com' % SYSLINUX,
                    '%s/boot/syslinux/gfxboot.com' % dst)

        shutil.copy('%s/hdt.c32' % SYSLINUX,
                    '%s/boot/syslinux/hdt.c32' % dst)

    for file in glob.glob('%s/pardus/boot/*' % GFXTHEME):
        file_name = os.path.split(file)[1]
        shutil.copy(file, '%s/boot/syslinux/%s' % (dst, file_name))

    shutil.copy(syslinux_conf_file, '%s/boot/syslinux/syslinux.cfg' % dst)

def getMounted(disk_path):
    parts = {}
    for line in open("/proc/mounts"):
        if line.startswith("/dev/"):
            device, path, other = line.split(" ", 2)
            parts[path] = device

    return parts[disk_path]

# General Informations
app_name = _('Pardus USB Image Creator')
app_launch_name = 'puic'
app_version = '0.0.5'
app_description = _("An USB Image Creator For Pardus Linux.")
app_url = 'http://www.gokmengorgen.net/puic'
app_license_name = 'GPLv3'
core_developer = 'Gökmen Görgen'
core_developer_email = 'gkmngrgn@gmail.com'
copyright = _("Copyright") + " \302\251 2009 Gökmen Görgen, <%s>" % core_developer_email
license = _("""\
Puic is an USB image creator for Pardus Linux.
%s

Puic is a free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Pati is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.\
""" % copyright)
