import json
from utils.event.actions import *
from utils.event.constants import *
from utils.common import validateInput

#load json imports
try:
	from types import SimpleNamespace as Namespace
except ImportError:
	# Python 2.x fallback
	from argparse import Namespace

script_events = []

def runScript():
	if len(script_events) < 1:
		return False
	else:
		numTimes = input(" Run script how many times?\n")
		numTimes = validateInput(0, numTimes)
		print('\nOpen Desired Screen and Press "TAB" to Begin\n')
		while 1:
			if startScriptOption():
				break
			perform_delay(100,0)
		for _ in range(numTimes):
			abortScriptOption()
			print ('\nRunning Script\n')
			for event in script_events:
				abortScriptOption()
				event_type = event.type
				if event_type == CLICK_TYPE:
					perform_click(event.xCoord, event.yCoord, event.pixelOffset, event.clickType)
				elif event_type == DELAY_TYPE:
					perform_delay(event.delayTime, event.timeOffset)
				elif event_type == NUM_TYPE:
					perform_numpress(event.value)
				elif event_type == KEY_TYPE:
					perform_key_action(event.key, event.action)
				elif event_type == TEXT_TYPE:
					print ("Text: %s" % (event.pText))
			print ('\nScript Completed\n')
		return True
		
def saveScript(filename):
	try:
		#convert storage lists to json
		print('scriptEvents', script_events)
		script = json.dumps([event.__dict__ for event in script_events])
		orig_stdout = sys.stdout
		#write jsons to file
		fout = open(filename, 'w')
		sys.stdout = fout
		print (script)
		sys.stdout = orig_stdout
		fout.close()
		print ('Script Saved Successfully\n')
	except:
		print('\nScript Failed To Save\n')

def loadScript(filename):
	global script_events
	try:	
		script = open(filename, 'r')
		script_events = json.loads(script.readline(), object_hook=lambda d: Namespace(**d))
		script.close()
		print ('\nScript Loaded Successfully\n')
	except:
		print('\nScript Failed To Load\n')

def printSeq():
	dcount = 1
	if len(script_events) < 1:
		return False
	else:
		print ('\nCurrent Script\n')
		for event in script_events:
			event_type = event.type
			if event_type == CLICK_TYPE:
				print ("%d) click: (%d,%d), offset: %d, type: %s" % (dcount, event.xCoord, event.yCoord, event.pixelOffset, event.clickType))
			elif event_type == DELAY_TYPE:
				print ("%i) delay: %i, offset: %i" % (dcount, event.delayTime, event.timeOffset))
			elif event_type == NUM_TYPE:
				print ("%d) num: %d" % (dcount, event.value))
			elif event_type == KEY_TYPE:
				print ("%d) key: %s, action: %s" % (dcount, event.key, event.action))
			elif event_type == TEXT_TYPE:
				print ("%d) Text: %s" % (dcount, event.value))
			dcount += 1
		print ('\n')
		return True

def updatescript_events(direction, idx, type):
	ct = 0
	for j in script_events[idx:]:
		if j[0] == type:
			ci = idx + ct
			if direction < 0:
				script_events[ci][1] = script_events[ci][1] - 1
			else:
				script_events[ci][1] = script_events[ci][1] + 1
		ct += 1

def removeElem(idx):
	idx -= 1 #account for UI offset
	del script_events[idx]
	print ('Item #%d Successfully Removed' % (idx + 1))

def addItem(idx, event):
	if idx <= 1:
		idx = 1
	if idx > len(script_events):
		script_events.append(event)
	else:
		idx -= 1
		script_events.insert(idx, event)

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