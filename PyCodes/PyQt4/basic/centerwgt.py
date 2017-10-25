#!/usr/bin/python

# center.py

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import QPushButton,QVBoxLayout,QHBoxLayout

class Center(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('center')
        vLay = QVBoxLayout(self)
        btn1 = QPushButton('关于Qt',self)
        btn2 = QPushButton('关于Py',self)
        hLay = QHBoxLayout()
        hLay.addStretch()
        hLay.addWidget(btn1)
        hLay.addWidget(btn2)
        hLay.addStretch()
        vLay.addLayout(hLay)
        btn1.clicked.connect(lambda: QtGui.QApplication.instance().aboutQt())
        btn2.clicked.connect(lambda:  print(sys.version))
        # self.resize(600, 400)
        self.setGeometry(300, 300, 350, 300)
        QTimer.singleShot(1000,self.center)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
       
        # self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        size.moveCenter(screen.center())
        self.setGeometry(size)

    def showEvent(self,evt):
        print ('show it befor shown')


app = QtGui.QApplication(sys.argv)
# app.aboutQt()
print(sys.version_info)
qb = Center()
qb.show()
sys.exit(app.exec_())
