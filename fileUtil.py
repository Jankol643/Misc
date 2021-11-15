"""
Various helper functions for file operations
Creation: 2021/10/03
"""

import os
import sys

import masterUtil

import linecache
from pathlib import Path
from itertools import islice
import datetime
import random
import re


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
    Computes the size of a file in bytes
    :string file_path: path to file to calculate filesizes of
    :returns: filesize in bytes
    :raises FileNotFoundError: when file cannot be found
    """
    if os.path.isfile(file_path):
        filesize_B = os.stat(file_path).st_size
        return filesize_B
    else:
        raise FileNotFoundError


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
    allowed_modes = ['r', 'w', 'w+', 'x', 'x+', 'a', 'a+', 'b', 't']
    if mode not in allowed_modes:
        raise ValueError("Mode is not allowed")
    if os.path.isfile(file_path):
        if (empty == False and get_filesize(file_path) == 0):
            raise EOFError
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
        filename, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:]
        if file_extension == extension:
            return True
        else:
            return False
    else:
        raise FileNotFoundError


def print_filesize(file_path, unit="all"):
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
    if unit == '' or unit == "all":
        print("Filesize B: " + filesize_B)
        print("Filesize MB: " + filesize_MB)
        print("Filesize GB: " + filesize_GB)


def read_file_to_list(file_path, no_newlines):
    """
    Reads a file to a list
    :string file_path: name of file
    :boolean no_newlines: True if newline character should be stripped from list
    :returns: list with file contents
    :raises Exception: file is too large for a single list
    """
    if file_lines(file_path) > sys.maxsize/8:
        raise Exception("File is too large to write to a single list.")
    else:
        list1 = list()
        file = open_file(file_path, 'r', False)
        for line in file:
            if no_newlines == True:
                line = line.rstrip('\n')
                list1.append(line)
            else:
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


def access_file_line(file_path, line_number, action, big_file, empty, text=''):
    """
    Performs an action at the specified line of the specified file 
    :string file_path: name of file
    :int line_number: line to access
    :char action: action to perform
    :boolean big_file: true if file is a big file (optimised line access)
    :boolean empty: if file can be empty
    :string text: text to write to file
    :returns: contents of line
    :raises ValueError: wrong action
    :raises ValueError: line_number cannot be found
    """
    if file_path == '' or line_number <= 0 or big_file not in [True, False] or empty not in [True, False]:
        raise ValueError("Input not correct.")
    if action == 'r' and line_number > file_lines(file_path):
        raise ValueError("File does not have that many lines.")

    text = str(text)
    line_count = 1
    if big_file == True:
        if action == 'r':
            with open(file_path, 'r') as fp:
                for i, line in enumerate(fp):
                    if i == line_number + 1:
                        return line
        elif action == 'w':
            with open(file_path, 'w') as fp:
                for line in fp:
                    line_count += 1
                    if line_count == line_number:
                        line = text
        else:
            raise ValueError("Action must be 'r' or 'w'.")
    else:
        if action == 'r':
            return linecache.getline(file_path, line_number)
        elif action == 'w':
            file = open_file(file_path, 'w', True)
            if line_number > 1:
                for line in file:
                    line_count += 1
                    if line_count == line_number:
                        line = text
                file.close()
            else:  # only one line in file
                file.write(text)
        else:
            raise ValueError("Action must be 'r' or 'w'.")


def create_file_folder(gui, n=0, file_extensions=['txt'], from_file=False, namepath=None, folder_path=None):
    """
    Creates files in given folder
    :boolean gui: if gui should be used to select folder
    :int n: number of files to create
    :list file_extensions: list of file extensions to choose from (without dot)
    :boolean from_file: if filenames should be read from file
    :string namepath: path to file with filenames
    :string folder_path: directory in which to create files (if no gui is used)
    """

    if (from_file not in [True, False]):
        raise ValueError("from_file must be true or false")
    if (n == 0 and from_file == False):
        raise ValueError("n or from_file must be specified")
    if (from_file == True and namepath == None):
        raise ValueError("Namepath must be specified when using from_file")
    if (gui == False and folder_path == None):
        raise ValueError(
            "When gui is not used, path to folder must be specified")

    if (gui == True):
        folder_path = masterUtil.ask_file_or_directory('directory')

    if not (os.path.isdir(folder_path)):
        try:
            os.makedirs(folder_path)
        except OSError:
            raise OSError
    errors = list()

    if from_file == True:
        filelist = read_file_to_list(namepath)
        for name in filelist:
            name = name.strip()
            final_path = os.path.join(folder_path, name)
            if "." not in name:  # file extension missing
                errors.append(final_path)
            try:
                fp = open(final_path, 'x')
            except Exception:
                errors.append(final_path)
            fp.close()

    if from_file == False:
        for i in range(0, n):
            file_ext = random.choice(file_extensions)
            file_name = str(i) + '.' + file_ext
            final_path = os.path.join(folder_path, file_name)
            try:
                fp = open(final_path, 'x')
            except Exception:
                errors.append(final_path)
            fp.close()

    if len(errors) > 0:
        print("Errors occured.")
        print(errors)


def get_dir_size(start_path='.'):
    """
    Prints the total size of all files and folders in a directory
    :string start_path: directory to search (default: current directory)
    :returns: total file size
    """
    total_size = 0
    if 'scandir' in dir(os):
        # using fast 'os.scandir' method (new in version 3.5)
        for entry in os.scandir(start_path):
            if entry.is_dir(follow_symlinks=False):
                total_size += get_dir_size(entry.path)
            elif entry.is_file(follow_symlinks=False):
                total_size += entry.stat().st_size
    else:
        # using slow, but compatible 'os.listdir' method
        print(start_path)
        for entry in os.listdir(start_path):
            full_path = os.path.abspath(os.path.join(start_path, entry))
            if os.path.isdir(full_path):
                total_size += get_dir_size(full_path)
            elif os.path.isfile(full_path):
                total_size += os.path.getsize(full_path)
    return total_size


def filesizes_dir():
    """
    Gets a dict of files and corresponding filesizes for a given directory
    :returns: dict with file names and file sizes
    """
    files_list = list()
    no_files = 0
    directory_path = masterUtil.ask_file_or_directory('directory')

    if 'scandir' in dir(os):
        for entry in os.scandir(directory_path):
            path = entry.path()
            no_files += 1
            if (no_files > sys.maxsize/8):
                raise Exception(
                    "Too many files in chosen directory. Maximum is " + sys.maxsize/8)
            files_list.append(path)
    else:
        for entry in os.listdir(directory_path):
            full_path = os.path.abspath((os.path.join(directory_path, entry)))
            if (no_files > sys.maxsize/8):
                raise Exception(
                    "Too many files in chosen directory. Maximum is " + sys.maxsize/8)
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
        dir = masterUtil.ask_file_or_directory('directory')
    else:
        if dir_path == '':
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
    Gets a list of file paths of non-empty files with a given extension in a directory
    :boolean gui: if GUI should be used to select folder
    :boolean recursive: if directory should be searched recursively
    :list extension_list: list with file extensions (if empty return all files)
    :string dir_path: path to folder if no GUI is used
    :returns: list with file paths
    """
    if gui == True:
        directory_path = masterUtil.ask_file_or_directory('directory')
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
        """
        Checks if the extension of x is in the extension list
        if true, append to result
        if extension list is empty, append to result
        :string x: path of file to check
        :list extension_list: list with file extensions
        """
        if get_filesize(x) < 0:
            pass
        else:
            arr = x.split('/')
            filename = arr[-1]
            root, extension = os.path.splitext(filename)
            extension = extension[1:]
            if len(extension_list) > 0:
                if extension in extension_list:
                    path_list.append(x)
            else:  # extension list is empty
                path_list.append(x)

    if recursive == True:
        if 'scandir' in dir(os):
            lst = list(os.scandir(directory_path))
            if len(lst) == 0:
                return lst
            for x in lst:
                a = x.path
                a = a.replace('\\', '/')
                if os.path.isfile(x):
                    split_add(a, extension_list)
        else:
            for root, directories, files in os.walk(directory_path):
                for file in files:
                    split_add(file, extension_list)
    else:
        lst = list(os.listdir(directory_path))
        if len(lst) == 0:
            return lst
        sorted_list = sorted(lst)
        for x in sorted_list:
            file_path = os.path.join(directory_path, x)
            file_path = file_path.replace('\\', '/')
            if os.path.isfile(file_path):
                split_add(file_path, extension_list)

    return path_list


def remove_characters_filename_folder(gui, recursive, chars_to_remove, dir_path=''):
    """
    Remove characters from filenames in a folder

    :param gui: if a GUI should be used to select the folder
    :type gui: boolean
    :param recursive: search for file recursively
    :type recursive: boolean
    :param chars_to_remove: list of characters to remove the
    :type chars_to_remove: list
    :param dir_path: path to folder to clean if no GUI is used, defaults to ''
    :type dir_path: str, optional
    :raises ValueError: if no GUI is used and dir_path is empty
    :raises ValueError: if dir_path is invalid
    :raises ValueError: if recursive is not a boolean
    :raises ValueError: if list of characters is empty or contains whitespaces
    """
    if gui == True:
        directory_path = masterUtil.ask_file_or_directory('directory')
    else:
        if dir_path is None:
            raise ValueError("When using arguments, dir_path must be used")
        if not os.path.isdir(dir_path):
            raise ValueError("dir_path must be valid")
        directory_path = dir_path

    if recursive not in [True, False]:
        raise ValueError("Recursive must be True or False")
    if (len(chars_to_remove) < 1) or masterUtil.check_list_empty(chars_to_remove) is True:
        raise ValueError("List is empty or contains whitespaces.")

    def remove_char(x):
        for char in x:
            if char in chars_to_remove:
                x.replace(char, '')

    if recursive == True:
        if 'scandir' in dir(os):
            lst = list(os.scandir(directory_path))
            for x in lst:
                x = x.path
                if os.path.isfile(x):
                    remove_char(x)
        else:
            for _, _, files in os.walk(directory_path):
                for file in files:
                    remove_char(file)
    else:
        lst = list(os.listdir(directory_path))
        sorted_list = sorted(lst)
        for x in sorted_list:
            file_path = os.path.join(directory_path, x)
            if os.path.isfile(file_path):
                remove_char(x)


def tree(level=-1, limit_to_directories=False, length_limit=1000):
    """
    Given a directory Path object print a visual tree structure
    :int level: maximum display depth of directory tree
    :boolean limit_to_directories: if true only directories are shown
    :int length_limit: limit iteration so editor is not full of text
    """
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '
    dir_path = masterUtil.ask_file_or_directory('directory')
    dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0

    def inner(dir_path: Path, prefix: str = '', level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' +
          (f', {files} files' if files else ''))


def last_modified_files(n):
    """
    Returns the file paths of the n last modified files in a folder
    :int n: number of files to return
    :returns: file paths of last n modified files
    """
    file_list = filetypes_path_dir(True, False, [])
    last_modified = list()
    for i in range(0, len(file_list)):
        time = os.stat(file_list[i]).st_mtime
        dt = datetime.datetime.fromtimestamp(time)
        last_modified.append(dt)

    sorted_list = sorted(last_modified, reverse=True)
    result = sorted_list[0:n]  # returns first n elements
    return result


def prepend_file(file_path, string):
    """
    Prepends a file with a given string
    :str filepath: file to prepend to
    :str string: string to prepend
    """
    lines = list()
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line)
    string = string + '\n'
    lines.insert(0, string)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)


def write_shebang(file_path, version):
    """
    Prepends file with python shebang for the given version
    :string file_path: path to python file
    :int version: python version of file, 2 or 3
    """
    print("Writing shebang to file" + file_path)
    shebang = '#!/usr/bin/env python' + str(version)
    # delete wrong shebangs
    lines = list()
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line)
    shebang_newline = shebang + '\n'
    for line in lines:
        index = lines.index(line)
        if index < 10:
            if line.startswith('#!') and line != shebang_newline:
                lines.remove(line)
    lines.insert(0, shebang_newline)  # insert correct shebang

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
    print("Successfully written shebang to file.")


def uncommented_imports(file_path):
    """
    Print line number and imports if they are not commented
    :string file_path: file to search
    """
    file_lines = list()
    uncommented_imports = dict()
    # matches #, zero or more spaces and characters thereafter
    regex = re.compile('# *\w+')
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            file_lines.append(line)
    for line in file_lines:
        match = re.search(regex, line)
        if 'import' in line and match is None:
            index = file_lines.index(line) + 1
            uncommented_imports.update({index: line})
    if len(uncommented_imports) > 0:
        print("Uncommented imports:")
        for key, value in uncommented_imports.items():
            print(str(key) + ":" + value)


def relative_to_absolute_path(file_path):
    """
    Transforms a relative path to an absolute path

    :param file_path: relative path to convert
    :type file_path: string
    :return: absolute path
    :rtype: string
    """
    final_path = ''
    current_path = os.path.dirname(os.path.realpath(__file__))
    splitted = current_path.split(os.path.sep)
    no_points = file_path.count('..')
    count = len(splitted) - no_points
    splitted = splitted[:count]
    splitted_filepath = file_path.split(os.path.sep)
    filename = splitted_filepath[-1]
    regexPattern = re.compile('(?<!\.)\.(?!\.)')  # matches single dot
    no_points_filename = len(regexPattern.findall(filename))
    no_single_points = len(regexPattern.findall(file_path))
    count = no_points + no_single_points - no_points_filename
    splitted_filepath = splitted_filepath[count:]
    final_path_list = splitted + splitted_filepath
    string = ''
    for elem in final_path_list:
        if final_path_list.index(elem) == len(final_path_list)-1:
            string += elem
        else:
            string += elem + os.path.sep
    final_path = string
    return final_path
