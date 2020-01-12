# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   design.py                                       #
#       By: licwim                                  #
#                                                   #
#   Created: 06-01-2020 16:34:56 by licwim          #
#   Updated: 12-01-2020 17:39:32 by licwim          #
#                                                   #
# ************************************************* #

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\design.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(546, 628)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/f2nc.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.btnBrowseOpenFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseOpenFolder.setMaximumSize(QtCore.QSize(100, 30))
        self.btnBrowseOpenFolder.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
        self.btnBrowseOpenFolder.setObjectName("btnBrowseOpenFolder")
        self.gridLayout.addWidget(self.btnBrowseOpenFolder, 3, 2, 1, 1)
        self.lineOpen = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setItalic(False)
        self.lineOpen.setFont(font)
        self.lineOpen.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineOpen.setInputMask("")
        self.lineOpen.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineOpen.setObjectName("lineOpen")
        self.gridLayout.addWidget(self.lineOpen, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineSave = QtWidgets.QLineEdit(self.centralwidget)
        self.lineSave.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineSave.setObjectName("lineSave")
        self.gridLayout_2.addWidget(self.lineSave, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.btnBrowseSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowseSave.setMaximumSize(QtCore.QSize(100, 30))
        self.btnBrowseSave.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
        self.btnBrowseSave.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.btnBrowseSave.setObjectName("btnBrowseSave")
        self.gridLayout_2.addWidget(self.btnBrowseSave, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textNew = QtWidgets.QTextBrowser(self.frame)
        self.textNew.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textNew.setObjectName("textNew")
        self.verticalLayout.addWidget(self.textNew)
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnConvert1 = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert1.setMaximumSize(QtCore.QSize(200, 23))
        self.btnConvert1.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
        self.btnConvert1.setObjectName("btnConvert1")
        self.horizontalLayout_2.addWidget(self.btnConvert1)
        self.btnConvert2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert2.setMaximumSize(QtCore.QSize(200, 23))
        self.btnConvert2.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
        self.btnConvert2.setObjectName("btnConvert2")
        self.horizontalLayout_2.addWidget(self.btnConvert2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnConvert12 = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert12.setMaximumSize(QtCore.QSize(250, 23))
        self.btnConvert12.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
        self.btnConvert12.setObjectName("btnConvert12")
        self.horizontalLayout_3.addWidget(self.btnConvert12)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fanuc to NC Converter"))
        self.label.setText(_translate("MainWindow", "Folder path:"))
        self.btnBrowseOpenFolder.setText(_translate("MainWindow", "Select folder"))
        self.label_2.setText(_translate("MainWindow", "Save path:"))
        self.btnBrowseSave.setText(_translate("MainWindow", "Select folder"))
        self.btnConvert1.setText(_translate("MainWindow", "Convert - Step 1"))
        self.btnConvert2.setText(_translate("MainWindow", "Convert - Step 2"))
        self.btnConvert12.setText(_translate("MainWindow", "Convert - Step 1 + Step 2"))


import design_rc
