# Necessary imports
import os # for file checks
from tqdm import tqdm # needed for progress bar tqdm
import shutil # for copying files

# Setting standard variables
separator='---------------------------------------------------------------'
errormsg="Exiting script..."
tempoutput="temp.txt"
defaultoutputdir="cleaned" # path to output directory
withcount=0
nolines=0

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big
def print_header():
    text = "Cleaner"
    selectedFont = "Big"
    result = pyfiglet.figlet_format(text, font = selectedFont )
    print(result)

def checkFile(filename):
    print "Check if file exists..."
    if os.path.isfile(filename):
        print("File exists.")
        if filename.endswith('.txt'):
            print("File is a text file.")
            if os.stat(filename).st_size > 0
                print("File has some data")
            else
                print("File is empty")
                print(errormsg)
                sys.exit()
        else
            print("File is not a text file.")
            print(errormsg)
            sys.exit()
    else
        print("File does not exist")
        print("Usage: ./cleaner.sh filename.txt")
        print(errormsg)
        sys.exit()

def print_info_wrapper(filename):
    def print_info(filename):
        print("print general information about the file")
        print("filename:", filename)
        global nolines=file_len(filename)
        print("No. of lines in file:", nolines)

    def file_len(fname):
        with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

    print_info(filename)

def ordering(filename):
    # Create an empty dictionary
    dict0 = dict()
        
    def writeWordsToDict(filename):
        for line in text: # Loop through each line of the file
            # Check if the word is already in dictionary
            if line in dict0:
                # Increment count of word by 1
                dict0[line] = dict0[line] + 1
            else:
                # Add the word to dictionary with count 1
                dict0[line] = 1
        return dict0
    
    dict = writeWordsToDict(filename)
    
    def sortDictByFreq(dict0):
        sorted_d = dict( sorted(dict0.items(), key=operator.itemgetter(1),reverse=True))
        return sorted_d
        
    dictSorted = sortDictByFreq(dict)
    
    # Writes the given dictionary to the given output file
    # Delimiter is required as an argument
    def writeDicToFile(dictSorted, delimiter):
        print("Writing dictionary to output file...")
        wcount = open(wcount,"w") # erasing all content in file
        print("Writing words with count")
        for key,val in dictSorted.items(): 
           s = str(val) + delimiter + str(key)
           b = wcount.write(s)
        wcount.close()
        words = open(words,"w") # erasing all content in file
        print("Writing words only")
        for val in dictSorted.items():
            s = str(key)
            words.write(s)
        words.close()
    
    writeDicToFile(dictSorted, " ")
    print(separator)

def wordcount():
    print("Counting lines and duplicates")
    print("Number of lines original:", nolines)
    nolinesoutput = file_len(tempoutput)
    print("Number of lines output:", nolinesoutput)
    linessaved = nolines - nolinesoutput
    print("Lines saved", linessaved)
    percentagesaved = linessaved/nolines*100
    print('Cleaning deleted :0} lines and saved :1} % of total :2}'.format(linessaved, percentagesaved, nolines))
    print(separator)

def filesize(filename, output):

    def calculatingSizes(filename, output):
        print("Calculating file size")
        def calcNormal(filename):
            fileb  = os.stat(filename).st_size
            print("Filesize B: " + fileb)
            filemb = fileb/1024
            print("Filesize MB: " + filemb)
            filegb = filemb/(1024 ** 2) # ** is power operator
            print("Filesize GB: " + filegb)
        
        def calcOutput(tempoutput):
            print("Calculating file size of output file...")
            calcNormal(tempoutput)
            filebout = fileb # filesize in bytes of output file
            filembout = filemb
            filegbout = filegb

        def calcSaved():
            savedmb = filemb - filembout
            savedgb = filegb - filegbout
            print('Cleaning saved :0} MB or :1} GB'.format(savedmb, savedgb))
        
        if output == 1 : # call with output file
            calcOutput(tempoutput)
            calcSaved()
        else :
            calcNormal(fileName)
    
    print(separator)

def PACKAnalysis(wocount):
    pack = input("PACK analysis [y/n]")
    if pack in ('y', 'Y','yes', 'Yes', 'YES')
        print("Feeding the file to PACK for analysis")
        statsgen wocount -o passwords_masks
        print(errormsg)
        sys.exit()
    elif pack in ('n', 'N', 'no', 'No', 'NO')
        print("Not analysing file.")
        print(errormsg)
        sys.exit()

def copyDefinite(filename, tempoutput):
    print("Copying file to final destination")
    base = os.path.basename(filename) # Filename with extension, without folder paths
    basename = os.path.splitext(base)[0] # Filename without extension
    print("Checking if folder for files exists...")
    if not os.path.exists(basename) :
        print("Creating folder for files")
        os.makeDirs(basename)
        
    print("Setting parameters for copying.")
    original = tempoutput
    target = r'basename/base'
    print("Copying file to destination")
    shutil.move(original, target)