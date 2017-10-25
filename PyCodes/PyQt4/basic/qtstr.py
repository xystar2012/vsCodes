import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import qApp
from PyQt4.QtGui import *
from PyQt4.QtCore import *



if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    # app.aboutQt()
    str = QString("%1,%2").arg('hello','today')
    str.insert(1, 'test')
    # print str.split(' ').join("-")
    str2 = unicode("汉","utf8",'ignore')
    print str,type(str),str2
 
    sys.exit(app.exec_())