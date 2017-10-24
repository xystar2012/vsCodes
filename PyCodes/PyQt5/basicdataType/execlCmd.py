#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout,qApp
from PyQt5.QtCore import *
import sys,os,json,subprocess
import time  

class mywindow(QDialog):
    def __init__(self,p = None):
        super(mywindow,self).__init__()
        self.resize(800,400)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        mainl = QVBoxLayout(self)
        self.setWindowTitle('Build vs application')
        hl = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setText(r"ping www.baidu.com -n 5")
        fmL = QFormLayout()
        fmL.addRow('命令行:',self.lineEdit)
        self._proc = QProcess()
        self.cmbbuild = QComboBox()
        self.cmbbuild.addItems(['cmd /c','shell -c'])
        self.btnExec = QPushButton('运行')
        hl.addLayout(fmL)
        hl.addWidget(self.cmbbuild)
        hl.addWidget(self.btnExec)

        mainl.addLayout(hl)

        self.textEdit = QTextEdit()
        mainl.addWidget(self.textEdit)

        self.dlgbtns = QDialogButtonBox()
        self.dlgbtns.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Abort)
        hl = QHBoxLayout()
        hl.addStretch()
        hl.addWidget(self.dlgbtns)
        mainl.addLayout(hl)

        self.dlgbtns.button(QDialogButtonBox.Abort).setText('关于Qt')
        self.dlgbtns.button(QDialogButtonBox.Abort).clicked.connect(lambda: QCoreApplication.instance().aboutQt())
        self.dlgbtns.button(QDialogButtonBox.Cancel).clicked.connect(lambda: QCoreApplication.instance().quit())
        self.dlgbtns.button(QDialogButtonBox.Ok).clicked.connect(self.on_build)
        self.lineEdit.returnPressed.connect(self.on_build)
        self.btnExec.clicked.connect(self.dlgbtns.button(QDialogButtonBox.Ok).clicked)

    def buildInProcess(self):
        cmd = self.lineEdit.text()
        cmd = self.cmbbuild.currentText()  + ' ' + cmd
        print(cmd)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            while True:
                r = proc.stdout.readline().strip().decode('gbk')
                if r:
                    QCoreApplication.processEvents(QEventLoop.AllEvents)
                    # print(r)
                    self.textEdit.append(r)
                    self.textEdit.moveCursor(QTextCursor.End)
                if subprocess.Popen.poll(proc) != None and not r:
                    break
            QApplication.restoreOverrideCursor() 
        except:
            print('cat error here')
            QApplication.restoreOverrideCursor() 


    def on_build(self):
        self.buildInProcess()

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())