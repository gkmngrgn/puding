#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

from os import getenv

NAME = "puic"
LOCALE = "/usr/share/locale"
VERSION = "0.1"
HOME = "%s/.puic" % getenv("HOME")
SHARE = "/usr/share/%s" % NAME
SYSLINUX = "/usr/lib/syslinux"
GFXTHEME = "/usr/share/gfxtheme/"
URL = "http://www.gokmengorgen.net/puic"
LICENSE_NAME = "GPLv3"
CORE_DEVELOPER = "Gökmen Görgen"
CORE_EMAIL = "gkmngrgn@gmail.com"
SUMMARY = "An USB Image Creator For Pardus Linux."
DESCRIPTION = "Puic is an USB image creator for Pardus Linux."
COPYRIGHT = u"Copyright (c) 2009 Gökmen Görgen, <%s>" % CORE_EMAIL
USAGE = "%s\n%s\n\nUsage: %s [options]" % (DESCRIPTION, COPYRIGHT, NAME)
LICENSE = """%s

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
""" % COPYRIGHT
