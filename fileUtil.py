"""
Various helper functions for file operations
Creation: 2021/10/03
"""

import stringUtil
import os
import sys
from tkinter import Tk, filedialog # for selecting folder with GUI
import linecache

def file_lines(file_path):
    """
    Counts the number of lines of a file using buffered count
    :string fname: path to file
    :return noLines: number of lines in file
    """
    if os.path.isfile(file_path):
        def _make_gen(reader):
            b = reader(2 ** 16)
            while b:
                yield b
                b = reader(2 ** 16)

        with open(file_path, "rb") as f:
            count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
        noLines = count + 1
        return noLines
    else:
        return 0

def get_filesize(file_path):
    """
    Computes the size of a file in bytes, megabytes and gigabytes
    :string file_path: path to file to calculate filesizes of
    :returns: filesize in bytes, megabytes and gigabytes
    :raises FileNotFoundError: when file cannot be found
    """
    if os.path.isfile(file_path):
        filesize_B = os.stat(file_path).st_size
        filesize_MB = filesize_B / 1024
        filesize_GB = filesize_MB / 1024
        return filesize_B, filesize_MB, filesize_GB
    else:
        raise FileNotFoundError

def ask_file_or_directory(type, action='', extension=''):
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
            var = filedialog.asksaveasfile_path(mode ='w', filetypes=['File', extension])
        else:
            raise ValueError("Action must be open or save.")
    else:
        raise ValueError("Type must be file or directory")
    stringUtil.print_separator('-', 80)
    return var

def open_file(file_path, mode, empty):
    """
    Opens a file and returns it
    :string file_path: path to file
    :string mode: in which mode to open file
    :boolean empty: if True file can be empty
    :returns: opened file
    :raises ValueError: mode is not allowed
    :raises EOFError: if empty is False and file is empty
    :raises OSError: file cannot be opened
    :raises FileNotFoundError: file cannot be found
    :raises Exception: file_path is not a file
    """
    if os.path.isfile(file_path):
        allowed_modes = ['r', 'w', 'w+', 'x', 'x+', 'a', 'a+', 'b', 't']
        if mode not in allowed_modes:
            raise ValueError("Mode is not allowed")
        try:
            file = open(file_path, mode)
            return file
        except OSError:
            raise OSError
        except FileNotFoundError:
            raise FileNotFoundError
    else:
        if mode not in ['w', 'w+', 'a', 'a+', 'x', 'x+']:
            raise Exception("Specified file is not a file.")
        else:
            file = open(file_path, mode)
            return file

def check_file_type(file_path, extension):
    """
    Checks if the file exists and is a non-empty file with the specified extension
    :string file_path: path to file
    :string extension: extension of file to check
    :returns: boolean True if the file has the specified extension
    :raises FileNotFoundError: file cannot be found
    """
    print("Check if file exists...")
    if os.path.isfile(file_path):
        print("File exists.")
        extension = '.' + extension
        if file_path.endswith(extension):
            print("File has extension " + extension + ".")
        else:
            return False
    else:
        raise FileNotFoundError

def print_filesize(file_path, unit):
    """
    Displays file sizes of a file in the given unit (Bytes, Megabytes, Gigabytes)
    :string file_path: path to file of which to display file sizes
    :string unit: unit to display file sizes (if not given, all file sizes are printed)
    """
    filesize_B, filesize_MB, filesize_GB = get_filesize(file_path)
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

def read_file_to_list(file_path):
    """
    Reads a file to a list
    :string file_path: name of file
    :returns: list with file contents
    :raises Exception: file is too large for a single list
    """
    if file_lines(file_path) > sys.maxsize/8:
        raise Exception("File is too large to write to a single list.")
    else:
        list1 = list()
        file = open_file(file_path, 'r', False)
        for line in file:
            list1.append(line)
        file.close()
        return list1

def count_words_file(file_path):
    """
    Counts number of words in a file
    :string file_path: path to file
    :returns: number of words in file
    """
    count = 0
    file = open_file(file_path, 'r', True)
    for line in file:
        count += 1
    file.close()
    return count

def access_file_line(file_path, line_number, action, big_file, text = ''):
    """
    Performs an action at the specified line of the specified file 
    :string file_path: name of file
    :int line_number: line to access
    :char action: action to perform
    :boolean big_file: true if file is a big file (optimised line access)
    :string text: text to write to file
    :returns: contents of line
    :raises ValueError: wrong action
    :raises ValueError: line_number cannot be found
    """
    line_count = 1
    file = open_file(file_path, 'r', False)
    if big_file == True:
        with open("file") as fp:
            for i, line in enumerate(fp):
                if i == line_number + 1:
                    return line
    else:
        if action == 'r':
            return linecache.getline(file_path, line_number)
        elif action == 'w':
            for line in file:
                line_count += 1
                if line_count == line_number:
                    line = text
                    file.close()
        else:
            raise ValueError("Action must be 'r' or 'w'.")

def create_file_folder(folder_path, n=0, from_file=False, namepath=None):
    """
    Creates files in given folder
    :string folder_path: directory in which to create files
    :int n: number of files to create
    :boolean from_file: if filenames should be read from file
    :string namepath: path to file with filenames
    """
    if not (os.path.isdir(folder_path)):
        try:
            os.makedirs(folder_path)
        except OSError:
            raise OSError
    
    if (n == 0 and from_file == False):
        raise ValueError("n or from_file must be specified")
    if (from_file == True and namepath == None):
        raise ValueError("Namepath must be specified when using from_file")

    errors = list()

    if from_file == True:
        filelist = read_file_to_list(namepath)
        for name in filelist:
            name = name.strip()
            if "." not in name:
                raise ValueError("File extension missing")
            final_path = os.path.join(folder_path, name)
            try:
                fp = open(final_path, 'x')
            except Exception:
                errors.append(final_path)
            fp.close()

    if from_file == False:
        for i in range(0, n):
            file_name = str(i) + ".txt"
            final_path = os.path.join(folder_path, file_name)
            try:
                fp = open(final_path, 'x')
            except Exception:
                errors.append(final_path)
            fp.close()

    if len(errors) > 0:
        print("Errors occured.")
        print(errors)

def get_dir_size(start_path = '.'):
    """
    Prints the total size of all files and folders in a directory
    :string start_path: directory to search (default: current directory)
    :returns: total file size
    """
    total_size = 0
    if 'scandir' in dir(os):
        # using fast 'os.scandir' method (new in version 3.5)
        for entry in os.scandir(start_path):
            if entry.is_dir(follow_symlinks = False):
                total_size += get_dir_size(entry.path)
            elif entry.is_file(follow_symlinks = False):
                total_size += entry.stat().st_size
    else:
        # using slow, but compatible 'os.listdir' method
        print (start_path)
        for entry in os.listdir(start_path):
            full_path = os.path.abspath(os.path.join(start_path, entry))
            if os.path.isdir(full_path):
                total_size += get_dir_size(full_path)
            elif os.path.isfile(full_path):
                total_size += os.path.getsize(full_path)
    return total_size

def filesizes_dir():
    directory_path = ask_file_or_directory('directory')
    """
    Gets a list of files and corresponding filesizes for a given directory
    :returns: list with file names and file sizes
    """
    files_list = list()
    no_files = 0

    if 'scandir' in dir(os):
        for entry in os.scandir(directory_path):
            no_files += 1
            if (no_files > sys.maxsize/8):
                raise Exception("Too many files in chosen directory. Maximum is " + sys.maxsize/8)
            files_list.append(entry)
    else:
        for entry in os.listdir(directory_path):
            full_path = os.path.abspath((os.path.join(directory_path, entry)))
            if (no_files > sys.maxsize/8):
                raise Exception("Too many files in chosen directory. Maximum is " + sys.maxsize/8)
            files_list.append(full_path)

    # Create a dict of files in directory along with the size
    filesize_dict = {}

    for file in files_list:
        filesize = os.stat(os.path.join(directory_path, file)).st_size
        filesize_dict[file] = filesize

    return filesize_dict

def count_files_directories(gui, recursive, dir_path=''):
    """
    Counts files and directories of a given folder
    :boolean gui: if GUI should be used to select folder
    :boolean recursive: if count should include subfolders
    :string dir_path: path to folder if no GUI is used
    :returns: number of files and directories
    """
    if gui == True:
        dir = ask_file_or_directory('directory')
    else:
        if dir_path is None:
            raise ValueError("When using arguments, dir_path must be used")
        if not os.path.isdir(dir_path):
            raise ValueError("dir_path must be valid")
        dir = dir_path
    
    if recursive not in [True, False]:
        raise ValueError("Recursive must be True or False")
    
    no_files = 0
    no_dirs = 0

    if recursive == True:
        if 'scandir' in dir(os):
            lst = list(os.scandir(dir))
            for x in lst:
                if os.path.isfile(x):
                    no_files += 1
                elif os.path.isdir(x):
                    no_dirs += 1
        else:
            for root, directories, files in os.walk(dir):
                for file in files:
                    no_files += 1
                for dir in directories:
                    no_dirs += 1
    else:
        lst = list(os.listdir(dir))
        sorted_list = sorted(lst)
        for x in sorted_list:
            file_path = os.path.join(dir, x)
            if os.path.isfile(file_path):
                no_files += 1
            elif os.path.isdir(file_path):
                no_dirs += 1

    return no_files, no_dirs

def filetypes_path_dir(gui, recursive, extension_list, dir_path=''):
    """
    Gets a list of file paths with a given extension in a directory
    :boolean gui: if GUI should be used to select folder
    :boolean recursive: if directory should be searched recursively
    :list extension_list: list with file extensions
    :string dir_path: path to folder if no GUI is used
    :returns: list with file paths, None if empty
    """
    if gui == True:
        directory_path = ask_file_or_directory('directory')
    else:
        if dir_path is None:
            raise ValueError("When using arguments, dir_path must be used")
        if not os.path.isdir(dir_path):
            raise ValueError("dir_path must be valid")
        directory_path = dir_path
    
    if recursive not in [True, False]:
        raise ValueError("Recursive must be True or False")

    path_list = list()

    def split_add(x, extension_list):
        arr = x.split('/')
        filename = arr[-1]
        root, extension = os.path.splitext(filename)
        extension = extension[1:]
        if extension in extension_list:
            path_list.append(x)
        
    if recursive == True:
        if 'scandir' in dir(os):
            lst = list(os.scandir(directory_path))
            print(lst)
            for x in lst:
                x = x.path
                x = x.replace('\\', '/')
                if os.path.isfile(x):
                    split_add(x, extension_list)
        else:
            for root, directories, files in os.walk(directory_path):
                for file in files:
                    split_add(file, extension_list)
    else:
        lst = list(os.listdir(directory_path))
        sorted_list = sorted(lst)
        for x in sorted_list:
            file_path = os.path.join(directory_path, x)
            file_path = file_path.replace('\\', '/')
            if os.path.isfile(file_path):
                split_add(file_path, extension_list)

    if len(path_list) > 0:
        return path_list
    else:
        return None

def remove_spaces_filename_folder(gui, recursive, dir_path=''):
    """
    Removes spaces from filenames in a folder
    :boolean gui: if GUI should be used to select folder
    :boolean recursive: if directory should be searched recursively
    :list extension_list: list with file extensions
    :string dir_path: path to folder if no GUI is used
    :returns: list with file paths, None if empty
    """
    if gui == True:
        directory_path = ask_file_or_directory('directory')
    else:
        if dir_path is None:
            raise ValueError("When using arguments, dir_path must be used")
        if not os.path.isdir(dir_path):
            raise ValueError("dir_path must be valid")
        directory_path = dir_path
    
    if recursive not in [True, False]:
        raise ValueError("Recursive must be True or False")

    def remove_spc(x):
        for char in x:
            if char == " ":
                x.replace(char, " ")
        
    if recursive == True:
        if 'scandir' in dir(os):
            lst = list(os.scandir(directory_path))
            print(lst)
            for x in lst:
                x = x.path
                x = x.replace('\\', '/')
                if os.path.isfile(x):
                    remove_spc(x)
        else:
            for root, directories, files in os.walk(directory_path):
                for file in files:
                    remove_spc(file)
    else:
        lst = list(os.listdir(directory_path))
        sorted_list = sorted(lst)
        for x in sorted_list:
            file_path = os.path.join(directory_path, x)
            file_path = file_path.replace('\\', '/')
            if os.path.isfile(file_path):
                remove_spc(x)