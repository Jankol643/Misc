import sys # for exiting script
import os # for file path and size
from pyfiglet import Figlet  # import font library

import masterUtil

# caesarCode.py
# 
# Created 30/04/2021
# Last edited 15/04/2021

# Setting standard variables
alphabet = "abcdefghijklmnopqrstuvwxyz"

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

codeFile = masterUtil.askForFileOrDirectory("file", "open", "txt")
outputFile = masterUtil.askForFileOrDirectory("file", "save", "txt")

"""
askForAction()
Ask the user if file should be encrypted or decrypted
"""
def askForAction():
    while True:
        data = input("Enter mode [encrypt or e/decrypt or d]")
        if data.lower() in ('encrypt', 'e'):
            print("Encrypting plain text file.")#
            s = int(input("Enter the shift to encrypt the text with: "))
            method = 'e'
        elif data.lower() in ('decrypt', 'd'):
            print("Decrypting code file.")
            method = input("Enter method [b or bruteforce/m or manual]")
            if method.lower() in ('bruteforce', 'b'):
                print("Decrypting the file with brute force")
                method = 'd-b'
            elif method.lower() in ('manual', 'm'):
                print("Decrypting code file manually")
                method = 'd-m'
            
        if method.lower() not in ('bruteforce', 'b', 'manual', 'm'):
            print("Not an appropriate choice.")
        if data.lower() not in ('encrypt', 'e', 'decrypt', 'd'):
            print("Not an appropriate choice.")
        return method
    
"""
readCodeFile
Reads the code file specified
file: file to be processed
"""
def readCodeFile(file, s):
    file = masterUtil.askForFileOrDirectory('file', 'open', 'txt')
    with open(file):
        for line in file:
            processLine(line, s)
        masterUtil.printSeparator

"""
processLine
Process a line
line: line to process
"""
def processLine(line, method, s):
    if (method == 'e'):
        encryptFilesManually(line, s)
    elif (method == 'd-b'):
        decryptCaesarBruteForce(line)
    elif (method == 'd-m'):
        decryptCaesarManually(line, s)

def encryptFilesManually(text,s):

    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text
        
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
        return result

"""
decryptCaesarBruteForce
Decrypts a line with brute force trying all shifts of alphabet
line: line to decode
"""
def decryptCaesarBruteForce(line):
    x = 0
    while x < 26:
        x = x + 1 
        stringtodecrypt=line
        stringtodecrypt=stringtodecrypt.lower()
        ciphershift=int(x)
        stringdecrypted=""
        for character in stringtodecrypt:
            position = alphabet.find(character)
            newposition = position-ciphershift
            if character in alphabet:
                stringdecrypted = stringdecrypted + alphabet[newposition]
            else:
                stringdecrypted = stringdecrypted + character
                
        ciphershift=str(ciphershift)
        print("i:",ciphershift, stringdecrypted)
    
def decryptCaesarManually(text, s):
    encrypted_message = text
    key = s
    for c in encrypted_message:
        if c in alphabet:
            position = alphabet.find(c)
            new_position = (position - key) % 26
            new_character = alphabet[new_position]
            decrypted_message += new_character
        else:
            decrypted_message += c
    print("Decrypted Message: ", decrypted_message)