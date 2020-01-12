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
#   Created: 05-01-2020 18:23:20 by licwim          #
#   Updated: 05-01-2020 20:18:31 by licwim          #
#                                                   #
# ************************************************* #

import re

tempvars = []
maxN = 0

def converter(lines, step):
	global maxN
	global tempvars
	tempvars = list(range(1,255))
	maxN = 0

	if step == 1: newlines = convertStep1(lines)
	elif step == 2: newlines = convertStep2(lines)
	else: newlines = convertStep2(convertStep1(lines))
	return (newlines)

def convertStep1(lines):
	# print("STEP 1")

	global tempvars
	newlines = []
	buflines = []

	i = 1
	for line in lines:
		# print('NEW LINE: %s' % line)
		# print('LINE: %d' % i)
		line = convertNum(line)
		checkN(line)
		line = checkComments(line)
		line = clearSpace(line)
		buflines.extend(line)
		i += 1
	i = 1
	tempvars = tuple(tempvars[:10])
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
			line = line.replace("INT", "FIX")
			newlines += [line]
	return (newlines)

##
##			Checks comments and N
##

def checkComments(line):
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
	global tempvars
	buflines = [line]
	newlines = []
	varlist = list(tempvars)
	line = line.replace("FIX", "INT")
	if re.search(r"[XYZ][\[#]", line.replace(' ', '')): buflines = convertCoords(line, varlist)
	if line.startswith("IF") and '[' in line: buflines = convertIf(line, varlist)
	for line in buflines:
		if "FUP" in line: newlines.extend(convertFup(line, varlist))
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

def convertNum(line):
	newline = []
	i = 0

	if not re.search(r"#\d", line):
		return (line)
	while i < len(line):
		j = i
		i = line.find('#',j)
		# print(i, line[i:])
		if i < 0:
			newline.append(line[j:])
			break
		newline.append(line[j:i])
		i += 1
		num = []
		while i < len(line) and line[i].isdigit():
			num.append(line[i])
			i += 1
		# print("NUM: ", num)
		newline.append(work_with_numbers(num))
	# print(''.join(newline))
	return (''.join(newline))

def work_with_numbers(num):
	global tempvars
	n = int(''.join(num))

	num.clear()
	num.append('#')
	# if n > 99:
	# 	n -= 40
	# elif n > 0 and n < 27:
	# 	n += 30
	if n == 0:
		n = 999999
		num.pop()
	num.append(str(n))
	if n in tempvars: tempvars.remove(n)
	return (''.join(num))

##
##			Coords
##

def convertCoords(line, varlist):
	firstline = []
	secondline = [re.match(r"[^XYZ]*", line)[0]]

	buflines = re.findall(r"[XYZ][^XYZ]*", line)
	# print("BUFF: %s" % buflines)
	# print("TEMP:", varlist)
	for line in buflines:
		onecoord = OneCoord()
		if '[' in line or '-#' in line:
			onecoord.convertOneCoord(line, varlist)
			firstline.append(onecoord.firstline)
			secondline.append(onecoord.secondline)
			# print(onecoord.firstline)
		else:
			secondline.append(line)
	secondline = [' '.join(secondline)]
	# print(firstline + secondline)
	return (firstline + secondline)

class OneCoord:

	firstline = "1"
	secondline = "2"

	def convertOneCoord(self, line, varlist):
		firstline = []
		secondline = []
		freevar = varlist.pop(0)
		# print(varlist)

		line = line.replace(' ', '')
		firstline.append("#%d=" % freevar)
		if line[1] == '-':
			firstline.append(line[1:])
		else:
			if line.count('[', 2) < line.count(']', 2): firstline.append(line[2:line.rindex(']')])
			else: firstline.append(line[2:-1])
		# print("FL: %s" % firstline)
		secondline.append("%s#%d" % (line[0], freevar))
		self.firstline = ''.join(firstline)
		self.secondline = ''.join(secondline)
		# print(firstline, secondline)

##
##			IF
##

def convertIf(line, varlist):
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
	if "AND" in line: newlines = opAndIf(blocks, varlist)
	elif "OR" in line: newlines = opOrIf(blocks, varlist)
	else: newlines = opNoIf(blocks, varlist)
	return (newlines)

def opNoIf(blocks, varlist):
	global maxN
	freeN = maxN + 1
	exitN = freeN + len(blocks) - 1
	newlines = []

	if re.search(r"[^#\[\]\.\w]+", blocks[0]): block = partIf(blocks[0], newlines, varlist)
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

def opAndIf(blocks, varlist):
	global maxN
	freeN = maxN + 1
	newlines = []

	exitN = freeN + len(blocks) - 1
	for block in blocks[:-1]:
		# print("BLOCK:", block)
		if re.search(r"[^#\[\]\.\w]+", block): block = partIf(block, newlines, varlist)
		newlines.append("IF%sGOTO%d" % (block, freeN))
		newlines.append("GOTO%d" % exitN)
		newlines.append("N%d" % freeN)
		freeN += 1
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("AND: ", newlines)
	maxN = exitN
	return (newlines)

def opOrIf(blocks, varlist):
	global maxN
	freeN = maxN + 1
	newlines = []

	exitN = freeN + 1
	for block in blocks[:-1]:
		if re.search(r"[^#\[\]\.\w]+", block): block = partIf(block, newlines, varlist)
		newlines.append("IF%sGOTO%d" % (block, freeN))
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("OR: ",newlines)
	maxN = exitN
	return (newlines)

def partIf(block, newlines, varlist):
	freevar1 = varlist.pop(0)
	freevar2 = varlist.pop(0)
	compop = re.search(r"[A-Z]+", block)[0]
	block = block.partition(compop)
	newlines.append(f"#{freevar1}={block[0][1:]}")
	newlines.append(f"#{freevar2}={block[2][:-1]}")
	block = f"[#{freevar1}{compop}#{freevar2}]"
	return (block)


##
##			FUP
##

def convertFup(line, varlist):
	global maxN
	freeN = maxN + 1
	freevar1 = varlist.pop(0)
	freevar2 = varlist.pop(0)
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
