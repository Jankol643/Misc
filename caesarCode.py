import sys # for exiting script
import os # for file path and size
from pyfiglet import Figlet  # import font library

# caesarCode.py
# 
# Created 30/04/2021
# Last edited 15/04/2021

# Setting standard variables
separator = '---------------------------------------------------------------'
errormsg = "Exiting script..."

"""
Prints the header in the defined font using pyfiglet
"""
def print_header():
    text = "CaesarCode"
    selectedFont = "Big"
    result = pyfiglet.figlet_format(text, font=selectedFont)
    print(result)

"""
checkTools
Checks if all tools required of the script are there
"""
def checkTools():
    requiredTools = ["pyfiglet"]
    for tool in requiredTools:
        if (is_tool(tool) == False):
            print("Required tool " + tool + "does not exist. Aborting")
            sys.exit(-1)

"""
is_tool
Check whether `name` is on PATH and marked as executable.
"""
def is_tool(name):
    from shutil import which
    
    if which(name) is not None:
        return True
    else:
        return False


def readCode():
    result = list()

    """
    askForFilepath
    Asks the user for a filepath using a GUI
    filetypeName: name of the file type
    extension: extension of the file
    return file: the file the user requested
    """
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
    outputFile = askForFilepath("Text files", "txt")
    
    """
    askForChiffre()
    Ask the user if file should be encrypted or decrypted
    """
    def askForChiffre():
        while True:
            data = input("Enter mode [encrypt or e/decrypt or d]")
            if data.lower() in ('encrypt', 'e'):
                print("Encrypting plain text file.")
                #statsgen $output -o passwords_masks
            elif data.lower() in ('decrypt', 'd'):
                print("Decrypting code file.")
                method = input("Enter method [b or bruteforce/m or manual]")
                if method.lower() in ('bruteforce', 'b'):
                    print("Decrypting the file with brute force")
                    return method
                elif method.lower() in ('manual', 'm'):
                    print("Encrypting code file manually")
                    encryptFileManually()
            if method.lower() and data.lower() not in ('encrypt', 'e', 'decrypt', 'd'):
                print("Not an appropriate choice.")
            if data.lower() not in ('encrypt', 'e', 'decrypt', 'd'):
                print("Not an appropriate choice.")
            else:
                break
        
    """
    readCodeFile
    Reads the code file specified
    file: file to be processed
    """
    def readCodeFile(file):

        """
        checkFile
        Checks if the file exists and is a non-empty text file
        filename: user specified file
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
                print("Start the script again with the correct file.")
                print(errormsg)
                sys.exit()

        with open(file):
            for line in file:
                processLine(line)
                print(separator)
    
    """
    processLine
    Process a line
    line: line to process
    """
    def processLine(line):
        decodeCaesarBruteForce(line)
    
    """
    decodeCaesarBruteForce
    Decodes a line with brute force trying all shifts of letters
    line: line to decode
    """
    def decodeCaesarBruteForce(line):
        letters = "abcdefghijklmnopqrstuvwxyz"
        x = 0
        while x < 26:
            x = x + 1 
            stringtodecrypt=line
            stringtodecrypt=stringtodecrypt.lower()
            ciphershift=int(x)
            stringdecrypted=""
            for character in stringtodecrypt:
                position = letters.find(character)
                newposition = position-ciphershift
                if character in letters:
                    stringdecrypted = stringdecrypted + letters[newposition]
                else:
                    stringdecrypted = stringdecrypted + character
                    
            ciphershift=str(ciphershift)
            print("i:",ciphershift, stringdecrypted)