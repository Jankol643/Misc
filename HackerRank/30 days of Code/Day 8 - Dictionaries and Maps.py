#!/bin/python3
def readInput():
    # read phone book
    lines = []
    for i in range(0, n):
        lines.append(input())
    phoneBook = buildPhoneBook(lines)
    # read all queries
    queries = []
    while True:
        try:
            line = input()
            if line == '':
                break
            queries.append(line)
        except EOFError:
            break
    for query in queries:
        searchPhoneBook(phoneBook, query) # perform some operation(s) on given string
def buildPhoneBook(lines):
    phoneBook = dict()
    for line in lines :
        name = line.split(' ')[0]
        telNr = line.split(' ')[1]
        phoneBook[name] = telNr
    return phoneBook
def searchPhoneBook(phoneBook, nameQuery) :
    # looping through all keys manually is too slow (exceeding 10s time limit for python 3)
    if nameQuery in phoneBook:
        print(str(nameQuery) + "=" + str(phoneBook[nameQuery]))
    else :
        print("Not found")
if __name__ == '__main__':    
    n = int(input().strip())  # number of names and telephone numbers
    readInput()