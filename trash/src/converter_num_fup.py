# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_num_fup.py                            #
#       By: licwim                                  #
#                                                   #
#   Created: 05-01-2020 20:08:11 by licwim          #
#   Updated: 05-01-2020 20:08:15 by licwim          #
#                                                   #
# ************************************************* #

# from converter import maxvar
from converter import *

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
