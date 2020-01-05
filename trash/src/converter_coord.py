# ************************************************* #
#                                                   #
#    ───╔═╗──╔══╗╔══╗╔═╗╔═╗╔═╗╔══╗╔═╗─────╔═╗───    #
#    ───║ ║──╚╗╔╝║╔═╝║ ║║ ║║ ║╚╗╔╝║ ║─────║ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╚═╗ ╔═╝ ║───    #
#    ───║ ║───║║─║║──║ ║║ ║║ ║─║║─║ ╔═╗ ╔═╗ ║───    #
#    ───║ ╚═╗╔╝╚╗║╚═╗║ ╚╝ ╚╝ ║╔╝╚╗║ ║ ╚═╝ ║ ║───    #
#    ───╚═══╝╚══╝╚══╝╚══╝ ╚══╝╚══╝╚═╝─────╚═╝───    #
#                                                   #
#   converter_coord.py                              #
#       By: licwim                                  #
#                                                   #
#   Created: 05-01-2020 19:53:51 by licwim          #
#   Updated: 05-01-2020 19:59:05 by licwim          #
#                                                   #
# ************************************************* #

from converter import *

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
		self.firstline = ''.join(firstline)
		self.secondline = ''.join(secondline)
		# print(firstline, secondline)
