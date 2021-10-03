#!/usr/bin/python
"""
This program calculates the writing speed for a dummy text
Creation date 09/30/2021
Author Jankol643
"""

import masterUtil
import fileUtil
import internet
from datetime import datetime as DateTime, timedelta as TimeDelta # for setting timeout

def calculate_speed(seconds):
    
    def decide_text():
        """
        Asks the user if the text should come from the internet or a file
        :returns: choice of user ('internet' or 'file')
        :raises ValueError: wrong input
        """
        source = input("Would you like to get a dummy text from the internet or from a file? (internet/file) ")
        if source in ('INTERNET', 'Internet', 'internet'):
            return 'internet'
        if source in ('FILE', 'File', 'file'):
            return 'file'
        else:
            raise ValueError("Wrong choice. Please select 'internet' or 'file'.")

    def print_text(text):
        """
        Prints a text with separators before and after the text
        :string text: text to print
        """
        masterUtil.print_separator('=', 80)
        print(text)
        masterUtil.print_separator('=', 80)
    
    def time_typing(seconds):
        """
        Returns written text after a certain amount of seconds have passed
        :int seconds: time limit in seconds
        :returns written_text: user input during time limit
        """
        endTime = DateTime.now() + TimeDelta(seconds = seconds)
        while True:
            if DateTime.now() >= endTime:
                break
        
        written_text = input()
        print("Time is up.")
        return written_text

    decision = decide_text()
    if (decision == 'internet'):
        text = internet.getTextFromURL()
    elif (decision == 'file'):
        filepath = input("Please specify a filepath: ")
        text = fileUtil.read_line_file(filepath, 1)
    
    print_text(text)
    written_text = time_typing()
    word_count = masterUtil.count_words(written_text)
    WPM = word_count/(seconds/60)
    return WPM

if __name__ == '__main__':
    seconds = int(input("Please enter how many seconds the test should take: "))
    res = calculate_speed(seconds)
    print("Words per minute: ", res)