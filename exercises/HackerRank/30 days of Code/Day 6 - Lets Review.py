#!/bin/python3
# Enter your code here. Read input from STDIN. Print output to STDOUT

def printStrings(n, string):
    evenChars = ""
    oddChars = ""
    for i in range(0, len(string)):
        char = string[i]
        if (i % 2 == 0):  # even character position
            evenChars += char
        else:  # uneven/odd character position
            oddChars += char
    print(evenChars, oddChars)

if __name__ == '__main__':
    n = int(input().strip())
    string = []
    for i in range(0, n):
        string.append(input())
    for i in range(0, n):
        printStrings(n, string[i])
