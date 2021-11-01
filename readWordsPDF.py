# Extracts numbers delimited by a character from a text file
import sys

import tkinter
from tkinter import filedialog
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


def askForFilepath(filetypeName, extension):
    root = tkinter.Tk()  # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()  # Hides small tkinter window.
    # Opened windows will be active. above all windows despite of selection.
    root.attributes('-topmost', True)
    extension = '*.' + extension
    file = filedialog.askopenfile(
        mode='r', filetypes=[(filetypeName, extension)])
    if file is not None:
        return file
    else:
        raise FileNotFoundError


def readCode():
    
    code_lines = []
    def readCodeFile(file):
        for line in file:
            code_lines.append(line)
        file.close()

    codeFile = askForFilepath("Text files", "txt")
    readCodeFile(codeFile)
    pdfFile = askForFilepath("PDF files", "pdf")
    result = list()
    for line in code_lines:
        processCodeLine(line, pdfFile, result)
    print(result)


def processCodeLine(line, pdfFile, result):
    splitLine = line.split(".")
    page = (int)(splitLine[0])
    line = (int)(splitLine[1])
    word = (int)(splitLine[2])

    with pdfplumber.open(pdfFile.name) as pdf:
        word = processPDFLine(pdf, page, line, word)
        result.append(word)


def processPDFLine(pdf, page, line, word):
    try:
        pageN = pdf.pages[page-1]
        text = pageN.extract_text()
        lines = text.split('\n')
        found_line = lines[line - 1]
        words = found_line.split(' ')
        found_word = words[word - 1]
        return found_word
    except Exception:
        pass

def main():
    readCode()


main()
