from pyautogui import hotkey
import sys
try:
	flag = sys.argv[1]
except:
	flag = "noflag"
if flag == 'shift':
	hotkey('ctrl', 'shift', 'v')
elif flag == 'noflag' or flag == '':
	hotkey('ctrl', 'v')
else:
	print ("Unknown flag")