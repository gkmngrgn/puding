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
        self.connect(self.button_prev, QtCore.SIGNAL("clicked()"), self.__actionPreview)
        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

    def __actionNext(self):
        src = self.line_src.displayText()
        dst = self.line_dst.displayText()

        if not self.__checkSource(src):
            self.label_warning.setText("<font color=\"red\">The ISO path you have specified is invalid!</font>")
            
            return False

        if not self.__checkDestination(dst):
            self.label_warning.setText("<font color=\"red\">The USB disk path you have specified is invalid!</font>")
            
            return False

        self.label_warning.setText("<strong>The paths you have specified are valid..</strong>")

        id = self.stackedWidget.currentIndex()
        if id < 1:
            self.stackedWidget.setCurrentIndex(id + 1)
            
        return True

    def __actionPreview(self):
        id = self.stackedWidget.currentIndex()
        
        if id > 0:
            self.stackedWidget.setCurrentIndex(id - 1)

    def __checkSource(self, src):
        if QtCore.QString(src).isEmpty():

            return False

        else:
            src_extension = path.splitext(str(src))[1] == ".iso"

            return path.isfile(src) and src_extension

    def __checkDestination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        else:
            return path.ismount(str(dst))
