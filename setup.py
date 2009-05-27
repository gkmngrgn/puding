#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen, <gkmngrgn_gmail.com>
# license: GPLv3
#

import os
import shutil

from distutils.core import setup
from puic.const import app_launch_name, app_version, app_description, \
                       core_developer, core_developer_email, \
                       app_url, app_license_name

script = '%s/%s' % (app_launch_name, app_launch_name)
shutil.copyfile('%s.py' % app_launch_name, script)
os.chmod(script, 0755)

DOC_DIR = '/usr/share/doc'
SBIN_DIR = '/usr/sbin'
LOCALE_DIR = '/usr/share/locale'

datas = [
    ('%s/%s' % (DOC_DIR, app_launch_name), ['NOTES', 'TODO']),
    (SBIN_DIR, [script, ]),
    ]

setup(
    name = app_launch_name,
    version = app_version,
    description = app_description,
    author = core_developer,
    author_email = core_developer_email,
    url = app_url,
    license = app_license_name,
    platforms = ['Linux', ],
    packages = ['%s/' % app_launch_name, ],
    data_files = datas,
    po_directory = 'po',
    po_package = app_launch_name,
    )

