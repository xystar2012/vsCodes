# -*- coding: utf-8 -*-

from PyQt5 import QtCore,QtGui,QtWidgets
import sys,os
sys.path.append('./serialport')
os.chdir(sys.path[0])
import serialport.serialportwindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = serialport.serialportwindow.SerialPortWindow()
    win.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()