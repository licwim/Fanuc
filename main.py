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
#   Created: 06-01-2020 16:34:56 by licwim          #
#   Updated: 13-01-2020 02:08:32 by licwim          #
#                                                   #
# ************************************************* #

import sys
import os
import re
import winreg
from PyQt5 import QtCore, QtWidgets

from design import Ui_MainWindow
from converter_nc import converter_nc
from converter_syntec import converter_syntec

# with open('tests/test.nc') as file:
	# text = file.read()
src = '' # text
dst = ''

class mywindow(QtWidgets.QMainWindow):
	filetype = "list"
	filelist = []
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders", 0, winreg.KEY_ALL_ACCESS)
	docpath = winreg.QueryValueEx(key, "Personal")[0]
	# print(docpath)
	if "%USERPROFILE%" in docpath: docpath = docpath.replace("%USERPROFILE%", os.environ["USERPROFILE"])
	savepath = docpath + "\\Fanuc Converter Files"
	# savepath = os.getcwd() + "\\Converted_NC_files"

	msgPathNotFound = ''
	msgConvertError = ''
	msgConvertDone = ''

	flags_nc = [1, 1, 1, 1]
	lang = "nc"

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.textNew.setText(dst)
		self.ui.lineOpen.setText(self.docpath)
		self.ui.lineSave.setText(self.savepath)
		self.ui.btnConvert1.clicked.connect(self.clickConvert1)
		self.ui.btnConvert2.clicked.connect(self.clickConvert2)
		self.ui.btnConvert12.clicked.connect(self.clickConvert12)
		self.ui.btnBrowseOpenFolder.clicked.connect(self.clickBrowseOpenFoder)
		self.ui.btnBrowseSave.clicked.connect(self.clickBrowseSaveFolder)
		self.ui.lineOpen.returnPressed.connect(self.openFromLine)
		self.ui.set_nc_LocalVar.stateChanged.connect(self.setLocalVar)
		self.ui.set_nc_GlobalVar.stateChanged.connect(self.setWorkVar)
		self.ui.set_nc_If.stateChanged.connect(self.setIf)
		self.ui.set_nc_Fup.stateChanged.connect(self.setFup)
		self.ui.rbtnNc.clicked.connect(self.setNc)
		self.ui.rbtnSyntec.clicked.connect(self.setSyntec)
		self.msgBoxes()

	def test(self, state):
		print("TEST", state)

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

	def setNc(self, state):
		print("NC", state)
		if (state == False): self.ui.rbtnNc.toggle()
		else:
			self.ui.rbtnSyntec.toggle()
			self.ui.frameNc.setEnabled(True)
			self.ui.frameSyntec.setEnabled(False)
			self.lang = "nc"

	def setSyntec(self, state):
		print("Syntec", state)
		if (state == False): self.ui.rbtnSyntec.toggle()
		else:
			self.ui.rbtnNc.toggle()
			self.ui.frameSyntec.setEnabled(True)
			self.ui.frameNc.setEnabled(False)
			self.lang = "syntec"

	def setLocalVar(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc[0] = 1
		else: self.flags_nc[0] = 0
	
	def setWorkVar(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc[1] = 1
		else: self.flags_nc[1] = 0
	
	def setIf(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc[2] = 1
		else: self.flags_nc[2] = 0
	
	def setFup(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc[3] = 1
		else: self.flags_nc[3] = 0

	def clickConvert1(self):
		self.clickConvert(1)

	def clickConvert2(self):
		self.clickConvert(2)

	def clickConvert12(self):
		self.clickConvert(12)

	def clickConvert(self, step):

		if not os.path.exists(self.savepath):
			os.mkdir(self.savepath)

		if self.filetype == "list":
			filelist = self.filelist
			lines = []
			for file in filelist:
				# lines = converter_nc(self.openFile(file), step, self.flags_nc)
				try:
					if (self.lang == "nc"): lines = converter_nc(self.openFile(file), step, self.flags_nc)
					elif (self.lang == "syntec"): lines = converter_syntec(self.openFile(file), step, self.flags_syntec)
					else:
						self.msgConvertError.exec()
						break
				except: 
					self.msgConvertError.exec()
					break
				# print(lines)
				if not lines: break
				newfile = open(self.newFilename(step, file), "w")
				newfile.write('\n'.join(lines))
				newfile.close()
			if lines: self.msgConvertDone.exec()
		else: self.msgConvertError.exec()

	def newFilename(self, step, oldfile):
		savepath = self.savepath
		
		if step == 12: step = 2
		stepname = f"step {step}"
		# basename = os.path.basename(file)
		progpart = re.match(r"\[FC[\s_-]*\(step[\s_-]*\d\)\][\s_-]*", oldfile)
		if progpart:
			progpart = progpart[0]
			oldfile = oldfile.replace(progpart, '')
			progpart = progpart[::-1].replace(re.findall(r"step.*(\d)", progpart)[0], str(step), 1)[::-1]
		else:
			progpart = f"[FC ({stepname})] "
		newfile = f"{savepath}\\{progpart}{oldfile}"
		return (newfile)

	def openFile(self, filename):
		print("\t\t", filename)
		if not os.access(filename, os.R_OK):
			self.msgPathNotFound.exec()
			return ()
		with open(filename) as file:
			lines = file.readlines()
		return (lines)

	def	clickBrowseOpenFoder(self):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder or files", self.docpath)
		path = path.replace('/', '\\')
		print(path)
		if not path:
			return (1)
		self.ui.lineOpen.setText(path)
		self.openFromLine(path)

	def openFromLine(self, path = 0):
		# print(path)
		self.filelist.clear()
		if path == 0: path = self.ui.lineOpen.text()
		os.chdir(path)
		if os.path.isfile(path):
			# self.ui.textNew.clear()
			self.filelist.append(path)
			self.filetype = "list"
		elif os.path.isdir(path):
			self.filelist += self.findFilelist(path)
			self.filetype = "list"
		else:
			self.filetype = "err"
			self.msgPathNotFound.exec()

	def findFilelist(self, path):
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
		path = path.replace('/', '\\')
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