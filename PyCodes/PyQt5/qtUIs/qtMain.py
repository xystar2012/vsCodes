from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal,QTimer,QThread,Qt,QEvent
from PyQt5.QtGui import QImage,QPainter,QFont,QIcon,QPalette,QImage,QPixmap,QPalette,QMovie,qGray
from PyQt5.QtWidgets import QDialog,QWidget,QMainWindow,qApp,QFrame,QLabel,QPushButton,QSpinBox,QListWidget
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout,QStackedLayout,QGridLayout
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
        frmLay.addRow('è·³è½¬:',self._spinBox)
        btnGo = QPushButton('Go',self)      
    
        btnPrev = QPushButton('ä¸Šä¸€å¼ ',self)
        self.btnNext = QPushButton('ä¸‹ä¸€å¼ ',self)
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
        frm1.addRow('å…±:',self._label)
        frm1.setRowWrapPolicy(QFormLayout.WrapLongRows)
        labLay.addStretch()
        labLay.addLayout(frm1)
        frm1 = QFormLayout()
        self._labInfo = QLabel()
        # self._labInfo.setWordWrap(True)
        frm1.addRow('å½“å‰�:',self._labInfo)
        # frm1.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        frm1.setRowWrapPolicy(QFormLayout.WrapLongRows)
        labLay.addLayout(frm1)
        frm1 = QFormLayout()
        self._labPlay = QLabel()
        frm1.addRow('æ’­æ”¾å¸§å�·:',self._labPlay)
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
        self._labPlay.setText(' {} å¸§'.format(n))
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
        self._label.setText('%03dæ�¡è®°å½•'%len(self._gifs))
        if len(self._gifs) > 0:
            self._movie.setFileName(self._gifs[0])
            self._movie.start()
            self._labInfo.setText('{},{}å¸§\n{}'.format(
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
        self._labInfo.setText('{},{}å¸§\n{}'.format(
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
    
class Demo4(QDialog):
    # stackl = QStackedLayout()
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        self.resize(400,600)
        mainl = QGridLayout(self)
        self.stackl = QStackedLayout()
        self.stackl.setStackingMode(QStackedLayout.StackAll)

        for i in range(10):
            lab = QLabel(self)
            lab.setText('%d_label' % (i+1))
            lab.setMinimumSize(100,100)

            lab.setAutoFillBackground(True)
           
            pt = lab.palette()
            # pt = QPalette()
            pt.setBrush(QPalette.Background,Qt.black)
            pt.setBrush(QPalette.WindowText,Qt.white)
            lab.setPalette(pt)
            lab.setAlignment(Qt.AlignCenter)
            self.stackl.addWidget(lab)
            btn = QPushButton('item:%d'%(i+1))
            mainl.addWidget(btn,i,0)
            btn.clicked.connect(self.on_btnClick)

        mainl.addLayout(self.stackl,0,1,self.stackl.count(),1)

    def on_btnClick(self):
        btn = QPushButton()
        i = int(self.sender().text()[len('item:'):]) - 1
        print('btn:' ,i)
        self.stackl.setCurrentIndex(i)

class Demo5(QDialog):
    
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        self.resize(400,600)
        mainl = QHBoxLayout(self)
        self.stackl = QStackedLayout()
        _listWgt = QListWidget(self)

        for i in range(1000):
            lab = QLabel(self)
            lab.setText('%d_label' % (i+1))
            lab.setMinimumSize(100,100)

            lab.setAutoFillBackground(True)
           
            pt = lab.palette()
            pt.setBrush(QPalette.Background,Qt.black)
            pt.setBrush(QPalette.WindowText,Qt.white)
            lab.setPalette(pt)
            lab.setAlignment(Qt.AlignCenter)
            self.stackl.addWidget(lab)
            _listWgt.addItem("label:{}".format(i + 1))

        mainl.addWidget(_listWgt,1);
        mainl.addLayout(self.stackl,2)

        _listWgt.currentRowChanged.connect(self.stackl.setCurrentIndex)

class Demo6(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        self.setFixedSize(800,600)
        mainl = QVBoxLayout(self)
        
        hL1 = QHBoxLayout()
        self.lab1 = QLabel(self)
        self.srcImg = QImage(r'C:\Users\xystar\Downloads\10bit.tif')
        hL1.addWidget(self.lab1,1)
        self.lab1.setScaledContents(True)
        self.lab1.setAlignment(Qt.AlignCenter)
        self.lab1.setPixmap(QPixmap.fromImage(self.srcImg).scaledToWidth(400))
        
        self.lab2 = QLabel(self)
        self.lab2.setAlignment(Qt.AlignCenter)
        self.lab1.setScaledContents(True)
        pt = self.lab2.palette()
        pt.setBrush(QPalette.Background,Qt.black)
        pt.setBrush(QPalette.WindowText,Qt.white)
        self.lab2.setPalette(pt)
        hL1.addWidget(self.lab2,1)

        hL2 = QHBoxLayout()
        btn1 = QPushButton('转换')
        btn1.clicked.connect(self.on_cvt)
        hL2.addStretch()
        hL2.addWidget(btn1)

        mainl.addLayout(hL1,1)
        mainl.addLayout(hL2)

    def on_cvt(self):
        print(self.srcImg.allGray(),self.srcImg.depth(),self.srcImg.width(),self.srcImg.height())
        for i in range(self.srcImg.width()):
            print(self.srcImg.pixel(100,i),qGray(self.srcImg.pixel(100,i)),end = ' ')
        
        # for i in range(self.srcImg.width()):
        #     for j in range(self.srcImg.height()):
        #         print(self.srcImg.pixelColor(i,j).value(),end = ' ')
        #     print()
        image = QImage(self.srcImg.width(),self.srcImg.height(),QImage.Format_RGB888)



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
        class_name = "Demo" + index #ç±»å��  
        # module_name = "qtMain"   #æ¨¡å�—å��  
        # module = __import__(module_name) # import module  module
        module = sys.modules['__main__']
        print(module)
        try:
            c = getattr(module,class_name)  
            print(c,type(c))
            dlg = c(self)
            if hasattr(c,'exec_'):
                dlg.resize(400,400)
                dlg.exec_()
            else:
                dlg.show()

        except AttributeError as e:
            print(str(e),end=' --> ')
            print('Click %s error here!!'%text)
        except:
            err = sys.exc_info()
            print('Else error:',type(err),err)

    def closeEvent(self,evt):
        print('main close here!')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = mainWindow(app)
    dlg.show()
    sys.exit(app.exec_())