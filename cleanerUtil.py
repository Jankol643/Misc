# Necessary imports
import os  # for file checks
import shutil  # for copying files
import sys  # for terminating script
from operator import itemgetter

from pyfiglet import Figlet  # import font library
from tqdm import tqdm  # needed for progress bar tqdm

# Setting standard variables
separator = '---------------------------------------------------------------'
errormsg = "Exiting script..."
tempoutput = "temp.txt"
defaultoutputdir = "cleaned"  # path to output directory
withcount = 0
nolines = 0

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big

"""
Prints the header in the defined font using pyfiglet
"""
def print_header():
    text = "Cleaner"
    selectedFont = "Big"
    result = pyfiglet.figlet_format(text, font=selectedFont)
    print(result)

"""
Counts the number of lines of a files using enumerate
"""
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

"""
Checks if the file exists and is a non-empty text file
"""
def checkFile(filename):
    print("Check if file exists...")
    if os.path.isfile(filename):
        print("File exists.")
        if filename.endswith('.txt'):
            print("File is a text file.")
            if os.stat(filename).st_size > 0:
                print("File has some data")
            else:
                print("File is empty")
                print(errormsg)
                sys.exit()
        else:
            print("File is not a text file.")
            print(errormsg)
            sys.exit()
    else:
        print("File does not exist")
        print("Usage: ./cleaner.sh filename.txt")
        print(errormsg)
        sys.exit()

"""print_info_wrapper
Prints info about the file
"""
def print_info_wrapper(filename):

    nolines=file_len(filename)
    def print_info(filename):
        print("print general information about the file")
        print("filename:", filename)
        print("No. of lines in file:", nolines)
    print_info(filename)

"""
Function that handles ordering of the words
"""
def ordering(filename):
    dict0 = {}  # Create an empty dictionary

    """writeWordsToDict(filename)
    Writes the words to an empty dictionary and returns it
    """
    def writeWordsToDict(filename):
        for line in filename:  # Loop through each line of the file
            # Check if the word is already in dictionary
            if line in dict0:
                # Increment count of word by 1
                dict0[line] = dict0[line] + 1
            else:
                # Add the word to dictionary with count 1
                dict0[line] = 1
        return dict0

    dict = writeWordsToDict(filename)

    """
    Sorts the directionary by frequency of words
    """
    def sortDictByFreq(dict0):
        sorted_d = dict(
            sorted(dict0.items(), key=operator.itemgetter(1), reverse=True))
        return sorted_d

    dictSorted = sortDictByFreq(dict)

    # Writes the given dictionary to the given output file
    # Delimiter is required as an argument
    def writeDicToFile(dictSorted, delimiter):
        print("Writing dictionary to output file...")
        dicOutputFile = "wcount.txt"
        wcount = open(dicOutputFile, "w")  # erasing all content in file
        print("Writing words with count")
        for key, val in dictSorted.items():
            s = str(val) + delimiter + str(key)
            b = wcount.write(s)
        wcount.close()
        wordsOutputFile = "words.txt"
        words = open(wordsOutputFile, "w")  # erasing all content in file
        print("Writing words only")
        for val in dictSorted.items():
            s = str(key)
            words.write(s)
        words.close()

    writeDicToFile(dictSorted, " ")
    print(separator)

# Counts lines before and after cleaning and saved lines
def wordcount():
    print("Counting lines and duplicates")
    print("Number of lines original:", nolines)
    nolinesoutput = file_len(tempoutput)
    print("Number of lines output:", nolinesoutput)
    linessaved = nolines - nolinesoutput
    print("Lines saved", linessaved)
    percentagesaved = linessaved/nolines*100
    print('Cleaning deleted :0} lines and saved :1} % of total :2}'.format(
        linessaved, percentagesaved, nolines))
    print(separator)


def filesize(filename, output):

    def calculatingSizes(filename, output):
        print("Calculating file size")

        def calcNormal(filename):
            fileb = os.stat(filename).st_size
            print("Filesize B: " + fileb)
            filemb = fileb/1024
            print("Filesize MB: " + filemb)
            filegb = filemb/(1024 ** 2)  # ** is power operator
            print("Filesize GB: " + filegb)

        def calcOutput(tempoutput):
            print("Calculating file size of output file...")
            # filesize in bytes of output file
            filebout = calcNormal(filename).fileb
            filembout = calcNormal(filename).filemb
            filegbout = calcNormal(filename).filegb

        def calcSaved(tempoutput):
            savedmb = calcNormal(tempoutput).filemb - \
                calcOutput(tempoutput).filembout
            savedgb = calcNormal(tempoutput).filegb - \
                calcOutput(tempoutput).filegbout
            print('Cleaning saved :0} MB or :1} GB'.format(savedmb, savedgb))

        if output == 1:  # call with output file
            calcOutput(tempoutput)
            calcSaved()
        else:
            calcNormal(filename)

    print(separator)


def PACKAnalysis(wocount):
    pack = input("PACK analysis [y/n]")
    if pack in ('y', 'Y', 'yes', 'Yes', 'YES'):
        print("Feeding the file to PACK for analysis")
        #statsgen wocount - o passwords_masks
        print(errormsg)
        sys.exit()
    elif pack in ('n', 'N', 'no', 'No', 'NO'):
        print("Not analysing file.")
        print(errormsg)
        sys.exit()


def copyDefinite(filename, tempoutput):
    print("Copying file to final destination")
    # Filename with extension, without folder paths
    base = os.path.basename(filename)
    basename = os.path.splitext(base)[0]  # Filename without extension
    print("Checking if folder for files exists...")
    if not os.path.exists(basename):
        print("Creating folder for files")
        os.makeDirs(basename)

    print("Setting parameters for copying.")
    original = tempoutput
    target = r'basename/base'
    print("Copying file to destination")
    shutil.move(original, target)
