from PyQt5.QtCore import QDate, QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QListView, QListWidget, QListWidgetItem, QPushButton, QSpinBox,
        QStackedWidget, QVBoxLayout, QWidget,QMenuBar,QMenu)

import configdialog_rc

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)

        self.contentsWidget = QListWidget()
        self.contentsWidget.setViewMode(QListView.IconMode)
        self.contentsWidget.setIconSize(QSize(96, 84))
        self.contentsWidget.setMovement(QListView.Static)
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setSpacing(12)
        self.createIcons()

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close)

        # horizontalLayout = QHBoxLayout()
        # horizontalLayout.addWidget(self.contentsWidget)
        # horizontalLayout.addWidget(self.pagesWidget, 1)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.contentsWidget,Qt.AlignCenter)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Config Dialog")
        
        menuBar = QMenuBar(self)
        # group.setExclusive(True)  ## 只允许一个
        menu = menuBar.addMenu("&About")
        menu.addAction('about',lambda:QApplication.instance().aboutQt())
        mainLayout.setMenuBar(menuBar)

    def createIcons(self):
        configButton = QListWidgetItem(self.contentsWidget)
        configButton.setIcon(QIcon(':/images/config.png'))
        configButton.setText("Configuration")
        configButton.setTextAlignment(Qt.AlignHCenter)
        configButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        updateButton = QListWidgetItem(self.contentsWidget)
        updateButton.setIcon(QIcon(':/images/update.png'))
        updateButton.setText("Update")
        updateButton.setTextAlignment(Qt.AlignHCenter)
        updateButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        queryButton = QListWidgetItem(self.contentsWidget)
        queryButton.setIcon(QIcon(':/images/query.png'))
        queryButton.setText("Query")
        queryButton.setTextAlignment(Qt.AlignHCenter)
        queryButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contentsWidget.currentItemChanged.connect(self.changePage)
    
    def changePage(self, current, previous):
        if not current:
            current = previous
        print(current.text(),self.contentsWidget.row(current))
        # self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))


if __name__ == '__main__':
    
    import sys

    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    sys.exit(dialog.exec_())   