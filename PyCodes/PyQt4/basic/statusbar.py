#!/usr/bin/python

# statusbar.py

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(250, 150)
        self.setWindowTitle('statusbar')
        self.statusBar().showMessage('Ready')
        QMessageBox.warning(self,'Message','this is content')
        QMessageBox.question(self,'Message','this is quesion',QMessageBox.Ok,QMessageBox.No)
        


app = QtGui.QApplication(sys.argv)
QtGui.qApp.aboutQt()
main = MainWindow()
main.show()
sys.exit(app.exec_())
