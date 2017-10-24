#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout
from PyQt5.QtCore import *
import sys,os,json

class myWindow(QDialog):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        main_lay = QVBoxLayout(self)
        self.resize(600,400)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinimizeButtonHint)
        self._lineEdit = QLineEdit('e:/svn_Root/ReleaseBuild/')
        frmLay = QFormLayout()
        frmLay.addRow('收集路径:',self._lineEdit)
        self ._btnSend = QPushButton('开始打包')
        lay = QHBoxLayout()
        lay.addLayout(frmLay,2)
        self._cmbType = QComboBox()
        type = ['normale','chengg4','chengg5']
        print(type)
        self._cmbType.addItems(type)
        frmLay = QFormLayout()
        frmLay.addRow('Eagle版本:',self._cmbType)
        lay.addLayout(frmLay,1)
        lay.addWidget(self._btnSend)
        main_lay.addLayout(lay)

        self._textEdit = QTextEdit(self)
        self._dlgBtn = QDialogButtonBox()
        self._dlgBtn.setStandardButtons(QDialogButtonBox.Cancel)

        btn_lay = QHBoxLayout()
        btn_lay.addStretch()
        btn_lay.addWidget(self._dlgBtn)
        main_lay.addWidget(self._textEdit)
        main_lay.addLayout(btn_lay)
        btn = self._dlgBtn.button(QDialogButtonBox.Cancel)
        btn.clicked.connect(self.on_btnCancel)
        self._btnSend.clicked.connect(self.on_startWork)
        # self._cmbType
        # self._btnSend.clicked.emit()


    def on_startWork(self):
        self._textEdit.clear()
        rootdir = r'E:\svn_Root\Eagle_Branch_Dir\EagleClusterTrunk\MainFrame\Release'
        list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path = os.path.join(rootdir,list[i])
            if os.path.isfile(path):
                self._textEdit.append(path)
        self._textEdit.moveCursor(QTextCursor.End)

    def on_btnCancel(self):
        msgbox = QMessageBox()
        btnOK = msgbox.addButton('好的',QMessageBox.YesRole)
        btnNo = msgbox.addButton('不好',QMessageBox.NoRole)
        msgbox.setText('你要关掉嘛？')
        msgbox.setWindowTitle('关前卡住')
        msgbox.exec()
        # print(msgbox.exec(),QMessageBox.Yes,QMessageBox.No)
        if msgbox.clickedButton() == btnOK:
            self.reject()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(QCoreApplication.libraryPaths())
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
