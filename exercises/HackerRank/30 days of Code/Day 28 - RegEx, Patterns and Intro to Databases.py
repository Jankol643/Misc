#!/bin/python3

import re


if __name__ == '__main__':
    N = int(input().strip())
    names = []
    for N_itr in range(N):
        first_multiple_input = input().rstrip().split()

        firstName = first_multiple_input[0]
        emailID = first_multiple_input[1]

        match = re.search(r'[\w\.-]+@gmail.com', emailID)

        if match:
            names.append(firstName)
names.sort()
for name in names:
    print( name )