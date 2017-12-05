from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
import os,os.path,sys,math
import operator


class myScrool(QScrollArea):
    def __init__(self,parent = None):
        super(myScrool,self).__init__()
        self.setWidgetResizable(True)
        self.setBackgroundRole(QPalette.Light)

class cfgPage(QTabWidget):
    def __init__(self,parent = None):
        super(cfgPage,self).__init__()
        page = QWidget(self)
        self.resize(600,400)
        self.addTab(page,'系统设置')
        self.page1(page)
        page = QWidget(self)
        self.addTab(page,'采集参数设置')
        self.page2(page)

        page = QWidget(self)
        self.addTab(page,'磁盘配置')
        self.page3(page)


    def on_groupbtnClick(self,btn):
        
        btnGroup = self.sender()
        # check = (QCheckBox)(btn)
        # print("checked:",check.isChecked(),btnGroup.buttons(),self.sender(),btnGroup)
        # check = (QCheckBox)(btnGroup.button(id))
        print(type(btn),'btnID:',btnGroup.id(btn)," checked:",btn.isChecked())
        if btn.isChecked():
            for ii in btnGroup.buttons():
                if ii != btn:
                    ii.setChecked(False)


    def page3(self,page):
        _vLayout = QVBoxLayout(page)
        scroll = myScrool()
        _vLayout.addWidget(scroll)
        wgt = QWidget()
        gridLayout = QGridLayout(wgt)
        scroll.setWidget(wgt)
        labDev = QLabel('设备名')
        labCam = QLabel('相机')
        gridLayout.addWidget(labDev, 0, 0)
        gridLayout.setColumnMinimumWidth(0, 100)
        gridLayout.setColumnMinimumWidth(1, 80)
        gridLayout.addWidget(labCam, 0, 1)

        def getLine():
            line = QFrame(self)
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            return line

        nDisk = 100
        nCCd = 50
        for i in range(0,nDisk):
            diskN = QLabel('磁盘%d\n(%dGB)'% (i,i*100 + 500))
            diskN.setWordWrap(True)
            # 第二列开始
            gridLayout.addWidget(diskN, 0, 2 + i)
            line = getLine()
            # 第二行 从第二列合并
            gridLayout.addWidget(line, 1, 2,1,nDisk,Qt.AlignVCenter)
        
        labDevNam = QLabel('设备->abcdefg')
        labDevNam.setWordWrap(True)
        ## 第一列  从第第三行合并
        gridLayout.addWidget(labDevNam, 2, 0,nCCd,0,Qt.AlignVCenter)

        for i in range(0,nCCd):
            labCCDNam = QLabel('CCD:%d'%(i+100))
            gridLayout.addWidget(labCCDNam,i + 2,1)   #  第一列

        for i in range(0,nDisk):
            btnGroup = QButtonGroup(self)
            ## 多参数 信号
            btnGroup.setExclusive(False)
            btnGroup.buttonClicked[QAbstractButton].connect(self.on_groupbtnClick)
            for j in range(0,nCCd):
                diskN = QCheckBox(str(i))
                diskN.setCheckable(True)
                gridLayout.addWidget(diskN,j + 2, i + 2)
                btnGroup.addButton(diskN,j)
            # self._btns.append(btnGroup)
        line = getLine()
        # line.setFrameShape(QFrame.HLine)
        # line.setFrameShadow(QFrame.Sunken)
        gridLayout.addWidget(line,gridLayout.rowCount(),0,1,gridLayout.columnCount(),Qt.AlignTop)

    def page2(self,page):
        _vLayout = QVBoxLayout(page)
        _group = QGroupBox('CameraLink相机参数设置',self)
        _group.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        _group.setStyleSheet("QGroupBox {border:1px solid;border-color:darkblue;color:darkred;\
						  						  	font:bold Consolas large;font-size:12px;}");
        _paramGridL = QGridLayout()
        _group.setLayout(_paramGridL)
        nCol = 0
        for ii in '设备名称|相机|帧头大小|帧数据大小'.split('|'):
            labelCol = QLabel(ii)
            _paramGridL.addWidget(labelCol,0,nCol,Qt.AlignTop)
            nCol +=1
        _paramGridL.setRowMinimumHeight(0,20)
        scroll = myScrool()
        scroll.setWidget(_group)
        _vLayout.addWidget(scroll)
        _vLayout.addStretch(1)
        # _paramGridL.setColumnStretch(2,1)
        # _paramGridL.setColumnStretch(3,1)
        for i in range(1,100):
            labDevN = QLabel('Device:%d'%i)
            labCCD =  QLabel('Channel:%d'%i)
            _paramGridL.addWidget(labDevN,i,0,Qt.AlignLeft|Qt.AlignTop)
            _paramGridL.addWidget(labCCD,i,1,Qt.AlignLeft|Qt.AlignTop)
            cmbHead = QComboBox()
            cmbHead.setEditable(True)
            cmbHead.setMinimumWidth(50)
            cmbHead.addItems('1,2,3,4,5'.split(','))
            _paramGridL.addWidget(cmbHead,i,2,Qt.AlignLeft|Qt.AlignTop)
            cmbBody = QComboBox()
            cmbBody.setMinimumWidth(50)
            cmbBody.setEditable(True)
            cmbBody.addItems('11,22,32,42,52'.split(','))
            _paramGridL.addWidget(cmbBody,i,3,Qt.AlignLeft|Qt.AlignTop)
            
        

    def page1(self,page): 
        mainOut = QVBoxLayout(page)
        wget = QWidget()
        ## task + hLine
        mainLay = QVBoxLayout()  ## 111
        mainOut.addLayout(mainLay)
        scroll = myScrool()
        wget.setAutoFillBackground(True)
        mainOut.addWidget(scroll)
        hlay = QHBoxLayout()
        lab = QLabel('任务名',self)
        hlay.addWidget(lab)
        lineEdt = QLineEdit('testName')
        hlay.addWidget(lineEdt)
        mainLay.addLayout(hlay)
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameStyle(QFrame.Sunken)
        # ,Qt.AlignTop
        mainLay.addWidget(hLine)

        maiGrad = QGridLayout(wget)
        scroll.setWidget(wget)
        mainLay.addLayout(maiGrad,1)
        labDisk = QLabel('磁盘报警阈值(GB)')
        labDev = QLabel('设备名称')
        labWrite = QLabel('存储模式(循环/正常)')
        # maiGrad.setVerticalSpacing(20)
	    # maiGrad.setHorizontalSpacing(150)
        maiGrad.addWidget(labDisk,0,0,Qt.AlignTop)
        maiGrad.addWidget(labDev,0,1,Qt.AlignLeft|Qt.AlignTop)
        maiGrad.addWidget(labWrite,0,2,Qt.AlignLeft|Qt.AlignTop)
        # maiGrad.setColumnStretch(0,1)
        # maiGrad.setColumnStretch(1,3)
        # maiGrad.setColumnStretch(2,3)
        maiGrad.setRowStretch(0,0)

        for i in range(1,100):
            labDevN = QLabel('abcdefghg')
            maiGrad.addWidget(labDevN,i,0,Qt.AlignTop)
            cmb1 = QComboBox()
            cmb1.addItems({'30','11','22','33','44'})
            cmb1.setEditable(True)
            cmb1.setMaximumWidth(150)
            cmb1.setCurrentIndex(2)
            maiGrad.addWidget(cmb1,i,1,Qt.AlignTop)
            cmb2 = QComboBox()
            cmb2.setEditable(True)
            cmb2.setMaximumWidth(150)
            cmb2.addItems({'normal write','recycle write'})
            cmb2.setCurrentIndex(1)
            maiGrad.addWidget(cmb2,i,2,Qt.AlignTop)
        tmp = scroll.widget()
        print(tmp.size())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = cfgPage()
    dlg.show()
    sys.exit(app.exec_())