# Extracts numbers delimited by a character from a text file
import sys
import pdfplumber

def checkTools():
    requiredTools = ["pdfplumber"]
    for tool in requiredTools:
        if (is_tool(tool) == False):
            print("Required tool " + tool + "does not exist. Aborting")
            sys.exit(-1)

def is_tool(name):
    # Check whether `name` is on PATH and marked as executable.
    from shutil import which
    
    if which(name) is not None:
        return True
    else:
        return False

def readCode():
    result = list()
    def askForFilepath(filetypeName, extension):
        root = Tk() # pointing root to Tk() to use it as Tk() in program.
        root.withdraw() # Hides small tkinter window.
        root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
        extension = '*.' + extension
        file = askopenfile(mode ='r', filetypes =[(filetypeName, extension)])
        if file is not None:
            return file
        else:
            print("File not found. Aborting")
            sys.exit(-1)
        
    codeFile = askForFilepath("Text files", "txt")
    pdfFile = askForFilepath("PDF files", "pdf")
    
    def readCodeFile(file):
        with open(file) as txt:
            for line in file:
                processLine(line)
                
    def processLine(line):
        def getWord(pdf, page, line, word):
            page = pdf.pages[page]
            lineString = page.extractText()
            lineArray = lineString.split(" ")
            word = lineArray[word-1]
        
        splitLine = line.split(".")
        page = splitLine[0]
        line = splitLine[1]
        word = splitLine[2]
        with pdfplumber.open(pdfFile) as pdf:
            word = getWord(pdf, page, line, word)
            result.append(word)
        return result