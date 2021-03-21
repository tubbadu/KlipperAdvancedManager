decryptScript = "/home/tubbadu/code/GitHub/KlipperAdvancedManager/decryptKlipperHistory.sh"
pastePath = "/home/tubbadu/code/GitHub/KlipperAdvancedManager/KlipperAdvancedManager_paste.py"
screenSize = (1920, 1080)
import os
import glob
import PySimpleGUI as sg
import pyperclip
import subprocess
import sys
import pyautogui

sg.theme('DarkBlue2')

def readClips():
	ret = []
	os.system(decryptScript) #generate file
	for file in sorted(glob.glob('/home/tubbadu/.local/share/klipper/*.cliptxt')):
		with open(file, 'r') as f:
			txt = f.read()
			ret.append(txt)
	return ret

def spawn_program_and_die(program, exit_code=0): #copiata lol
    """
    Start an external program and exit the script 
    with the specified return code.

    Takes the parameter program, which is a list 
    that corresponds to the argv of your command.
    """
    # Start the external program
    subprocess.Popen(program)
    # We have started the program, and can suspend this interpreter
    sys.exit(exit_code)

def paste(ch, shift=True):
	if(shift):
		flag = 'shift'
	else:
		flag = ''
	pyperclip.copy(ch)
	spawn_program_and_die(['python3', pastePath, flag])
	exit()



def getlist(cliplist, index):
	clist = []
	for i in range(len(cliplist)):
		if cliplist[i] != '':
			if i != index:
				clist.append('   ' + cliplist[i])
			else:
				clist.append('> ' + cliplist[i])
	return clist

def main():
	try:
		cliplist = readClips()
		clist = getlist(cliplist, 0)
		index = 0
		currentMouseX, _ = pyautogui.position()
		pos = ((screenSize[0] - 300)/2, (screenSize[1] - 185)/2)
		if currentMouseX > screenSize[0]:
			#sono nel secondo schermo
			pos = (pos[0] + screenSize[0], pos[1])
		layout = [[sg.Checkbox("shift", default=False, key='--checkbox--', enable_events=True)],[sg.Listbox(values=clist, size=(30, 7), key='--listbox--', enable_events=True, font=(None, 12), no_scrollbar=True)]]
		window = sg.Window('Klipper', layout, element_justification='center', return_keyboard_events=True, location=pos, size=(300, 215))
		
		while(True):
			event, values = window.read()
			shift = values['--checkbox--']
			if 'Shift' in event:
				window['--checkbox--'].update(value = not shift)
			clist = getlist(cliplist, index)
			if 'Up' in event and index > 0:
				index -= 1
			elif 'Down' in event and index < len(clist) - 1:
				index += 1
			
			clist = getlist(cliplist, index)
			
			if 'KP_Enter' in event or 'Return' in event:
				ch = cliplist[index] #refreshList(txt)[0]
				print(ch)
				paste(ch, shift)
			elif event == sg.WINDOW_CLOSED or 'Escape' in event:
				break
			elif event == '--listbox--':
				# è stato premuto un char!
				ch = values['--listbox--'][0]
				print(ch)
				paste(ch, shift)
			
			window['--listbox--'].update(values = clist)
		window.close()
	except Exception as e:
		print('An error occourred while running KlipperAdvancedManager:', e)
main()