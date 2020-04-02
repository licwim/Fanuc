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
	buflines = []
	newlines = []

	newlines.append("%@MACRO")
	for line in lines:
		line = line.rstrip('\n \t')
		buflines += convert_one_line(line)
	for line in buflines:
		line = line.rstrip('/t/n ')
		line = addSemicolon(line)
		newlines.append(line)
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
	if ('CEIL' in line) or ('FLOOR' in line) or ('ROUND' in line):
		line = convertRounds(line)
	line = convertInt(line)
	newlines.insert(0, line)
	return (newlines)

##
##			Rounds
##

def convertRounds(line):
	newline = ""
	rounds = findRounds(line)

	for round_ in rounds:
		old = round_
		i = line.index(old) + len(old)
		if not re.match(r"\s*\*\s*1.", line[i:]):
			new = round_ + '*1.'
			line = line.replace(old, new, 1)
			i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line
	return (newline)

def findRounds(line):
	bufrounds = []
	rounds = re.findall(r"CEIL\s*[#-\(]|FLOOR\s*[#-\(]|ROUND\s*[#-\(]", line)

	for round_ in rounds:
		line_slice = line[line.index(round_):]
		bufrounds.append(findOneRound(line_slice))
	return (bufrounds)

def findOneRound(line, sign=0):
	op = re.findall(r"^[A-Z]+\s*([^A-Z])", line)[0]
	op_word = re.findall(r"(^[A-Z]+\s*)[^A-Z]", line)[0]

	if (op == '#'):
		round_ = re.findall(r"^[A-Z]+\s*#\d+", line)[0]
	elif (op == '('):
		i = len(op_word) + 1
		while line.count('(', 0, i) != line.count(')', 0, i): i += 1
		round_ = line[:i]
	elif (op == '-'):
		line = line.replace('-', '', 1)
		round_ = findOneRound(line, 1)
	if (sign == 1):
		return (round_.replace(op_word, op_word + '-', 1))
	return (round_)

##
##			Integers
##

def convertInt(line):
	nums = re.findall(r"#\d+|\d+\.\d+|\d+\.|\d+", line)
	if not nums: return (line)
	newline = ""

	for num in nums:
		old = num
		i = line.index(old) + len(old)
		if not ('#' in num or '.' in num):
			new = num + '.'
			line = line.replace(old, new, 1)
			i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line
	return (newline)

##
##			Semicolon
##

def addSemicolon(line):
	if ('(*' in line and '*)' in line) or \
		(line.endswith(';')) or \
		(line == "%"):
		return (line)
	return (line + ';')