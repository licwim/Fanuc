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
	blocks = []
	newline = ""
	if "IF" in line:
		blocks.append(re.findall(r"^IF\s*\((.*)\)\s*", line[:line.index("THEN")])[0])
	if ':=' in line:
		blocks.append(re.findall(r":=\s*(.*)$", line)[0])
	for block in blocks:
		old = block
		new = convertBlockRound(block)
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line
	return (newline)

def convertBlockRound(block):
	if block.count("CEIL") + block.count("FLOOR") + block.count("ROUND") > 1:
		block = convertSomeRounds(block)
	else:
		block = convertOneRound(block)
	return (block)

def convertSomeRounds(block):
	block = block.rstrip('\t ')
	i = block.find('(') + 1
	while block.count('(', 0, i) != block.count(')', 0, i): i += 1
	if block[i:].replace(' ', '') == "*1.":
		return (block)
	if i < len(block):
		return (f"({block})*1.")
	else:
		return (f"{block}*1.")

def convertOneRound(block):
	rounds = re.findall(r"CEIL\s*[#\(]|FLOOR\s*[#\(]|ROUND\s*[#\(]", block)
	if not rounds:
		return (block)
	op = rounds[0][-1]
	op_word = rounds[0][:-1]
	block_slice = block[block.index(op_word):]

	if (op == '#'):
		round_block = re.findall(r"^[A-Z]+\s*#\d+", block_slice)[0]
	elif (op == '('):
		i = len(op_word) + 1
		while block_slice.count('(', 0, i) != block_slice.count(')', 0, i): i += 1
		round_block = block_slice[:i]
	i = block.index(round_block) + len(round_block)
	if not re.match(r"\s*\*\s*1.", block[i:]):
		block.replace(round_block, round_block + "*1.")
	return (block)


##
##			Integers
##

def convertInt(line):
	nums = re.findall(r"#\d+|N\d+|\d+\.\d+|\d+\.|\d+", line)
	if not nums: return (line)
	newline = ""

	for num in nums:
		old = num
		i = line.index(old) + len(old)
		if not ('#' in num or 'N' in num or '.' in num):
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
	if '(*' in line and '*)' in line:
		if re.search(r";\s*\(\*", line):
			return (line)
		end = re.findall(r"\s*\(\*", line)[0]
		i = line.index(end)
		line = list(line)
		line.insert(i, ';')
		return (''.join(line))
	if (line.endswith(';')) or \
		(line == "%"):
		return (line)
	return (line + ';')