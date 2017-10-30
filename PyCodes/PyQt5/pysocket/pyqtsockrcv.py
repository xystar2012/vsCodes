#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
import sys,os
import struct
import binascii
import ctypes
# reload(sys)
# sys.setdefaultencoding('gb2312') 


class udpSock(QUdpSocket):

    evt_data = pyqtSignal(str)
    def __init__(self,parent = None):
        super(udpSock,self).__init__()
        self._port = 1234
        self.bind(QHostAddress.Any,self._port)
        self.readyRead.connect(self.on_readData)
        self._peerAddr = None
        self._peerPort = None

    def on_send(self,str):
        byte = str.encode('utf8')
        len1 = len(byte)
        fmt = ('=%ds'%(len1))
        print(str,len(str),byte,len1,fmt)
        data = struct.pack(fmt,byte)
        print ('After pack:',binascii.hexlify(data))
        self.writeDatagram(data,self._peerAddr,self._peerPort)

    def on_readData(self):
        while(self.hasPendingDatagrams()):
            data,self._peerAddr,self._peerPort = self.readDatagram(self._port)
            fmt = ('=%ds'% len(data))
            str =  data.decode('utf8') 
            # str = struct.unpack(fmt, data)
            self.evt_data.emit(str)
            print(self.peerAddress(),':',self.peerPort())

class myWindow(QDialog):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        main_lay = QVBoxLayout(self)
        self.resize(600,400)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinimizeButtonHint)
        self._lineEdit = QLineEdit('测试内容接收端')
        self ._btnSend = QPushButton('发送')
        lay = QHBoxLayout()
        lay.addWidget(self._lineEdit)
        lay.addWidget(self._btnSend)
        main_lay.addLayout(lay)
        self._textEdit = QTextEdit(self)
        self._dlgBtn = QDialogButtonBox()
        self._dlgBtn.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        btn_lay.addWidget(self._dlgBtn)

        main_lay.addWidget(self._textEdit)
        main_lay.addLayout(btn_lay)
        btn = self._dlgBtn.button(QDialogButtonBox.Ok)
        btn.clicked.connect(self.on_btnOK)
        btn = self._dlgBtn.button(QDialogButtonBox.Cancel)
        btn.clicked.connect(self.on_btnCancel)
        self._sock = udpSock()
        self._sock.evt_data.connect(self.on_dataCome)
        self._btnSend.clicked.connect(self.on_send)
        self._cnt = 0

    def on_send(self):
        try:
            self._cnt += 1
            text = self._lineEdit.text() + str(self._cnt)
            self._sock.on_send(self._lineEdit.text() + str(self._cnt))
            self._textEdit.append("---> " + text)
        finally:
            print('send error not connect yet!!')

    def on_dataCome(self,data):
        self._textEdit.append('<--- ' +data)

    def on_btnOK(self):
        print("ok")
    def on_btnCancel(self):
        self.reject()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
