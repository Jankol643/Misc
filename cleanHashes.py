# Cleans special files

# Necessary imports
#import pyfiglet # for header
import sys # for getting maximum length of list
import os # for file checks
import subprocess # to calculate word count
#from tqdm import tqdm # needed for progress bar tqdm
import shutil # for copying files
from collections import OrderedDict # for Ordered dictionary
import operator # for sorting dict

import masterUtil

# Setting standard variables
keepHashes = 1

filename = masterUtil.askForFileOrDirectory('file', 'open', 'txt')
masterUtil.getSize(filename)

def processFolder(outputdir, filepath, listFile, dicFile, withCount, counter, noOfFiles):
    
    def moveFiles(filepath, workdir, counter):
        # Loop through every file in directory
        for filename in os.listdir(filepath):
            counter += 1
            print("Copying file", counter, "of", noOfFiles, "called", filename)
            shutil.copy(filepath, workdir)
    
    def processFiles(workdir, counter):
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
        masterUtil.printSeparator
        return listFile
        
    def listToDict(lineList):
        print("Converting list to dictionary")
        freqDict = {} # Creating an empty dictionary 
        for item in lineList:
            if (item in freqDict):
                freqDict[item] += 1
            else:
                freqDict[item] = 1
        masterUtil.printSeparator
        return freqDict
    
    def sortDictByFreq(freqDict):
        print("Sorting dict by frequency")
        sortedDict = dict( sorted(freqDict.items(), key=operator.itemgetter(1),reverse=True))
        masterUtil.printSeparator
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
        
        masterUtil.printSeparator
        return dicFile

    workdir = masterUtil.masterUtil.askForFileOrDirectory('folder')
    moveFiles(filepath, workdir, counter)
    lineList = processFiles(workdir, counter)
    folderPath = masterUtil.askForFileOrDirectory('folder', '', "")
    listFile = masterUtil.askForFileOrDirectory('file', 'save', 'txt')
    writeListToFile(lineList, folderPath, listFile)
    freqDict = listToDict(lineList)
    sortedDict = sortDictByFreq(freqDict)
    folderPath = masterUtil.askForFileOrDirectory('folder', '', '')
    dicFile = masterUtil.askForFileOrDirectory('file', 'save', 'txt')
    file = writeDicToFile(sortedDict, folderPath, dicFile, 1)