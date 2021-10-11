#!/usr/bin/python
"""
This program calculates the writing speed for a dummy text
Creation date 09/30/2021
Author Jankol643
"""

#Necessary for importing file from parent folder
import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import masterUtil
import fileUtil
import stringUtil
import internet
import time

def calculate_speed():
    """
    Calculates writing speed for a given text in words per minute
    :int seconds: number of seconds
    """

    def calculate_WPM(text, seconds):
        """
        Calculates words per minute
        :string text: text to count WPM for
        :int seconds: number of seconds
        """
        word_count = masterUtil.count_words(text)
        if seconds > 60:
            WPM = word_count/(seconds/60)
        else:
            var = 60/seconds
            WPM = word_count * var
        return WPM

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
    
    def time_typing():
        """
        Returns written text after a certain amount of seconds have passed
        :int seconds: time limit in seconds
        :returns written_text: user input during time limit
        """
        start_time = time.perf_counter()
        written_text = input("Enter the above text. Press Enter if test should stop.")
        end_time = time.perf_counter()
        time_taken = end_time - start_time
        return time_taken, written_text

    decision = decide_text()
    if (decision == 'internet'):
        text = internet.get_text_from_URL()
    elif (decision == 'file'):
        filepath = input("Please specify a filepath: ")
        if filepath == "":
            filepath = internet.get_data_path()
            text = fileUtil.access_file_line(filepath, 2, 'r')
        text = fileUtil.access_file_line(filepath, 1, 'r')
    
    stringUtil.print_text_separators(text, 80)
    seconds, written_text = time_typing()
    wpm = calculate_WPM(written_text, seconds)
    return wpm

if __name__ == '__main__':
    seconds = int(input("Please enter how many seconds the test should take: "))
    res = calculate_speed()
    print("Words per minute: ", res)