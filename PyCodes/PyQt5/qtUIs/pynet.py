#encoding=utf8
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtGui import QFont,QImage,QIcon,QPixmap,QPainter,QPen,QPalette,QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
import sys,os


def netProxy():
    networkAccessManager = QNetworkAccessManager()
    url = QUrl("http://search.dongting.com/song/search/old")
    query = QUrlQuery()
    query.addQueryItem("q", "李荣浩")
    query.addQueryItem("page", "1")
    query.addQueryItem("size", "100")

    url.setQuery(query)

    request = QNetworkRequest()
    request.setHeader(QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded");
    request.setUrl(url);
    # 开始请求
    pReply = networkAccessManager.get(request)
    loop = QEventLoop()
    pReply.finished.connect(loop.quit)
    # connect(pReply, SIGNAL(finished()), &loop, SLOT(quit()))
    loop.exec();

    #  获取歌曲信息
    bytes = pReply.readAll()

    print(type(bytes),bytes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    netProxy()
    sys.exit(app.exec_())
