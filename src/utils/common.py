import sys
from resources.constants import INVALID_INPUT

def validateInput(iType, ipt):
	#0 = int, 1 = str
	if iType == 0:
		if ipt.isdigit():
			return int(ipt)
	elif iType == 1:
		if type(ipt) is str:
			return str(ipt)
	print (INVALID_INPUT)
	sys.exit(0)