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
from cleanerUtil import * as util

util.print_header()

copyright='(c) 2021 Jankol643'
print(copyright)

# TODO: Dependency check
# TODO: flags (CLI arguments)
# TODO: file names (check CopyDefinite)
# TODO: display tqdm progress bar for certain functions

filename = sys.argv[1]

util.checkFile(filename)
util.print_info_wrapper(filename)
util.ordering(filename)
util.wordcount()
util.filesize(filename, 0)
util.filesize(filename, 1)
util.readfilepath()
