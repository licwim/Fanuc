import re

maxvar = 0
maxN = 0

def converter(lines):
	buflines = []
	newlines = []
	i = 0
	for line in lines:
		line = convertNum(line)
		checkN(line)
		line = line.strip(' ')
		buflines.append(line)
	# print(maxvar, maxN)
	for line in buflines:
		# print('NEW LINE: %s' % line)
		print('LINE: %d' % i)
		templines = convertLine1(line)
		lines = []
		for line in templines:
			line = line.strip(' \n')
			if line:
				print(type(line), line)
				line = convertLine2(line)
				lines += [line]
		newlines.extend(lines)
		i += 1

	return (newlines)

def convertLine1(line):
	if line.startswith('X') or line.startswith('Y') or line.startswith('Z'): return (convertCoords(line))
	elif line.startswith("IF") and ("AND" in line or "OR" in line): return (convertIf(line))
	elif "FUP" in line: return (convertFup(line))
	else: return ([line])

def convertLine2(line):
	# line = ''
	if "FIX" in line: return (line.replace("FIX", "INT"))
	elif '(' in line:
		newline = line.partition('(')
		return ('\n'.join([newline[0], ';' + newline[1] + newline[2]]))
	elif re.match(r"N\d+", line): return ('"%s"' % line)
	elif line.startswith("GOTO"): return ('BNC,"N%s"' % line.replace(' ', '')[4:])
	elif line.startswith("IF"):
		block = re.search(r"\[[^\[\]]*\]", line).group(0)
		print("BLOCK: %s" % block)
		return (line)


def checkN(line):
	global maxN

	find = re.match(r"N\d*", line)
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
			firstline.append(line[2:-1])
		# print("FL: %s" % firstline)
		secondline.append("%s#%d" % (line[0], freevar))
		CoordLine.firstline = ''.join(firstline)
		CoordLine.secondline = ''.join(secondline)
		# print(firstline, secondline)

def convertIf(line):
	if "THEN" in line: search = "THEN"
	else: search = "GOTO"
	blocks = re.findall(r"\[[^\[\]]*\]", line[:line.rindex(search)])
	blocks.append(line[line.index(search) + 4:])
	# print(blocks)
	if "OR" in line: newlines = opOrIf(blocks)
	else: newlines = opAndIf(blocks)
	newlines.insert(-1, blocks[-1])
	# if re.search(r"[[", line):
	# 	firstline.append(line[2:-1])
	return (newlines)

def opAndIf(blocks):
	global maxN
	freeN = maxN + 1
	newlines = []

	exitN = freeN + len(blocks) - 1
	for block in blocks[:-1]:
		newlines.append("IF%sGOTO%d" % (block, freeN))
		newlines.append("GOTO%d" % exitN)
		newlines.append("N%d" % freeN)
		freeN += 1
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