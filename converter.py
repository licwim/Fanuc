# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter.py                                    #
#       By: licwim                                  #
#                                                   #
#   Created: 06-01-2020 15:16:36 by licwim          #
#   Updated: 13-01-2020 12:01:15 by licwim          #
#                                                   #
# ************************************************* #

import re

freevars = []
maxN = 0

def converter(lines, step):
	global maxN
	global freevars
	freevars = list(range(60,256))
	maxN = 0

	if step == 1: newlines = convertStep1(lines)
	elif step == 2: newlines = convertStep2(lines)
	else: newlines = convertStep2(convertStep1(lines))
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
		line = clearSpace(line)
		buflines.extend(line)
		i += 1
	i = 1
	freevars = tuple(freevars[:10])
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

def clearSpace(lines):
	newlines = []
	for line in lines:
		line = line.strip(' \n')
		if line:
			# line = convertLine2(line)
			newlines += [line]
	return (newlines)

##
##			Other
##

def splitComments(line):
	lines = [line]
	if '(' in line and ')' in line:
		newline = line.partition('(')
		lines = [';' + newline[1] + newline[2], newline[0]]
		# lines[0] = lines[0].strip(' \n')
		# lines[1] = lines[1].strip(' \n')
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
	global freevars
	buflines = [line]
	newlines = []
	tempvars = list(freevars)
	if '(' in line: return ([line])
	if re.search(r"[^A-Z][A-Z][\[#]|^[A-Z][\[#]|[^A-Z][A-Z]-[\[#]|^[A-Z]-[\[#]", line.replace(' ', '')):
		buflines = convertCoords(line, tempvars)
	if line.startswith("IF") and '[' in line:
		buflines = convertIf(line, tempvars)
	for line in buflines:
		if "FUP" in line: newlines.extend(convertFup(line, tempvars))
		else: newlines.append(line)
	return (newlines)

def convertLine2(line):
	if re.match(r"N\d+", line):
		N = re.search(r"N\d+", line)[0]
		line = '"%s"%s' % (N, line[line.index(N) + len(N):])
	if line.startswith("GOTO"):
		N = re.search(r"\d+", line.replace(' ', '')[4:])[0]
		line = '(BNC,"N%s")%s' % (N, line[line.index(N) + len(N):])
	if line.startswith("IF"):
		# print("LINE:",line)
		N = line[line.index("GOTO") + 4:]
		# print("N: %s" % N)
		block = re.search(r"\[.+\]", line[:line.index("GOTO")])[0]
		# print("BLOCK: %s" % block)
		op = re.search(r"[A-Z]+", block)[0]
		var1 = block[1:block.index(op)]
		var2 = block[block.index(op) + len(op):-1]
		# print(op, var1, var2)
		line = f'(B{op},{var1},{var2},"N{N}")'
		# print (line)
	line = line.replace("FIX", "INT")
	line = line.replace('[', '(').replace(']', ')')
	line = line.replace('#', 'E')
	return (line)

##
##			Numbers
##

def checkNum(line, lockvars):
	global freevars

	nums = re.findall(r"#(\d+)", line)
	nums = list(set(nums))
	for num in nums:
		num = int(num)
		if num in range(100, 140) and num not in lockvars: lockvars.append(num)
		elif num in range(60, 100) and num in freevars: freevars.remove(num)
		elif num >= 140 and num - 40 in freevars: freevars.remove(num - 40)

def convertNums(lockvars):
	global freevars
	newvars = dict()

	lockvars.sort()
	for num in lockvars:
		newnum = opNum(num)
		while newnum not in freevars:
			newnum += 1
		freevars.remove(newnum)
		newvars.update({'#' + str(num): '#' + str(newnum)})
	return (newvars)

def replaceNum(line, newvars):

	nums = re.findall(r"#\d+", line)
	nums = list(set(nums))
	for num in nums:
		if num in newvars:
			line = line.replace(num, newvars.get(num))
		else:
			if num == '#0': line = line.replace(num, "0.000001")
			else: line = line.replace(num, f"#{opNum(num)}")
	return (line)

def opNum(n):
	n = str(n)
	if n[0] == '#': n = int(n[1:])
	else: n = int(n)

	if n >= 100:
		n -= 40
	elif n in range(1, 27):
		n += 30
	return (n)

##
##			Coords
##

def convertCoords(line, tempvars):
	firstline = []
	secondline = line

	bufcoords = findCoords(line)
	# print("BUFF: %s" % bufcoords)
	# print("TEMP:", tempvars)
	for coord in bufcoords:
		secondline = secondline.replace(coord, convertOneCoord(coord, tempvars, firstline))
	# print(firstline + secondline, '\n')
	return (firstline + [secondline])

def convertOneCoord(coord, tempvars, firstline):
	freevar = tempvars.pop(0)
	# print(tempvars)

	if (coord[1] == '#'): return (coord)
	firstline.append(f"#{freevar}={coord[1:]}")
	return (f"{coord[0]}#{freevar}")

def findCoords(line):
	bufcoords = []

	print(line)
	line = '!' + line.replace(' ', '')
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
		while line.count('[', 0, i) != line.count(']', 0, i):
			i += 1
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

	if re.search(r"[^#\[\]\.\w]+", blocks[0]): block = partIf(blocks[0], newlines, tempvars)
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

	exitN = freeN + len(blocks) - 1
	for block in blocks[:-1]:
		# print("BLOCK:", block)
		if re.search(r"[^#\[\]\.\w]+", block): block = partIf(block, newlines, tempvars)
		newlines.append("IF%sGOTO%d" % (block, freeN))
		newlines.append("GOTO%d" % exitN)
		newlines.append("N%d" % freeN)
		freeN += 1
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
		if re.search(r"[^#\[\]\.\w]+", block): block = partIf(block, newlines, tempvars)
		newlines.append("IF%sGOTO%d" % (block, freeN))
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("OR: ",newlines)
	maxN = exitN
	return (newlines)

def partIf(block, newlines, tempvars):
	freevar1 = tempvars.pop(0)
	freevar2 = tempvars.pop(0)
	compop = re.search(r"[A-Z]+", block)[0]
	block = block.partition(compop)
	newlines.append(f"#{freevar1}={block[0][1:]}")
	newlines.append(f"#{freevar2}={block[2][:-1]}")
	block = f"[#{freevar1}{compop}#{freevar2}]"
	return (block)


##
##			FUP
##

def convertFup(line, tempvars):
	global maxN
	freeN = maxN + 1
	freevar1 = tempvars.pop(0)
	freevar2 = tempvars.pop(0)
	newlines = []

	var = line[:line.index('=')]
	math = line[line.index("FUP") + 4:-1]
	newlines.append("#%d=%s" % (freevar1, math))
	newlines.append("#%d=FIX[#%d]" % (freevar2, freevar1))
	newlines.append("IF[#%d-#%dGE0.001]GOTO%d" % (freevar1, freevar2, freeN))
	newlines.extend(["GOTO%d" % (freeN + 1), "N%d" % freeN])
	newlines.append("#%d=#%d+1" % (freevar1, freevar2))
	newlines.extend(["N%d" % (freeN + 1), "%s=#%d" % (var, freevar1)])
	# print(newlines)
	return (newlines)
