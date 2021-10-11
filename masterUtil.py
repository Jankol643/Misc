"""
Various helper functions
Created: 25/07/2021
"""

import sys
import os
import platform
import string

def get_platform():
    """
    Gets the operating system currently running
    :returns: name of operating system
    """
    if platform.system() == 'Darwin':
        return 'Mac OS'
    return sys.platform

def create_key_list():
    """
    Creates a list of keys that are used on an European keyboard
    """
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)
    shift_number_chars = ['!', '"', '§', '$', '&', '/', '(', ')', '=']
    other_chars = ['+', '*', '~', '#', '\'', '-', '–', ',', ';', '.', ':', '^', '°', '<', '>', '|']
    key_array = lowercase + uppercase + shift_number_chars + other_chars
    return key_array

def list_fcts_file():
    """
    Returns a list of all top level functions in current file (to be used within target file)
    :returns: list of functions
    """
    lst = []
    for key, value in locals().items():
        if callable(value) and value.__module__ == __name__:
            lst.append(key)
    return lst