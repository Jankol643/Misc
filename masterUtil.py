"""
Various useful functions to avoid code duplication
Created: 25/07/2021
"""

import sys
import os
from tkinter import Tk, filedialog # for selecting folder with GUI

def print_separator(character, frequency):
    """
    Prints specified character with the given frequency
    :string character: character to print
    :int frequency: number of times to print character
    """
    sep = ''
    for i in range(1, frequency):
        sep += character
    print(sep)

def print_text_ascii(text):
    """
    Prints text in ASCII Art
    :string text: string to print
    https://github.com/pwaller/pyfiglet
    """
    selectedFont = "Big"
    print(text, selectedFont)
    #result = pyfiglet.figlet_format(text, font = selectedFont )
    #print(result)

def ask_file_or_directory(type, action, extension):
    """
    Asks the user to specify a file or a directory using a GUI
    :string type: type to do action on (file or directory)
    :string action: action to perform (open or save)
    :string extension: extension of file(s) to open
    :return var: path to file or directory
    """
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active above all windows despite of selection.
    if (type == 'directory'):
        var = filedialog.askdirectory() # Returns opened path as str
    elif (type == 'file'):
        extension = '*.' + extension
        if (action == 'open'):
            var = filedialog.askopenfile(mode ='r', filetypes=['File', extension])
        elif (action == 'save'):
            var = filedialog.asksaveasfilename(mode ='w', filetypes=['File', extension])
        else:
            raise ValueError("Action must be open or save.")
    else:
        raise ValueError("Type must be file or directory")
    print_separator('-', 80)
    return var

def file_len(fname):
    """
    Counts the number of lines of a file using enumerate
    :string fname: name of file
    :return noLines: number of lines in file
    :raises FileNotFoundError: when file cannot be found
    """
    try:
        with open(fname,"r") as f:
            for i, l in enumerate(f):
                pass
            noLines = i + 1
            return noLines
    except FileNotFoundError:
        raise FileNotFoundError

def check_file_type(filename, extension):
    """
    Checks if the file exists and is a non-empty file with the specified extension
    :string filename: name of file to check
    :string extension: extension of file to check
    :returns: boolean True if the file has the specified extension
    :raises FileNotFoundError: when file cannot be found
    """
    print("Check if file exists...")
    if os.path.isfile(filename):
        print("File exists.")
        extension = '.' + extension
        if filename.endswith(extension):
            print("File has extension " + extension + ".")
        else:
            return False
    else:
        raise FileNotFoundError

def get_filesize(filename):
    """
    Computes the size of a file in bytes, megabytes and gigabytes
    :string filename: name of file to calculate filesizes
    :returns: filesize in bytes, megabytes and gigabytes
    :raises FileNotFoundError: when file cannot be found
    """
    if os.path.isfile(filename):
        filesize_B = os.stat(filename).st_size
        filesize_MB = filesize_B / 1024
        filesize_GB = filesize_MB / 1024
        return filesize_B, filesize_MB, filesize_GB
    else:
        raise FileNotFoundError


def print_filesize(filename, unit):
    """
    Displays file sizes of a file in the given unit (Bytes, Megabytes, Gigabytes)
    :string filename: name of file to display file sizes
    :string unit: unit to display file sizes (if not given, all file sizes are printed)
    """
    filesize_B, filesize_MB, filesize_GB = get_filesize(filename)
    unit = unit.lower()
    if unit in ['b', 'bytes']:
        print("Filesize B: " + filesize_B)
    elif unit in ['mb', 'megabytes']:
        print("Filesize MB: " + filesize_MB)
    elif unit in ['gb', 'gigabytes']:
        print("Filesize GB: " + filesize_GB)
    if unit == '':
        print("Filesize B: " + filesize_B)
        print("Filesize MB: " + filesize_MB)
        print("Filesize GB: " + filesize_GB)
