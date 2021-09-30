#!/bin/python3
# deleted '__name__ == "__main__"' because first word of line must not be used

def toInteger(S):
    try:
        print(int(S))
    except ValueError:
        print("Bad String")

S = input().strip()
toInteger(S)
