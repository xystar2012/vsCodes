from PyQt5 import QtWidgets,QtGui,QtCore
###  用于类型提升  实际无 eventfitle 好用
class SerialPortInput(QtWidgets.QTextEdit):
    def __init__(self,parent = None):
        super(SerialPortInput,self).__init__(parent)
        self._is_hex = False
        
    def keyPressEvent(self, event):
        if self._is_hex:
            #event.setText("%2dX " % (ord(str(event.text()))))
            print(str(event.text()))
            hex_data = "%02X " % (ord(str(event.text())))
            qhex_data = "%s" % hex_data
            #print('hex_data = %s' % hex_data)
            new_event = QtGui.QKeyEvent(event.type(),event.key(),event.modifiers(),
                                       qhex_data,
                                        event.isAutoRepeat(),event.count())
            return super(SerialPortInput,self).keyPressEvent(new_event)
        else:
            return super(SerialPortInput,self).keyPressEvent(event)
        
    def setIsHex(self,isHex):
        self._is_hex = isHex