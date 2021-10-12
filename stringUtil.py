"""
Various helper functions for operations with strings
Created: 11/10/2021
"""

import os
import itertools
import fileUtil

def print_separator(character, frequency):
    """
    Prints specified character with the given frequency
    :string character: character to print
    :int frequency: number of times to print character
    """
    sep = ''
    for i in range(1, frequency):
        sep += character
    print(sep)

def print_text_separators(text, n):
    """
    Prints a text with separators before and after the text
    :string text: text to print
    """
    print_separator('=', n)
    print(text)
    print_separator('=', n)

def print_text_ascii(text):
    """
    Prints text in ASCII Art
    :string text: string to print
    https://github.com/pwaller/pyfiglet
    """
    selectedFont = "Big"
    print(text, selectedFont)
    #result = pyfiglet.figlet_format(text, font = selectedFont )
    #print(result)

def count_consonants(text):
    """
    Counts the occurences of consonants and other characters in a text
    """
    text = text.lower()
    words = text.split(' ')
    consonants = 0
    other_chars = 0
    for word in words: # iterate over words
        for i in range(0, len(word)): # iterate over characters of word
            char = word[i]
            if char in ['a', 'e', 'i', 'o', 'u']:
                consonants += 1
            else:
                other_chars += 1
    print("Consonants: ", consonants)
    print("Other chars: ", other_chars)

def stutter(word):
    """
    Writes a word as if someone is stuttering it/struggling to read it.
    :string word: word to stutter
    """
    copy_string = word[0:2]
    attempts = 2
    result = ""
    for i in range(0, attempts):
        result += copy_string + "... "
    
    result += word + "?"
    print(result)

def printPermutations(array):
    """
    Prints all permutations for a given array
    :array array: array to permutate
    """
    perm = itertools.permutations(array) 
    for i in list(perm): 
        print(i)

def clean_HTML(text, paragraphs):
    """
    Delete all HTML tags from text
    :string text: text to clean
    :boolean paragraphs: if True paragraphs are converted to newlines
    :returns: cleaned text
    """
    currentdir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(currentdir, "html_tags.txt")
    tag_list = fileUtil.read_file_to_list(file_path)
    for tag in tag_list:
        tag = tag.replace('\n', '')
        tag = tag.strip()
        open = '<' + tag + '>'
        close = '</' + tag + '>'
        text = text.replace(open, '')
        if paragraphs == True:
            if tag == 'p':
                text = text.replace(close, '\n')
        else:
            text = text.replace(close, '')
    return text

def count_words(text):
    """
    Counts the number of words in a given text
    :string text: text to count
    :returns: number of words in text
    :raises Exception: text is empty
    """
    words = 0
    # Here we are removing the spaces from start and end,
    # and breaking every word whenever we encounter a space
    # and storing them in a list. The len of the list is the
    # total count of words.
    words = len(text.strip().split(" "))
    return words

def getPermutations(word):
    """
    Permutates a word
    :string word: word to permutate
    :returns: number of permutations, permutated list of words
    """
    if word == "":
        raise ValueError("Words must have a value")
    perm = list(itertools.permutations(word))
    noPerms = len(perm)
    return noPerms, perm

def check_palindrome(string):
    """
    Checks if a string is a palindrome
    :string string: string to check
    :returns: True or False
    """
    length = len(string)
    string = string.lower()
    first = 0
    last = length - 1
    status = True
    while(first < last):
           if(string[first] == string[last]):
               first = first + 1
               last = last - 1
           else:
               status = False
               break
    return status