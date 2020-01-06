# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   main.py                                         #
#       By: licwim                                  #
#                                                   #
#   Created: 05-01-2020 18:23:20 by licwim          #
#   Updated: 05-01-2020 19:59:31 by licwim          #
#                                                   #
# ************************************************* #

import sys
import os
import winreg
from PyQt5 import QtWidgets

from design import Ui_MainWindow
from converter import converter

with open('tests/test.nc') as file:
	text = file.read()
src = text
dst = ''

class mywindow(QtWidgets.QMainWindow):
	filetype = "file"
	filelist = []
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders", 0, winreg.KEY_ALL_ACCESS)
	docpath = winreg.QueryValueEx(key, "Personal")[0]
	savepath = docpath + "\\F2NC Files"
	# savepath = os.getcwd() + "\\Converted_NC_files"

	msgPathNotFound = ''
	msgConvertError = ''
	msgConvertDone = ''

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.textOld.setText(src)
		self.ui.textNew.setText(dst)
		self.ui.lineOpen.setText(self.docpath)
		self.ui.lineSave.setText(self.savepath)
		self.ui.btnConvert1.clicked.connect(self.clickConvert1)
		self.ui.btnConvert2.clicked.connect(self.clickConvert2)
		self.ui.btnConvert12.clicked.connect(self.clickConvert12)
		self.ui.btnBrowseOpenFile.clicked.connect(self.clickBrowseOpenFile)
		self.ui.btnBrowseOpenFolder.clicked.connect(self.clickBrowseOpenFoder)
		self.ui.btnBrowseSave.clicked.connect(self.clickBrowseSaveFolder)
		self.ui.lineOpen.returnPressed.connect(self.openFromLine)
		# self.filelist = self.findFilelist(os.getcwd())
		self.msgBoxes()


	def msgBoxes(self):
		self.msgPathNotFound = QtWidgets.QMessageBox()
		self.msgConvertError = QtWidgets.QMessageBox()
		self.msgConvertDone = QtWidgets.QMessageBox()

		self.msgPathNotFound.setWindowTitle("Error:")
		self.msgPathNotFound.setText("This path is not found.")
		self.msgPathNotFound.setIcon(QtWidgets.QMessageBox.Critical)
		self.msgPathNotFound.setStandardButtons(QtWidgets.QMessageBox.Ok)

		self.msgConvertError.setWindowTitle("Error:")
		self.msgConvertError.setText("Convert error!")
		self.msgConvertError.setIcon(QtWidgets.QMessageBox.Warning)
		self.msgConvertError.setStandardButtons(QtWidgets.QMessageBox.Ok)

		self.msgConvertDone.setWindowTitle("Succes")
		self.msgConvertDone.setText("Convert is done.")
		self.msgConvertDone.setIcon(QtWidgets.QMessageBox.Information)
		self.msgConvertDone.setStandardButtons(QtWidgets.QMessageBox.Ok)



	def clickConvert1(self):
		self.clickConvert(1)

	def clickConvert2(self):
		self.clickConvert(2)

	def clickConvert12(self):
		self.clickConvert(12)

	def clickConvert(self, step):
		savepath = self.savepath

		if not os.path.exists(self.savepath):
			os.mkdir(self.savepath)

		if self.filetype == "file":
			text = self.ui.textOld.toPlainText()
			lines = text.split('\n')
			# print(lines)
			lines = converter(lines, step)
			fulltext = '\n'.join(lines)
			self.ui.textNew.setText(fulltext)
			# line = converter(oldfile)
		elif self.filetype == "list":
			filelist = self.filelist
			for file in filelist:
				lines = converter(self.openFile(file), step)
				# print(lines)
				if not lines: break
				newfile = open("%s/[F2NC] %s" % (savepath, os.path.basename(file)), "w")
				newfile.write('\n'.join(lines))
				newfile.close()
			if lines: self.msgConvertDone.exec()
		else: self.msgConvertError.exec()


	def openFile(self, filename):
		print("\t\t", filename)
		if not os.access(filename, os.R_OK):
			self.msgPathNotFound.exec()
			return ()
		with open(filename) as file:
			lines = file.readlines()
		return (lines)

	def clickBrowseOpenFile(self):
		path = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "","All Files (*)")[0]
		if not path:
			return (1)
		self.ui.lineOpen.setText(path)
		self.openFromLine()

	def	clickBrowseOpenFoder(self):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")
		if not path:
			return (1)
		self.ui.lineOpen.setText(path)
		self.openFromLine()

	def openPath(self, paths = 0):
		if paths == 0: paths = (self.ui.lineOpen.text())
		self.filelist.clear()
		for path in paths:
			self.openFromLine(path)

	def openFromLine(self):
		path = self.ui.lineOpen.text()
		# print(path)
		if os.path.isfile(path):
			self.ui.textNew.clear()
			with open(path) as file:
				text = file.read()
			self.ui.textOld.setText(text)
			self.filetype = "file"
		elif os.path.isdir(path):
			self.ui.textOld.clear()
			self.filelist = self.findFilelist(path)
			self.filetype = "list"
		else:
			self.filetype = "err"
			self.msgPathNotFound.exec()

	def findFilelist(self, path):
		os.chdir(path)
		files = os.listdir(path)
		filelist = []
		# print (files)
		for file in files:
			if not os.path.isdir(file):
				filelist.append(file)
		self.ui.textNew.setText("\n".join(filelist))
		return (filelist)

	def clickBrowseSaveFolder(self):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")
		if not path:
			return (1)
		self.savepath = path
		self.ui.lineSave.setText(path)


def main():
	app = QtWidgets.QApplication([])
	window = mywindow()
	window.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
input("Press Enter")