#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class MyWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.ok_button = QtGui.QPushButton("OK", self)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        self.connect(self.ok_button, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("slot1()"))
        self.connect(self, QtCore.SIGNAL('emit_python_list(PyQt_PyObject)'), 
                     self, QtCore.SLOT("slot2(PyQt_PyObject)"))

    @QtCore.pyqtSlot()
    def on_button_clicked(self):    
        print "click me!!!!"

    @QtCore.pyqtSlot()    
    def slot1(self):
        self.emit(QtCore.SIGNAL("emit_python_list(PyQt_PyObject)"), [1, 2, 3, 4, 5, 6])

    @QtCore.pyqtSlot("PyQt_PyObject")    
    def slot2(self, alist):
        print alist

if __name__ == "__main__":        
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    app.exec_()