"""
Various helper functions
Created: 25/07/2021
"""

import fileUtil
import sys
import os

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

def clean_HTML(text, paragraphs):
    """
    Delete all HTML tags from text
    :string text: text to clean
    :boolean paragraphs: if True paragraphs are converted to newlines
    :returns: cleaned text
    """
    tag_list = fileUtil.read_file_to_list('html_tags.txt')

    for tag in tag_list:
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
    if text != "":
        words = 0
        # Here we are removing the spaces from start and end,
        # and breaking every word whenever we encounter a space
        # and storing them in a list. The len of the list is the
        # total count of words.
        words = len(text.strip().split(" "))
        return words
    else:
        raise ValueError("Cannot count words because text is empty.")