#!/usr/bin/env python
"""
This program reads a filename from STDIN and cleans the file
Script must be in same folder as specified file
Usage ./cleaner.py filename.txt
Date 28/3/2021
Author Jankol643
Dependencies: bc for calculation, time for measuring execution time, awk, wc
"""

# Necessary imports
import os  # for file checks
import shutil  # for copying files
import sys  # for terminating script
from operator import itemgetter
import stringUtil  # for commonly used functions
import masterUtil
import fileUtil

# from pyfiglet import Figlet  # import font library
# from tqdm import tqdm  # needed for progress bar tqdm

# Setting standard variables
tempoutput = "temp.txt"
defaultoutputdir = "cleaned"  # path to output directory
withcount = 0
nolines = 0
separating_char = '-'
separating_freq = 80


def print_info_wrapper(filename):
    """
    Prints general information about the file
    param filename: filename of file to analyze
    type filename: string
    """
    nolines = fileUtil.file_lines(filename)
    print("general information about the file")
    print("filename:", filename)
    print("No. of lines in file:", nolines)


def check_separated(filename):
    """
    Check if file lines are separated by colon

    :param filename: path to file
    :type filename: string
    :returns b: if file is properly separated
    :rtype: boolean
    """
    line_count = 0
    for line in filename:
        line_count = line_count + 1
        if line_count > 9:
            break
        if ':' in line:
            splitted = line.split(':')
            if splitted[0] == '' and splitted[1] == '':
                return False
        else:
            return False
    return True


def write_words_to_dict(filename):
    """
    Writes the words to an empty dictionary and returns it
    """
    dict0 = {}  # Create an empty dictionary
    if check_separated(filename) == True:
        for line in filename:  # Loop through each line of the file
            splitted = line.split(':')
            # Check if the word is already in dictionary
            if splitted[1] in dict0:
                # Increment count of word by 1
                dict0[splitted[0]] = dict0[splitted[0]] + 1
            else:
                # Add the word to dictionary with count 1
                dict0[line] = 1
    else:
        raise ValueError(
            "File is not properly separated. Only words are not allowed for now")
    return dict0


def sort_dict_by_freq(dict0):
    """
    Sorts the directionary by frequency of words
    """
    sorted_d = dict(sorted(dict0.items(), key=itemgetter(1), reverse=True))
    return sorted_d


def write_dict_to_file(dict_sorted, delimiter):
    """
    Writes the given dictionary to the given output file

    :param dict_sorted: [description]
    :type dict_sorted: [type]
    :param delimiter: [description]
    :type delimiter: [type]
    """
    print("Writing dictionary to output file...")
    dic_output_file = "wcount.txt"
    wcount = open(dic_output_file, "w")  # erasing all content in file
    print("Writing words with count")
    for key, val in dict_sorted.items():
        s = str(val) + delimiter + str(key)
        b = wcount.write(s)
    wcount.close()
    words_output_file = "words.txt"
    words = open(words_output_file, "w")  # erasing all content in file
    print("Writing words only")
    for val in dict_sorted.items():
        s = str(key)
        words.write(s)
    words.close()


def wordcount():
    """Counts lines before and after cleaning and saved lines"""
    print("Counting lines and duplicates")
    print("Number of lines original:", nolines)
    nolines_output = fileUtil.file_lines(tempoutput)
    print("Number of lines output:", nolines_output)
    lines_saved = nolines - nolines_output
    print("Lines saved", lines_saved)
    percentage_saved = lines_saved/nolines*100
    print('Cleaning deleted :0} lines and saved :1} % of total :2}'.format(
        lines_saved, percentage_saved, nolines))
    stringUtil.print_separator(separating_char, separating_freq)


def calculating_sizes(filename, output):
    print("Calculating file size")

    def calcSaved(filename, tempoutput):
        filesize_B_original = fileUtil.get_filesize(filename)
        filesize_B_output = fileUtil.get_filesize(tempoutput)

        difference = filesize_B_original - filesize_B_output
        if difference > 0:
            if difference >= 1000 and difference < 1000000:
                print("Cleaning saved " + str(difference/1000) + " MB")
            elif difference >= 1000000:
                print("Cleaning saved " + str(difference/1000000) + " GB")

    if output == 1:  # call with output file
        calcSaved(filename, tempoutput)
    else:
        masterUtil.getSize(filename)
    stringUtil.print_separator(separating_char, separating_freq)


def PACK_analysis(wocount):
    pack = input("PACK analysis [y/n]")
    if pack in ('y', 'Y', 'yes', 'Yes', 'YES'):
        print("Feeding the file to PACK for analysis")
        # statsgen wocount - o passwords_masks
        sys.exit()
    elif pack in ('n', 'N', 'no', 'No', 'NO'):
        print("Not analysing file.")
        sys.exit()


def copy_definite(filename, tempoutput):
    print("Copying file to final destination")
    # Filename with extension, without folder paths
    base = os.path.basename(filename)
    basename = os.path.splitext(base)[0]  # Filename without extension
    print("Checking if folder for files exists...")
    if not os.path.exists(basename):
        print("Creating folder for files")
        os.makedirs(basename)

    print("Setting parameters for copying.")
    original = tempoutput
    target = r'basename/base'
    print("Copying file to destination")
    shutil.move(original, target)


if __name__ == '__main__':
    filename = masterUtil.ask_file_or_directory('file', 'open', 'txt')
    dict1 = write_words_to_dict(filename)
    dict_sorted = sort_dict_by_freq(dict1)
    write_dict_to_file(dict_sorted, " ")
    stringUtil.print_separator(separating_char, separating_freq)
