#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import getopt
import sys

from puic import ui_cmd
from puic import const
from puic import _

class Options:
    def parseArgs(self):
        from optparse import OptionParser

        parser = OptionParser(version = const.app_version)

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
                source = sys.argv[2]
                destination = sys.argv[3]

                ui_cmd.Create(source, destination)

            except IndexError:
                print(_("Invalid usage. Example:"))
                print("%s --create /mnt/archive/Pardus_2009_Prealpha3.iso /media/disk" % const.app_launch_name)

        elif opts.license:
            print(const.license)

        else:
            print(_("%s: Missing argument." % const.app_name))
            print(_("For more information, type '%s --help'." % sys.argv[0]))

if __name__ == '__main__':
    try:
        Options().main()

    except KeyboardInterrupt:
        print(_("\nQuit."))
