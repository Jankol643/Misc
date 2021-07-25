#!/usr/bin/python
"""
This program reads a filename from STDIN and cleans the file
Script must be in same folder as specified file
Usage ./cleaner.py filename.txt
Date 28/3/2021
Author Jankol643
Dependencies: bc for calculation, time for measuring execution time, awk, wc
"""

# Import local scripts
import masterUtil
import cleanerUtil

cleanerUtil.print_header()

copyright='(c) 2021 Jankol643'
print(copyright)

# TODO: Dependency check
# TODO: display tqdm progress bar for certain functions

filename = masterUtil.askForFileOrDirectory('file', 'open', 'txt')
masterUtil.checkFile(filename)
cleanerUtil.print_info_wrapper(filename)
cleanerUtil.ordering(filename)
cleanerUtil.wordcount()
cleanerUtil.filesize(filename, 0)
cleanerUtil.filesize(filename, 1)
cleanerUtil.readfilepath()
