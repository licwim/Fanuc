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
		MainWindow.resize(334, 531)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/icon/fc.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		MainWindow.setStyleSheet("background-color: rgb(216, 216, 216);")
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
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
		self.label = QtWidgets.QLabel(self.centralwidget)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setItalic(True)
		self.label.setFont(font)
		self.label.setStyleSheet("color: rgb(0, 0, 0);")
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
		self.verticalLayout_2.addLayout(self.gridLayout)
		self.gridLayout_2 = QtWidgets.QGridLayout()
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.btnBrowseSave = QtWidgets.QPushButton(self.centralwidget)
		self.btnBrowseSave.setMaximumSize(QtCore.QSize(100, 30))
		self.btnBrowseSave.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
		self.btnBrowseSave.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
		self.btnBrowseSave.setObjectName("btnBrowseSave")
		self.gridLayout_2.addWidget(self.btnBrowseSave, 1, 1, 1, 1)
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
		self.verticalLayout_2.addLayout(self.gridLayout_2)
		self.frame = QtWidgets.QFrame(self.centralwidget)
		self.frame.setEnabled(True)
		self.frame.setStyleSheet("")
		self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName("frame")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.textNew = QtWidgets.QTextBrowser(self.frame)
		self.textNew.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.textNew.setObjectName("textNew")
		self.horizontalLayout.addWidget(self.textNew)
		self.verticalLayout_5 = QtWidgets.QVBoxLayout()
		self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
		self.verticalLayout_5.setSpacing(10)
		self.verticalLayout_5.setObjectName("verticalLayout_5")
		self.btnConvert1 = QtWidgets.QPushButton(self.frame)
		self.btnConvert1.setMaximumSize(QtCore.QSize(230, 35))
		self.btnConvert1.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
		self.btnConvert1.setObjectName("btnConvert1")
		self.verticalLayout_5.addWidget(self.btnConvert1)
		self.btnConvert2 = QtWidgets.QPushButton(self.frame)
		self.btnConvert2.setMaximumSize(QtCore.QSize(230, 35))
		self.btnConvert2.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
		self.btnConvert2.setObjectName("btnConvert2")
		self.verticalLayout_5.addWidget(self.btnConvert2)
		self.btnConvert12 = QtWidgets.QPushButton(self.frame)
		self.btnConvert12.setMaximumSize(QtCore.QSize(230, 35))
		self.btnConvert12.setStyleSheet("background-color: rgb(182, 182, 182);\n"
"color: rgb(0, 0, 0);")
		self.btnConvert12.setObjectName("btnConvert12")
		self.verticalLayout_5.addWidget(self.btnConvert12)
		self.horizontalLayout.addLayout(self.verticalLayout_5)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.tabSettings = QtWidgets.QTabWidget(self.frame)
		self.tabSettings.setEnabled(True)
		self.tabSettings.setObjectName("tabSettings")
		self.tab_nc = QtWidgets.QWidget()
		self.tab_nc.setObjectName("tab_nc")
		self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_nc)
		self.verticalLayout_6.setObjectName("verticalLayout_6")
		self.rbtnNc = QtWidgets.QRadioButton(self.tab_nc)
		self.rbtnNc.setCheckable(True)
		self.rbtnNc.setChecked(True)
		self.rbtnNc.setAutoRepeat(True)
		self.rbtnNc.setObjectName("rbtnNc")
		self.verticalLayout_6.addWidget(self.rbtnNc)
		self.frameNc = QtWidgets.QFrame(self.tab_nc)
		self.frameNc.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frameNc.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frameNc.setObjectName("frameNc")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameNc)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_3 = QtWidgets.QLabel(self.frameNc)
		self.label_3.setObjectName("label_3")
		self.horizontalLayout_2.addWidget(self.label_3)
		self.set_nc_Null = QtWidgets.QLineEdit(self.frameNc)
		self.set_nc_Null.setMaximumSize(QtCore.QSize(145, 16777215))
		self.set_nc_Null.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.set_nc_Null.setObjectName("set_nc_Null")
		self.horizontalLayout_2.addWidget(self.set_nc_Null)
		self.verticalLayout_3.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.label_4 = QtWidgets.QLabel(self.frameNc)
		self.label_4.setObjectName("label_4")
		self.horizontalLayout_3.addWidget(self.label_4)
		self.set_nc_Gt = QtWidgets.QLineEdit(self.frameNc)
		self.set_nc_Gt.setMaximumSize(QtCore.QSize(145, 16777215))
		self.set_nc_Gt.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.set_nc_Gt.setObjectName("set_nc_Gt")
		self.horizontalLayout_3.addWidget(self.set_nc_Gt)
		self.verticalLayout_3.addLayout(self.horizontalLayout_3)
		self.set_nc_LocalVar = QtWidgets.QCheckBox(self.frameNc)
		self.set_nc_LocalVar.setChecked(True)
		self.set_nc_LocalVar.setObjectName("set_nc_LocalVar")
		self.verticalLayout_3.addWidget(self.set_nc_LocalVar)
		self.set_nc_GlobalVar = QtWidgets.QCheckBox(self.frameNc)
		self.set_nc_GlobalVar.setChecked(True)
		self.set_nc_GlobalVar.setObjectName("set_nc_GlobalVar")
		self.verticalLayout_3.addWidget(self.set_nc_GlobalVar)
		self.set_nc_OverGlobalVar = QtWidgets.QCheckBox(self.frameNc)
		self.set_nc_OverGlobalVar.setChecked(True)
		self.set_nc_OverGlobalVar.setObjectName("set_nc_OverGlobalVar")
		self.verticalLayout_3.addWidget(self.set_nc_OverGlobalVar)
		self.set_nc_If = QtWidgets.QCheckBox(self.frameNc)
		self.set_nc_If.setEnabled(True)
		self.set_nc_If.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.set_nc_If.setChecked(True)
		self.set_nc_If.setObjectName("set_nc_If")
		self.verticalLayout_3.addWidget(self.set_nc_If)
		self.set_nc_Fup = QtWidgets.QCheckBox(self.frameNc)
		self.set_nc_Fup.setEnabled(True)
		self.set_nc_Fup.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.set_nc_Fup.setChecked(True)
		self.set_nc_Fup.setObjectName("set_nc_Fup")
		self.verticalLayout_3.addWidget(self.set_nc_Fup)
		self.verticalLayout_6.addWidget(self.frameNc)
		self.tabSettings.addTab(self.tab_nc, "")
		self.tab_syntec = QtWidgets.QWidget()
		self.tab_syntec.setObjectName("tab_syntec")
		self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_syntec)
		self.verticalLayout_7.setObjectName("verticalLayout_7")
		self.rbtnSyntec = QtWidgets.QRadioButton(self.tab_syntec)
		self.rbtnSyntec.setObjectName("rbtnSyntec")
		self.verticalLayout_7.addWidget(self.rbtnSyntec)
		self.frameSyntec = QtWidgets.QFrame(self.tab_syntec)
		self.frameSyntec.setEnabled(False)
		self.frameSyntec.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frameSyntec.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frameSyntec.setObjectName("frameSyntec")
		self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frameSyntec)
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.set_syntec_Set1 = QtWidgets.QCheckBox(self.frameSyntec)
		self.set_syntec_Set1.setChecked(True)
		self.set_syntec_Set1.setObjectName("set_syntec_Set1")
		self.verticalLayout_4.addWidget(self.set_syntec_Set1)
		self.set_syntec_Set2 = QtWidgets.QCheckBox(self.frameSyntec)
		self.set_syntec_Set2.setChecked(True)
		self.set_syntec_Set2.setObjectName("set_syntec_Set2")
		self.verticalLayout_4.addWidget(self.set_syntec_Set2)
		self.set_syntec_Set3 = QtWidgets.QCheckBox(self.frameSyntec)
		self.set_syntec_Set3.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.set_syntec_Set3.setChecked(True)
		self.set_syntec_Set3.setObjectName("set_syntec_Set3")
		self.verticalLayout_4.addWidget(self.set_syntec_Set3)
		self.set_syntec_Set4 = QtWidgets.QCheckBox(self.frameSyntec)
		self.set_syntec_Set4.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.set_syntec_Set4.setChecked(True)
		self.set_syntec_Set4.setObjectName("set_syntec_Set4")
		self.verticalLayout_4.addWidget(self.set_syntec_Set4)
		self.verticalLayout_7.addWidget(self.frameSyntec)
		self.tabSettings.addTab(self.tab_syntec, "")
		self.verticalLayout.addWidget(self.tabSettings)
		self.verticalLayout_2.addWidget(self.frame)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.msgBoxes(icon)
		self.retranslateUi(MainWindow)
		self.tabSettings.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Fanuc Converter"))
		self.btnBrowseOpenFolder.setText(_translate("MainWindow", "Обзор..."))
		self.label.setText(_translate("MainWindow", "Путь папки с конвертируемыми файлами:"))
		self.btnBrowseSave.setText(_translate("MainWindow", "Обзор..."))
		self.label_2.setText(_translate("MainWindow", "Путь папки сохранения:"))
		self.btnConvert1.setText(_translate("MainWindow", "Конвертировать\n"
"Этап 1"))
		self.btnConvert2.setText(_translate("MainWindow", "Конвертировать\n"
"Этап 2"))
		self.btnConvert12.setText(_translate("MainWindow", "Конвертировать\n"
"Этап 1 + Этап 2"))
		self.rbtnNc.setText(_translate("MainWindow", "Конвертировать в язык NC"))
		self.label_3.setText(_translate("MainWindow", "Значение для #0:"))
		self.label_4.setText(_translate("MainWindow", "Значение для GT0:"))
		self.set_nc_LocalVar.setText(_translate("MainWindow", "Локальные переменные (+30)"))
		self.set_nc_GlobalVar.setText(_translate("MainWindow", "Глобальные переменные > 100 (-40)"))
		self.set_nc_OverGlobalVar.setText(_translate("MainWindow", "Глобальные переменные > 500 (-300)"))
		self.set_nc_If.setText(_translate("MainWindow", "IF - THEN"))
		self.set_nc_Fup.setText(_translate("MainWindow", "FUP"))
		self.tabSettings.setTabText(self.tabSettings.indexOf(self.tab_nc), _translate("MainWindow", "Fanuc -> NC"))
		self.rbtnSyntec.setText(_translate("MainWindow", "Конвертировать в язык Syntec"))
		self.set_syntec_Set1.setText(_translate("MainWindow", "Настройка 1"))
		self.set_syntec_Set2.setText(_translate("MainWindow", "Настройка 2"))
		self.set_syntec_Set3.setText(_translate("MainWindow", "Настройка 3"))
		self.set_syntec_Set4.setText(_translate("MainWindow", "Настройка 4"))
		self.tabSettings.setTabText(self.tabSettings.indexOf(self.tab_syntec), _translate("MainWindow", "Fanuc -> Syntec"))

	def msgBoxes(self, icon):
		self.msgPathNotFound = QtWidgets.QMessageBox()
		self.msgConvertError = QtWidgets.QMessageBox()
		self.msgConvertDone = QtWidgets.QMessageBox()

		self.msgPathNotFound.setWindowTitle("Error:")
		self.msgPathNotFound.setText("This path is not found.")
		self.msgPathNotFound.setWindowIcon(icon)
		self.msgPathNotFound.setIcon(QtWidgets.QMessageBox.Critical)
		self.msgPathNotFound.setStandardButtons(QtWidgets.QMessageBox.Ok)

		self.msgConvertError.setWindowTitle("Error:")
		self.msgConvertError.setText("Convert error!")
		self.msgConvertError.setWindowIcon(icon)
		self.msgConvertError.setIcon(QtWidgets.QMessageBox.Warning)
		self.msgConvertError.setStandardButtons(QtWidgets.QMessageBox.Ok)

		self.msgConvertDone.setWindowTitle("Succes")
		self.msgConvertDone.setText("Convert is done.")
		self.msgConvertDone.setWindowIcon(icon)
		self.msgConvertDone.setIcon(QtWidgets.QMessageBox.Information)
		self.msgConvertDone.setStandardButtons(QtWidgets.QMessageBox.Ok)

import design_rc
