__author__    = "Christopher Piekarski"
__email__     = "@c_piekarski"
 
import time, os, sys
from PyQt4 import QtCore, QtGui
from pygooglechart import *
 
def QChart(parent, type, **kwargs):
    class PyQtChart(type, QtGui.QWidget):
        def __init__(self, parent, **kwargs):
            QtGui.QWidget.__init__(self, parent, **kwargs)
            type.__init__(self, kwargs["size"].width(), kwargs["size"].height())
            self.pix = QtGui.QPixmap()
 
        def download(self):
            file = "./%f.png" % time.time()
            type.download(self, file)
            self.pix.load(file)
 
        def paintEvent(self, event):
            p = QtGui.QPainter(self)
            p.drawPixmap(0,0,self.pix)
            super(PyQtChart, self).paintEvent(event)
 
    return PyQtChart(parent, **kwargs)
 
class MainWindow(QtGui.QMainWindow):
    def __init__(self, **kwargs):
        super(QtGui.QMainWindow, self).__init__(**kwargs)
 
        t = QChart(self, PieChart3D, size=QtCore.QSize(250,100))
        t.add_data([10,20])
        t.set_pie_labels(['Hello', 'World'])
        t.download()
 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("PyQt Charting Demo")
    app.setQuitOnLastWindowClosed(True)
 
    scaledSize = QtCore.QSize(500,500)
    window = MainWindow(size=scaledSize)
    window.setWindowTitle("PyQt Charting Demo")
    window.show()
 
    sys.exit(app.exec_())