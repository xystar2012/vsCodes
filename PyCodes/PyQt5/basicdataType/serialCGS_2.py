# code:utf-8
import sys,os
import serial
import time
import struct
from datetime import datetime
from threading import Thread
import random,re
from tendo import singleton
from PyQt5.QtSerialPort import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush,QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
# print(sys.path,sys.version_info)
from datetime import datetime, date,timedelta
import logging
import logging.handlers
import logging.config  



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
        serial = mywindow.g_ser
        currentTimeout = self.waitTimeout

        print("alive:",self.isAlive(),self.is_alive)
        while not self.quit:
                if self.bwait:
                    time.sleep(0.5)
                    continue

                def inner(self):
                    try:
                        if not serial.isOpen():
                            if not serial.open():
                                # self.error.emit("can't not open %s,error code:%d"%(serial.portName(),serial.error()))
                                return

                        if serial.inWaiting() == 0:
                            return

                        data = bytes()
                        requestData = bytes()
                        # print('wait:',serial.in_waiting)
                        requestData = serial.read(serial.inWaiting())
                        hexData = ' '.join('{:02x}'.format(x) for x in requestData)  
                        self.request.emit(hexData)
                        # else:
                        #     self.timeout.emit("Wait read ready timeout %s"%(QTime.currentTime().toString()))
                    except TypeError as e:
                        print('Got Error',e)
                
                inner(self)
                time.sleep(0.01)
                
    def startSlave(self,timeout= 1000):
        self.waitTimeout = timeout
        if not self.isAlive():
            self.start()

class mywindow(QDialog):
    movetoEnd = pyqtSignal()
    g_ser = serial.Serial()

    def __init__(self,p = None):
        super(mywindow,self).__init__()
        self.resize(800,400)
        self.transactionCount = 0
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        mainl = QVBoxLayout(self)
        self.setWindowTitle('成光五期模拟主控串口收发')
        self.thread = SlaveThread(self)

        hl = QHBoxLayout()
        self.timeout = QComboBox()
        self.timeout.addItems('50|100|200|500|1000|2000|3000'.split('|'))
        self.timeout.setCurrentText('1000')
        fmL = QFormLayout()
        fmL.addRow('串口超时:',self.timeout)
        self.serialPortComboBox = QComboBox()
        fmL2 = QFormLayout()
        self.baudrateCmd = QComboBox()
        self.baudrateCmd.setEditable(True)
        self.baudrateCmd.addItems(['4800','115200','9600','19200','460800'])
        self.baudrateCmd.setCurrentIndex(1)
        fmL2.addRow('串口波特率:',self.baudrateCmd)
        for ii in QSerialPortInfo.availablePorts():
                self.serialPortComboBox.addItem(ii.portName())
        # self.serialPortComboBox.setCurrentIndex(0)
        self.serialPortComboBox.setCurrentIndex(self.serialPortComboBox.count() -1)
        self.btnExec = QPushButton('执行')
        self.btnStop = QPushButton('停止')
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
        
        self.btn_startTask = QPushButton('开始任务')
        self.btn_stopTask = QPushButton('停止任务')
        self.btn_startRec = QPushButton('开始记录')
        self.btn_pauseRec = QPushButton('暂停记录')
        self.btn_resumeRec = QPushButton('恢复记录')
        self.btn_stopRec = QPushButton('停止记录')
        fl = QFormLayout()
        taskname = 'test_' + '{:%Y%m%d}'.format(datetime.now())
        self.editTask  = QLineEdit(taskname)
        
        fl.addRow('任务名：',self.editTask)
        group1 = QGroupBox('任务')

        vl = QVBoxLayout(group1)

        
        hl = QHBoxLayout()
        self.boxs = []
        for i in range(1,5):
            self.boxs.append(QCheckBox('ccd%d'%i))
            # if i == 1:
            #     self.boxs[0].setChecked(True)
            self.boxs[i - 1].setChecked(True)
        hl.addStretch()
        for box in self.boxs:
            box.setCheckable(True)
            hl.addWidget(box)
        vl.addLayout(hl)

        hl = QHBoxLayout()
        # hl.addStretch()
        hl.addLayout(fl)
        hl.addWidget(self.btn_startTask)
        hl.addWidget(self.btn_stopTask)
        vl.addLayout(hl)
        
        gl = QGridLayout()
        gl.addWidget(group1,0,0,2,1)
        gl.addWidget(self.btn_startRec,0,1,Qt.AlignRight)
        gl.addWidget(self.btn_stopRec,0,2,Qt.AlignLeft)
        gl.addWidget(self.btn_pauseRec,1,1,Qt.AlignRight)
        gl.addWidget(self.btn_resumeRec,1,2,Qt.AlignLeft)
        gl.setSpacing(5)
        frm = QFrame(self)
        frm.setFrameShape(QFrame.HLine)
        frm.setFrameShadow(QFrame.Sunken)
        gl.addWidget(frm,2,0,1,4)

        mainl.addLayout(gl)

        self.textEdit = QTextEdit()
        mainl.addWidget(self.textEdit)
        self.textEdit.document().setMaximumBlockCount(102400)
        self.dlgbtns = QDialogButtonBox()
        self.dlgbtns.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel|QDialogButtonBox.Abort)
        
        hl = QHBoxLayout()
        hl.setSpacing(10)
        self.statusLabel = QLabel("status label")
        self.countLabel = QLabel('统计')
        self.countLabel.setWordWrap(True)
        hl.addWidget(self.statusLabel,1)
        hl.addWidget(self.countLabel,1)
        hl.addWidget(self.dlgbtns)
        mainl.addLayout(hl)

        self.dlgbtns.button(QDialogButtonBox.Abort).setText('关于Qt')
        self.dlgbtns.button(QDialogButtonBox.Ok).setText('Run')
        self.dlgbtns.button(QDialogButtonBox.Abort).clicked.connect(lambda: QCoreApplication.instance().aboutQt())
        self.dlgbtns.button(QDialogButtonBox.Cancel).clicked.connect(lambda: QCoreApplication.instance().quit())
        self.dlgbtns.button(QDialogButtonBox.Ok).clicked.connect(self.startSlave)
        
        self.btn_startTask.clicked.connect(self.on_startTask)
        self.btn_stopTask.clicked.connect(self.on_stopTask)
        self.btn_startRec.clicked.connect(self.on_startRec)
        self.btn_pauseRec.clicked.connect(self.on_pauseRec)
        self.btn_resumeRec.clicked.connect(self.on_resumRec)
        self.btn_stopRec.clicked.connect(self.on_stopRec)

        self.btnExec.clicked.connect(self.dlgbtns.button(QDialogButtonBox.Ok).clicked)
        self.runButton = self.dlgbtns.button(QDialogButtonBox.Ok)
        self.thread.request.connect(self.showRequest)
        self.thread.error.connect(self.processError)
        self.thread.timeout.connect(self.processTimeout)
        self.btnStop.clicked.connect(self.on_stopRecv)
        self.movetoEnd.connect(lambda: self.textEdit.moveCursor(QTextCursor.End))
        self.initLog()   
        print(QThread.currentThreadId(),' main is running ...')
        self._timer = QTimer(self)
        self._timer.setInterval(20*1000)
        self._timer.timeout.connect(self.on_autoRecord)
        self._autoRecCnt = 0
        self._timer.start()
        QTimer.singleShot(0,self.on_autoStart)

    def on_autoStart(self):
        self.startSlave()
        self.on_autoRecord()

    def on_autoRecord(self):
        self.on_startRec()
        info = time.ctime()
        self._autoRecCnt += 1
        info = 'auto start record,count:%d %s'%(self._autoRecCnt,time.ctime())
        self.logger.info(info)
        QTimer.singleShot(10*1000,self.on_autoStop)
        self.countLabel.setText(info)

    def on_autoStop(self):
        self.on_stopRec()
        info = 'auto stop record,count:%d %s'%(self._autoRecCnt,time.ctime())
        self.logger.info(info)
        self.countLabel.setText(info)

    def initLog(self):
        filename = os.path.basename(os.path.realpath(sys.argv[0]))
        LOG_FILE = os.path.splitext(filename)[0] + time.strftime('_%Y%m%d') + '.log' 
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
        # fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s' 
        fmt = '%(asctime)s - %(levelname)s: %(message)s' 
        formatter = logging.Formatter(fmt)   # 实例化formatter  
        handler.setFormatter(formatter)      # 为handler添加formatter  
        self.logger = logging.getLogger('serial')    # 获取名为tst的logger  
        self.logger.addHandler(handler)           # 为logger添加handler  
        self.logger.setLevel(logging.DEBUG) 

    def getCameras(self):
        cams = bytearray(4)
        i = 0
        for box in self.boxs:
            if box.isChecked():
                cams[i] = 0x1
            i += 1
        return  cams

    def on_serialCmdSend(self,data):
        if not mywindow.g_ser.isOpen():
            return

        if len(data)%4 != 0:
            data += bytearray(4 - len(data)%4)

        try:
            msg = bytearray.fromhex('e7'*4)
            msg += struct.pack('>H',len(data) + 4)
            msg += data
            msg += bytearray.fromhex('7e'*4)          
            nLen = self.g_ser.write(msg)
            if nLen == len(msg):
                bData = bytes(msg)
                hexData = ' '.join('{:02x}'.format(x) for x in bData)
                self.textEdit.append('sendCMD:' + hexData)
                # self.textEdit.moveCursor(QTextCursor.End)
                print('cmdsnd:' +  hexData)
                self.logger.info('cmdsnd:' +hexData)
            else:
                self.thread.timeout.emit(self.g_ser.portName() + ":Wait write response timeout %s"%(QTime.currentTime().toString()))
        except:
            print('on_serialCmdSend error ...')
        
    def on_startTask(self):
        self.on_serialCmdSend(self.fmtStartTask())
      
    def on_stopTask(self):
        self.on_serialCmdSend(self.fmtStopTask())

    def on_startRec(self):
        self.on_serialCmdSend(self.fmtStartRecord())

    def on_pauseRec(self):
        self.on_serialCmdSend(self.fmtPauseRec())

    def on_resumRec(self):
        self.on_serialCmdSend(self.fmtResumRec())

    def on_stopRec(self):
        self.on_serialCmdSend(self.fmtStopRecod())

    def fmtStartRecord(self):
        data = bytearray()
        data += b'1011;'
        data += self.getCameras()
        frams = struct.pack('=I',0)
        data += frams*4
        tims = struct.pack('=I',0)
        data += tims*4

        return data

    def fmtPauseRec(self):
        data = bytearray()
        data += b'1012;'
        data += self.getCameras()
        
        return data

    def fmtResumRec(self):
        data = bytearray()
        data += b'1013;'
        data += self.getCameras()

        return data
    
    def fmtStopRecod(self):
        data = bytearray()
        data += b'1014;'
        data += self.getCameras()

        return data

    def fmtStopTask(self):
        data = bytearray()
        data += b'1015;'
        data += self.getCameras()

        return data

    def fmtStartTask(self):
        data = bytearray()
        data += b'1010;'
        ## taskname
        taskNam = self.editTask.text()
        data += struct.pack('32s',bytes(taskNam,'utf8'))
        # char task_type;					
        # bit[0-3]--0:self check data; 1:cameralink; 2:gtx; 4:sdi; 
        # bit[4-7]--when self check data, 0:horizontal; 1:vertical;
        data += bytearray.fromhex('01')
        # char store_type;
        data += bytearray(1)
        data += self.getCameras()

        return data
    
    def startSlave(self):
        self.g_ser.port = self.serialPortComboBox.currentText()
        self.g_ser.baudrate = self.baudrateCmd.currentText()
        mywindow.g_ser.timeout = 0.5
        mywindow.g_ser.writeTimeout = 0.5

        if not self.g_ser.isOpen():
            self.g_ser.open()
        mywindow.g_ser.flushInput()
        self.btnStop.setEnabled(True)
        self.thread.bwait = False
        self.runButton.setEnabled(False)
        self.btnExec.setEnabled(False)
        self.statusLabel.setText("Status: Running, connected to port %s."%(self.serialPortComboBox.currentText()))
        self.thread.startSlave(int(self.timeout.currentText()))

    def on_stopRecv(self):
        self.thread.bwait = True
        self.btnExec.setEnabled(True)
        self.runButton.setEnabled(True) 
        self.btnStop.setEnabled(False)
        self._timer.stop()
        mywindow.g_ser.close()

    def showSysStatus(self,rawdata):
        # rawdata = bytearray()
        fmt = 'h'*10 + '4s4si'
        data = struct.unpack(fmt,rawdata)
        print(data)
        self.logger.info('cmdupk:' + str(data))
        self.textEdit.append('cmdupk:' + str(data))

    def showRequest(self,s):
        # self.transactionCount += 1
        # self.textEdit.append("transaction #%d:-response: %s"%(self.transactionCount,s))
        
        self.logger.info('cmdrcv:' + s)
        
        # self.textEdit.moveCursor(QTextCursor.End)
        m = re.search(r'e7 e7 e7 e7 00 2a 30 3b 32 30 32 33 3b 30 3b (.*?) 3b 7e 7e 7e 7e', s)
        if m:
            print(s)
            # self.logger.info('cmdrcv:' + str(m.groups(1)))
            self.textEdit.append('cmdrcv:' + str(m.groups(1)))
            self.showSysStatus(bytearray.fromhex(m.group(1)))

    def processError(self,s):
        self.activateRunButton()
        self.statusLabel.setText(("Status: Not running, %s.")%(s))
        self.textEdit.append("Error here,No traffic.")

    def processTimeout(self,s):
        self.statusLabel.setText(("Status: Running, %s.")%(s))
        # self.textEdit.append("Timeout here,No traffic.")

    def activateRunButton(self):
        self.btnExec.setEnabled(True)
        self.runButton.setEnabled(True)

if __name__ == '__main__':
    oneApp = singleton.SingleInstance()
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
