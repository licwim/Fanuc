# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_nc.py                                 #
#       By: licwim                                  #
#                                                   #
#   Created: 18-01-2020 20:42:55 by licwim          #
#   Updated: 18-01-2020 23:15:36 by licwim          #
#                                                   #
# ************************************************* #

import re

# freevars = []
# maxN = 0

class setFlags_nc():
	LocalVar = 1
	GlobalVar = 1
	OverGlobalVar = 1
	If = 1
	Fup = 1
	Null = "0.000001"
	Gt = "0.000001"

def converter_nc(lines, step, set_flags):
	global maxN, freevars, flags

	flags = setFlags_nc()
	flags = set_flags
	if (flags.GlobalVar): freevars = list(range(60,1000))
	else: freevars = list(range(100,1000))
	maxN = 0
	# print(flags.LocalVar, flags.GlobalVar, flags.If, flags.Fup)
	if step == 1: newlines = convertStep1(lines)
	elif step == 2: newlines = convertStep2(lines)
	else: newlines = convertStep2(convertStep1(lines))
	del maxN, freevars, flags
	return (newlines)

def convertStep1(lines):
	# print("STEP 1")

	global freevars
	newlines = []
	buflines = []
	lockvars = []

	i = 1
	for line in lines:
		checkN(line)
		checkNum(line, lockvars)
	# print(f"FREEVARS: {freevars}")
	newvars = convertNums(lockvars)
	for line in lines:
		# print('NEW LINE: %s' % line)
		# print('LINE: %d' % i)
		line = replaceNum(line, newvars)
		line = splitComments(line)
		# line = clearSpace(line)
		buflines.extend(line)
		i += 1
	i = 1
	freevars.sort()
	freevars = tuple(freevars[:20])
	for line in buflines:
		# print('NEW LINE: %s' % line)
		# print('LINE: %d' % i)
		lines = convertLine1(line)
		lines = clearSpace(lines)
		newlines.extend(lines)
		i += 1
	return (newlines)

def convertStep2(lines):
	# print("STEP 2")

	newlines = []

	i = 1
	lines = clearSpace(lines)
	for line in lines:
		# print('NEW LINE: %s' % line)
		# print('LINE: %d' % i)
		line = convertLine2(line)
		newlines += [line]
		i += 1
	return (newlines)

##
##			Other
##

def clearSpace(lines):
	newlines = []
	for line in lines:
		line = line.strip(' \n')
		if line:
			# line = convertLine2(line)
			newlines += [line]
	return (newlines)

def splitComments(line):
	lines = [line]
	if '(' in line and ')' in line:
		if line.lstrip('; \t')[0] == '(':
			lines = [';' + line.lstrip('; \t')]
		else:
			newline = line.partition('(')
			lines = [';' + newline[1] + newline[2], newline[0]]
		if lines[0][2:].startswith("DIS,"):
			lines[0] = lines[0][1:]
	return (lines)

def checkN(line):
	global maxN

	find = re.match(r"N\d+", line)
	# print(find.group(0))
	if find and int(find.group(0)[1:]) > maxN:
		maxN = int(find.group(0)[1:])

##
##			Lines
##

def convertLine1(line):
	global freevars, flags
	newlines = []
	tempvars = list(freevars)
	if '(' in line: return ([line])
	line = line.replace(' ', '')
	buflines = [line]
	if (re.search(r"[^A-Z][A-Z][\[#]|^[A-Z][\[#]|[^A-Z][A-Z]-[\[#]|^[A-Z]-[\[#]", line)):
		buflines = convertCoords(line, tempvars)
	if (flags.If and line.startswith("IF") and '[' in line):
		buflines = convertIf(line, tempvars)
	newlines = convertLine1_5(buflines, tempvars, 0)
	return (newlines)

def convertLine1_5(lines, tempvars, i):
	newlines = []

	for line in lines:
		checklist = {
			convertFup : flags.Fup and "FUP" in line,
			convertFix : "FIX" in line,
			convertGt : "GT0" in line # re.search(r"GT0\.?\D", line)
		}
		act = list(checklist.keys())[i]
		if checklist.get(act):
			newlines += act(line, tempvars)
		else:
			newlines += [line]
	i += 1
	if (i == len(checklist)):
		return (newlines)
	else:
		return (convertLine1_5(newlines, tempvars, i))

def convertLine2(line):
	global flags

	if '(' in line:
		return (line)
	if re.match(r"N\d+", line):
		N = re.search(r"N\d+", line)[0]
		line = '"%s"%s' % (N, line[line.index(N) + len(N):])
	if line.startswith("GOTO"):
		N = re.search(r"\d+", line[4:])[0]
		line = '(BNC,N%s)%s' % (N, line[line.index(N) + len(N):])
	if flags.If and line.startswith("IF"):
		# print("LINE:",line)
		N = line[line.index("GOTO") + 4:]
		# print("N: %s" % N)
		block = re.search(r"\[.+\]", line[:line.index("GOTO")])[0]
		# print("BLOCK: %s" % block)
		op = re.search(r"[A-Z]+", block)[0]
		var1 = block[1:block.index(op)]
		var2 = block[block.index(op) + len(op):-1]
		# print(op, var1, var2)
		line = f'(B{op},{var1},{var2},N{N})'
		# print (line)
	line = line.replace("FIX", "INT")
	line = line.replace("SQRT", "SQR")
	line = line.replace("ATAN", "ART")
	line = line.replace('[', '(').replace(']', ')')
	line = line.replace('#', 'E')
	return (line)

##
##			Numbers
##

def checkNum(line, lockvars):
	global freevars

	if ('(' in line):
		line = line[:line.index('(')]
	nums = re.findall(r"#(\d+)", line)
	nums = list(set(nums))
	for num in nums:
		num = int(num)
		if num in range(100, 140) and num not in lockvars: lockvars.append(num)
		if num in range(500, 800) and num not in lockvars: lockvars.append(num)
		if num in freevars: freevars.remove(num)
		# elif num in range(60, 100) and num in freevars: freevars.remove(num)
		# elif num >= 140 and num - 40 in freevars: freevars.remove(num - 40)

def convertNums(lockvars):
	global freevars, flags
	newvars = dict()

	if (flags.GlobalVar == 0 and flags.OverGlobalVar == 0): return (newvars)
	lockvars.sort()
	for num in lockvars:
		if (num in range(100, 140)): newnum = num - 40
		if (num in range(500, 800)): newnum = num - 300
		while newnum not in freevars:
			newnum += 1
		freevars.remove(newnum)
		freevars.append(num)
		newvars.update({'#' + str(num): '#' + str(newnum)})
	return (newvars)

def replaceNum(line, newvars):
	newline = ""

	nums = re.findall(r"#\d+", line)
	for num in nums:
		if num in newvars:
			newnum = newvars.get(num)
		else:
			if '(' in line and line.find('(') < line.find(num): comment = 1
			else: comment = 0
			newnum = opNum(num, comment)
		line = line.replace(num, newnum, 1)
		i = line.index(newnum) + len(newnum)
		newline += line[:i]
		line = line[i:]
	newline += line
	return (newline)

def opNum(num, comment):
	global freevars, flags
	num = int(num[1:])
	n = num

	if (flags.GlobalVar and n >= 100):
		n -= 40
		if (n in freevars and not comment):
			freevars.remove(n)
			freevars.append(num)
	elif (flags.LocalVar and n in range(1, 27)):
		n += 30
	elif (flags.OverGlobalVar and n >= 500):
		n -= 300
		if (n in freevars and not comment):
			freevars.remove(n)
			freevars.append(num)
	elif (n == 0):
		return (flags.Null)
	return (f"#{n}")

##
##			Coords
##

def convertCoords(line, tempvars):
	firstlines = []
	secondline = line

	bufcoords = findCoords(line)
	# print("BUFF: %s" % bufcoords)
	# print("TEMP:", tempvars)
	for coord in bufcoords:
		secondline = secondline.replace(coord, convertOneCoord(coord, tempvars, firstlines))
	# print(firstlines + secondline, '\n')
	return (firstlines + [secondline])

def convertOneCoord(coord, tempvars, firstlines):
	freevar = tempvars.pop(0)
	# print(tempvars)

	if (coord[1] == '#'): return (coord)
	firstlines.append(f"#{freevar}={coord[1:]}")
	return (f"{coord[0]}#{freevar}")

def findCoords(line):
	bufcoords = []

	# print(line)
	line = '!' + line
	coords = re.findall(r"[^A-Z]([A-Z][#\[-])", line)
	for coord in coords:
		# print(coord, line)
		line = line[line.index(coord):]
		coord = findOneCoord(line)
		bufcoords += [coord]
		# print(coord)
		line = line[len(coord):]
	return (bufcoords)

def findOneCoord(line, sign = 0):
	op = line[1]

	# print("IN", line)
	if (op == '#'):
		coord = re.findall(r"[A-Z]#\d+", line)[0]
	elif (op == '['):
		i = 2
		while line.count('[', 0, i) != line.count(']', 0, i): i += 1
		coord = line[:i]
	elif (op == '-'):
		line = line.replace('-', '', 1)
		coord = findOneCoord(line, 1)
	if (sign == 1): return (coord[0] + '-' + coord[1:])
	else: return (coord)

##
##			IF
##

def convertIf(line, tempvars):
	blocks = []

	if "AND" in line or "OR" in line:
		if "AND" in line: tmp = line.split("AND")
		else: tmp = line.split("OR")
		blocks.append(re.findall(r"\[(.+)", tmp[0])[0])
		blocks.append(''.join(re.findall(r"(.+)\].*THEN|(.+)\].*GOTO", tmp[1])[0]))
	else: blocks.append(''.join(re.findall(r"(\[.+\]).*THEN|(\[.+\]).*GOTO", line)[0]))
	# print("BLOCKS:", blocks)
	if "THEN" in line:
		blocks.append(re.findall(r"THEN(.+)", line)[0])
		# print("\t\t\t\tTHEN:", re.findall(r"THEN(.+)", line)[0])
	else: blocks.append(re.findall(r"GOTO.+", line)[0])
	if "AND" in line: newlines = opAndIf(blocks, tempvars)
	elif "OR" in line: newlines = opOrIf(blocks, tempvars)
	else: newlines = opNoIf(blocks, tempvars)
	return (newlines)

def opNoIf(blocks, tempvars):
	global maxN
	freeN = maxN + 1
	exitN = freeN + len(blocks) - 1
	newlines = []

	if re.search(r"[^#\[\]\.\w]", blocks[0]): block = partIf(blocks[0], newlines, tempvars)
	else: block = 0
	if "GOTO" in blocks[-1]:
		if block: newlines.append("IF%s" % block + blocks[-1])
		else: newlines.append("IF%s" % ''.join(blocks))
		return (newlines)
	if block: newlines.append("IF%sGOTO%d" % (block, freeN))
	else: newlines.append("IF%sGOTO%d" % (blocks[0], freeN))
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	maxN = exitN
	# print("BLOCK:", blocks)
	return (newlines)

def opAndIf(blocks, tempvars):
	global maxN
	freeN = maxN + 1
	newlines = []

	if ("GOTO" in blocks[-1]): exitN = freeN + len(blocks) - 2
	else: exitN = freeN + len(blocks) - 1
	for block in blocks[:-1]:
		# print("BLOCK:", block)
		if re.search(r"[^#\[\]\.\w]", block): block = partIf(block, newlines, tempvars)
		if (freeN == exitN):
			newlines.append("IF%s%s" % (block, blocks[-1]))
			break
		newlines.append("IF%sGOTO%d" % (block, freeN))
		newlines.append("GOTO%d" % exitN)
		newlines.append("N%d" % freeN)
		freeN += 1
	if not ("GOTO" in blocks[-1]):
		newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("AND: ", newlines)
	maxN = exitN
	return (newlines)

def opOrIf(blocks, tempvars):
	global maxN
	freeN = maxN + 1
	newlines = []

	exitN = freeN + 1
	for block in blocks[:-1]:
		if re.search(r"[^#\[\]\.\w]", block): block = partIf(block, newlines, tempvars)
		if ("GOTO" in blocks[-1]): newlines.append("IF%s%s" % (block, blocks[-1]))
		else: newlines.append("IF%sGOTO%d" % (block, freeN))
	if ("GOTO" in blocks[-1]):
		return (newlines)
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("OR: ",newlines)
	maxN = exitN
	return (newlines)

def partIf(block, newlines, tempvars):
	i = 0

	compop = re.findall(r"[A-Z]+", block)
	# print(f"ALL: {compop}")
	while (compop[i] in ["FUP", "FIX", "START"]): i += 1
	compop = compop[i]
	# print(f"OP: {compop}")
	block = block[1:-1].partition(compop)
	if re.search(r"[^#\[\]\.\w]", block[0]):
		freevar1 = f"#{tempvars.pop(0)}"
		newlines.append(f"{freevar1}={block[0]}")
	else: freevar1 = block[0]
	if re.search(r"[^#\[\]\.\w]", block[2]):
		freevar2 = f"#{tempvars.pop(0)}"
		newlines.append(f"{freevar2}={block[2]}")
	else: freevar2 = block[2]
	block = f"[{freevar1}{compop}{freevar2}]"
	return (block)

##
##			FUP
##

def convertFup(line, tempvars):
	firstlines = []
	secondline = ""
	blocks = []

	bufblocks = re.findall(r"FUP(\[.*)", line)
	if not bufblocks: return ([line])
	for block in bufblocks:
		i = 1
		while block.count('[', 0, i) != block.count(']', 0, i): i += 1
		blocks += [block[1:i - 1]]

	for block in blocks:
		old = f"FUP[{block}]"
		new = f"#{convertOneFup(block, firstlines, tempvars)}"
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		secondline += line[:i]
		line = line[i:]
	secondline += line
	return (firstlines + [secondline])

def convertOneFup(block, newlines, tempvars):
	global maxN
	freeN = maxN + 1
	exitN = freeN + 1
	maxN = exitN
	freevar1 = tempvars.pop(0)
	freevar2 = tempvars.pop(0)
	freevar3 = tempvars.pop(0)

	newlines += [
		f"#{freevar1}={block}",
		f"#{freevar2}=FIX[#{freevar1}]",
		f"#{freevar3}=#{freevar1}-#{freevar2}",
		f"IF[#{freevar3}GE0.001]GOTO{freeN}",
		f"GOTO{exitN}",
		f"N{freeN}",
		f"#{freevar1}=#{freevar2}+1",
		f"N{exitN}"
	]
	# print(newlines)
	return (freevar1)

def convertFix(line, tempvars):
	firstlines = []
	secondline = ""
	blocks = []

	bufblocks = re.findall(r"FIX(\[.*)", line)
	if not bufblocks: return ([line])
	for block in bufblocks:
		i = 1
		while block.count('[', 0, i) != block.count(']', 0, i): i += 1
		blocks += [block[1:i - 1]]
	# print (blocks)
	for block in blocks:
		if not re.search(r"[^#\[\]\.\w]", block): continue
		freevar = tempvars.pop(0)
		firstlines.append(f"#{freevar}={block}")
		old = f"FIX[{block}]"
		new = f"FIX[#{freevar}]"
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		secondline += line[:i]
		line = line[i:]
	secondline += line
	return (firstlines + [secondline])

def convertGt(line, tempvars):
	global flags
	newline = ""

	if ("GT0." in line):
		blocks = re.findall(r"[^A-Z](GT0\.)\D", line)
	else:
		blocks = re.findall(r"[^A-Z](GT0)\D", line)
	for block in blocks:
		old = block
		new = f"GT{flags.Gt}"
		line = line.replace(old, new, 1)
		i = line.index(new) + len(new)
		newline += line[:i]
		line = line[i:]
	newline += line
	return ([newline])


#############
	#############
	#############		SQRT -> SQR
	#############		ATAN -> ART
#############