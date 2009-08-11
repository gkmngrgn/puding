#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import sys
from os import path

from common import share_dir
from PyQt4 import (QtCore, QtGui, uic)

class Create(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Create, self).__init__(parent)
        uic.loadUi("%s/ui/qtMain.ui" % share_dir, self)
        self.text_src = self.label_src.text()
        self.text_dst = self.label_dst.text()

        self.connect(self.button_next, QtCore.SIGNAL("clicked()"), self.__actionNext)
        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

    def __actionNext(self):
        src = self.line_src.displayText()
        dst = self.line_dst.displayText()

        if not self.__checkSource(src):
            self.label_info.setText("<font color=\"red\">The ISO path you have specified is invalid!</font>")

        elif not self.__checkDestination(dst, self.text_dst):
            self.label_info.setText("<font color=\"red\">The USB disk path you have specified is invalid!</font>")

        else:
            pass

    def __checkSource(self, src):
        if QtCore.QString(src).isEmpty():

            return False

        else:
#===============================================================================
#            src_extension = path.splitext(src) == ".iso"
#            if not path.isfile(src) and not src_extension:
#===============================================================================
            if not path.isfile(src):

                return False

            else:

                return True

    def __checkDestination(self, dst, text):
        if QtCore.QString(dst).isEmpty():

            return False

        else:
            if not path.isdir(dst) and not path.ismount(dst):

                return False

            else:

                return True
