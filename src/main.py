import sys
import json
from subprocess import Popen
import random

from utils.event.classes import *
from utils.event.actions import *
from utils.event.constants import *
from utils.script.actions import *
from utils.common import validateInput
from resources.constants import INVALID_INPUT
from utils.event.classes import *

#load json imports
try:
	from types import SimpleNamespace as Namespace
except ImportError:
	# Python 2.x fallback
	from argparse import Namespace

def run_auto_clicker():
	#loadScript('mining.txt')
	while 1:
		tv = input("\
	\n\tScripting Menu\n \
	---------------------------\n \
	1. View Current Script\n \
	2. Add / Edit Current Script\n \
	3. Load Script\n \
	4. Run Script\n \
	---------------------------\n \
	q. Quit\n \
	---------------------------\n \
	")
		if tv == 'q':
			print (' Bye!')
			sys.exit(0)
		if tv == 'b':
			break
		if not tv.isdigit():
			print (INVALID_INPUT)
		#print script sequence
		elif int(tv) == 1:
			if not printSeq():
				print ("\nScript not created or loaded\n")
		#add/edit script menu
		elif int(tv) == 2:
			while 1:
				tv = input("\
	\t Add / Edit Script Menu\n \
	---------------------------------\n \
	1. View Current Script\n \
	2. Add Click\n \
	3. Add Delay\n \
	4. Add Number Press\n \
	5. Add Key Action\n \
	6. Add Text\n \
	7. Remove Entry\n \
	8. Save Script\n \
	9. Load Script\n \
	10. Run Script\n \
	---------------------------------\n \
	b. Go Back\n \
	q. Quit\n \
	---------------------------------\n \
	")
				if tv == 'q':
					print (' Bye!')
					sys.exit(0)
				if not tv.isdigit():
					print (INVALID_INPUT)
				#print script sequence
				elif int(tv) == 1:
					if not printSeq():
						print ("\nScript not created or loaded\n")
				#add click
				elif int(tv) == 2:
					tt = input(" Choose Coordinate Entry Method\n \
	1. Visual Method\n \
	2. Manual Method\n")
					tt = validateInput(0, tt)
					if tt == 1:
						cx, cy = captureMouseCoords()
					elif tt == 2:
						cx = input(" Enter x coord\n")
						cx = validateInput(0, cx)
						cy = input(" Enter y coord\n")
						cy = validateInput(0, cy)
					tc = input(" 1. Left Click\n \
	2. Right Click\n")
					tc = validateInput(0, tc)
					tc =  LEFT_CLICK if tc == 1 else RIGHT_CLICK
					co = input(" Enter offset (pixels):\n")
					co = validateInput(0, co)
					c = Click(tc,co, cx, cy)
					status = printSeq()
					if status:
						where = input(" Enter index to insert\n")
						where = validateInput(0, where)
					else:
						where = 0
					addItem(where, c)
				#add delay
				elif int(tv) == 3:
					td = input(" Enter delay time (ms):\n")
					td = validateInput(0, td)
					do = input(" Enter delay offset (ms):\n")
					do = validateInput(0, do)
					d = Delay(td,do)
					status = printSeq()
					if status:
						where = input(" Enter index to insert\n")
						where = validateInput(0, where)
					else:
						where = 0
					addItem(where, d)
				#add number
				elif int(tv) == 4:
					nn = input(" Enter number:\n")
					nn = validateInput(0, nn)
					n = Num(nn)
					status = printSeq()
					if status:
						where = input(" Enter index to insert\n")
						where = validateInput(0, where)
					else:
						where = 0
					addItem(where, n)
				#add key action
				elif int(tv) == 5:
					print(" Enter key:\n")
					ascii_key = capture_key_press()
					action = input(" Choose Action:\n\
					1) Hold\n\
					2) Release\n\
					3) Press\n")
					action = validateInput(0, action)
					if action == 1:
						action = KEY_HOLD
					elif action == 2:
						action = KEY_RELEASE
					else:
						action = KEY_PRESS
					key_action = Key(ascii_key, action)
					status = printSeq()
					if status:
						where = input(" Enter index to insert\n")
						where = validateInput(0, where)
					else:
						where = 0
					addItem(where, key_action)
				#add text
				elif int(tv) == 6:
					nt = input(" Enter text:\n")
					nt = validateInput(1, nt)
					t = Text(nt)
					printSeq()
					where = input(" Enter index to insert\n")
					where = validateInput(0, where)
					addItem(where, t)
				#remove entry
				elif int(tv) == 7:
					if printSeq():
						elem = input("Enter # of element to remove:\n")
						elem = validateInput(0,elem)
						removeElem(elem)
				#save script
				elif int(tv) == 8:
					fn = input(" Enter File Name:\n")
					fn = validateInput(1,fn)
					saveScript(fn)
				#load script
				elif int(tv) == 9:
					fn = input(" Enter File Name:\n")
					validateInput(1,fn)
					loadScript(fn)
				elif int(tv) == 10:
					runScript()
				else:
					print (INVALID_INPUT)
		#load script
		elif int(tv) == 3:
			fn = input(" Enter File Name:\n")
			validateInput(1,fn)
			loadScript(fn)
		#run script	
		elif int(tv) == 4:
			runScript()
		else:
			print (INVALID_INPUT)

if __name__ == '__main__':
	random.seed()
	run_auto_clicker()