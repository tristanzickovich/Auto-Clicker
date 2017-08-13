#runs on python 2.7 w/ pywin32 64 bit
import sys
import json
from subprocess import Popen
import random
import win32api, win32con
import msvcrt
#load json imports
try:
	from types import SimpleNamespace as Namespace
except ImportError:
	# Python 2.x fallback
	from argparse import Namespace
	
#variables
DEF_CLICK = 0
DEF_DELAY = 1
DEF_NUMPRESS = 2
DEF_TEXT = 3

#storage lists
cList = [] #click list, list 0
dList = [] #delay list, list 1
nList = [] #num press list, list 2
tList = [] #text list, list 3
sList = [] #script list (combo of entries)

#messages
INVALIDINPUT = "\n Invalid Input\n"

#classes
#click class
class aClick:
	def __init__(self, ct, co, cx, cy):
		self.clkType = ct
		self.cOffset = co
		self.x = cx
		self.y = cy
#delay class
class tDelay:
	def __init__(self, dtime, doff):
		self.dTime = dtime #time in ms
		self.dOffset = doff #range of time in ms offset
#num class		
class aNum:
	def __init__(self, num):
		self.pNum = num
#text class
class aText:
	def __init__(self, text):
		self.pText = text

#functions
def abortScriptOption():
	#esc to stop
	stopKey = 27
	if (win32api.GetKeyState(stopKey) & (1 << 7)):
		sys.exit()
def startScriptOption():
	#tab to start
	startKey = 9
	if (win32api.GetKeyState(startKey) & (1 << 7)):
		return True
	return False
def runScript():
	if len(sList) < 1:
		return False
	else:
		numTimes = input(" Run script how many times?\n")
		numTimes = validateInput(0, numTimes)
		print('\nOpen Desired Screen and Press "TAB" to Begin\n')
		while 1:
			if startScriptOption():
				break
			perform_delay(100,0)
		for x in range(numTimes):
			abortScriptOption()
			dcount = 1
			print ('\nRunning Script\n')
			for i in sList:
				abortScriptOption()
				if i[0] == DEF_CLICK:
					perform_click(cList[i[1]].x,cList[i[1]].y,cList[i[1]].cOffset,cList[i[1]].clkType)
				elif i[0] == DEF_DELAY:
					perform_delay(dList[i[1]].dTime, dList[i[1]].dOffset)
				elif i[0] == DEF_NUMPRESS:
					perform_numpress(nList[i[1]].pNum)
				elif i[0] == DEF_TEXT:
					print ("%d) Text: %s" % (dcount, tList[i[1]].pText))
				dcount += 1
			print ('\nScript Completed\n')
		return True
		
def saveScript(filename):
	try:
		#convert storage lists to json
		cTmp = json.dumps([c.__dict__ for c in cList])
		dTmp = json.dumps([d.__dict__ for d in dList])
		nTmp = json.dumps([n.__dict__ for n in nList])
		tTmp = json.dumps([t.__dict__ for t in tList])
		sTmp = json.dumps(sList)
		orig_stdout = sys.stdout
		#write jsons to file
		fout = open(filename, 'w')
		sys.stdout = fout
		print (cTmp)
		print (dTmp)
		print (nTmp)
		print (tTmp)
		print (sTmp)
		sys.stdout = orig_stdout
		fout.close()
		print ('Script Saved Successfully\n')
	except:
		print('\nScript Failed To Save\n')
def loadScript(filename):
	global cList, dList, nList, tList, sList
	try:	
		saved = open(filename, 'r')
		cList = json.loads(saved.readline(), object_hook=lambda d: Namespace(**d))
		dList = json.loads(saved.readline(), object_hook=lambda d: Namespace(**d))
		nList = json.loads(saved.readline(), object_hook=lambda d: Namespace(**d))
		tList = json.loads(saved.readline(), object_hook=lambda d: Namespace(**d))
		sList = json.loads(saved.readline(), object_hook=lambda d: Namespace(**d))
		saved.close()
		print ('\nScript Loaded Successfully\n')
	except:
		print('\nScript Failed To Load\n')
def printSeq():
	dcount = 1
	if len(sList) < 1:
		return False
	else:
		print ('\nCurrent Script\n')
		for i in sList:
			if i[0] == DEF_CLICK:
				print ("%d) click: (%d,%d), offset: %d, type: %d" % (dcount, cList[i[1]].x,cList[i[1]].y,cList[i[1]].cOffset,cList[i[1]].clkType))
			elif i[0] == DEF_DELAY:
				print ("%i) delay: %i, offset: %i" % (dcount, dList[i[1]].dTime, dList[i[1]].dOffset))
			elif i[0] == DEF_NUMPRESS:
				print ("%d) num: %d" % (dcount, nList[i[1]].pNum))
			elif i[0] == DEF_TEXT:
				print ("%d) Text: %s" % (dcount, tList[i[1]].pText))
			dcount += 1
		print ('\n')
		return True
		
def validateInput(iType, ipt):
	#0 = int, 1 = str
	if iType == 0:
		if ipt.isdigit():
			return int(ipt)
	elif iType == 1:
		if type(ipt) is str:
			return str(ipt)
	print (INVALIDINPUT)
	sys.exit(0)

def updateSList(direction, idx, type):
	ct = 0
	for j in sList[idx:]:
		if j[0] == type:
			ci = idx + ct
			if direction < 0:
				sList[ci][1] = sList[ci][1] - 1
			else:
				sList[ci][1] = sList[ci][1] + 1
		ct += 1

def removeElem(idx):
	idx -= 1 #account for UI offset
	tmp = sList[idx]
	i = tmp[1]
	if tmp[0] == DEF_CLICK:
		#readjust index references
		updateSList(-1, idx, DEF_CLICK)
		del cList[i]
	elif tmp[0] == DEF_DELAY:
		#readjust index references
		updateSList(-1, idx, DEF_DELAY)
		del dList[i]
	elif tmp[0] == DEF_NUMPRESS:
		#readjust index references
		updateSList(-1, idx, DEF_NUMPRESS)
		del nList[i]
	elif tmp[0] == DEF_NUMPRESS:
		#readjust index references
		updateSList(-1, idx, DEF_TEXT)
		del tList[i]
	del sList[idx]
	print ('Item #%d Successfully Removed' % (idx + 1))

def addItem(idx, item, type):
	if idx <= 1:
		idx = 1
	if idx > len(sList):
		if type == 	DEF_CLICK:
			cList.append(item)
			sList.append([type,len(cList)-1])
		elif type == DEF_DELAY:
			dList.append(item)
			sList.append([type,len(dList)-1])
		elif type == DEF_NUMPRESS:
			nList.append(item)
			sList.append([type,len(tList)-1])
		elif type == DEF_TEXT:
			tList.append(item)
			sList.append([type,len(tList)-1])
	else:
		idx -= 1
		updateSList(1, idx, type)
		loc = 0;
		for i in range(0, idx):
			if sList[i][0] == type:
				loc += 1
		if type == 	DEF_CLICK:
			cList.insert(loc, item)
		elif type == DEF_DELAY:
			dList.insert(loc, item)
		elif type == DEF_NUMPRESS:
			nList.insert(loc, item)
		elif type == DEF_TEXT:
			tList.insert(loc, item)
		sList.insert(idx, [type, loc])
#click function
def perform_click(x, y, offset, type):
	if offset > 0:
		x += random.randint(-offset, offset)
		y += random.randint(-offset, offset)
	win32api.SetCursorPos((x,y))
	if type == 1:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	elif type == 2:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
#delay function
def perform_delay(length, offset):
	if offset > 0:
		length += random.randint(0, offset)
	win32api.Sleep(length)
#press number function
def perform_numpress(num):
	num = str(num)
	asciinum = ord(num)
	win32api.keybd_event(asciinum, 0, )
#capture coords by mouse position
def visualCoords():
	print ("Move mouse to desired location and\npress any key to capture coords")
	while True:
			x, y = win32api.GetCursorPos()
			win32api.Sleep(100)
			#check for keyboard interrupt
			if msvcrt.kbhit() and ord(msvcrt.getch()) != None:
				break
	print ("x: %d, y: %d" % (x,y))
	return x, y

#main loop
while 1:
	random.seed()
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
		print (INVALIDINPUT)
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
5. Add Text\n \
6. Remove Entry\n \
7. Save Script\n \
8. Load Script\n \
9. Run Script\n \
---------------------------------\n \
b. Go Back\n \
q. Quit\n \
---------------------------------\n \
")
			if tv == 'q':
				print (' Bye!')
				sys.exit(0)
			if not tv.isdigit():
				print (INVALIDINPUT)
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
					cx, cy = visualCoords()
				elif tt == 2:
					cx = input(" Enter x coord\n")
					cx = validateInput(0, cx)
					cy = input(" Enter y coord\n")
					cy = validateInput(0, cy)
				tc = input(" 1. Left Click\n \
2. Right Click\n")
				tc = validateInput(0, tc)
				co = input(" Enter offset (pixels):\n")
				co = validateInput(0, co)
				c = aClick(tc,co, cx, cy)
				status = printSeq()
				if status:
					where = input(" Enter index to insert\n")
					where = validateInput(0, where)
				else:
					where = 0
				addItem(where, c, DEF_CLICK)
			#add delay
			elif int(tv) == 3:
				td = input(" Enter delay time (ms):\n")
				td = validateInput(0, td)
				do = input(" Enter delay offset (ms):\n")
				do = validateInput(0, do)
				d = tDelay(td,do)
				status = printSeq()
				if status:
					where = input(" Enter index to insert\n")
					where = validateInput(0, where)
				else:
					where = 0
				addItem(where, d, DEF_DELAY)
			#add number
			elif int(tv) == 4:
				nn = input(" Enter number:\n")
				nn = validateInput(0, nn)
				n = aNum(nn)
				status = printSeq()
				if status:
					where = input(" Enter index to insert\n")
					where = validateInput(0, where)
				else:
					where = 0
				addItem(where, n, DEF_NUMPRESS)
			#add text
			elif int(tv) == 5:
				nt = input(" Enter text:\n")
				nt = validateInput(1, nt)
				t = aText(nt)
				printSeq()
				where = input(" Enter index to insert\n")
				where = validateInput(0, where)
				addItem(where, t, DEF_TEXT)
			#remove entry
			elif int(tv) == 6:
				if printSeq():
					elem = input("Enter # of element to remove:\n")
					elem = validateInput(0,elem)
					removeElem(elem)
			#save script
			elif int(tv) == 7:
				fn = input(" Enter File Name:\n")
				fn = validateInput(1,fn)
				saveScript(fn)
			#load script
			elif int(tv) == 8:
				fn = input(" Enter File Name:\n")
				validateInput(1,fn)
				loadScript(fn)
			elif int(tv) == 9:
				runScript()
			else:
				print (INVALIDINPUT)
	#load script
	elif int(tv) == 3:
		fn = input(" Enter File Name:\n")
		validateInput(1,fn)
		loadScript(fn)
	#run script	
	elif int(tv) == 4:
		runScript()
	else:
		print (INVALIDINPUT)

