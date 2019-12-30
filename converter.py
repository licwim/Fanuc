import re

maxvar = 0
maxN = 0

def converter(lines):
	global maxvar
	global maxN
	buflines = []
	newlines = []
	i = 1
	maxvar = 0
	maxN = 0
	# print("MAX: %d, %d" % (maxvar, maxN))
	for line in lines:
		# print('LINE: %d' % i)
		line = convertNum(line)
		checkN(line)
		line = checkComments(line)
		buflines.extend(line)
		i += 1
	# print(maxvar, maxN)
	i = 1
	for line in buflines:
		# print('NEW LINE: %s' % line)
		# print('LINE: %d' % i)
		lines = convertLine1(line)
		lines = convertLines(lines)
		newlines.extend(lines)
		i += 1
	return (newlines)

def convertLines(lines):
	newlines = []
	for line in lines:
		line = line.strip(' \n')
		if line:
			# line = convertLine2(line)
			newlines += [line]
	return (newlines)

def checkComments(line):
	lines = [line.strip(' ')]
	if '(' in line and ')' in line:
		newline = line.partition('(')
		lines = [newline[0], ';' + newline[1] + newline[2]]
		lines[0] = lines[0].strip(' \n')
		lines[1] = lines[1].strip(' \n')
	return (lines)

def convertLine1(line):
	newlines = [line]
	if line.startswith('X') or line.startswith('Y') or line.startswith('Z'): newlines = convertCoords(line)
	if line.startswith("IF") and '[' in line: newlines = convertIf(line)
	if "FUP" in line: newlines = convertFup(line)
	return (newlines)

def convertLine2(line):
	if re.match(r"N\d+", line):
		N = re.search(r"N\d+", line)[0]
		line = '"%s"%s' % (N, line[line.index(N) + len(N):])
	if line.startswith("GOTO"):
		N = re.search(r"\d+", line.replace(' ', '')[4:])[0]
		line = '(BNC,"N%s")%s' % (N, line[line.index(N) + len(N):])
	if line.startswith("IF"):
		N = line[line.index("GOTO") + 4:]
		print("N: %s" % N)
		block = re.search(r"\[[^\[\]]*\]", line)[0]
		print("BLOCK: %s" % block)
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

def checkN(line):
	global maxN

	find = re.match(r"N\d+", line)
	# print(find.group(0))
	if find and int(find.group(0)[1:]) > maxN:
		maxN = int(find.group(0)[1:])

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
	global maxvar
	n = int(''.join(num))

	num.clear()
	num.append('#')
	if n > 99:
		n -= 40
	elif n > 0 and n < 27:
		n += 30
	elif n == 0:
		n = 999999
		num.pop()
	num.append(str(n))
	if n != 999999 and n > maxvar:
		maxvar = n
	return (''.join(num))

def convertCoords(line):
	firstline = []
	secondline = []

	buflines = re.findall(r"[XYZ][^XYZ]*",line)
	# print("BUFF: %s" % buflines)
	for line in buflines:
		coordline = CoordLine()
		if '[' in line or '-#' in line:
			coordline.convertOneCoord(line)
			firstline.append(coordline.firstline)
			secondline.append(coordline.secondline)
			# print(coordline.firstline)
		else:
			secondline.append(line)
	secondline = [' '.join(secondline)]
	# print(firstline + secondline)
	return (firstline + secondline)

class CoordLine:

	firstline = "1"
	secondline = "2"

	def convertOneCoord(self, line):
		global maxvar
		firstline = []
		secondline = []
		maxvar += 1
		freevar = maxvar

		line = line.replace(' ', '')
		firstline.append("#%d=" % freevar)
		if line[1] == '-':
			firstline.append(line[1:])
		else:
			if line.count('[', 2) < line.count(']', 2): firstline.append(line[2:line.rindex(']')])
			else: firstline.append(line[2:-1])
		# print("FL: %s" % firstline)
		secondline.append("%s#%d" % (line[0], freevar))
		CoordLine.firstline = ''.join(firstline)
		CoordLine.secondline = ''.join(secondline)
		# print(firstline, secondline)

def convertIf(line):
	if "OR" in line: newlines = opOrIf(blocks)
	elif "AND" in line: newlines = opAndIf(blocks)
	else: newlines = opNoIf(blocks)
	if "THEN" in line: search = "THEN"
	else: search = "GOTO"
	blocks = re.findall(r"\[[^\[\]]*\]", line[:line.rindex(search)])
	if search == "THEN": blocks.append(line[line.index(search) + 4:])
	else: blocks.append(line[line.index(search):])
	# print(blocks)
	print(re.findall(r"\[.*\]", line[:line.rindex(search)]))
	# if re.search(r"[[", line):
	# firstline.append(line[2:-1])
	return (newlines)

def opNoIf(blocks):
	global maxN
	freeN = maxN + 1
	exitN = freeN + len(blocks) - 1
	newlines = []

	if "GOTO" in blocks[-1]:
		return (["IF" + ''.join(blocks)])
	newlines.append("IF%sGOTO%d" % (blocks[0], freeN))
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("BLOCK:", blocks)
	return (newlines)

def opAndIf(line):
	global maxN
	freeN = maxN + 1
	newlines = []
	blocks = []

	line = line.partition("AND")
	blocks[0] = re.search(r"", line[0])
	exitN = freeN + len(blocks) - 1
	for block in blocks[:-1]:
		newlines.append("IF%sGOTO%d" % (block, freeN))
		newlines.append("GOTO%d" % exitN)
		newlines.append("N%d" % freeN)
		freeN += 1
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("AND: ", newlines)
	maxN = freeN
	return (newlines)

def opOrIf(blocks):
	global maxN
	freeN = maxN + 1
	newlines = []

	exitN = freeN + 1
	for block in blocks[:-1]:
		newlines.append("IF%sGOTO%d" % (block, freeN))
	newlines.append("GOTO%d" % exitN)
	newlines.append("N%d" % freeN)
	newlines.append(blocks[-1])
	newlines.append("N%d" % exitN)
	# print("OR: ",newlines)
	maxN = freeN
	return (newlines)

def convertFup(line):
	global maxvar
	global maxN
	freevar = maxvar + 1
	freeN = maxN + 1
	newlines = []
	var = line[:line.index('=')]
	math = line[line.index("FUP") + 4:-1]
	newlines.append("#%d=%s" % (freevar, math))
	newlines.append("#%d=FIX[#%d]" % (freevar + 1, freevar))
	newlines.append("IF[#%d-#%dGE0.0001]GOTO%d" % (freevar, freevar + 1, freeN))
	newlines.extend(["GOTO%d" % (freeN + 1), "N%d" % freeN])
	newlines.append("#%d=#%d+1" % (freevar, freevar + 1))
	newlines.extend(["N%d" % (freeN + 1), "%s=#%d" % (var, freevar)])
	# print(newlines)
	return (newlines)
