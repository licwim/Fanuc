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
	OverGlobalVar = 1

def converter_syntec(lines, step, set_flags):
	global flags, newvars

	flags = setFlags_syntec()
	flags = set_flags
	newvars = {}
	newlines = convert_lines(lines)
	del flags, newvars
	return (newlines)

def convert_lines(lines):
	buflines = []
	newlines = []
	lockvars = []

	newlines.append("%@MACRO")
	if (flags.OverGlobalVar == 1):
		for line in lines:
			checkNum(line, lockvars)
		if lockvars:
			convertNums(lockvars)
	for line in lines:
		line = line.rstrip('\n \t')
		buflines += convert_line(line)
	for line in buflines:
		line = addSemicolon(line)
		if line:
			newlines.append(line)
	newlines.append("%")
	return (newlines)

def convert_line(line):
	newlines = []

	# line = line.replace(' ', '')
	if line == "%": return ([])
	if (flags.OverGlobalVar == 1):
		line = replaceNum(line)
	if ('(' in line):
		line, comment = convertComment(line)
	else: comment = ''
	if re.match(r"IF\s*\[.*\]\s*GOTO", line):
		line = line.replace("GOTO", "THEN GOTO", 1)
	if "IF" in line:
		newlines.append("END_IF")
	line = convertSign(line)
	line = convertOp(line)
	if ('CEIL' in line) or ('FLOOR' in line) or ('ROUND' in line):
		line = convertRounds(line)
	line = convertInt(line)
	newlines.insert(0, line + comment)
	return (newlines)

def convertComment(line):
	comment = re.search(r"\s*\(.*\)", line)
	if not comment:
		return (line, '')
	line = line.replace(comment[0], '')
	comment = comment[0].replace('(', '(*', 1)[:-1] + '*)'
	return (line, comment)

def convertOp(line):
	if ('(*' in line):
		i = line.index('(*')
		comment = line[i:]
		line = line[:i]
	else: comment = ""
	pattern = r"""^FUP[^A-Z]|[^A-Z]FUP[^A-Z]|
				^FIX[^A-Z]|[^A-Z]FIX[^A-Z]|
				^EQ[^A-Z]|[^A-Z]EQ[^A-Z]|
				^GT[^A-Z]|[^A-Z]GT[^A-Z]|
				^GE[^A-Z]|[^A-Z]GE[^A-Z]|
				^LT[^A-Z]|[^A-Z]LT[^A-Z]|
				^LE[^A-Z]|[^A-Z]LE[^A-Z]|
				^NE[^A-Z]|[^A-Z]NE[^A-Z]"""
	# preops = re.findall(r"FUP|FIX|EQ|GT|GE|LT|LE|NE", line)
	# ops = []
	# for op in preops:
	# 	ops += re.findall(fr"[^A-Z]{op}[^A-Z]|^{op}[^A-Z]", line)
	ops = re.findall(pattern, line)
	convert_ops = {
		"FUP": "CEIL",
		"FIX": "FLOOR",
		"EQ": '=',
		"GT": '>',
		"GE": '>=',
		"LT": '<',
		"LE": '<=',
		"NE": '<>'
	}
	newline = ""
	for op in ops:
		if op[0].isupper():
			old = op[:-1]
		else:
			old = op[1:-1]
		i = line.index(op)
		newline += line[:i]
		line = line[i:]
		new = convert_ops.get(old)
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line + comment
	return (newline)

def convertSign(line):
	line = line.replace('[', '(').replace(']', ')')
	line = line.replace('=', ':=')
	return (line)

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
	nums = re.findall(r"#\d+|[A-Z]\d+|\d+\.\d+|\d+\.|\d+", line)
	if not nums: return (line)
	newline = ""

	for num in nums:
		old = num
		i = line.index(old) + len(old)
		if not re.search(r"\D", num):
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
	if line.endswith(';'):
		return (line)
	return (line + ';')

##
##			Numbers
##

def checkNum(line, lockvars):
	if ('(' in line):
		line = line[:line.index('(')]
	nums = re.findall(r"#(\d+)", line)
	lockvars += [int(num) for num in nums if int(num) in range(200, 800)]

def convertNums(lockvars):
	lockvars = list(set(lockvars))
	lockvars.sort()
	changevars = [num for num in lockvars if num >= 500]
	lockvars = [num for num in lockvars if num < 500]
	for num in changevars:
		newnum = num - 300
		while (newnum in lockvars):
			newnum += 1
		lockvars.append(newnum)
		newvars.update({num: newnum})

def replaceNum(line):
	nums = re.findall(r"#(\d+)", line)
	if not nums: return (line)
	newline = ""
	nums = [int(num) for num in nums if int(num) >= 500]
	for num in nums:
		old = '#' + str(num)
		if num in newvars:
			new = '#' + str(newvars.get(num))
		else:
			new = '#' + str(num - 300)
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line
	return (newline)
