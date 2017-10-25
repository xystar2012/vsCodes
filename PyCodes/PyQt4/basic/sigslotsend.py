#!/usr/bin/python
# -*- coding: utf-8 -*-

# emit.py

import sys
import random
from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        vLay = QtGui.QVBoxLayout()
        self.setObjectName('Example哈哈')
        self._cmb = QtGui.QComboBox(self)
        self._cmb.addItems(('are','you','ok','!'))
        self._btn = QtGui.QPushButton('chageColor',self)
        self._btn.clicked.connect(self.on_btnclick)
        vLay.addWidget(self._cmb)
        vLay.addWidget(self._btn)
        self.setLayout(vLay)
        # self._cmb.currentIndexChanged['QString'].connect(self.on_cmbChange)
        self._cmb.currentIndexChanged['int'].connect(self.on_cmbChange)
        QtCore.QTimer.singleShot(100,self.on_timeOut)
        self._cmb.currentIndexChanged.emit(2)
        # self._btn.clicked.emit(True)
        self._btn.setCheckable(True)


    def initUI(self):
        self.connect(self, QtCore.SIGNAL('closeEmitApp()'),
            self.on_sigGet)
            # QtCore.SLOT('close()'))

        self.setWindowTitle('emit')
        self.resize(250, 150)

    def showEvent(self,evt):
        # rec = self._btn.rect()
        # rec.moveCenter(self.rect().center())
        # self._btn.setGeometry(rec)
        print('show before you see')

    def on_timeOut(self):
        print('timeOut')
        # self._btn.click()
        # self._btn.emit(QtCore.SIGNAL("clicked(bool)"))
        self._btn.clicked.emit(True)

    def on_cmbChange(self,str):
        
        print('cmb triggered:',self._cmb.currentIndex(),self._cmb.currentText(),str)

    def on_btnclick(self,ret):
        print(self.sender().text(),'btn clicked',ret)
        palette = QtGui.QPalette()
        a = QtCore.Qt.black
        b = QtCore.Qt.darkYellow
        print(a,b)
        palette.setColor(self.backgroundRole(),QtCore.Qt.GlobalColor(random.uniform(a,b)))
        print(self.backgroundRole())
        self.setPalette(palette)

    def on_sigGet(self):
        self.sender()
        print('Got closeEmitApp',self.sender().objectName())

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('closeEmitApp()'))


app = QtGui.QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
