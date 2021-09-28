#!/bin/python3

def reverseArray(n, arr) :
    items = [] # another method: item = []* n
    for i in range(0,n) :
        items.append(arr[n-i-1]) # another method: item[i] = arr[n-i-1]
    listOfStrings = [str(item) for item in items]
    result = ' '.join(listOfStrings)
    print(result)

if __name__ == '__main__':
    n = int(input().strip()) # size of array
    arr = list(map(int, input().rstrip().split())) # n space separated elements of array (integers)
    reverseArray(n, arr)