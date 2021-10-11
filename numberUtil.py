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
    Checks if three numbers fulfill the Pythagorean Theorem
    :int x:
    :int y:
    :int z:
    :returns: true if the numbers fulfill the Pythagorean Theorem
    """
    if (math.pow(x, 2) + math.pow(y, 2) == math.pow(z, 2)):
        return True
    elif (math.pow(x, 2) + math.pow(z, 2) == math.pow(y, 2)):
        return True
    elif (math.pow(y, 2) + math.pow(x, 2) == math.pow(z, 2)):
        return True
    elif (math.pow(y, 2) + math.pow(z, 2) == math.pow(x, 2)):
        return True
    elif (math.pow(z, 2) + math.pow(x, 2) == math.pow(y, 2)):
        return True
    elif (math.pow(z, 2) + math.pow(y, 2) == math.pow(x, 2)):
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
    
    if (start_time > end_time) or (start_time == end_time):
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