#!/bin/python3

def bubbleSort(n, a):
    # Track number of elements swapped during a single array traversal
    number_of_swaps = 0
    for i in range(n):        
        for j in range(n-1):
            # Swap adjacent elements if they are in decreasing order
            if (a[j] > a[j + 1]):
                a[j], a[j+1] = a[j+1], a[j]
                number_of_swaps = number_of_swaps + 1
        
        # If no elements were swapped during a traversal, array is sorted
        if (number_of_swaps == 0):
            break

    return number_of_swaps

if __name__ == '__main__':
    n = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    number_of_swaps = bubbleSort(n, a)
    print("Array is sorted in " + str(number_of_swaps) + " swaps.")
    print("First Element:", a[0])
    print("Last Element:", a[n-1])