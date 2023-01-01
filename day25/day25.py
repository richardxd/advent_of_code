"""
Day 25
https://adventofcode.com/2022/day/25
1st time: 
2nd time: 

"""
import sys
sys.path.append("../")

import parse
import copy
import util
import math
import sys
import re
import time
from collections import deque
from collections import Counter
from collections import defaultdict
import bisect

from functools import cmp_to_key
from functools import lru_cache

from util import log


def snafu_to_decimal(number:str):
    '''
    Given number represented in snafu, convert it to decimal
    '''
    decimal = 0
    for digit in number:
        addtional = 0
        if digit == '-':
            additional = - 1
        elif digit == '=':
            additional = -2
        else:
            additional = int(digit)
        decimal = decimal * 5 + additional
    return decimal
    
    

def decimal_to_snafu(number, carry):
    '''
    Given number represented in decimal, convert it to SNAFU
    '''
    if carry:
        number += 1
    if number < 5:
        if number in [3,4]:
            return "1" + "=" if number == 3 else "1" + "-"            
        else:
            return str(number)
    if number % 5 in [3,4]:
        carry = True
        remainder = "=" if number % 5 == 3 else "-"
    else:
        carry = False
        remainder = str(number % 5)
    return decimal_to_snafu(number // 5, carry) + remainder


def simulate(raw_input):
    '''
    Given the inputs, sum up and return the final result in SNAFU
    '''
    cnt = 0
    for num in raw_input:
        decimal = snafu_to_decimal(num)
        cnt += decimal
    return decimal_to_snafu(cnt, False)
        


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/25.in", sep="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(simulate, sample)
    util.call_and_print(simulate, input)

    



