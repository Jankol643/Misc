#!/bin/python3

def binaryNumbers(n) :

    def convertToBinary(n) :
        res = 0
        binary= []
        while(n>0):
            d=n%2
            binary.append(d)
            n=n//2
        binary.reverse()
        return binary
    
    def countConsecutive(binary, toCount) :
        consecutiveArray = []
        consecutive = 0
        for char in binary:
            if (char == toCount) :
                consecutive += 1
                consecutiveArray.append(consecutive)
            else :
                consecutive = 0
                consecutiveArray.append(consecutive)
        
        consecutive = max(consecutiveArray)
        return consecutive

    binary = convertToBinary(n)
    result = countConsecutive(binary, 1)    

    return result
if __name__ == '__main__':
    n = int(input().strip())
    result = binaryNumbers(n)
    print(result)