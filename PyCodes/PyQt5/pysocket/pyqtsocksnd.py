#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush,QTextDocument
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
import sys,os

class myWindow(QDialog):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        main_lay = QVBoxLayout(self)
        self._sock = QUdpSocket()
        self.resize(600,400)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinimizeButtonHint)
        self._lineEdit = QLineEdit('测试内容发送端')
        self._lineAddr = QLineEdit("10.10.10.211:1234")
        self ._btnSend = QPushButton('发送')
        lay = QHBoxLayout()
        lay.addWidget(self._lineEdit,2)
        lay.addWidget(self._lineAddr,1)
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
        self._sock = QUdpSocket()
        self._sock.readyRead.connect(self.on_dataCome)
        self._btnSend.clicked.connect(self.on_send)
        self._cnt = 0
        self._time = QTimer()
        self._time.timeout.connect(self.on_send)
        self._time.start(1000)
        self._textEdit.document().setMaximumBlockCount(1000)
        self._textEdit.textChanged.connect(lambda:self._textEdit.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor))

    def on_send(self):
        self._cnt += 1
        addr = self._lineAddr.text().split(':')
        self._sock.connectToHost(QHostAddress(addr[0]),int(addr[1]))
        text = self._lineEdit.text()
        text += str(self._cnt)
        nRet = self._sock.write(text.encode('utf8'))
        self._textEdit.append('---> ' + text + ' sndCnt:' + str(nRet))
        
    def on_dataCome(self):
        while(self._sock.hasPendingDatagrams()):
            peerAddr = QHostAddress()
            peerPort = 0
            # data,peerAddr,peerPort = self._sock.readDatagram(self._sock.localPort())
            data = self._sock.read(self._sock.peerPort())
            if not data:
                break
            str = data.decode('utf8')
            self._textEdit.append('<--- ' + str)
            print(peerAddr,':',peerPort,'Local:',self._sock.localPort(),'Peer:',self._sock.peerPort())

    def on_btnOK(self):
        print("ok")
    def on_btnCancel(self):
        self.reject()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
