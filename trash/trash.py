def selectnum(line, i):
	num = []

	i = line.find('#')
	i += 1
	while i < len(line) and (line[i].isdigit() or (line[i - 1] == '#' and line[i] == '-')):
		num.append(line[i])
		i += 1
	return (num)

def convertNum(line):
	newline = line
	i = 0

	while i < len(line):
		j = i
		i = line[j:].find('#')
		i += len(line[:j])
		newline.append(line[j:i])
		i += 1
		num = []
		while i < len(line) and (line[i].isdigit() or (line[i - 1] == '#' and line[i] == '-')):
			num.append(line[i])
			i += 1
		newline.append(work_with_numbers(num))
		if i < 0:
			newline.append(line[j:])
			break
	return (''.join(newline))

def work_with_numbers(num):
	global maxnum
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
	if n != 999999 and n > maxnum:
		maxnum = n
	return (''.join(num))

def convertIf(line):
	if "THEN" in line: search = "THEN"
	else: search = "GOTO"
	blocks = re.findall(r"\[[^\[\]]*\]", line[:line.rindex(search)])
	if search == "THEN": blocks.append(line[line.index(search) + 4:])
	else: blocks.append(line[line.index(search):])
	if "OR" in line: newlines = opOrIf(blocks)
	elif "AND" in line: newlines = opAndIf(blocks)
	else: newlines = opNoIf(blocks)
	# print(blocks)
	# print(re.findall(r"\[.*\]", line[:line.rindex(search)]))
	# if re.search(r"[[", line):
	# firstline.append(line[2:-1])
	return (newlines)

	def findTempvar():
	global lockvar
	global tempvar

	print(lockvar)
	for n in range(1, 255):
		if not n in lockvar and not n in tempvar: tempvar.append(n)
		if len(tempvar) > 4: break
	print(tempvar)
