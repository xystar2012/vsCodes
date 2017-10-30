# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'udpsendbyqt.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UDPSendByQtClass(object):
    def setupUi(self, UDPSendByQtClass):
        UDPSendByQtClass.setObjectName("UDPSendByQtClass")
        UDPSendByQtClass.resize(634, 497)
        self.centralWidget = QtWidgets.QWidget(UDPSendByQtClass)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 2, 4, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("\n"
"  QGroupBox {\n"
"      background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 0 #E0E0E0, stop: 1 #FFFFFF);\n"
"      border: 2px solid gray;\n"
"      border-radius: 5px;\n"
"      margin-top: 1ex; /* leave space at the top for the title */\n"
"  }\n"
"\n"
"  QGroupBox::title {\n"
"      subcontrol-origin: margin;\n"
"      subcontrol-position: top center; /* position at the top center */\n"
"      padding: 0 3px;\n"
"      background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                        stop: 0 darkBlue, stop: 1 #FFFFFF);\n"
"  }")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.hlay_group = QtWidgets.QHBoxLayout(self.groupBox)
        self.hlay_group.setContentsMargins(11, 11, 11, 11)
        self.hlay_group.setSpacing(6)
        self.hlay_group.setObjectName("hlay_group")
        self.hlay_mutil = QtWidgets.QHBoxLayout()
        self.hlay_mutil.setContentsMargins(11, 11, 11, 11)
        self.hlay_mutil.setSpacing(6)
        self.hlay_mutil.setObjectName("hlay_mutil")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.hlay_mutil.addWidget(self.label)
        self.addr_Muti = QtWidgets.QLineEdit(self.groupBox)
        self.addr_Muti.setObjectName("addr_Muti")
        self.hlay_mutil.addWidget(self.addr_Muti)
        self.hlay_group.addLayout(self.hlay_mutil)
        self.hlay_single = QtWidgets.QHBoxLayout()
        self.hlay_single.setContentsMargins(11, 11, 11, 11)
        self.hlay_single.setSpacing(6)
        self.hlay_single.setObjectName("hlay_single")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.hlay_single.addWidget(self.label_2)
        self.Addr_Single = QtWidgets.QLineEdit(self.groupBox)
        self.Addr_Single.setObjectName("Addr_Single")
        self.hlay_single.addWidget(self.Addr_Single)
        self.hlay_group.addLayout(self.hlay_single)
        self.hlay_gps = QtWidgets.QHBoxLayout()
        self.hlay_gps.setContentsMargins(11, 11, 11, 11)
        self.hlay_gps.setSpacing(6)
        self.hlay_gps.setObjectName("hlay_gps")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.hlay_gps.addWidget(self.label_3)
        self.Addr_Gps = QtWidgets.QLineEdit(self.groupBox)
        self.Addr_Gps.setObjectName("Addr_Gps")
        self.hlay_gps.addWidget(self.Addr_Gps)
        self.hlay_group.addLayout(self.hlay_gps)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 7)
        self.btn_start = QtWidgets.QPushButton(self.centralWidget)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 2, 5, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 7)
        spacerItem = QtWidgets.QSpacerItem(389, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.centralWidget)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 2, 6, 1, 1)
        self.scrollCaptionLabel = QtWidgets.QLabel(self.centralWidget)
        self.scrollCaptionLabel.setAutoFillBackground(True)
        self.scrollCaptionLabel.setStyleSheet("font: 75 12pt \"Consolas\";\n"
"text-decoration: underline;\n"
"")
        self.scrollCaptionLabel.setText("")
        self.scrollCaptionLabel.setObjectName("scrollCaptionLabel")
        self.gridLayout.addWidget(self.scrollCaptionLabel, 4, 0, 1, 5)
        self.cmb_data = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_data.sizePolicy().hasHeightForWidth())
        self.cmb_data.setSizePolicy(sizePolicy)
        self.cmb_data.setMinimumSize(QtCore.QSize(75, 0))
        self.cmb_data.setObjectName("cmb_data")
        self.cmb_data.addItem("")
        self.cmb_data.addItem("")
        self.gridLayout.addWidget(self.cmb_data, 2, 2, 1, 2)
        self.checkBox_log = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_log.setObjectName("checkBox_log")
        self.gridLayout.addWidget(self.checkBox_log, 2, 1, 1, 1)
        UDPSendByQtClass.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(UDPSendByQtClass)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 634, 23))
        self.menuBar.setObjectName("menuBar")
        UDPSendByQtClass.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(UDPSendByQtClass)
        self.statusBar.setObjectName("statusBar")
        UDPSendByQtClass.setStatusBar(self.statusBar)

        self.retranslateUi(UDPSendByQtClass)
        self.comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(UDPSendByQtClass)

    def retranslateUi(self, UDPSendByQtClass):
        _translate = QtCore.QCoreApplication.translate
        UDPSendByQtClass.setWindowTitle(_translate("UDPSendByQtClass", "UDPSendByQt"))
        self.comboBox.setItemText(0, _translate("UDPSendByQtClass", "Debug"))
        self.comboBox.setItemText(1, _translate("UDPSendByQtClass", "Warn"))
        self.comboBox.setItemText(2, _translate("UDPSendByQtClass", "Fatal"))
        self.comboBox.setItemText(3, _translate("UDPSendByQtClass", "Info"))
        self.groupBox.setTitle(_translate("UDPSendByQtClass", "SendAddr"))
        self.label.setText(_translate("UDPSendByQtClass", "Multi："))
        self.addr_Muti.setText(_translate("UDPSendByQtClass", "234.5.6.7:2600"))
        self.label_2.setText(_translate("UDPSendByQtClass", "Single："))
        self.Addr_Single.setText(_translate("UDPSendByQtClass", "192.168.1.220:2200"))
        self.label_3.setText(_translate("UDPSendByQtClass", "GPs："))
        self.Addr_Gps.setText(_translate("UDPSendByQtClass", "192.168.1.220:3006"))
        self.btn_start.setText(_translate("UDPSendByQtClass", "开始"))
        self.btn_stop.setText(_translate("UDPSendByQtClass", "结束"))
        self.cmb_data.setItemText(0, _translate("UDPSendByQtClass", "顺序递增"))
        self.cmb_data.setItemText(1, _translate("UDPSendByQtClass", "随机值"))
        self.checkBox_log.setText(_translate("UDPSendByQtClass", "记日志"))

# import udpsendbyqt_rc
