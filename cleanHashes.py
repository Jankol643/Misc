# Cleans special files

# import pyfiglet # for header
import os  # for file checks
# from tqdm import tqdm # needed for progress bar tqdm
import shutil  # for copying files
import operator  # for sorting dict

import masterUtil
import stringUtil  # for printing separator
import fileUtil  # for counting files in directory

WITH_HASHES = True
WITH_COUNT = True

filename = masterUtil.ask_file_or_directory('file', 'open', 'txt')


def moveFiles(filepath, workdir, no_files):
    """
    Copies files to temporary working directory

    :param filepath: original file path
    :type filepath: string
    :param workdir: path to working directory
    :type workdir: string
    :param no_files: number of files to copy
    :type no_files: int
    """
    # Loop through every file in directory
    counter = 0
    for filename in os.listdir(filepath):
        counter += 1
        print("Copying file", counter, "of", no_files, "called", filename)
        shutil.copy(filepath, workdir)


def processFiles(workdir):
    """
    Cleans all files in the working directory

    :param workdir: path to directory of files to process
    :type workdir: string
    :return: cleaned lines
    :rtype: list
    """
    line_list = list()
    counter = 0
    for filename in os.listdir(workdir):
        counter += 1
        print("Processing file", counter, "of", no_files, "called", filename)
        filename = workdir + os.path.sep + filename
        with open(filename, "r") as file:
            # Read each line of the file
            for line in file:
                cleaned_line = cleanLine(line)
                line_list.append(cleaned_line)
                file.write(cleaned_line)
    return line_list


def cleanLine(line):
    """
    Cleans a line

    :param line: line to clean
    :type line: string
    :return: cleaned line
    :rtype: string
    """
    split_string = line.split(" ")[1]
    if (WITH_HASHES is False):
        cleaned_line = split_string
    else:
        cleaned_line = split_string.split(":")[1]
    return cleaned_line


def write_list_to_file(line_list, folder_path, list_file):
    print("Writing concatenated list to file")
    list_file = folder_path + os.path.sep + list_file
    print("File", list_file)
    with open(list_file, 'w') as f:  # creates the file if it does not exist
        for item in line_list:
            f.write("%s\n" % item)
    stringUtil.print_separator('-', 80)
    return list_file


def list_to_dict(line_list):
    """
    Deduplicates a list and converts it to a dictionary with occurrences of list items

    :param line_list: list with duplicates
    :type line_list: list
    :return: dict with occurrences
    :rtype: dict
    """
    print("Converting list to dictionary")
    freq_dict = {}  # Creating an empty dictionary
    for item in line_list:
        if (item in freq_dict):
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    stringUtil.print_separator('-', 80)
    return freq_dict


def sort_dict_by_freq(freqDict):
    print("Sorting dict by frequency...")
    sortedDict = dict(
        sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True))
    stringUtil.print_separator('-', 80)
    return sortedDict


def write_dic_to_file(sorted_dict, folder_path, dict_file):
    print("Writing dictionary to file")
    dict_file = folder_path + os.path.sep + dict_file
    print("File", dict_file)
    with open(dict_file, "w") as f:
        if (WITH_COUNT is True):
            for key, value in sorted_dict.items():
                f.write(str(key) + " " + str(value) + '\n')
        else:
            for key in sorted_dict:
                f.write(str(key))

    stringUtil.print_separator('-', 80)
    return dict_file


filepath = masterUtil.ask_file_or_directory('folder')
no_files = fileUtil.count_files_directories(False, True, filepath)
workdir = masterUtil.ask_file_or_directory('folder')
moveFiles(filepath, workdir, no_files)
line_list = processFiles(workdir, no_files)
folder_path = masterUtil.ask_file_or_directory('folder')
list_file = masterUtil.ask_file_or_directory('file', 'save', 'txt')
write_list_to_file(line_list, folder_path, list_file)
freq_dict = list_to_dict(line_list)
sorted_dict = sort_dict_by_freq(freq_dict)
folder_path = masterUtil.ask_file_or_directory('folder', '', '')
dict_file = masterUtil.ask_file_or_directory('file', 'save', 'txt')
file = write_dic_to_file(sorted_dict, folder_path, dict_file)
