"""
Various useful functions to avoid code duplication
Created: 25/07/2021
"""

import sys
import os
from tkinter import Tk, filedialog # for selecting folder with GUI

# Setting variables
noOfHyphens = 80
character = '-'
sep = ''
errormsg = 'An error occured.'

def printSeparator(sep):
    for i in range(1, noOfHyphens):
        sep += character

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big
def print_header(text):
    selectedFont = "Big"
    print(text, selectedFont)
    #result = pyfiglet.figlet_format(text, font = selectedFont )
    #print(result)

def printError():
    print(errormsg)

def askForFileOrDirectory(type, action, extension):
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    if (type=='folder'):
        var = filedialog.askdirectory() # Returns opened path as str
    else:
        extension = '*.' + extension
        if (action=='open'):
            var = filedialog.askopenfile(mode ='r', filetypes=['File', extension])
        elif (action=='save'):
            var = filedialog.asksaveasfilename(mode ='w', filetypes=['File', extension])
    print(sep)
    return var

"""
Counts the number of lines of a file using enumerate
"""
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        noLines = i + 1
    return noLines

"""
Checks if the file exists and is a non-empty text file
"""
def checkFile(filename):
    print("Check if file exists...")
    if os.path.isfile(filename):
        print("File exists.")
        if filename.endswith('.txt'):
            print("File is a text file.")
            if os.stat(filename).st_size > 0:
                print("File has some data")
            else:
                print("File is empty")
                print(errormsg)
                sys.exit()
        else:
            print("File is not a text file.")
            print(errormsg)
            sys.exit()
    else:
        print("File does not exist")
        print(errormsg)
        sys.exit()

"""
Computes the size of a file in bytes, megabytes and gigabytes
"""
def getSize(filename):
    filesizeB = os.stat(filename).st_size
    filesizeMB = filesizeB / 1024
    filesizeGB = filesizeMB / 1024
    return filesizeB, filesizeMB, filesizeGB

"""
Displays file sizes
"""
def printSize(filename):
    fileb = getSize(filename)[0]
    print("Filesize B: " + fileb)
    filemb = fileb/1024
    print("Filesize MB: " + filemb)
    filegb = filemb/(1024 ** 2)  # ** is power operator
    print("Filesize GB: " + filegb)