#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen, <gkmngrgn_gmail.com>
# license: GPLv3
#

import glob
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
LANGS = ['tr', ]

def locale(lang):
    return('share/locale/%s/LC_MESSAGES' % lang,
            ['po/locale/%s/%s.mo' % (lang, app_launch_name)])

#Create .mo files
if not os.path.exists('po/locale'):
    os.mkdir('po/locale')

    for lang in LANGS:
        pofile = 'po/' + lang + '.po'
        mofile = 'po/locale/' + lang + '/%s.mo' % app_launch_name

        os.mkdir('po/locale/' + lang + '/')
        print("generating %s" % mofile)
        os.system('msgfmt %s -o %s' % (pofile, mofile))

datas = [
    ('%s/%s' % (DOC_DIR, app_launch_name), ['NOTES', 'TODO', 'COPYING']),
    (SBIN_DIR, [script, ]),
    ('share/%s' % app_launch_name, glob.glob('datas/syslinux.cfg.*')),
    locale('tr'),
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
    )

