"""
Day 3
https://adventofcode.com/2022/day/2
1st star: 15 min
2nd star: less than 5 min
F**ing merged interval
"""
import sys
sys.path.append("../")

import util
import math
import sys
import re
from collections import deque

from util import log

def check_overlap(interval1, interval2):
    """
    Given two intervals, check if there is any overlap
    return True if there is overlap, else False
    """
    x0, y0 = interval1
    x1, y1 = interval2
    if x0 > y1 or x1 > y0:
        return False
    return True
    

def compare_interval(interval1, interval2):
    """
    Given two interval, check if one interval contains another
    return 1 if interval1 /subset interval2
    return -1 if interval2 /subset interval1
    return 0 if no full containment
    """
    x0,y0 = interval1
    x1,y1 = interval2
    # check interval1 /subset interval2
    if int(x1) <= int(x0) and int(y0) <= int(y1):
        return 1  
    # check interval2 /subset interval1
    if int(x0) <= int(x1) and int(y1) <= int(y0):
        return -1
    return 0

def intervals(assignments, part):
    # extract the intervals out
    cnt = 0
    for assignment in assignments:
        left, right = assignment
         
        interval1 = tuple(map(lambda x:int(x), left.split("-")))
        interval2 = tuple(map(lambda x:int(x), right.split("-")))
        if part == 1:
            result = compare_interval(interval1, interval2)
            if result == 1 or result == -1:
                cnt += 1
        elif part == 2:
            if check_overlap(interval1, interval2):
                cnt += 1
    return cnt

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=",")
    input = util.read_strs("input/04.in", sep="\n", sep2=",")

    print("TASK 1")
    util.call_and_print(intervals, sample, 1)
    util.call_and_print(intervals, input, 1)

    print("\nTASK 2")
    util.call_and_print(intervals, sample, 2)
    util.call_and_print(intervals, input, 2)