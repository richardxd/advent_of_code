"""
Day 2
https://adventofcode.com/2022/day/2
1st star: a bit long setting up everything
2nd star: long enough to hardcode a hashmap
I don't know what to put here. the compute score function is indeed messy
"""
import sys
sys.path.append("../")

import util
import math
import sys
import re
from collections import deque

from util import log

def compute_priority(ascii_code):
    # calculate the priority
    score = 0
    if 65 <= ascii_code <= 90:
        score = ascii_code - 64 + 26
    elif 97 <= ascii_code <=  122:
        score = ascii_code - 96
    else:
        raise Exception("dirty input")
    return score


def part1(items):
    """
    Given a list of items, compute the total sum of the properties of each items
    """
    score = 0
    for item in items:
        length = len(item)
        half = length // 2
        left = set(item[0:half])
        right = set(item[half:])
        result = left & right
        if len(result) != 1:
            raise Exception("incorrect input")
        common = result.pop()
        ascii_code = ord(common)
        score += compute_priority(ascii_code)
        
    return score

def part2(items):
    score = 0
    current_group = []
    items = deque(items)
    while len(current_group) < 3 and items:
        current_group.append(items.popleft())
        if len(current_group) != 3:
            continue
        result = set(current_group[0]) & set(current_group[1]) & set(current_group[2])
        
        if len(result) != 1:
            raise Exception("bad input")
        common = result.pop()
        ascii_code = ord(common)
        score += compute_priority(ascii_code)
        current_group = []
    return score


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/03.in", sep="\n")

    print("TASK 1")
    util.call_and_print(part1, sample)
    util.call_and_print(part1, input)

    print("\nTASK 2")
    util.call_and_print(part2, sample)
    util.call_and_print(part2, input)