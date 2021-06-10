#!/usr/bin/env python

# Necessary imports
from tkinter import Tk, filedialog # for selecting folder with GUI
import zipfile
import os
import time
#from tqdm import tqdm # needed for progress bar tqdm

def askForFilepath():
    root = Tk() # pointing root to Tk() to use it as Tk() in program.
    root.withdraw() # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
    open_dir = filedialog.askdirectory() # Returns opened path as str
    return open_dir

def loopExtractFiles(zipDirectory, targetDirectory):
    
    def extractFiles(zipDirectory, targetDirectory):

        def isSubset(fileListZip, fileListTarget):
            stringToAppend = '.zip'
            available = []
            available = [s + stringToAppend for s in fileListTarget]
            diff = []
            fileListTarget = set(fileListTarget)
            diff = [item for item in fileListZip if item not in fileListTarget]
            return diff

        fileListZip = os.listdir(zipDirectory)
        fileListZip.sort()
        fileListTarget = os.listdir(targetDirectory)
        fileListTarget.sort()
        
        noOfFilesTotal = len(fileListZip)
        fileCounter = 0 # number of current file
        faultyFiles = []
        excCounter = 0
        diff = isSubset(fileListZip, fileListTarget)
        noOfFilesUnprocessed = len(diff)
        tic = time.perf_counter()
        for filename in diff:   # loop through list of files
        #for file in tqdm(diff,noOfFiles):
            fileCounter += 1
            processingTxt = "Processing file {} of {} ({} in total) called {}"
            print(processingTxt.format(fileCounter, noOfFilesUnprocessed, noOfFilesTotal, filename))
            filename = zipDirectory + "/" + filename # full path to file (needed for extraction)
            if zipfile.is_zipfile(filename): # if it is a zipfile, extract it
                try:
                    with zipfile.ZipFile(filename) as item: # treat the file as a zip
                        item.extractall(targetDirectory)  # extract it
                        # os.remove(file_name) # delete zipped file
                except:
                    print("An error occured while processing", filename)
                    faultyFiles.append(filename)
                    
        toc = time.perf_counter()
        timeS = toc - tic
        return fileCounter, excCounter, faultyFiles, timeS

    def getInfoFromFolder(targetDirectory):
        print("getInfo", targetDirectory)
        fileList = os.listdir(targetDirectory)
        noOfFiles = len(fileList)
        lineSum = 0
        filesizeSumGB = 0

        def getLinesFromFile(targetDirectory, filename):
            filename = targetDirectory + "/" + filename
            lines = 0
            #https://stackoverflow.com/a/27518377/15316445
            f = open(filename)
            buf_size = 1024 * 1024
            read_f = f.read # loop optimization

            buf = read_f(buf_size)
            while buf:
                lines += buf.count('\n')
                buf = read_f(buf_size)

            return lines

        def getSizeOfFile(targetDirectory, filename):
            filename = targetDirectory + "/" + filename
            fileB = os.stat(filename).st_size
            fileGB = fileB / 1000000000
            return fileGB
        
        for filename in fileList:   # loop through list of files
        #for file in tqdm(fileList,noOfFiles):
            lineSum += getLinesFromFile(targetDirectory, filename)
            filesizeSumGB += getSizeOfFile(targetDirectory, filename)
        return lineSum,filesizeSumGB
        
        TODO: move faulty files to separate folder
        def printFaultyFiles(faultyFiles):
            noFaulty = len(faultyFiles)
            noFaultyText = "{} faulty files found"
            print(noFaultyText.format(noFaulty))
            for item in faultyFiles
                print(item)

    fileCounter, excCounter, faultyFiles, timeS = extractFiles(zipDirectory, targetDirectory)
    printFaultyFiles(faultyFiles)
    lineSum,filesizeSumGB = getInfoFromFolder(targetDirectory)

    return fileCounter, excCounter, faultyFiles, timeS, lineSum, filesizeSumGB
    
def printStatistics(fileCounter, excCounter, faultyFiles, timeS, lineSum, filesizeSumGB):
    extrPerS = timeS / fileCounter
    txt = "Unzipped {:,} zip files in {} seconds, averaging {} seconds per extraction"
    print(txt.format(fileCounter, timeS, extrPerS))
    linesPerFile = lineSum / fileCounter
    print("A file on average has", linesPerFile, "lines in it")
    print("The files in the folder are", filesizeSumGB, "GB big")
    averageSize = filesizeSumGB / fileCounter
    print("Average size of file in folder is", averageSize, "GB big")
    exc_text = "Of {} processed files {} or {:.2%} were faulty"
    excPercentage = excCounter / fileCounter
    print(exc_text.format(fileCounter, excCounter, excPercentage))
    
print("Directory with zip files")
zipDirectory = askForFilepath()

print("Directory to extract to")
targetDirectory = askForFilepath()

fileCounter, excCounter, faultyFiles, timeS, lineSum, filesizeSumGB = loopExtractFiles(zipDirectory, targetDirectory)
printStatistics(fileCounter, excCounter, faultyFiles, timeS, lineSum, filesizeSumGB)
