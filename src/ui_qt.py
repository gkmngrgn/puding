#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

from PyQt4 import (QtCore, QtGui, uic)
from sys import (argv, exit)

from common import share_dir

class Create(QMainWindow):
    def __init__(self, parent = None):
        super(Create, self).__init__(parent)
        ui.LoadUi("%s/ui/qtMain.ui" % share_dir, self)

        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        
        self.main()

    def main(self):
        app = QtGui.QApplication(argv)
        form = Create()
        form.show()
        exit(app.exec_())