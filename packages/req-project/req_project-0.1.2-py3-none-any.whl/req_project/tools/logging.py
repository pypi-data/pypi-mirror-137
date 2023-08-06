

DEBUGGING = False


##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | Cancel 
##  6 : Cancel | Try Again | Continue
## To also change icon, add these values to previous number
# 16 Stop-sign icon
# 32 Question-mark icon
# 48 Exclamation-point icon
# 64 Information-sign icon consisting of an 'i' in a circle
def Mbox(title, text, style):

	try:
		import ctypes  # An included library with Python install.

		style |= 0x40000
		return ctypes.windll.user32.MessageBoxW(0, text, title, style)

	except ImportError:
	    # Python 3.x imports
		import tkinter as tk
		from tkinter import messagebox

		root = tk.Tk()
		root.overrideredirect(1)
		root.withdraw()
		if style == 16:
			messagebox.showerror(title, text) 
		elif style  == 32:
			messagebox.askquestion(title, text) 
		elif style  == 48:
			messagebox.showwarning(title, text) 
		elif style  == 64:			
			messagebox.showinfo(title, text) 
	



def print_error(text):
	print("ERROR: " + str(text))
	Mbox('CapellaReqifSync ERROR', str(text), 16)
	raise ValueError(text)

def print_warning(text):
	Mbox('CapellaReqifSync WARNING', str(text), 48)
	print("WARNING: " + str(text))

def print_info(text):
	print("INFO: " + str(text))

def print_debug(text):
	global DEBUGGING
	if DEBUGGING:
		print("DEBUG: " + str(text))
		1

