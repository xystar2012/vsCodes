from PyQt4.QtCore import QTime,QTimer,pyqtSignal,QThread
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import time


class SlaveThread(QThread):
    request = pyqtSignal(str)
    error = pyqtSignal(str)
    timeout = pyqtSignal(str)

    def __init__(self,parent = None):
        super(SlaveThread,self).__init__()
        self.waitTimeout = 0
        self.quit = False
        self.mutex = QMutex()

    def __del__(self):
        self.mutex.lock()
        self.quit = True
        self.mutex.unlock()

    def run(self):
        
        while not self.quit:
            try:
                self.error.emit("can't not open %s,error code:%d"%("com3",12345))
                self.timeout.emit("Wait write response timeout %s"%(QTime.currentTime().toString()))
                self.request.emit("RequesData: %s"%(QTime.currentTime().toString()))
            except TypeError as e:
                print('Got Error',e)
            finally:
                print("Continus working ...")
            time.sleep(0.5)


    def startSlave(self,portNam,timeout,respone):
        locker = QMutexLocker(self.mutex)
        if not self.isRunning():
            self.start()
        

class myWindow(QDialog):
    def __init__(self,parent = None):
        super(myWindow,self).__init__()
        self.thread = SlaveThread(self)
        self.transactionCount = 0
        self.serialPortLabel = QLabel("Serial port:")
        self.serialPortComboBox = QComboBox()
        self.waitRequestSpinBox = QSpinBox()
        self.waitRequestLabel = QLabel('Wait request, msec:')
        self.responseLabel = QLabel("Response:")
        self.responseLineEdit = QLineEdit("Hello, I'm Slave.")
        self.trafficLabel = QLabel("No traffic.")
        self.statusLabel = QLabel("Status: Not running.")
        self.runButton = QPushButton('Start')
        

        self.waitRequestSpinBox.setRange(0,10000)
        self.waitRequestSpinBox.setValue(100000)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.serialPortLabel,0,0)
        mainLayout.addWidget(self.serialPortComboBox,0,1)
        mainLayout.addWidget(self.waitRequestLabel,1,0)
        mainLayout.addWidget(self.waitRequestSpinBox,1,1)
        mainLayout.addWidget(self.runButton,0,2,2,1)
        mainLayout.addWidget(self.responseLabel,2,0)
        mainLayout.addWidget(self.responseLineEdit,2,1)
        mainLayout.addWidget(self.trafficLabel,3,0)
        mainLayout.addWidget(self.statusLabel,3,1)

        self.setWindowTitle('Blocking Slave')
        self.serialPortComboBox.setFocus()

        self.runButton.clicked.connect(self.startSlave)
        self.thread.request.connect(self.showRequest)
        self.thread.error.connect(self.processError)
        self.thread.timeout.connect(self.processTimeout)        

    def startSlave(self):
        self.runButton.setEnabled(False)
        self.statusLabel.setText("Status: Running, connected to port %s."%(self.serialPortComboBox.currentText()))
        self.thread.startSlave(self.serialPortComboBox.currentText(),self.waitRequestSpinBox.value(),
        self.responseLineEdit.text())

    
    def startSlave(self):
        self.runButton.setEnabled(False)
        self.statusLabel.setText("Status: Running, connected to port %s."%(self.serialPortComboBox.currentText()))
        self.thread.startSlave(self.serialPortComboBox.currentText(),self.waitRequestSpinBox.value(),
        self.responseLineEdit.text())

    def showRequest(self,s):
        self.transactionCount += 1
        self.trafficLabel.setText("Traffic, transaction #%d:"
                             "\n\r-request: %s"
                             "\n\r-response: %s"%(self.transactionCount,s,self.responseLineEdit.text()))
    
    def processError(self,s):
        self.activateRunButton()
        self.statusLabel.setText(("Status: Not running, %s.")%(s))
        self.trafficLabel.setText("No traffic.")

    def processTimeout(self,s):
        self.statusLabel.setText(("Status: Running, %s.")%(s))
        self.trafficLabel.setText("No traffic.")

    def activateRunButton(self):
        self.runButton.setEnabled(True)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myWindow()
    window.show()
    sys.exit(app.exec_())
