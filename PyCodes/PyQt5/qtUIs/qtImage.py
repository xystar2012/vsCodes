from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal,QTimer,QThread,Qt,QEvent
from PyQt5.QtGui import QImage,QPainter,QFont
from PyQt5.QtWidgets import QWidget,QDialog,QPushButton,QCheckBox,QLineEdit,QLabel,QListWidget,QMainWindow
from PyQt5.QtCore import QDir
import os,os.path,sys,math
import operator

__author__ = 'xystar'

class myDlg(QDialog):
    def __init__(self,parent = None):
        super(myDlg,self).__init__()
        self.createLayOut()

    def createLayOut(self):
        mainLay = QtWidgets.QVBoxLayout(self)
        hlay = QtWidgets.QHBoxLayout()
        self.line = QLineEdit()
        self.btn_ok = QPushButton("OK",self)
        hlay.addWidget(self.line)
        hlay.addWidget(self.btn_ok)
        self.list = QListWidget()
        mainLay.addLayout(hlay)
        mainLay.addWidget(self.list)

class myPaint(QWidget):
    _image = QImage(1024,1024,QImage.Format_RGB888)
    _image.fill(Qt.black)
    def __init__(self,parent= None):
        super(myPaint,self).__init__()

    def paintEvent(self,event):
        if(self._image.isNull()):
            return QWidget().paintEvent(event)
        painter = QPainter(self)
        painter.drawImage(self.rect(),self._image)
    
    def on_paint(self,path,img):
        self._image = img
        self._image = img.scaled(self.size(), Qt.IgnoreAspectRatio)
        self.update()
        # print(path)

class imageLoader(QThread):
    ## 定义 2个参数的 信号
    evt_showImg = QtCore.pyqtSignal(str,QImage)
    def __init__(self,parent = None):
        super(imageLoader,self).__init__()
        self.image_list = []  # [] 列表   {} 字典

    def run(self):
        print(QThread.currentThread(),' is running ...')
        print(QDir.homePath(),QDir.currentPath())
        rootdir = QDir.homePath() + '/pics'
        list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        for i in range(0,min(len(list),200)):
            path = os.path.join(rootdir,list[i])
            types = ('.bmp','.jpg','.tif','.png')
            if os.path.isfile(path) and path.endswith(types):
                # self.image_list[path] = QImage(path)
                self.image_list.append((path,QImage(path)))
        self.image_list.sort()
        sorted(self.image_list, key=operator.itemgetter(0))

        if len(self.image_list) == 0:
            return;
        self.bStop = False
        while self.isRunning():
            # break
            # for (k,v) in self.image_list.items():  # 字典类型遍历  随机访问 会乱序 
            for k,v in enumerate(self.image_list):
                # print(k,v)
                # print(type(k),type(v))
                # self.evt_showImg.emit(k,v)
                self.evt_showImg.emit(v[0],v[1])  ## 发射自定义信号
                if(self.isInterruptionRequested()):
                    print("----> get isInterruptionRequested")
                    self.bStop = True
                    break
                QThread.msleep(25)
            if self.bStop:
                break
        print("----> thread quit here!!")

class myWindow(QDialog):
    evt_print = QtCore.pyqtSignal()  #  必须放在全局区域才能发射
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        self._widget = myPaint(self)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        self._widget.installEventFilter(self)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.start(1)
        self._imagLoader = imageLoader(self)
        ## 布局设置
        self.createLayOut()
        self.createConnect()
    
    def eventFilter(self,o,e):
        if o == self._widget:
            if e.type() == QtCore.QEvent.MouseButtonDblClick:
                if self._widget.isFullScreen():
                    self._widget.setWindowFlags(Qt.SubWindow)
                    self._widget.showNormal()
                else:
                    self._widget.setWindowFlags(Qt.Window)
                    self._widget.showFullScreen()
                return True
        #   return QDialog.eventFilter(self, o, e)#将事件交给上层对话框  
        return False;
                
    def createLayOut(self):
        vlay = QtWidgets.QHBoxLayout()
        self.edits = []
        self.labs = []

        for i in range(10):
            lab = QLabel("Address%d:"%(i + 1),self)
            edit= QLineEdit()
            fram_lay = QtWidgets.QFormLayout()
            fram_lay.addRow(lab,edit);
            self.labs.append(lab)
            self.edits.append(edit)
            vlay.addLayout(fram_lay)

        main_lay = QtWidgets.QVBoxLayout(self)
        self.resize(600,400)
        main_lay.addLayout(vlay)
        main_lay.addWidget(self._widget,1)
        hlay = QtWidgets.QHBoxLayout()
        self.btn_ok = QtWidgets.QPushButton("OK",self)
        self.btn_cancel = QtWidgets.QPushButton("Cancel",self)
        self.btn_showUI = QtWidgets.QPushButton("showUI",self)
        hlay.addStretch()
        hlay.addWidget(self.btn_ok)
        hlay.addWidget(self.btn_cancel)
        hlay.addWidget(self.btn_showUI)
        main_lay.addLayout(hlay)

    def createConnect(self):
        self.btn_cancel.clicked.connect(self.on_cancel)
        self.btn_ok.clicked.connect(self.on_OK)
        self.evt_print.connect(self.on_showUi)
        self._timer.timeout.connect(self.on_timeout)
        self._imagLoader.evt_showImg.connect(self._widget.on_paint)
        self._imagLoader.finished.connect(self._imagLoader.deleteLater)
        self.btn_showUI.clicked.connect(self.on_showUi)

    def on_timeout(self):
       self._imagLoader.start()
    # global g_dlg;
    
    def on_showUi(self):
        import ui_udpsendbyqt as uiform
        self.g_dlg = QMainWindow()
        ui = uiform.Ui_UDPSendByQtClass()
        ui.setupUi(self.g_dlg)
        self.g_dlg.setWindowModality(Qt.ApplicationModal)
        self.g_dlg.show()
        
    def on_cancel(self):
        #print("on_cancel")
        self.close()
        self.reject()
        # self.evt_print.emit()
        
    def on_OK(self):
        print("on_ok")
        dlg = myDlg(None)
        dlg.exec()
        self.accept()

    def closeEvent(self,evt):
        self._imagLoader.requestInterruption()
        self._imagLoader.wait(1000)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = myWindow()
    dlg.show()
    sys.exit(app.exec_())