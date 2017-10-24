from PyQt5.QtSerialPort import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush,QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
import threading
from threading import Thread
import sys
import time
import struct,re,math,random
import binascii
import ctypes
from tendo import singleton

class SlaveThread(QObject,Thread):
    request = pyqtSignal(str)
    error = pyqtSignal(str)
    timeout = pyqtSignal(str)

    def __init__(self,parent = None):
        super(SlaveThread,self).__init__()
        self.waitTimeout = 0
        self.quit = False
        self.mutex = QMutex()
        print(QThread.currentThreadId(),' Init is running ...')
        self._count = 0
        self.bwait = False
        self.bVariantData = False
        
    def on_time():
        pass 

    def __del__(self):
        self.mutex.lock()
        self.quit = True
        self.mutex.unlock()

    def run(self):
        print(QThread.currentThreadId(),' is running ...')
        currentChange = False
        self.mutex.lock()
        currentPortNam = ""
        if currentPortNam != self.portName:
            currentPortNam = self.portName
            self.currentChange = True

        currentTimeout = self.waitTimeout
        self.mutex.unlock()
        serial = QSerialPort()
        serial.setBaudRate(460800)
        serial.setDataBits(QSerialPort.Data8)
        serial.setFlowControl(QSerialPort.NoFlowControl)
        serial.setStopBits(QSerialPort.OneStop)
        serial.setPortName(currentPortNam)

        print("alive:",self.isAlive(),self.is_alive)
        while not self.quit:
            try:
                if self.bwait:
                    time.sleep(0.5)
                    continue

                if not serial.isOpen():
                    if not serial.open(QIODevice.ReadWrite):
                        self.error.emit("can't not open %s,error code:%d"%(currentPortNam,serial.error()))
                        return

                if serial.waitForReadyRead(currentTimeout):
                    requestData = bytes()
                    requestData = serial.readAll()
                    while serial.waitForReadyRead(10):
                        requestData += serial.readAll()

                    # hexb = binascii.b2a_hex(bytes(requestData)) 
                    # m = re.search('(7e.{20,20}e7)', str(hexb))
                    # print(str(hexb))
                    # requestStr = str(bytes(requestData))
                    bData = bytes(requestData)
                    hex = ' '.join('{:02x}'.format(x) for x in bData)  
                    m = re.search('(7e.{31,31}e7)', hex)
                    if m:
                        requestStr = m.group(0)
                        # requestStr = str(bytes(requestData))
                        self.request.emit(requestStr)
                    ### 构造发送数据
                    dateSend = self.fmtDateSend()
                    serial.write(dateSend)
                    if serial.waitForBytesWritten(currentTimeout):
                        print(' '.join('{:02x}'.format(x) for x in dateSend))
                    else:
                        self.timeout.emit("Wait write response timeout %s"%(QTime.currentTime().toString()))
                else:
                    self.timeout.emit("Wait read ready timeout %s"%(QTime.currentTime().toString()))
            except TypeError as e:
                print('Got Error',e)
                
    def fmtDateSend(self):
        ### 年 月 日
        rate = 1 if self.bVariantData else 0
        self._count += 1
        data = bytearray.fromhex('7e')
        date = QDateTime.currentDateTime()
        dt = date.date()
        data += struct.pack('=BBB',dt.year() - 2000,dt.month(),dt.day())
        tm = date.time()
        ms = (tm.msecsSinceStartOfDay())*10
        data += struct.pack('=I',ms)

        ## 帧频   相机类型8,9  ok
        i = 0x1 if rate*self._count%2 else 0x10
        data += struct.pack('=BB',i,0x02)
        # print(type(data),len(data),data)
        ## A、E 角度
        A = int((10.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        E = int((20.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        dA = struct.pack('I',A)
        data += dA[0:3]
        dE = struct.pack('I',E)
        data += dE[0:3]

        ## 调光调焦 16,17   0.0560456
        foclen = (20 + rate*random.uniform(0.1,0.9))*pow(10,3)/1.6
        print('foclen',hex((int(foclen))))
        data += struct.pack('=H',int(foclen))
        data += bytearray.fromhex('00'*2)
        ## 目标距离
        data += struct.pack('=I',50 + rate*int(random.uniform(1,9)))
        
        ## 滤光片  拖把量 24,25
        list1 = [0x01,0x02,0x2,0x3,0x4]
        list2 = [0x0,0x11]
        data += struct.pack('=BB',list1[rate*self._count%4],list2[rate*self._count%2])
        ### miss A E
        missAE = struct.pack('=HH',0x8050 + rate*int(random.uniform(1,9)),0x7000 + rate*int(random.uniform(1,9)))
        print('missAE:',missAE)
        data += missAE
        data += bytearray.fromhex('00'*1)
        ## A  E 速度
        A = int((10.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        E = int((20.123456 + rate*int(random.uniform(1,9)))*pow(2,24)/360)
        dA = struct.pack('I',A)
        data += dA[0:3]
        dE = struct.pack('I',E)
        data += dE[0:3]
        print('AESpeed:',A,E)
        data += bytearray.fromhex('00'*2)
        ## 尾部
        data += bytearray.fromhex('e7')
        print(len(data))
        return data

    def startSlave(self,portNam,timeout= 1000):
        locker = QMutexLocker(self.mutex)
        self.portName = portNam
        self.waitTimeout = timeout

        if not self.isAlive():
            self.start()

class mywindow(QDialog):
    movetoEnd = pyqtSignal()
    def __init__(self,p = None):
        super(mywindow,self).__init__()
        self.resize(800,400)
        self.transactionCount = 0
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        mainl = QVBoxLayout(self)
        self.setWindowTitle('Build vs application')

        self.thread = SlaveThread(self)
        hl = QHBoxLayout()
        self.timeout = QComboBox()
        self.timeout.addItems('50|100|200|500|1000|2000|3000'.split('|'))
        self.timeout.setCurrentText('1000')
        fmL = QFormLayout()
        fmL.addRow('串口超时:',self.timeout)
        self.serialPortComboBox = QComboBox()
        fmL2 = QFormLayout()
        self.valiantCmb = QComboBox()
        self.valiantCmb.addItems(['0','1'])
        self.valiantCmb.setCurrentIndex(1)
        fmL2.addRow('随机值:',self.valiantCmb)
        for ii in QSerialPortInfo.availablePorts():
                self.serialPortComboBox.addItem(ii.portName())
        self.serialPortComboBox.setCurrentIndex(self.serialPortComboBox.count() -1)
        self.btnExec = QPushButton('运行')
        self.btnStop = QPushButton('取消')
        # hl.addLayout(fmL)
        hl.setSpacing(10)
        hl.addStretch()
        hl.addLayout(fmL)
        hl.addLayout(fmL2)
        hl.addWidget(self.serialPortComboBox)
        hl.addWidget(self.btnExec)
        hl.addWidget(self.btnStop)

        mainl.addLayout(hl)

        frm = QFrame(self)
        frm.setFrameShape(QFrame.HLine)
        frm.setFrameShadow(QFrame.Sunken)
        mainl.addWidget(frm)

        self.textEdit = QTextEdit()
        mainl.addWidget(self.textEdit)
        self.textEdit.document().setMaximumBlockCount(102400)
        self.dlgbtns = QDialogButtonBox()
        self.dlgbtns.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Abort)
        
        hl = QHBoxLayout()
        
        self.statusLabel = QLabel("status label")
        hl.addWidget(self.statusLabel,1)
        hl.addWidget(self.dlgbtns)
        mainl.addLayout(hl)

        self.dlgbtns.button(QDialogButtonBox.Abort).setText('关于Qt')
        self.dlgbtns.button(QDialogButtonBox.Ok).setText('Run')
        self.dlgbtns.button(QDialogButtonBox.Abort).clicked.connect(lambda: QCoreApplication.instance().aboutQt())
        self.dlgbtns.button(QDialogButtonBox.Cancel).clicked.connect(lambda: QCoreApplication.instance().quit())
        self.dlgbtns.button(QDialogButtonBox.Ok).clicked.connect(self.startSlave)
        self.btnExec.clicked.connect(self.dlgbtns.button(QDialogButtonBox.Ok).clicked)
        self.runButton = self.dlgbtns.button(QDialogButtonBox.Ok)
        self.thread.request.connect(self.showRequest)
        self.thread.error.connect(self.processError)
        self.thread.timeout.connect(self.processTimeout)
        self.btnStop.clicked.connect(self.on_stopRecv)
        self.valiantCmb.currentIndexChanged[int].connect(self.on_dataTypeChange)
        self.movetoEnd.connect(lambda: self.textEdit.moveCursor(QTextCursor.End))
        
        print(QThread.currentThreadId(),' main is running ...')
    
    def on_dataTypeChange(self,data):
        self.thread.bVariantData = bool(data)


    def on_stopRecv(self):
        self.thread.bwait = True
        self.btnExec.setEnabled(True)
        self.runButton.setEnabled(True) 
        self.btnStop.setEnabled(False)

    def startSlave(self):
        self.btnStop.setEnabled(True)
        self.thread.bwait = False
        self.runButton.setEnabled(False)
        self.btnExec.setEnabled(False)
        self.statusLabel.setText("Status: Running, connected to port %s."%(self.serialPortComboBox.currentText()))
        self.thread.startSlave(self.serialPortComboBox.currentText(),int(self.timeout.currentText()))
        self.valiantCmb.currentIndexChanged.emit(self.valiantCmb.currentIndex())

    def showRequest(self,s):
        self.transactionCount += 1
        self.textEdit.append("Traffic, transaction #%d:"
                            "\n\r-response: %s" %(self.transactionCount,s))
        self.textEdit.moveCursor(QTextCursor.End)
        # self.movetoEnd.emit()

    def processError(self,s):
        self.activateRunButton()
        self.statusLabel.setText(("Status: Not running, %s.")%(s))
        self.textEdit.append("Error here,No traffic.")

    def processTimeout(self,s):
        self.statusLabel.setText(("Status: Running, %s.")%(s))
        self.textEdit.append("Timeout here,No traffic.")

    def activateRunButton(self):
        self.btnExec.setEnabled(True)
        self.runButton.setEnabled(True)

    
if __name__ == '__main__':
    oneApp = singleton.SingleInstance()
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
