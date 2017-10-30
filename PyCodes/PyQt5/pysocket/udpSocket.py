from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal,QTimer,QThread,Qt,QEvent
from PyQt5.QtGui import QImage,QPainter,QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os,os.path,sys,math,socket
import operator
import ui_udpsendbyqt as uiMain
import struct
import binascii
import ctypes
import random

class CUdp(QThread):
    def __init__(self,parent = None):
        QThread.__init__(self,parent)
        self.initSock()
        self._bInit = False
    
    def initSock(self):
        self._sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if not self._sock:
            print('sock error!')
        self._sock.setblocking(1)
        self._sock.settimeout(1)
        self._bInit = True

    
    def Init(self,port,addr):
        
        self.Quit()
        if not self._bInit:
            self.initSock()
        self._addr = addr
        if not self._sock:
            return
        
        localAddr = ('',port)
        self._sock.bind(localAddr)
        self._peerAddr = (addr[0],int(addr[1]))
        
    
    def Quit(self):
        
        if not self._sock:
            return
        self._sock.close()
        self._bInit = False
        
    def sendMsg(self,data):
        if not self._sock:
            return
        self._sock.sendto(data,self._peerAddr)
        

    def run(self):
        print(QThread.currentThread(),' is running ...')
        while self.isRunning():
            if self.isInterruptionRequested():
                break
            if not self._sock:
                QThread.sleep(1)
                continue
            try:
                data = self._sock.recvfrom(1024)
                if not data:
                    print('socket error here!!')
            except socket.error as msg:
                data = None
                continue

            
        print(QThread.currentThread(),' quitting ...')

class myWindow(QMainWindow):
    nPos = 0
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.ui = uiMain.Ui_UDPSendByQtClass()
        self.ui.setupUi(self)
        self._timerSroll = QTimer()
        self.m_scrollCaptionStr = '模拟西安Udp叠加发送端，包含 GPS、单播、组播'
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(-5, self.ui.scrollCaptionLabel.fontMetrics().height());
        self._timerSroll.start(500);
        shadow.setColor(Qt.darkMagenta);
        shadow.setBlurRadius(8)
        self.ui.scrollCaptionLabel.setText(self.m_scrollCaptionStr);
        self.ui.scrollCaptionLabel.setGraphicsEffect(shadow);
        self.ui.textEdit.document().setMaximumBlockCount(102400)
        self.relayoutUi()
        self._timeGPs = QTimer(self)
        self._timerMulti = QTimer(self)
        self._timeSingle = QTimer(self)

        self.m_udpMulti = CUdp(self)
        self.m_udpSingle = CUdp(self)
        self.m_udpSingle2 = CUdp(self)
        self.m_udpGps = CUdp(self)

        self.m_udpMulti.start()
        self.m_udpSingle.start()
        self.m_udpSingle2.start()
        self.m_udpGps.start()

        self.connect()

    def connect(self):
        self._timerSroll.timeout.connect(self.on_wordRun)
        self._timeGPs.timeout.connect(self.on_timeOut_gps)
        self._timerMulti.timeout.connect(self.on_timeOut_Multi)
        self._timeSingle.timeout.connect(self.on_timeOut_Single)
        self.ui.btn_start.clicked.connect(self.on_Init)
        self.ui.btn_stop.clicked.connect(self.on_Quit)

    def on_timeOut_gps(self):
        dt = QDateTime.currentDateTime()
        time = dt.time().msecsSinceStartOfDay()
        str = struct.pack('=BIBBB',0xAA,time,65,66,0xAA)
        self.m_udpGps.sendMsg(str)
        str = 'tData._time:%d'%(time)
        self.ui.textEdit.append(str)

    si_Cnt = 0
    def on_timeOut_Single(self):
        if self.ui.cmb_data.currentIndex() == 0: ##顺序递增  模拟
            myWindow.si_Cnt += 1
            myWindow.si_Cnt %= 100
            _fraps = 5000 + myWindow.si_Cnt*100
            _focus = 1000 + myWindow.si_Cnt*10
            _distance = 5000 + myWindow.si_Cnt*10
        else:
            a = int(random.uniform(1,1000))
            _fraps = 5000 + a%1000
            _focus = 1000 + a%1000
            _distance = 5000 + a%1000
        
        if self.m_check_single1.isChecked():
            str = struct.pack('8sLLLL40s',
            b'',_focus,_distance,_fraps,0,b'')
            # print ('After pack:',len(str),binascii.hexlify(str))
            self.m_udpSingle.sendMsg(str)
            str = 'tData._focus:%d,tData._fraps:%d,cnt:%d'%(_focus,_fraps,myWindow.si_Cnt)
            self.ui.textEdit.append(str)
        if self.m_check_single2.isChecked():
            str = struct.pack('=64s',b'')
            self.m_udpSingle2.sendMsg(str)
    
    sf_angle = 0.0
    def on_timeOut_Multi(self):
        
        angle = random.uniform(0,1)
        myWindow.sf_angle += 0.1
        if self.ui.cmb_data.currentIndex() == 0: ##顺序递增  模拟
            if myWindow.sf_angle > 1:
                myWindow.sf_angle -= 1
            angle = myWindow.sf_angle

        azimuth_angle = []
        pitch_angle= []
        for i in range(10):
            azimuth_angle.append(10*i + angle)
            pitch_angle.append(10*i + angle)
        strA = bytes()
        strE = bytes()
        for i in range(10):
            strA += struct.pack('=f',azimuth_angle[i])
            strE += struct.pack('=f',pitch_angle[i])

        str = struct.pack('=28s',b'')
        str += strA
        str += struct.pack('=40s',b'')
        str += strE
        str += struct.pack('=364s',b'')

        self.m_udpMulti.sendMsg(str)
        # print(len(str),type(str))
        # print(str)
        self.ui.textEdit.append(binascii.hexlify(strA).decode())


    def closeEvent(self,evt):
        self.on_Quit()
        list = [self.m_udpMulti,self.m_udpSingle,self.m_udpSingle2,self.m_udpGps]
        for ii in list:
            ii.requestInterruption()
            ii.quit()
        
        for ii in list:
            ii.Quit()
            ii.wait(1000)
        
        
    def relayoutUi(self):
        hLayout = QHBoxLayout()
        label_single2 = QLabel('单播2:',self.ui.groupBox)
        self.addr_single2 = QLineEdit('192.168.1.220:15000',self.ui.groupBox)
        hLayout.setSpacing(6);
        hLayout.addWidget(label_single2);
        hLayout.addWidget(self.addr_single2);
        self.m_check_single2 = QCheckBox(self.ui.groupBox);
        self.m_check_single2.setChecked(True);
        self.ReplaceWidgets(hLayout, self.m_check_single2);

        self.m_check_mutil = QCheckBox(self);
        self.m_check_mutil.setChecked(True);
        self.m_check_single1 = QCheckBox(self);
        self.m_check_single1.setChecked(True);
        self.m_check_gps = QCheckBox(self);
        self.m_check_gps.setChecked(True);

        self.ReplaceWidgets(self.ui.hlay_gps,self.m_check_gps);
        self.ReplaceWidgets(self.ui.hlay_single,self.m_check_single1);
        self.ReplaceWidgets(self.ui.hlay_mutil,self.m_check_mutil);
        # 重新排序 [4/27/2017 xystar]
        self.ui.hlay_group.removeItem(self.ui.hlay_gps);
        self.ui.hlay_group.addItem(hLayout);
        self.ui.hlay_group.addItem(self.ui.hlay_gps);
        self.ui.hlay_group.setSpacing(2);

    def ReplaceWidgets(self,lay,check):
        nCnt = lay.count()
        wgetList = []
        while 1:
            wgetList.append(lay.itemAt(0).widget())
            lay.removeItem(lay.itemAt(0))
            nCnt = lay.count()
            if nCnt == 0:
                break
        lay.addWidget(check)

        for var in wgetList:
            lay.addWidget(var);
            edit = var
            edit.setMinimumWidth(edit.fontMetrics().averageCharWidth()*len(edit.text()) + 10);
        lay.setStretch(2,1)
        lay.addStretch(1)

    def on_Init(self):
        value = self.ui.addr_Muti.text().split(':')
        self.m_udpMulti.Init(int(value[1]) + 1,tuple(value))
        value = self.ui.Addr_Single.text().split(':')
        self.m_udpSingle.Init(int(value[1])+ 1,tuple(value))
        value = self.addr_single2.text().split(':')
        self.m_udpSingle2.Init(int(value[1])+ 1,tuple(value))
        value = self.ui.Addr_Gps.text().split(':')
        self.m_udpGps.Init(int(value[1])+ 1,tuple(value))

        if self.m_check_mutil.isChecked():
            self._timerMulti.start(500)
        if self.m_check_single1.isChecked():
            self._timeSingle.start(500) 
        if self.m_check_gps.isChecked():
            self._timeGPs.start(500) 

    def on_Quit(self):
        self._timeGPs.stop()
        self._timerMulti.stop()
        self._timeSingle.stop()


    def on_wordRun(self):
        
        if myWindow.nPos > len(self.m_scrollCaptionStr):
            myWindow.nPos = 0
        self.ui.scrollCaptionLabel.setText(self.m_scrollCaptionStr[myWindow.nPos:])
        myWindow.nPos += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = myWindow()
    dlg.show()
    sys.exit(app.exec_())