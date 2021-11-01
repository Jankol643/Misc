#!/bin/python3

#
# Complete the 'bitwiseAnd' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER N
#  2. INTEGER K
#


def bitwiseAnd(N, K):
    max_bit = 0
    for i in range(1,N+1):
        for j in range(1,i):
            bit_value = i & j
            if max_bit < bit_value < K :
                max_bit = bit_value
                if max_bit == K-1:
                    return max_bit

    return max_bit

if __name__ == '__main__':
    result = list()
    t = int(input().strip())
    for t_itr in range(t):
        n,k = input().strip().split(' ')
        n,k = [int(n),int(k)]

        result.append(bitwiseAnd(n, k))

    for i in range(len(result)):
        print(result[i])
