#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout
from PyQt5.QtCore import *
import sys,os,json
from qtImage import  imageLoader,myPaint



strStyle = '''QScrollBar:horizontal {
    border: 2px solid green;
    background: cyan;
    height: 15px;
    margin: 0px 40px 0 0px;
}

QScrollBar::handle:horizontal {
    background: gray;
    min-width: 20px;
}

QScrollBar::add-line:horizontal {
    background: blue;
    width: 16px;
    subcontrol-position: right;
    subcontrol-origin: margin;
    border: 2px solid black;
}

QScrollBar::sub-line:horizontal {
    background: magenta;
    width: 16px;
    subcontrol-position: top right;
    subcontrol-origin: margin;
    border: 2px solid black;
    position: absolute;
    right: 20px;
}

QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    width: 3px;
    height: 3px;
    background: pink;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}


 QScrollBar:vertical {
     border: 2px solid grey;
     background: #32CC99;
     width: 15px;
     margin: 22px 0 22px 0;
 }
 QScrollBar::handle:vertical {
     background: white;
     min-height: 20px;
 }
 QScrollBar::add-line:vertical {
     border: 2px solid grey;
     background: #32CC99;
     height: 20px;
     subcontrol-position: bottom;
     subcontrol-origin: margin;
 }

 QScrollBar::sub-line:vertical {
     border: 2px solid grey;
     background: #32CC99;
     height: 20px;
     subcontrol-position: top;
     subcontrol-origin: margin;
 }
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
     border: 2px solid grey;
     width: 3px;
     height: 3px;
     background: white;
 }

 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
     background: none;
 }

'''
class myWindow(QDialog):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        self.resize(600,400)
        self._imagLoader = imageLoader(self)
        self._scroll = QScrollArea(self)
        # self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll.setAlignment(Qt.AlignCenter)
        self._scroll.setStyleSheet(strStyle)
        self._widget = myPaint(self)
        self._widget.resize(1000,1000)
        
        self._widget.setFocusPolicy(Qt.WheelFocus)
        hLay  = QHBoxLayout(self._widget)
        self._widget.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self._scroll.setWidget(self._widget)
        self._scroll.installEventFilter(self)
        self._widget.installEventFilter(self)
        main_lay = QVBoxLayout(self)
        main_lay.addWidget(self._scroll)

        hlay = QHBoxLayout()
        self.btn_about = QPushButton("aboutQt",self)
        self.btn_pause = QPushButton("Pause",self)
        self.btn_cancel = QPushButton("Cancel",self)
        hlay.addStretch()
        hlay.addWidget(self.btn_pause)
        hlay.addWidget(self.btn_about)
        hlay.addWidget(self.btn_cancel)
        main_lay.addLayout(hlay)
        
        menuBar = QMenuBar(self)
        group = QActionGroup(self)
        # group.setExclusive(True)  ## 只允许一个
        menu = menuBar.addMenu("DlgMenu")
        act1 = group.addAction(QAction('111'))
        act2 = group.addAction(QAction('222'))
        act3 = group.addAction(QAction('333'))
        menu.addAction(act1)
        menu.addAction(act2)
        menu.addAction(act3)
        for i in range(1,4):
            str = 'act%d.setCheckable(True)'% i 
            eval(str)
            str = 'act%d.setChecked(True)'% i 
            eval(str)
        # act1.setChecked(True)

        main_lay.setMenuBar(menuBar)
        self.btn_about.clicked.connect(lambda: QApplication.instance().aboutQt())
        self.btn_pause.clicked.connect(self.on_PauseClick)
        self.btn_cancel.clicked.connect(lambda: self.reject())
        self._imagLoader.evt_showImg.connect(self._widget.on_paint)
        self._imagLoader.finished.connect(self._imagLoader.deleteLater)
        QTimer.singleShot(0,lambda:self._imagLoader.start())

    def on_PauseClick(self):
        if self.btn_pause.text() == 'Pause':
            self.btn_pause.setText('Resume')
            self._imagLoader.evt_showImg.disconnect()
        else:
            self.btn_pause.setText('Pause')   
            self._imagLoader.evt_showImg.connect(self._widget.on_paint)
        
    def eventFilter(self,o,e):
        if o == self._scroll:
            if e.type() == QtCore.QEvent.MouseButtonDblClick:
                if self._scroll.isFullScreen():
                    self._scroll.setWindowFlags(Qt.SubWindow)
                    self._scroll.showNormal()
                else:
                    self._scroll.setWindowFlags(Qt.Window)
                    self._scroll.showFullScreen()
                return True

            elif e.type() == QEvent.Wheel:
                event  = QWheelEvent(e)
                # print('\033[31mScrollWheel:',event.globalPos(),event.pos())
                newSize = self._widget.size()
                s = self._scroll.size()
                # print(event.angleDelta(),event.pixelDelta())
                if event.angleDelta().y() > 0:
                    if newSize.width() > s.width()*4:
                        return True
                    newSize*= 1.25
                else:
                    if s.width() == newSize.width():
                        return True
                    newSize*= 0.75
                
                if newSize.width() <= s.width():
                    self._widget.resize(self._scroll.maximumViewportSize())
                    return True

                self._widget.resize(newSize)
                # self._scroll.ensureVisible(event.pos().x(),event.pos().y(),50,50)

                return True

            elif e.type() == QEvent.Resize:
                evt = QResizeEvent(e)
                print('\033[34mScroll resize:',self._scroll.viewport().size(),self._scroll.size(),self._widget.size())
                # print(evt.oldSize(),evt.size(),self._scroll.maximumViewportSize())
                # if evt.oldSize() != evt.size():
                self._scroll.viewport().resize(self._scroll.maximumViewportSize())
                self._widget.resize(self._scroll.maximumViewportSize())
                return True
                

        #   return QDialog.eventFilter(self, o, e)#将事件交给上层对话框  
        return False

    def closeEvent(self,evt):
            self._imagLoader.requestInterruption()
            self._imagLoader.wait(1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(QCoreApplication.libraryPaths())
    print(QtCore.qVersion())
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
