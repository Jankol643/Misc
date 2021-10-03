"""
Various helper functions for file operations
Creation: 2021/10/03
"""

import masterUtil
import os
import sys
from tkinter import Tk, filedialog # for selecting folder with GUI

def file_len(fname):
    """
    Counts the number of lines of a file using enumerate
    :string fname: name of file
    :return noLines: number of lines in file
    """
    file = open_file(fname, 'r', False)
    for i, l in enumerate(fname):
        pass
        noLines = i + 1
    return noLines

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

def ask_file_or_directory(type, action, extension):
    """
    Asks the user to specify a file or a directory using a GUI
    :string type: type to do action on (file or directory)
    :string action: action to perform (open or save)
    :string extension: extension of file(s) to open
    :return var: path to file or directory
    :raises ValueError: wrong type or action
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
    masterUtil.print_separator('-', 80)
    return var

def open_file(filename, mode, empty):
    """
    Opens a file and returns it
    :string filename: name of file
    :string mode: in which mode to open file
    :boolean empty: if True file can be empty
    :returns: opened file
    :raises ValueError: mode is not allowed
    :raises EOFError: if empty is False and file is empty
    :raises OSError: file cannot be opened
    :raises FileNotFoundError: file cannot be found
    :raises Exception: filename is not a file
    """
    if os.path.isfile(filename):
        allowed_modes = ['r', 'w', 'x', 'a', 'b', 't', '+']
        if mode not in allowed_modes:
            raise ValueError("Mode is not allowed")
        try:
            file = open(filename, mode)
            if file_len(filename) == 0:
                if empty == False:
                    raise EOFError
            return file
        except OSError:
            raise OSError
        except FileNotFoundError:
            raise FileNotFoundError
    else:
        raise Exception("Specified file is not a file.")

def check_file_type(filename, extension):
    """
    Checks if the file exists and is a non-empty file with the specified extension
    :string filename: name of file to check
    :string extension: extension of file to check
    :returns: boolean True if the file has the specified extension
    :raises FileNotFoundError: file cannot be found
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

def read_file_to_list(filename):
    """
    Reads a file to a list
    :string filename: name of file
    :returns: list with file contents
    :raises Exception: file is too large for a single list
    """
    if file_len(filename) > sys.maxsize/8:
        raise Exception("File is too large to write to a single array.")
    else:
        list1 = list()
        file = open_file(filename, 'r', False)
        for line in file:
            list1.append(line)
        file.close()
        return list1

def count_words_file(filename):
    """
    Counts number of words in a file
    :string filename: name of file
    :returns: number of words in file
    """
    count = 0
    file = open_file(filename, 'r', True)
    for line in file:
        count += 1
    file.close()
    return count