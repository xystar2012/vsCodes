from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal,QTimer,QThread,Qt,QEvent
from PyQt5.QtGui import QImage,QPainter,QFont,QIcon,QPalette,QImage,QPixmap,QPalette,QMovie
from PyQt5.QtWidgets import QDialog,QWidget,QMainWindow,qApp,QFrame,QLabel,QPushButton,QSpinBox
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout
# from PyQt5.QtCore import qApp
import os,os.path,sys,math
import operator,copy
import main_rc

class Demo1(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        hLay = QtWidgets.QHBoxLayout()
        btn_tool = QtWidgets.QDialogButtonBox(self);
        btn_tool.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        hLay.addStretch()
        hLay.addWidget(btn_tool)
        main_lay = QtWidgets.QVBoxLayout()
        self.setLayout(main_lay)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        line2 = QFrame()
        line2.setFrameShape(QFrame.VLine)
        line2.setFrameShadow(QFrame.Sunken)

        hlay2 = QtWidgets.QHBoxLayout()
        main = QWidget(self)
        # main.setMinimumSize(300,200)
        #copy.deepcopy
        main2 = QWidget(self)

        hlay2.addWidget(main)
        hlay2.addWidget(line2)
        hlay2.addWidget(main2)
        main_lay.addLayout(hLay)
        main_lay.addWidget(line)
        main_lay.addLayout(hlay2,1)

class Demo2(QWidget):
    def __init__(self,parent = None):
        QWidget.__init__(self,parent)
        self.resize(400,200)
        self.setWindowFlags(dlg.windowFlags() | Qt.Dialog)
        # self.setWindowModality(Qt.WindowModal)
        mainLay = QHBoxLayout(self)
        self.labeLeft = QLabel('left')
        self.labeMidle = QLabel('middle')
        self.labeRight = QLabel('right')
        i = 0
        for lab in (self.labeLeft,self.labeMidle,self.labeRight):
            i += 1
            lab.setAutoFillBackground(False)
            lab.setStyleSheet("background-color: rgb(0, 0, 0);")
            mainLay.addWidget(lab)
            lab.setAlignment(Qt.AlignCenter)
            img,scale = ("image/stop_record_64px.png",True) if i%2  else ("image/Capture_64px.png",False)
            lab.setPixmap(QPixmap(img))
            lab.setScaledContents(scale)
        QTimer.singleShot(10,self.on_showImg)
        # timer = QTimer(self)
        # timer.start(1000)
        # timer.timeout.connect(self.on_showImg)

    def on_showImg(self):
        if self.labeLeft.pixmap():
            print(self.labeLeft.text(),self.labeLeft.hasScaledContents(),self.labeLeft.pixmap().rect())
            # print(self.sender().remainingTime(),self.labeLeft.text(),self.labeLeft.hasScaledContents(),self.labeLeft.pixmap().rect())

class Demo3(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        self.setWindowTitle('show_gif')
        self.setWindowIcon(QIcon('image/Capture_64px.png'))
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        # self.resize(400,400)
        self.setFixedSize(800,600)
        mainl = QVBoxLayout(self)
        self.labelShow = QLabel()
        self.labelShow.setContentsMargins(0,0,0,0)
        pat = self.labelShow.palette()
        pat.setBrush(QPalette.Background,Qt.darkGray)
        self.labelShow.setAutoFillBackground(True)
        self.labelShow.setPalette(pat)
        self.labelShow.setAlignment(Qt.AlignCenter)
        # self.labelShow.setScaledContents(True)
        mainl.addWidget(self.labelShow,1)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        mainl.addWidget(line)
        btnLay = QHBoxLayout()
        
        frmLay = QFormLayout()
        self._spinBox = QSpinBox()
        frmLay.addRow('跳转:',self._spinBox)
        btnGo = QPushButton('Go',self)      
    
        btnPrev = QPushButton('上一张',self)
        self.btnNext = QPushButton('下一张',self)
        btnPrev.clicked.connect(self.on_prev)
        self.btnNext.clicked.connect(self.on_next)
        btnGo.clicked.connect(lambda: self.flashMovie(self._spinBox.value()))
        self._spinBox.valueChanged.connect(lambda n: self.flashMovie(n))
        btnLay.addStretch()
        btnLay.addLayout(frmLay)
        btnLay.addWidget(btnGo)
        btnLay.addWidget(btnPrev)
        btnLay.addWidget(self.btnNext)
        btnLay.addStretch()
        mainl.addLayout(btnLay)

        labLay = QHBoxLayout()
        labLay.setSpacing(10)
        self._label = QLabel()
        frm1 = QFormLayout()
        frm1.addRow('共:',self._label)
        frm1.setRowWrapPolicy(QFormLayout.WrapLongRows)
        labLay.addStretch()
        labLay.addLayout(frm1)
        frm1 = QFormLayout()
        self._labInfo = QLabel()
        # self._labInfo.setWordWrap(True)
        frm1.addRow('当前:',self._labInfo)
        # frm1.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        frm1.setRowWrapPolicy(QFormLayout.WrapLongRows)
        labLay.addLayout(frm1)
        frm1 = QFormLayout()
        self._labPlay = QLabel()
        frm1.addRow('播放帧号:',self._labPlay)
        labLay.addLayout(frm1)
        frm1.setRowWrapPolicy(QFormLayout.WrapLongRows)

        labLay.addStretch()
        labLay.setSpacing(10)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        mainl.addWidget(line)
        mainl.addLayout(labLay)
        self._gifs = []
        self._movie = QMovie()
        self.labelShow.setMovie(self._movie)
        QTimer.singleShot(0,self.on_firstShow)
        self._picIndex = 0
        self._movie.frameChanged.connect(self.on_frameChange)
        # self._movie.finished.connect(lambda:self.btnNext.clicked.emit())
    
    def on_frameChange(self,n):
        self._labPlay.setText(' {} 帧'.format(n))
        if n + 1 == self._movie.frameCount():
            self.btnNext.clicked.emit()

    def on_firstShow(self):
        dir = r'E:\jiandanspider\pic'
        for i in os.listdir(dir):
            # print(os.path.isfile(i),i.lower(),i.lower().endswith('gif'))
            fullPath = os.path.join(dir,i)
            if os.path.isfile(fullPath) and i.lower().endswith('gif'):
                self._gifs.append(fullPath)
        
        self._spinBox.setMaximum(len(self._gifs))
        self._label.setText('%03d条记录'%len(self._gifs))
        if len(self._gifs) > 0:
            self._movie.setFileName(self._gifs[0])
            self._movie.start()
            self._labInfo.setText('{},{}帧\n{}'.format(
                    os.path.split(self._movie.fileName())[1],self._movie.frameCount(),
                    self._movie.frameRect()
            ))
                

    def flashMovie(self,index):
        
        if index >= len(self._gifs):
            return
        self._movie.stop()
        self._movie.setFileName(self._gifs[index])
        self._movie.start()

        self._spinBox.valueChanged.disconnect()
        self._spinBox.setValue(index)
        self._labInfo.setText('{},{}帧\n{}'.format(
                    os.path.split(self._movie.fileName())[1],self._movie.frameCount(),
                    self._movie.frameRect()
            ))
        self._spinBox.valueChanged.connect(lambda n: self.flashMovie(n))
        self._picIndex = index

    def on_next(self):
        self._picIndex += 1
        if self._picIndex >= len(self._gifs):
            self._picIndex = len(self._gifs) - 1
        self.flashMovie(self._picIndex)

    def on_prev(self):
        self._picIndex -= 1
        if self._picIndex < 0:
            self._picIndex = 0
        self.flashMovie(self._picIndex)

class myWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Background)
        pa = QPalette(Qt.black)
        self.setPalette(pa)
        

    def mouseDoubleClickEvent(self,event):
        if self.isFullScreen():
            self.setWindowFlags(Qt.SubWindow)
            self.showNormal()
        else:
            self.setWindowFlags(Qt.Window)
            self.showFullScreen()

class mainWindow(QMainWindow):
    def __init__(self,parent = None):
        # super(mainWindow,self).__init__()
        QMainWindow.__init__(self)
        self.resize(600,400)
        self.setWindowTitle('Demo')
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        for i in range(1,11):
            action = self.toolbar.addAction('demo%d'%i,self.on_tool1)
            icon = ':/image/Capture.png' if i%2 else ':/image/stop_preview.png'
            action.setIcon(QIcon(icon))
        # QApplication.instance().aboutQt  
        action = self.toolbar.addAction('aboutQt',qApp.aboutQt)
        action.setIcon(QIcon(':/image/Download_64px.png'))
        mainwnd = QWidget()
        self.setCentralWidget(mainwnd)
        self.setWindowTitle('main')
        mainLay = QHBoxLayout(mainwnd)
        mainLay.setSpacing(2)
        wndleft = myWidget(mainwnd)
        mainLay.addWidget(wndleft)
        wndright = myWidget(mainwnd)
        mainLay.addWidget(wndright)

    def on_tool1(self):
        text = self.sender().text()
        print('whichSender:' + text)
        index = text[4:]
        class_name = "Demo" + index #类名  
        # module_name = "qtMain"   #模块名  
        # module = __import__(module_name) # import module  module
        module = sys.modules['__main__']
        print(module)
        try:
            c = getattr(module,class_name)  
        except AttributeError as e:
            print(str(e),end=' --> ')
            print('Click %s error here!!'%text)
            return
        
        print(c,type(c))
        dlg = c(self)

        if hasattr(c,'exec_'):
            dlg.resize(400,400)
            dlg.exec_()
        else:
            dlg.show()    

        # if index == 1:
        #     dlg = Demo1(self)
        #     dlg.exec_()
        # elif index == 2:
        #     dlg = Demo2(self)
        #     dlg.show()
        # elif index == 3:
        #     dlg = Demo3(self)
        #     dlg.exec_()

    def closeEvent(self,evt):
        print('main close here!')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = mainWindow(app)
    dlg.show()
    sys.exit(app.exec_())