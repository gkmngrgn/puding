#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import getopt
import os
import sys

from optparse import OptionParser
from puic.common import (_, run)
from puic.constants import (HOME, LICENSE, NAME, VERSION)

class Options:
    def parseArgs(self, parser):
        parser.add_option('-l', '--license', dest = 'license', action = 'store_true',
                          help = _("show program's license info and exit"))
        parser.add_option("-c", "--create", dest = "create", action = "store_true",
                          help = _("create Pardus USB image from console"))
        parser.add_option("--with-qt", dest = "with_qt", action = "store_true",
                          help = _("run Puic with Qt4 graphical interface"))

        return parser.parse_args()

    def main(self):
        parser = OptionParser(version = VERSION)
        (opts, args) = self.parseArgs(parser)

        if opts.create:
            if not os.getuid() == 0:
                print(_("You need superuser permissions to run this application."))
 
                sys.exit(0)

            try:
                from puic import ui_cmd

                source = os.path.realpath(args[0])

                ui_cmd.Create(source)

            except IndexError:
                print(_("Invalid usage. Example:"))
                print("%s --create /mnt/archive/Pardus-2009.iso" % \
                      NAME)

        elif opts.license:
            print(license)

        elif opts.with_qt:
            from puic import ui_qt
            from PyQt4 import QtGui

            app = QtGui.QApplication(sys.argv)
            form = ui_qt.Create()
            form.show()
            sys.exit(app.exec_())

        else:
            parser.print_help()

if __name__ == '__main__':
    if not os.path.exists(HOME):
        os.mkdir(HOME)

    try:
        Options().main()

    except KeyboardInterrupt:
        print(_("\nQuit."))
