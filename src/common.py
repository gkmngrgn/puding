#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import gettext

# General variables
app_launch_name = "puic"
share_dir = "/usr/share/%s" % app_launch_name

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
