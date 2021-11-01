import math

def is_prime(n):
    if n <= 1:
        return False
    sqrt_n = math.sqrt(n)
    if sqrt_n.is_integer():
        return False # divisor of n
    for i in range(2, int(sqrt_n) + 1): # added one if it rounds down during casting
        if (n % i == 0):
            return False
    return True

num_testcases = int(input())
for i in range(num_testcases):
    n = int(input())
    if is_prime(n):
        print("Prime")
    else:
        print("Not prime")