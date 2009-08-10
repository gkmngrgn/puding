#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import getopt
import os
import sys

from puic.common import (app_launch_name, app_name, app_version, license, _)
from puic import ui_cmd

class Options:
    def parseArgs(self):
        from optparse import OptionParser

        parser = OptionParser(version = app_version)

        parser.add_option('-c', '--create', dest = 'create', action = 'store_true',
                          help = _("create Pardus USB image from console"))
        parser.add_option('-l', '--license', dest = 'license', action = 'store_true',
                          help = _("show program's license info and exit"))

        return parser.parse_args()

    def main(self):
        opts, args = self.parseArgs()

        if opts.create:
            from puic import ui_cmd

            try:
                source = os.path.realpath(sys.argv[2])
                destination = os.path.realpath(sys.argv[3])

                ui_cmd.Create(source, destination)

            except IndexError:
                print(_("Invalid usage. Example:"))
                print("%s --create /mnt/archive/Pardus-2009.iso /media/disk" % \
                      app_launch_name)

        elif opts.license:
            print(license)

        else:
            from puic import ui_qt
            
            try:
                ui_qt.Create()
            
            except:
                print(_("%s: Missing argument." % app_name))
                print(_("For more information, type '%s --help'." % sys.argv[0]))

if __name__ == '__main__':
    try:
        Options().main()

    except KeyboardInterrupt:
        print(_("\nQuit."))
