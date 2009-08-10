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

if not os.path.exists("puic/"):
    shutil.copytree("src/", "puic/")
from puic.common import (app_launch_name, app_version, app_description, \
                         core_developer, core_developer_email, app_url, \
                         app_license_name)

script = "%s/%s" % (app_launch_name, app_launch_name)
shutil.copyfile("%s/%s.py" % (app_launch_name, app_launch_name), script)
os.chmod(script, 0755)

#LANGS = ["tr"]

# General installation functions
# def locale(lang):
#    return("share/locale/%s/LC_MESSAGES" % lang,
#            ["data/po/locale/%s/%s.mo" % (lang, app_launch_name)])

def removeBuildFiles():
    rmDir = ["build", "data/po/locale", app_launch_name]

    # remove build directories
    for dir in rmDir:
        try:
            print("Removing directory, %s.." % dir)
            shutil.rmtree(dir)
        except:
            pass

    # remove compiled Python files.
    for file in os.listdir("./"):
        if file.endswith(".pyc"):
            os.remove(file)

# Create .mo files
# if not os.path.exists("data/po/locale"):
#    os.mkdir("data/po/locale")
# 
#    for lang in LANGS:
#        pofile = "data/po/" + lang + ".po"
#        mofile = "data/po/locale/" + lang + "/%s.mo" % app_launch_name
# 
#        os.mkdir("data/po/locale/" + lang + "/")
#        print("generating %s" % mofile)
#        os.system("msgfmt %s -o %s" % (pofile, mofile))

data = [
    ("share/doc/%s" % app_launch_name, ["ChangeLog", "COPYING", "NOTES", \
                                            "README", "TODO"]),
    ("share/%s" % app_launch_name, glob.glob("data/syslinux.cfg.*")),
    ("share/%s/ui" % app_launch_name, glob.glob("data/ui/*"))]
#    ("share/%s/ui" % app_launch_name, glob.glob("data/ui/*")),
#    locale("tr")]

setup(
    name = app_launch_name,
    version = app_version,
    description = app_description,
    author = core_developer,
    author_email = core_developer_email,
    url = app_url,
    license = app_license_name,
    packages = [app_launch_name],
    scripts = [script],
    data_files = data,
    )

# Clean build files and directories
removeBuildFiles()