from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QFormLayout
from PyQt5.QtCore import *
import sys,os,json,re


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
        height = (option.rect.height() - 9) / 2
        decorationRect = QRect(option.rect.left() + option.rect.width() - 30,
             option.rect.top() + height, 9,9)
        mouseEvent = event
        if event.type() == QEvent.MouseButtonPress and decorationRect.contains(mouseEvent.pos()):
            self.deleteItem.emit(index)

        elif event.type() == QEvent.MouseMove and decorationRect.contains(mouseEvent.pos()):
            cursor = QCursor(Qt.PointingHandCursor);
            QApplication.setOverrideCursor(cursor);
            strText = "删除账号信息"
            QToolTip.showText(mouseEvent.globalPos(), strText)
        else:
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        return QStyledItemDelegate.editorEvent(self,event, model, option, index)


class  myWindow(QWidget):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        mainLay = QVBoxLayout(self)
        self.cmb = QComboBox(self)
        self.cmb.addItems('张飞|吕布|关羽|刘备|赵云'.split('|'))
        self.cmb.setMinimumWidth(200)
        # self.cmb.setMinimumHeight(64)
        self.cmb.setEditable(True)
        pDelegate = itemDelegate(self)
        self.cmb.setItemDelegate(pDelegate)
        pDelegate.deleteItem.connect(self.on_delItem)
        mainLay.addWidget(self.cmb)
        mutilCmb = myCmb(self)
        mainLay.addWidget(mutilCmb)

    def on_delItem(self,index):
        if QMessageBox.question(self,'提示',"是否删除 '{0}'?".format(self.cmb.itemText(index.row())),
            QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
            self.cmb.removeItem(index.row())
            self.sender().removeItem(index.row())


class myCmb(QComboBox):
    def __init__(self,parent = None):
        super(myCmb,self).__init__()
        self.pListWidget = QListWidget()
        for i in range(5):
            item = QListWidgetItem(self.pListWidget)
            self.pListWidget.addItem(item)
            item.setData(Qt.UserRole,i)
            checkbox = QCheckBox(self)
            checkbox.setText('Qter%d'% i)
            self.pListWidget.setItemWidget(item,checkbox)
            checkbox.stateChanged.connect(self.on_stateChange)
            
        # self.cmb = QComboBox(self)
        self.pLineEdit  = QLineEdit(self)
        self.setMinimumWidth(200)
        self.setModel(self.pListWidget.model())
        self.setView(self.pListWidget)
        self.setLineEdit(self.pLineEdit)
        self.pLineEdit.setReadOnly(True)
        # self.pLineEdit.textChanged.connect(self.on_textChanged)
        self.bSelect = False

    def on_stateChange(self,stat):
        # self.bSelect = True
        # check = QCheckBox()
        check = self.sender()
        table = str.maketrans(';',' ')
        preTextList = self.pLineEdit.text().translate(table).split()
        # preTextList = self.pLineEdit.text().split(';')
        if check.isChecked():
            if check.text() not in  preTextList:
                preTextList.append(check.text())
                self.pLineEdit.setText(';'.join(preTextList))
        else:
            if check.text() in preTextList:
                preTextList.remove(check.text())
                self.pLineEdit.setText(';'.join(preTextList))

    def on_textChanged(self,text):
        if not self.bSelect: 
            self.pLineEdit.setText(text)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
