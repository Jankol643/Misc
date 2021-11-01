#!/bin/python3
# Script will only run in Python 3.6 or higher because f-strings are used

import math
import os
import random
import re
import sys

def printMultiples(n) :
    i = 0
    for i in range(1,11) :
        print(f'{n} x {i} = {n*i}')

if __name__ == '__main__':
    n = int(input().strip())
    printMultiples(n)