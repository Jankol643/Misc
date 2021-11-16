"""
Various helper functions for operations with numbers
Created: 10/10/2021
"""

from decimal import Decimal
import math
import datetime

def noDecimalPlaces(number):
    """
    Counts the number of decimal places in a number (only accurate if number has fewer than 17 decimal places)
    :int number: number to calculate decimal places from
    :returns: number of decimal places
    """
    number_string = str(number)
    decimal = Decimal(number_string)
    print(decimal)
    lenstr = len(str(decimal).split(".")[1])
    return lenstr

def calc_discount(price, discount):
    """
    Returns the price after subtracted discount
    :int price: price
    :int discount: discount percentage
    :returns: discounted price
    """
    amount_discount = price * discount/100
    final_price = price - amount_discount
    final_price = round(final_price, 2)
    return final_price

def check_pythagoras(x, y, z):
    """
    Checks if three numbers form a Pythagorean triple
    :int x: number 1
    :int y: number 2
    :int z: number 3
    :returns: true if the numbers form a Pythagorean triple
    """
    if (x * x + y * y == z * z):
        return True
    elif (x * x + z * z == y * y):
        return True
    elif (y * y + x * x == z * z):
        return True
    elif (y * y + z * z == x * x):
        return True
    elif (z * z + x * x == y * y):
        return True
    elif (z * z + y * y == x * x):
        return True
    return False

def divide_time(start_time, end_time, number_parts):
    """
    Divides a timeframe specified by start and end time into even chunks
    :string start_time: start time in format "%H:%M:%S"
    :string end_time: end time in format "%H:%M:%S"
    :int number_parts: number of parts to divide time into
    :returns: list with splitted times
    """
    try:
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%H:%M:%S")
    except ValueError:
        raise ValueError("Cannot convert entered time to required format.")
    
    if (start_time >= end_time):
        raise ValueError("Start time must be less than end time")

    times = list()
    add = (float)((end_time - start_time).total_seconds()/number_parts)
    old_time = start_time
    for part in range(0, number_parts + 1):
        add_seconds = add * part
        new_time = old_time + datetime.timedelta(seconds = add_seconds)
        hour = str(new_time.hour).zfill(2)
        minute = str(new_time.minute).zfill(2)
        seconds = str(new_time.second).zfill(2)
        string = hour + ":" + minute + ":" + seconds
        times.append(string)
        new_time = old_time
    return times

def radians_to_degrees(radians):
    """
    Takes an angle in radians and returns the corresponding angle in degrees rounded to one decimal place
    :int radians: angle in radians
    :returns: angle in degrees
    """
    degrees = 0
    degrees = radians * 180/math.pi
    degrees = round(degrees, 1)
    return degrees

def fahrenheit_celsius(degreesF):
    """
    Converts degrees Fahrenheit to degrees Celsius
    :int degressF: degrees Fahrenheit
    :returns: degrees Celsius
    """
    degreesC = 0
    degreesC = (degreesF - 32) * 5/9
    return degreesC

def celsius_fahrenheit(degreesC):
    """
    Converts degrees Celsius to degrees Fahrenheit
    :int degressC: degrees Celsius
    :returns: degrees Fahrenheit
    """
    degreesF = 0
    degreesF = degreesC * 5/9 + 32
    return degreesF


def pythagoreanTriplets(limits):
    """
    Prints the Pythagorean triplets up to an upper limit

    :param limits: upper limit for triplets
    :type limits: int
    """
    lst = list()
    c, m = 0, 2
 
    # Limiting c would limit
    # all a, b and c
    while c < limits:
         
        # Now loop on n from 1 to m-1
        for n in range(1, m):
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
 
            # if c is greater than
            # limit then break it
            if c > limits:
                break
 
            lst.append([a, b, c])
        m = m + 1
    lst.sort()
    print(lst)