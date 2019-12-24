import sys
import os
import glob
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
	savepath = os.getcwd() + "\\Converted_NC_files"

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.textOld.setText(src)
		self.ui.textNew.setText(dst)
		self.ui.lineOpen.setText(os.getcwd())
		self.ui.lineSave.setText(mywindow.savepath)
		self.ui.btnConvert.clicked.connect(self.clickConvert)
		self.ui.btnBrowseOpenFile.clicked.connect(self.clickBrowseOpenFile)
		self.ui.btnBrowseOpenFolder.clicked.connect(self.clickBrowseOpenFoder)
		self.ui.btnBrowseSave.clicked.connect(self.clickBrowseSaveFolder)
		mywindow.filelist = self.findFilelist(os.getcwd())
		self.ui.lineOpen.returnPressed.connect(self.openFromLine)


	def clickConvert(self):
		savepath = mywindow.savepath

		if not os.path.exists(mywindow.savepath):
			os.mkdir(mywindow.savepath)

		if mywindow.filetype == "file":
			text = self.ui.textOld.toPlainText()
			lines = text.split('\n')
			lines = converter(lines)
			# print(type(lines), lines)
			fulltext = '\n'.join(lines)
			self.ui.textNew.setText(fulltext)
			# line = converter(oldfile)
		elif mywindow.filetype == "list":
			filelist = mywindow.filelist
			# print (filelist)
			for file in filelist:
				lines = converter(self.convertFile(file))
				newfile = open(savepath + "/[F2NC] " + os.path.basename(file), "w")
				newfile.writelines(lines)
				newfile.close()
		else:
			self.ui.textNew.setText("ERR: Convert error!")


	def convertFile(self, filename):
		# print(filename)
		file = open(filename)
		lines = file.readlines()
		file.close()
		return (lines)

	def clickBrowseOpenFile(self):
		path = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "","All Files (*);;FANUC Files (*.nc)")[0]
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
			file = open(path)
			text = file.read()
			self.ui.textNew.clear()
			self.ui.textOld.setText(text)
			file.close()
			mywindow.filetype = "file"
		elif os.path.isdir(path):
			mywindow.filelist = self.findFilelist(path)
			mywindow.filetype = "list"
		else:
			self.ui.textNew.setText("ERR: File not exist or not suppoted.")
			mywindow.filetype = "err"

	def findFilelist(self, path):
		files = os.listdir(path)
		filelist = []
		# print (files)
		for file in files:
			if (not os.path.isdir(file)) and file.lower().endswith(".nc"):
				filelist.append(file)
		self.ui.textNew.setText("\n".join(filelist))
		return (filelist)

	def clickBrowseSaveFolder(self):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder")
		if not path:
			return (1)
		mywindow.savepath = path
		self.ui.lineSave.setText(path)

		# print(type(text), text)




def main():
	app = QtWidgets.QApplication([])  # Новый экземпляр QApplication
	window = mywindow()  # Создаём объект класса MyWindow
	window.show()  # Показываем окно
	# app.exec_()  # и запускаем приложение
	sys.exit(app.exec())

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()

input("Press Enter")