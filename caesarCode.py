import sys # for exiting script

# caesarCode.py
# 
# Created 30/04/2021
# Last edited 15/04/2021

def checkTools():
    requiredTools = ["pdfplumber"]
    for tool in requiredTools
        if (is_tool(tool) == False):
            print("Required tool " + tool + "does not exist. Aborting")
            sys.exit(-1)

def is_tool(name):
    # Check whether `name` is on PATH and marked as executable.
    from shutil import which
    
    if which(name) is not None
        return True
    else
        return False

def readCode():
    result = list()
    def askForFilepath(filetypeName, extension):
        root = Tk() # pointing root to Tk() to use it as Tk() in program.
        root.withdraw() # Hides small tkinter window.
        root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
        extension = '*.' + extension
        file = askopenfile(mode ='r', filetypes =[(filetypeName, extension)])
        if file is not None
            return file
        else
            print("File not found. Aborting")
            sys.exit(-1)
        
    codeFile = askForFilepath("Text files", "txt")
    outputFile = askForFilepath("Text files", "txt")
    
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
                    return method
            if method.lower() not in ('encrypt', 'e', 'decrypt', 'd'):
                print("Not an appropriate choice.")
            if data.lower() not in ('encrypt', 'e', 'decrypt', 'd'):
                print("Not an appropriate choice.")
            else:
                break
        
        
    def readCodeFile(file):
        with open(file) as txt:
            for line in file:
                processLine(line)
                
    def processLine(line):
        
    
    def decodeCaesarBruteForce():
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