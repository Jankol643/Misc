# Cleans special files

# Necessary imports
#import pyfiglet # for header
import sys # for getting maximum length of list
import os # for file checks
import subprocess # to calculate word count
#from tqdm import tqdm # needed for progress bar tqdm
import shutil # for copying files
from tkinter import Tk, filedialog # for selecting folder with GUI
from collections import OrderedDict # for Ordered dictionary
import operator # for sorting dict

# Setting standard variables
separator = "---------------------------------------------------------------"
keepHashes = 1

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big
def print_header():
    text = "cleanHashesSpecial"
    selectedFont = "Big"
    print(text, selectedFont)
    #result = pyfiglet.figlet_format(text, font = selectedFont )
    #print(result)

def askForFilepath():
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    open_dir = filedialog.askdirectory() # Returns opened path as str
    return open_dir
    print(separator)

def getSize(filename):
    st = os.stat(filename)
    filesizeB = st.st_size
    filesizeMB = filesizeB / 1024
    filesizeGB = filesizeMB / 1024
    return filesizeB, filesizeMB, filesizeGB

def processFolder(outputdir, filepath, listFile, dicFile, withCount):
    def createWorkDir(filepath):
        workdir = askForFilepath()
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        return workdir
            
    def moveFiles(filepath, workdir):
        # Loop through every file in directory
        for filename in os.listdir(filepath):
            counter += 1
            print("Copying file", counter, "of", noOfFiles, "called", filename)
            shutil.copy(filepath, workdir)
                    
    def processFiles(workdir):
        lineList = list()
        for filename in os.listdir(workdir):
            counter += 1
            print("Processing file", counter, "of", noOfFiles, "called", filename)
            filename = workdir + "/" + filename
            with open(filename, "r") as file:
                # Read each line of the file
                for line in file:
                    cleanedLine = cleanLine(line)
                    lineList.append(cleanedLine)
                    file.write(cleanedLine)
        return lineList
                    
    def cleanLine(line):
        splitString = line.split(" ")[1]
        if (keepHashes == 0):
            cleanedLine = splitString.split(":")[1]
            return cleanedLine
        else :
            cleanedLine = splitString
            return cleanedLine
    


    def writeListToFile(lineList, folderPath, listFile):
        print("Writing concatenated list to file")
        listFile = folderPath + "/" + listFile
        print("File", listFile)
        with open(listFile, 'w') as f: # creates the file if it does not exist
            for item in lineList:
                f.write("%s\n" % item)
        print(separator)
        return listFile
        
    def listToDict(lineList):
        print("Converting list to dictionary")
        freqDict = {} # Creating an empty dictionary 
        for item in lineList:
            if (item in freqDict):
                freqDict[item] += 1
            else:
                freqDict[item] = 1
        print(separator)
        return freqDict
    
    def sortDictByFreq(freqDict):
        print("Sorting dict by frequency")
        sortedDict = dict( sorted(freqDict.items(), key=operator.itemgetter(1),reverse=True))
        print(separator)
        return sortedDict
        
    def writeDicToFile(sortedDict, folderPath, dicFile, withCount):
        print("Writing dictionary to file")
        dicFile = folderPath + "/" + dicFile
        print("File", dicFile)
        with open(dicFile, "w") as f:
            if (withCount == 1):
                for key, value in sortedDict.items():
                    f.write(str(key))
                    f.write(" ")
                    f.write(str(value))
                    f.write("\n")
            else:
                for key in sortedDict:
                    f.write(str(key))
        return dicFile
        print(separator)
