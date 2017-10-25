#!/usr/bin/python

# mainwindow.py

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import qApp
from PyQt4.QtGui import *
import main_rc


class myDlg(QDialog):
    def __init__(self,parent=None):
        super(myDlg,self).__init__()
        self._digbt = QDialogButtonBox(self)
        self._digbt.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.No
        |QDialogButtonBox.Abort)
        hbox = QHBoxLayout()
        hbox.addWidget(self._digbt)

        self.resize(400,200)

        manLay = QVBoxLayout()
        self._wgt = QWidget(self)
        manLay.addWidget(self._wgt,1)
        manLay.addLayout(hbox)
        self.setLayout(manLay)



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(350, 250)
        self.setWindowTitle('mainwindow')
        
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        exit = QtGui.QAction(QtGui.QIcon(':/icons/Precedent32.png'), 'ShowDlg', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        # self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        # self.connect(exit, QtCore.SIGNAL('triggered()'), )
        exit.triggered.connect(self.on_showDlg)
        okAct = QtGui.QAction(QtGui.QIcon(':/icons/Camera.png'),'Ok',self)
        # okAct.triggered.connect(QtCore.SLOT('close()'))
        self.connect(okAct,QtCore.SIGNAL('triggered()'),qApp,QtCore.SLOT('aboutQt()'))

        self.statusBar()

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        file.addAction(okAct)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)
        toolbar.addAction(okAct)

    def on_showDlg(self):
        dlg = myDlg()
        dlg.exec_()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
