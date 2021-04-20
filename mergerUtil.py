# Necessary imports
import os # for file checks
import subprocess # to calculate word count
from tqdm import tqdm # needed for progress bar tqdm
import shutil # for copying files
from tkinter import Tk, filedialog # for selecting folder with GUI
from collections import OrderedDict # import Ordered dictionary

# Setting standard variables
global separator='---------------------------------------------------------------'
global withcount = 0
listFile = "list.txt"
dicFile = "dic.txt"

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big
def print_header():
    text = "Merger"
    selectedFont = "Big"
    result = pyfiglet.figlet_format(text, font = selectedFont )
    print(result)

def askForFilepath():
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    open_dir = filedialog.askdirectory() # Returns opened path as str
    print(open_dir)
    return open_dir

def getSize(filename):
    st = os.stat(filename)
    filesizeB = st.st_size
    filesizeMB = filesizeB / 1024
    filesizeGB = filesizeMB / 1024
    return filesizeB, filesizeMB, filesizeGB

def wordcount(filepath, listFile, dicFile):
    def filesToList(filepath):
        print("Adding lines of files in folder", filepath, "to list")
        lineList = list()
        fileList = os.listdir(filepath)
        noOfFiles = len(fileList)
        counter = 0
        # Read every file in directory
        for filename in tqdm(os.listdir(filepath)):
            counter += 1
            print("Processing file", counter, "of", noOfFiles, "called", filename)
            with open(filename, "r") as f:
                # Read each line of the file
                for line in file:
                    lineList.append(line)
        return lineList
        
    def writeListToFile(lineList, listFile):
        print("Writing concatenated list to file")
        with open(listFile, 'w') as f: # creates the file if it does not exist
        for item in lineList:
            f.write("%s\n" % item)
        
    def listToDict(lineList):
        print("Converting list to dictionary")
        freqDict = {} # Creating an empty dictionary 
        for item in lineList:
            if (item in freq):
                freq[item] += 1
            else:
                freq[item] = 1
        return freqDict
    
    def sortDictByFrequency(freqDict):
        print("Sorting dict by frequency")
        sortedDict = dict( sorted(freqDict.items(), key=operator.itemgetter(1),reverse=True))
        return sortedDict
        
    def writeDicToFile(sortedDict, dicFile):
        with open(dicFile, "w") as f:
            if (withcount == 1):
                for key in sortedDict:
                    print(key, file=f)
            else:
                f.write( str(sortedDict) )
    
    def printStats(lineList, sortedDict, dicFile, listFile):
        noOfWordsDict = len(sortedDict)
        print("Dictionary consists of", noOfWordsDict, "words/entries")
        noOfWordsList = len(lineList)
        print("List consists of", noOfWordsList, "words/entries")
        duplicates = noOfWordsList - noOfWordsDict
        dupePercentage = duplicates / noOfWordsDict
        print("Duplicates", duplicates, "words,", "duplicate percentage", dupePercentage)
        dicFilesizeB, dicFilesizeMB, dicFilesizeGB = getSize(dicFile)
        dicFilesizeTxt = "Filesize of dictionary file is {} MB or {} GB".format(dicFilesizeMB, dicFilesizeGB)
        print(dicFilesizeTxt)
        listFilesizeB, listFilesizeMB, listFilesizeGB = getSize(listFile)
        listFilesizeTxt = "Filesize of list file is {} MB or {} GB".format(listFilesizeMB, listFilesizeGB)        
        savedStorageMB = listFilesizeMB - dicFilesizeMB
        savedStorageGB = listFilesizeGB - dicFilesizeGB
        savedStorageTxt = "Saved storage is {} MB or {} GB".format(savedStorageMB, savedStorageGB)
        
    lineList = filesToList(filepath)
    writeListToFile(lineList)
    DicOfLines = listToDict(lineList)
    sortedDict = sortDictByFreq(DicOfLines)
    printStats(lineList, sortedDict, dicFile, listFile)

def askUserAnalyse():
    while True:
        data = input("PACK analysis [y/n]")
        if data.lower() in ('y', 'yes'):
            print("Feeding the file to PACK for analysis")
            statsgen $output -o passwords_masks
            
        if data.lower() not in ('y', 'yes'):
            print("Not an appropriate choice.")
        else:
            break