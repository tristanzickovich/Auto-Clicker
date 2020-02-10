import win32api, win32con
import random
import sys
import msvcrt
from pynput import keyboard


from .constants import LEFT_CLICK, RIGHT_CLICK, KEY_HOLD, KEY_RELEASE

def perform_click(x, y, offset, type):
	if offset > 0:
		x += random.randint(-offset, offset)
		y += random.randint(-offset, offset)
	win32api.SetCursorPos((x,y))
	perform_delay(50, 5)
	if type == LEFT_CLICK:
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
	elif type == RIGHT_CLICK:
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def perform_delay(length, offset):
	if offset > 0:
		length += random.randint(0, offset)
	win32api.Sleep(length)

def perform_numpress(num):
	num = str(num)
	asciinum = ord(num)
	win32api.keybd_event(asciinum, 0, )

def perform_key_action(key, action):
	#key = str(key)
	ascii_key = 160
	print('key', ascii_key)
	if action == KEY_HOLD:
		win32api.keybd_event(ascii_key, 0, 1, 0)
	elif action == KEY_RELEASE:
		win32api.keybd_event(ascii_key, 0, win32con.KEYEVENTF_EXTENDEDKEY  | win32con.KEYEVENTF_KEYUP, 0)
	else:
		win32api.keybd_event(ascii_key, 0, 0, 0)
		win32api.keybd_event(ascii_key, 0, win32con.KEYEVENTF_KEYUP, 0)


key_press_buffer = []
def on_press(key):
	try:
		print('alphanumeric key {0} pressed'.format(
			key.char))
		key_press_buffer.append(ord(key.char))
	except AttributeError:
		print('special key {0} pressed'.format(
			key))
		print(type(key.value))
		key_press_buffer.append(key.value)

def on_release(key):
	print('{0} released'.format(
		key))
	return False

def capture_key_press():
	#bypass releasing 'enter' that got us here
	with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
		listener.join()
	#read actual keyboard input
	with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
		listener.join()
	print('tristan kpb', key_press_buffer)
	if len(key_press_buffer):
		return key_press_buffer[0]

def captureMouseCoords():
	print ("Move mouse to desired location and\npress any key to capture coords")
	while True:
		x, y = win32api.GetCursorPos()
		win32api.Sleep(500)
		print ("x: %d, y: %d" % (x,y))
		#check for keyboard interrupt
		if msvcrt.kbhit() and ord(msvcrt.getch()) != None:
			break
	print ("x: %d, y: %d" % (x,y))
	return x, y
