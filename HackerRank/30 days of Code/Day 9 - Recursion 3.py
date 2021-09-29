#!/bin/python3

import sys

#
# Complete the 'factorial' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER n as parameter.
#

# Recursion must be used (comment from author)
def factorial(n):
    # Write your code here
    if (n <= 0) :
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == '__main__':
    fptr = sys.stdout   # stdout is already an open stream

    n = int(input().strip())

    result = factorial(n)

    fptr.write(str(result) + '\n')

    fptr.close()
