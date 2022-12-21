"""
Day 6
https://adventofcode.com/2022/day/6
1st star: 10 min
2nd star: 2 min
Simple Deque
"""
import sys
sys.path.append("../")

import copy
import util
import math
import sys
import re
from collections import deque

from util import log


def first_non_repeat(data, length):
    window = deque()
    i = 0
    if length > len(data):
        raise Exception("bad input")
    while len(window) < length:
        window.append(data[i])
        i += 1
    while i < len(data):
        if len(set(window)) == length:
            return i 
        window.popleft()
        window.append(data[i])
        i += 1
    return i
        

def solution(datastreams, part):
    output = []
    for data in datastreams:
        if part == 1:
            result = first_non_repeat(data, 4)    
            output.append(result)
        elif part == 2:
            result = first_non_repeat(data, 14)    
            output.append(result)
        else:
            raise Exception("bad logic")
    return output

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/06.in", sep="\n")


    print("TASK 1")
    util.call_and_print(solution, sample, 1)
    util.call_and_print(first_non_repeat, input[0], 4)

    print("\nTASK 2")
    util.call_and_print(solution, sample, 2)
    util.call_and_print(first_non_repeat, input[0], 14)
