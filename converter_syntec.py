# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_syntec.py                             #
#       By: licwim                                  #
#                                                   #
#   Created: 18-01-2020 23:15:18 by licwim          #
#   Updated: 18-01-2020 23:20:40 by licwim          #
#                                                   #
# ************************************************* #

import re

class setFlags_syntec():
	set_1 = 0
	set_2 = 0
	set_3 = 0
	set_4 = 0

def converter_syntec(lines, step, set_flags):
	global flags

	flags = setFlags_syntec()
	flags = set_flags
	newlines = convert_lines(lines)
	return (newlines)

def convert_lines(lines):
	newlines = []

	newlines.append("%@MACRO")
	for line in lines:
		line = line.rstrip('\n \t')
		newlines += convert_one_line(line)
	return (newlines)

def convert_one_line(line):
	newlines = []

	# line = line.replace(' ', '')
	if re.match(r"IF\s*\[.*\]\s*GOTO", line):
		line = line.replace("GOTO", "THEN GOTO", 1)
	if "IF" in line:
		newlines.append("END_IF")
	line = line.replace('(', '(*').replace(')', '*)')
	line = line.replace('[', '(').replace(']', ')')
	line = line.replace("FUP", "CEIL")
	line = line.replace("FIX", "FLOOR")
	line = line.replace('=', ':=')
	line = line.replace("EQ", '=')
	line = line.replace("GT", '>')
	line = line.replace("GE", '>=')
	line = line.replace("LT", '<')
	line = line.replace("LE", '<=')
	line = line.replace("NE", '<>')
	newlines.insert(0, line)
	return (newlines)