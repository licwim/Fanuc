# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_lines.py                              #
#       By: licwim                                  #
#                                                   #
#   Created: 05-01-2020 20:04:29 by licwim          #
#   Updated: 05-01-2020 20:04:31 by licwim          #
#                                                   #
# ************************************************* #

from converter import *

def convertLine1(line):
	buflines = [line]
	newlines = []
	if line.startswith('X') or line.startswith('Y') or line.startswith('Z'): buflines = convertCoords(line)
	if line.startswith("IF") and '[' in line: buflines = convertIf(line)
	for line in buflines:
		if "FUP" in line: newlines.extend(convertFup(line))
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
