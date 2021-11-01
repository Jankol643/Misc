#!/bin/python3

import math
import os
import random
import re
import sys

def weirdNotWeird(n) :
    if (n % 2 != 0) : # odd number
        print("Weird")
    if (n % 2 == 0) : # even number
        if (n >= 2 and n <= 5) :
            print("Not Weird")
        elif (n >= 6 and n <= 20) :
            print("Weird")
        else:
            print("Not Weird") 

if __name__ == '__main__':
    N = int(input().strip())
    weirdNotWeird(N)