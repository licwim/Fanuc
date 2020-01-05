# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_if.py                                 #
#       By: licwim                                  #
#                                                   #
#   Created: 05-01-2020 19:53:40 by licwim          #
#   Updated: 05-01-2020 19:58:39 by licwim          #
#                                                   #
# ************************************************* #

from converter import *

def convertIf(line):
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
	if "AND" in line: newlines = opAndIf(blocks)
	elif "OR" in line: newlines = opOrIf(blocks)
	else: newlines = opNoIf(blocks)
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
