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
withcount = 0 # if target dictionary should contain frequencies
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


def check_separated(lst, max_count):
    """
    Check if file lines are separated by colon

    :param lst: file lines
    :type lst: list
    :param max_count: number of lines to check
    :type max_count: integer
    :returns b: if file is properly separated
    :rtype: boolean
    """
    line_count = 0
    for line in lst:
        line_count = line_count + 1
        if line_count > max_count:
            break
        if ':' in line:
            splitted = line.split(':')
            if splitted[0] == '' and splitted[1] == '':
                return False
        else:
            return False
    return True


def write_words_to_dict(lst):
    """
    Writes the words to an empty dictionary and returns it
    """
    dict0 = {}  # Create an empty dictionary
    if check_separated(lst, 10) == True:
        for line in lst:  # Loop through each line of the file
            splitted = line.split(':')
            # Check if the word is already in dictionary
            if splitted[1] in dict0:
                # Increment count of word by 1
                dict0[splitted[1]] = dict0[splitted[1]] + 1
            else:
                # Add the word to dictionary with count 1
                dict0[splitted[1]] = 1
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


def write_dict_to_file(dict_sorted, original_file, delimiter, mode):
    """
    Writes the given dictionary to the given output file

    :param dict_sorted: sorted dictionary with words
    :type dict_sorted: dict
    :param original_file: path to file with unordered wordlist
    :type original_file: string
    :param delimiter: delimiter between words and counts
    :type delimiter: string
    :param mode: 1 words and frequencies, 2 print only words
    :type mode: int
    """
    print("Writing dictionary to output file...")
    if mode == 1:
        dic_output_file = "wcount.txt"
        final_path = os.path.dirname(original_file) + os.path.sep + dic_output_file
        wcount = open(final_path, "w")  # erasing all content in file
        print("Writing words with count")
        for key, val in dict_sorted.items():
            s = str(key) + delimiter + str(val)
            wcount.write(s + "\n")
        wcount.close()
    if mode == 2:
        words_output_file = "words.txt"
        final_path = os.path.dirname(original_file) + os.path.sep + words_output_file
        words = open(final_path, "w")  # erasing all content in file
        print("Writing words only")
        for val in dict_sorted.items():
            s = str(key)
            words.write(s + "\n")
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

    def calcSaved(filename, tempoutput):
        filesize_B_original = fileUtil.get_filesize(filename)
        filesize_B_output = fileUtil.get_filesize(tempoutput)

        difference = filesize_B_original - filesize_B_output
        if difference > 0:
            if difference >= 1000 and difference < 1000000:
                print("Cleaning saved " + str(difference/1000) + " MB")
            elif difference >= 1000000:
                print("Cleaning saved " + str(difference/1000000) + " GB")

    print("Calculating file size")
    if output == 1:  # call with output file
        calcSaved(filename, tempoutput)
    else:
        masterUtil.getSize(filename)
    stringUtil.print_separator(separating_char, separating_freq)


def PACK_analysis():
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
    if os.stat(filename).st_size > 0:
        print_info_wrapper(filename)
        lst = fileUtil.remove_empty_lines(filename, True)
        dict1 = write_words_to_dict(lst)
        dict_sorted = sort_dict_by_freq(dict1)
        write_dict_to_file(dict_sorted, filename, " ", 1)
        stringUtil.print_separator(separating_char, separating_freq)
    else:
        sys.exit("File is empty. Aborting")