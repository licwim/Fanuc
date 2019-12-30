import sys
import os
import glob
from PyQt5 import QtWidgets

from design import Ui_MainWindow
from converter import converter

# with open('tests/test.nc') as file:
	# text = file.read()
src = '' # text
dst = ''

class mywindow(QtWidgets.QMainWindow):
	filetype = "list"
	filelist = []
	savepath = os.getcwd() + "\\Converted_NC_files"

	msgPathNotFound = ''
	msgConvertError = ''
	msgConvertDone = ''

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# self.ui.textOld.setText(src)
		self.ui.textNew.setText(dst)
		self.ui.lineOpen.setText(os.getcwd())
		self.ui.lineSave.setText(mywindow.savepath)
		self.ui.btnConvert.clicked.connect(self.clickConvert)
		# self.ui.btnBrowseOpenFile.clicked.connect(self.clickBrowseOpenFile)
		self.ui.btnBrowseOpenFolder.clicked.connect(self.clickBrowseOpenFoder)
		self.ui.btnBrowseSave.clicked.connect(self.clickBrowseSaveFolder)
		self.ui.lineOpen.returnPressed.connect(self.openFromLine)
		mywindow.filelist = self.findFilelist(os.getcwd())
		self.msgBoxes()


	def msgBoxes(self):
		mywindow.msgPathNotFound = QtWidgets.QMessageBox()
		mywindow.msgConvertError = QtWidgets.QMessageBox()
		mywindow.msgConvertDone = QtWidgets.QMessageBox()

		mywindow.msgPathNotFound.setWindowTitle("Error:")
		mywindow.msgPathNotFound.setText("This path is not found.")
		mywindow.msgPathNotFound.setIcon(QtWidgets.QMessageBox.Critical)
		mywindow.msgPathNotFound.setStandardButtons(QtWidgets.QMessageBox.Ok)

		mywindow.msgConvertError.setWindowTitle("Error:")
		mywindow.msgConvertError.setText("Convert error!")
		mywindow.msgConvertError.setIcon(QtWidgets.QMessageBox.Warning)
		mywindow.msgConvertError.setStandardButtons(QtWidgets.QMessageBox.Ok)

		mywindow.msgConvertDone.setWindowTitle("Succes")
		mywindow.msgConvertDone.setText("Convert is done.")
		mywindow.msgConvertDone.setIcon(QtWidgets.QMessageBox.Information)
		mywindow.msgConvertDone.setStandardButtons(QtWidgets.QMessageBox.Ok)



	def clickConvert(self):
		savepath = mywindow.savepath

		if not os.path.exists(mywindow.savepath):
			os.mkdir(mywindow.savepath)

		if mywindow.filetype == "file":
			text = self.ui.textOld.toPlainText()
			lines = text.split('\n')
			lines = converter(lines)
			fulltext = '\n'.join(lines)
			self.ui.textNew.setText(fulltext)
			# line = converter(oldfile)
		elif mywindow.filetype == "list":
			filelist = mywindow.filelist
			for file in filelist:
				lines = converter(self.openFile(file))
				# print(lines)
				if not lines: break
				newfile = open("%s/[F2NC] %s" % (savepath, os.path.basename(file)), "w")
				newfile.write('\n'.join(lines))
				newfile.close()
			if lines: mywindow.msgConvertDone.exec()
		else: mywindow.msgConvertError.exec()


	def openFile(self, filename):
		print("\t\t%s" % filename)
		if not os.access(filename, os.R_OK):
			mywindow.msgPathNotFound.exec()
			return ()
		file = open(filename)
		lines = file.readlines()
		file.close()
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
	
	def openFromLine(self):
		path = self.ui.lineOpen.text()
		# print(path)
		if os.path.isfile(path):
			self.ui.textNew.clear()
			file = open(path)
			text = file.read()
			self.ui.textOld.setText(text)
			file.close()
			mywindow.filetype = "file"
		elif os.path.isdir(path):
			# self.ui.textOld.clear()
			mywindow.filelist = self.findFilelist(path)
			mywindow.filetype = "list"
		else:
			mywindow.filetype = "err"
			mywindow.msgPathNotFound.exec()

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
		mywindow.savepath = path
		self.ui.lineSave.setText(path)


def main():
	app = QtWidgets.QApplication([])
	window = mywindow()
	window.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()