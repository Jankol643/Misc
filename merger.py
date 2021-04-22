#!/usr/bin/env python

"""
    This program merges and deduplicates all files in a folder
    Usage merger.sh
    Date 5/2/2021
    Author Jankol643
    Dependencies: wc (for counting words and file sizes), rm (for removing files), bc (for calculating)
"""

# Import local scripts
import mergerUtil as util

withCount = 1
listFile = "list.txt"
dicFile = "dic.txt"
outputDir = "output"

util.print_header()

copyright='(c) 2021 Jankol643'
print(copyright)

# TODO: Dependency check
# TODO: flags (CLI arguments)
# TODO: display tqdm progress bar for certain functions

#filename = sys.argv[1]

filepath = util.askForFilepath()
util.wordcount(outputDir, filepath, listFile, dicFile, withCount)
util.askUserAnalyse()