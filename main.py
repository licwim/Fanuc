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
import json
from PyQt5 import QtCore, QtWidgets

from design import Ui_MainWindow
from converter_nc import converter_nc, setFlags
from converter_syntec import converter_syntec

src = ''
dst = ''

class mywindow(QtWidgets.QMainWindow):
	filetype = "list"
	filelist = []

	srcpath = ""
	dstpath = ""

	# msgPathNotFound = ''
	# msgConvertError = ''
	# msgConvertDone = ''

	# flags:	0 - Local vars
	# 			1 - Global vars
	# 			2 - If
	# 			3 - Fup
	# 			4 - #0

	# flags_nc = ["0.000001", 1, 1, 1, 1, 1]
	flags_nc = setFlags()
	lang = "nc"

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.initDirs()
		self.ui.lineOpen.setText(self.srcpath)
		self.ui.lineSave.setText(self.dstpath)
		self.ui.btnConvert1.clicked.connect(self.clickConvert1)
		self.ui.btnConvert2.clicked.connect(self.clickConvert2)
		self.ui.btnConvert12.clicked.connect(self.clickConvert12)
		self.ui.btnBrowseOpenFolder.clicked.connect(self.clickBrowseOpenFoder)
		self.ui.btnBrowseSave.clicked.connect(self.clickBrowseSaveFolder)
		self.ui.lineOpen.returnPressed.connect(self.openFromLine)
		self.ui.set_nc_LocalVar.stateChanged.connect(self.setLocalVar)
		self.ui.set_nc_GlobalVar.stateChanged.connect(self.setGlobalVar)
		self.ui.set_nc_OverGlobalVar.stateChanged.connect(self.setOverGlobalVar)
		self.ui.set_nc_If.stateChanged.connect(self.setIf)
		self.ui.set_nc_Fup.stateChanged.connect(self.setFup)
		self.ui.rbtnNc.clicked.connect(self.setNc)
		self.ui.rbtnSyntec.clicked.connect(self.setSyntec)
		# self.msgBoxes()

	def test(self, state):
		print("TEST", state)

	def initDirs(self):
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
						"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders",
						0, winreg.KEY_ALL_ACCESS)
		docpath = winreg.QueryValueEx(key, "Personal")[0]
		if "%USERPROFILE%" in docpath: docpath = docpath.replace("%USERPROFILE%", os.environ["USERPROFILE"])
		temppath = os.environ["TEMP"]
		tempfile = f"{temppath}\\fanuc_convertor_dirs.json"
		if not os.access(tempfile, os.R_OK):
			self.srcpath = docpath
			self.dstpath = docpath + "\\Fanuc Converter Files"
		else:
			with open(tempfile, "r") as file:
				data = json.load(file)
			print(data)
			self.srcpath = data.get("srcpath")
			self.dstpath = data.get("dstpath")
			self.openFromLine(self.srcpath)

	def updateTemp(self):
		temppath = os.environ["TEMP"]
		tempfile = f"{temppath}\\fanuc_convertor_dirs.json"
		data = {
			"srcpath" : self.srcpath,
			"dstpath" : self.dstpath
		}
		with open(tempfile, "w") as file:
			json.dump(data, file)

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
		if state == QtCore.Qt.Checked: self.flags_nc.LocalVar = 1
		else: self.flags_nc.LocalVar = 0

	def setGlobalVar(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc.GlobalVar = 1
		else: self.flags_nc.GlobalVar = 0

	def setOverGlobalVar(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc.OverGlobalVar = 1
		else: self.flags_nc.OverGlobalVar = 0

	def setIf(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc.If = 1
		else: self.flags_nc.If = 0

	def setFup(self, state):
		if state == QtCore.Qt.Checked: self.flags_nc.Fup = 1
		else: self.flags_nc.Fup = 0

	def clickConvert1(self):
		self.clickConvert(1)

	def clickConvert2(self):
		self.clickConvert(2)

	def clickConvert12(self):
		self.clickConvert(12)

	def clickConvert(self, step):

		self.checkLines()

		if self.filetype == "list":
			filelist = self.filelist
			lines = []
			for file in filelist:
				lines = converter_nc(self.openFile(file), step, self.flags_nc)
				# try:
				# 	if (self.lang == "nc"): lines = converter_nc(self.openFile(file), step, self.flags_nc)
				# 	elif (self.lang == "syntec"): lines = converter_syntec(self.openFile(file), step, self.flags_syntec)
				# 	else:
				# 		self.msgConvertError.exec()
				# 		break
				# except: 
				# 	self.msgConvertError.exec()
				# 	break
				if not lines: break
				newfile = open(self.newFilename(step, file), "w")
				newfile.write('\n'.join(lines))
				newfile.close()
			if lines: self.ui.msgConvertDone.exec()
		else: self.ui.msgConvertError.exec()

	def checkLines(self):

		n = self.ui.set_nc_Null.text()
		if n: self.flags_nc.Null = n
		else: self.flags_nc.Null = "0.000001"

		n = self.ui.set_nc_Gt.text()
		if n: self.flags_nc.Gt = n
		else: self.flags_nc.Gt = "0.000001"

		self.dstpath = self.ui.lineSave.text()
		if not os.path.exists(self.dstpath):
			os.mkdir(self.dstpath)
		self.updateTemp()

	def newFilename(self, step, oldfile):
		dstpath = self.dstpath

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
		newfile = f"{dstpath}\\{progpart}{oldfile}"
		return (newfile)

	def openFile(self, filename):
		print("\t\t", filename)
		if not os.access(filename, os.R_OK):
			self.ui.msgPathNotFound.exec()
			return ()
		with open(filename) as file:
			lines = file.readlines()
		return (lines)

	def	clickBrowseOpenFoder(self):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", self.srcpath)
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
		if not os.path.isdir(path):
			self.filetype = "err"
			self.ui.msgPathNotFound.exec()
			return (1)
		os.chdir(path)
		self.srcpath = path
		self.updateTemp()
		self.filelist += self.findFilelist(path)
		self.filetype = "list"

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
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", self.dstpath)
		path = path.replace('/', '\\')
		if not path:
			return (1)
		self.ui.lineSave.setText(path)
		self.dstpath = path
		self.updateTemp()

def main():
	app = QtWidgets.QApplication([])
	window = mywindow()
	window.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
