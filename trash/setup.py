from cx_Freeze import setup, Executable

executables = [Executable("main.py", targetName = 'converter.exe')]

setup(
	name = "converter",
	version = "0.0.1",
	description = "Fanuc to NC Converter",
	executables = executables
)