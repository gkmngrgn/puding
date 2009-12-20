#!/usr/bin/python
# -*- coding: utf-8 -*-

def run():
    app = QtGui.QApplication(sys.argv)
    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load("%s/qm/puding_%s.qm" % (SHARE, locale))
    app.installTranslator(translator)
    form = Create()
    form.show()
    sys.exit(app.exec_())

