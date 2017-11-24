# -*- coding: utf-8 -*-

from PyQt5 import QtCore,QtGui,QtWidgets
import sys,os

def main():
    dir = os.path.split(os.path.realpath(__file__))[0]
    sys.path = [os.path.join(dir,'serialport')] + sys.path
    os.chdir(dir)
    import serialport.serialportwindow
    app = QtWidgets.QApplication(sys.argv)
    win = serialport.serialportwindow.SerialPortWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    
    main()