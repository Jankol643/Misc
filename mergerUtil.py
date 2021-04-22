#!/usr/bin/env python

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

# Print Header in ASCII Art
# https://github.com/pwaller/pyfiglet
# Font Big
def print_header():
    text = "Merger"
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

def wordcount(outputDir, filepath, listFile, dicFile, withCount):
    def filesToList(filepath):
        print("Adding lines of files in folder", filepath, "to list")
        lineList = list()
        fileList = os.listdir(filepath)
        noOfFiles = len(fileList)
        counter = 0
        # Read every file in directory
        for filename in os.listdir(filepath):
            counter += 1
            print("Processing file", counter, "of", noOfFiles, "called", filename)
            filename = filepath + "/" + filename
            print(filename)
            with open(filename, "r") as file:
                # Read each line of the file
                for line in file:
                    lineList.append(line)
                    
        if (len(lineList) > sys.maxsize):
            print("List is too large. Aborting")
            sys.exit(1)
        
        print(separator)
        return lineList

    def stripLinesFromList(lineList):
        print("Cleaning list")
        clean_List = []
        for element in lineList:
            clean_List.append(element.strip())
        return clean_List
    
    def createOutputFolder(filepath, outputDir):
        filepath = "C:/Users/Jan Kolnberger/Documents/Privat/Git"
        folderPath = filepath + "/" + outputDir
        print("Output folder path:", folderPath)
        if not os.path.exists(folderPath):
            print("Creating folder", outputDir, "in", filepath)
            os.makedirs(folderPath)
            print("New output folder:", folderPath)
        return folderPath

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
        
    def printStats(lineList, sortedDict, outputDir, dicFile, listFile):
        noOfWordsDict = len(sortedDict)
        print("Dictionary consists of", noOfWordsDict, "words/entries")
        noOfWordsList = len(lineList)
        print("List consists of", noOfWordsList, "words/entries")
        duplicates = noOfWordsList - noOfWordsDict
        dupePercentage = duplicates / noOfWordsList
        print("Duplicates", duplicates, "words,", "duplicate percentage", dupePercentage)
        dicFilesizeB, dicFilesizeMB, dicFilesizeGB = getSize(dicFile)
        dicFilesizeTxt = "Filesize of dictionary file is {} MB or {} GB".format(dicFilesizeMB, dicFilesizeGB)
        print(dicFilesizeTxt)
        listFilesizeB, listFilesizeMB, listFilesizeGB = getSize(listFile)
        listFilesizeTxt = "Filesize of list file is {} MB or {} GB".format(listFilesizeMB, listFilesizeGB)
        print(listFilesizeTxt)
        savedStorageMB = listFilesizeMB - dicFilesizeMB
        savedStorageGB = listFilesizeGB - dicFilesizeGB
        savedStorageTxt = "Saved storage is {} MB or {} GB".format(savedStorageMB, savedStorageGB)
        print(savedStorageTxt)
        
    lineList = filesToList(filepath)
    clean_List = stripLinesFromList(lineList)
    outputFolder = createOutputFolder(filepath, outputDir)
    listFile = writeListToFile(clean_List, outputFolder, listFile)
    DicOfLines = listToDict(clean_List)
    sortedDict = sortDictByFreq(DicOfLines)
    dicFile = writeDicToFile(sortedDict, outputFolder, dicFile, withCount)
    printStats(lineList, sortedDict, outputDir, dicFile, listFile)
    print(separator)
    
def askUserAnalyse():
    while True:
        data = input("PACK analysis [y/n]")
        if data.lower() in ('yes', 'y'):
            print("Feeding the file to PACK for analysis")
            #statsgen $output -o passwords_masks
        elif data.lower() in ('no', 'n'):
            print("Not feeding the file to PACK for analysis")
            sys.exit(0)
        if data.lower() not in ('y', 'yes', 'no', 'n'):
            print("Not an appropriate choice.")
        else:
            break