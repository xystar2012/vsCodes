#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout,qApp
from PyQt5.QtCore import *
import sys,os,json,subprocess
import time,configparser  
from tendo import singleton
import main_rc
configNam = 'buildApp.ini'


class itemDelegate(QStyledItemDelegate):
    deleteItem = pyqtSignal(QModelIndex)
    def __init__(self,parent = None):
        super(itemDelegate,self).__init__()

    def paint(self,painter,option,index):
        viewOption = QStyleOptionViewItem(option)

        # if viewOption.state & QStyle.State_HasFocus:
        #     viewOption = viewOption.state ^ QStyle.State_HasFocus
        QStyledItemDelegate.paint(self,painter,viewOption,index)
        size = QSize(11,11)
        height =  (viewOption.rect.height() - size.height())/ 2
        pixmap = QPixmap(':/image/Delete_64px.png') 
        point = QPoint(viewOption.rect.left() + viewOption.rect.width() - 30, 
            viewOption.rect.top() + height)   
        decorationRect =  QRect(point , size)
        painter.drawPixmap(decorationRect, pixmap)

    def editorEvent(self,event,model,option,index):
        size = QSize(11,11)
        height =  (option.rect.height() - size.height())/ 2
        point = QPoint(option.rect.left() + option.rect.width() - 30, 
            option.rect.top() + height)   
        decorationRect =  QRect(point , size)
        # height = (option.rect.height() - 9) / 2
        # decorationRect = QRect(option.rect.left() + option.rect.width() - 30,
        #      option.rect.top() + height, 9,9)
        mouseEvent = event
        if event.type() == QEvent.MouseButtonPress and decorationRect.contains(mouseEvent.pos()):
            self.deleteItem.emit(index)

        elif event.type() == QEvent.MouseMove and decorationRect.contains(mouseEvent.pos()):
            cursor = QCursor(Qt.PointingHandCursor);
            QApplication.setOverrideCursor(cursor);
            strText = "删除工程路径"
            QToolTip.showText(mouseEvent.globalPos(), strText)
        else:
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        return QStyledItemDelegate.editorEvent(self,event, model, option, index)



class mywindow(QDialog):
    def __init__(self,p = None):
        super(mywindow,self).__init__()
        self.resize(800,400)
        self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
        mainl = QVBoxLayout(self)
        self.setWindowTitle('Build vs application')
        hl = QHBoxLayout()
        self.lineEdit = QComboBox()
        self.lineEdit.setEditable(True)
        self.lineEdit.setDuplicatesEnabled(False)
        pDelegate = itemDelegate(self)
        self.lineEdit.setItemDelegate(pDelegate)
        pDelegate.deleteItem.connect(self.on_delItem)

        fmL = QFormLayout()
        fmL.addRow('工程路径:',self.lineEdit)
        self.btnPath = QPushButton('浏览')
        self._proc = QProcess()
        self.cmbbuild = QComboBox()
        self.cmbbuild.addItems(['build','Rebuild'])
        self.bintype = QComboBox()
        self.bintype.addItems(['Release','Debug'])
        self.config = configparser.ConfigParser()
        self.config.read(configNam)
        hl.addLayout(fmL)
        hl.addWidget(self.btnPath)
        hl.addWidget(self.cmbbuild)
        hl.addWidget(self.bintype)

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
        self.btnPath.clicked.connect(self.on_pathSel)
        self.lineEdit.currentTextChanged.connect(self.on_pathChange)
        
        try:
            if 'BASIC' in self.config:
                for i in range(int(self.config['BASIC']['count'])):
                    self.lineEdit.addItem(self.config['Projects']['path%d' % (i+1)])
            else:
                ## 配置不存在时
                self.lineEdit.addItem(r"E:\svn_Root\Eagle_Branch_Dir\EagleClusterTrunk\MainFrame\MainFrame.sln")
                self.config.add_section('BASIC')
                self.config.set('BASIC','count','0')
                self.config.set('BASIC','lastpath','')
                self.config.add_section('Projects')
        except configparser.Error as e:
            print('Parse %s error,' % configNam,e)

    def on_delItem(self,index):
        if QMessageBox.question(self,'提示',"是否删除工程文件 '{0}'?".format(self.lineEdit.itemText(index.row())),
            QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
            self.lineEdit.removeItem(index.row())
            self.on_saveConfig()
            
    def on_pathChange(self,path):
        palette = self.lineEdit.palette()
        if QFile(path).exists():
            palette.setColor(QPalette.Text,
                    self.cmbbuild.palette().color(QPalette.Text))
            self.config['BASIC']['lastpath'] = os.path.split(path)[0]
            
        else:
            palette.setColor(QPalette.Text, Qt.red)
        self.lineEdit.setPalette(palette)

    def on_saveConfig(self):
        
        self.config['BASIC']['count'] = str(self.lineEdit.count())
        for i in range(self.lineEdit.count()):
            self.config['Projects']['path%d' % (i+1)] = self.lineEdit.itemText(i)
        self.config['BASIC']['lastpath'] = os.path.split(self.lineEdit.currentText())[0]

        
    def on_pathSel(self):
        lastPath = self.config['BASIC']['lastpath']
        fileName, filetype = QFileDialog.getOpenFileName(self,'选择vs工程文件',lastPath,r"vs project Files (*.sln)")
        # print("Get file:",filename,' fileType:',filetype)
        if self.lineEdit.findText(fileName) < 0 and fileName != '':
            self.lineEdit.addItem(fileName)
            self.lineEdit.setCurrentText(fileName)
            self.on_saveConfig()

    def doWithQProcess(self):
        print('doWithQProcess running ...')
        ## 不可重复连接
        self._proc.readyRead.connect(self.on_procOutput)
        self._proc.finished.connect(self.on_finish)
        self._proc.errorOccurred.connect(self.on_error)
        self._proc.started.connect(self.on_start)

        path = self.lineEdit.currentText()
        fileInfo = QFileInfo(QFile(path))
        if not fileInfo.isFile() and  fileInfo.suffix() is not "sln":
            return
        args = ['/c','build.bat',path
        #  '"' + self.bintype.currentText() + '"'
          ,'/'   + self.cmbbuild.currentText(),self.bintype.currentText()]
        print(args)
        print('Path:',os.getcwd())
        print('Path:',qApp.applicationDirPath())
        print('Path:',sys.path[0])
        self._proc.setWorkingDirectory(os.getcwd())
        self._proc.start('cmd',args)
        # self._proc.start("cmd",['/c','ping','www.baidu.com','-n','2'])
        self.textEdit.clear()
        self.textEdit.document().setMaximumBlockCount(102400)

    def on_start(self):
        self.btnPath.setEnabled(False)
        self.dlgbtns.button(QDialogButtonBox.Ok).setEnabled(False)
        self.dlgbtns.button(QDialogButtonBox.Cancel).setEnabled(False)

    def on_error(self,error):
        print(error)
        
    def on_procOutput(self):
        if self._proc.canReadLine():
            data = self._proc.readLine()
            try:
                self.textEdit.append(bytes(data).decode('gbk'))
                self.textEdit.moveCursor(QTextCursor.End)
            except(TypeError,UnicodeDecodeError) as e:
                print('decode error:',e)   

    def on_finish(self,exitCode,exitStatus):
        self.textEdit.append('==='*10 + ' >> end!!')
        print(exitCode,exitStatus,type(exitStatus))
        self.textEdit.append('errorCode:' + str(exitCode))
        self._proc.close()
        ## 不可重复连接
        self._proc.readyRead.disconnect()
        self._proc.finished.disconnect()
        self._proc.errorOccurred.disconnect()
        self._proc.started.disconnect()
        self.btnPath.setEnabled(True)
        self.dlgbtns.button(QDialogButtonBox.Ok).setEnabled(True)
        self.dlgbtns.button(QDialogButtonBox.Cancel).setEnabled(True)

    def on_build(self):
        self.doWithQProcess()

    def closeEvent(self,e):
        with open(configNam,'w') as configFile:
            self.config.write(configFile)

if __name__=='__main__':
    oneApp = singleton.SingleInstance()
   
    print('sysPath0:',sys.path[0],'os.gecwd:',os.getcwd(),'sys.argv:',sys.argv[0])
    if sys.path[0] != os.getcwd():
        try:
            os.chdir(sys.path[0])
        except:
            print('chdir:',sys.path[0],'error')
            os.chdir(os.getcwd())

    ##导入 资源
    # sys.path.append('../qtUIs')
    # import main_rc
    
    app = QApplication(sys.argv)      
    window = mywindow()
    window.show()
    sys.exit(app.exec_())