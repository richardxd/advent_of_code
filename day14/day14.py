"""
Day 14
https://adventofcode.com/2022/day/14
1st time: 00:20:00
2nd time: 00:40:00
A fun question. I spent some time trying to get the details to work
Overall this is not very hard I like it 
"""
import sys
sys.path.append("../")

import parse
import copy
import util
import math
import sys
import re
from collections import deque
from collections import Counter
import bisect

from functools import cmp_to_key

from util import log


def query(rocks, x1, y1):
    '''
    Given a set of coordinates of rocks, and a coordinate to be queried (whether this coordinate is a rock or not)
    return False if the coordinate is a rock else False
    '''
    return False if (x1,y1) in rocks else True


def traverse(rocks, x0, y0, bottom=None):
    '''
    part1: 
    Given the current location of the sand, return the next location of the sand
    if no further move can be made, return None
    part2:
    on top of the normal check, if one rock reaches the bottom, then it is 
    fallen and can no longer move
    '''
    if bottom and y0 == bottom:
        return None

    if query(rocks, x0, y0+1):
        return x0, y0 + 1
    elif query(rocks, x0-1, y0+1):
        return x0-1, y0+1
    elif query(rocks, x0+1, y0+1):
        return x0+1, y0+1
    
    return None

def generate_line(x0, y0, x1, y1):
    '''
    Given two cooridinates, generate a set of the points along the line segment
    '''
    rocks = set()
    if x0 == x1:
        # generate a vertical line
        for y in range(min(y0, y1), max(y0, y1) + 1):
            rocks.add((x0, y))
    elif y0 == y1:
        # generate a horizontal line
        for x in range(min(x0, x1), max(x0, x1) + 1):
            rocks.add((x, y0))
    else:
        raise Exception("buggy inputs/logi")
    return rocks 

def process_io(raw_input):
    '''
    build a set of coordinates of rocks and return
    '''
    highest = 0
    rocks = set()
    for path in raw_input:
        # for string in path:
        #     x,y = string.split(",")
        #     rocks.add((int(x), int(y)))
        #     highest = max(highest, int(y))
        for i in range(1, len(path)):
            x0, y0 = path[i-1].split(",")
            x1, y1 = path[i].split(",")
            rock_sub = generate_line(int(x0), int(y0), int(x1), int(y1))
            rocks |= rock_sub
            highest = max(highest, int(y0), int(y1))

    return rocks, highest

def simulate(raw):
    '''
    Simulate the experiement produced by the rocks
    part is used to indicate if this is part1(T) or part2(F)
    '''
    rocks, highest = process_io(raw)
    cnt = 0
    x0 = 500
    y0 = 0
    ret = traverse(rocks, x0, y0)
    while ret:
        x1, y1 = ret
        if y1 > highest:
            break
        ret = traverse(rocks, x1, y1)
        if not ret:
            rocks.add((x1,y1))
            ret = traverse(rocks, x0, y0)
            cnt += 1
    return cnt

def simulate2(raw):
    '''
    Simulate the experiement produced by the rocks
    part is used to indicate if this is part1(T) or part2(F)
    '''
    rocks, highest = process_io(raw)
    cnt = 0
    x0 = 500
    y0 = 0
    bottom = highest + 2
    ret = traverse(rocks, x0, y0, bottom - 1)
    while ret:
        x1, y1 = ret
        if (x1, y1) == (500, 0):
            break
        ret = traverse(rocks, x1, y1, bottom - 1)
        if not ret:
            rocks.add((x1,y1))
            ret = traverse(rocks, x0, y0, bottom - 1)
            cnt += 1
    return cnt + 1


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=" -> ")
    input = util.read_strs("input/14.in", sep="\n", sep2=" -> ")
    

    print("TASK 1")
    util.call_and_print(simulate, copy.deepcopy(sample))
    util.call_and_print(simulate, copy.deepcopy(input))
    

    print("\nTASK 2")
    util.call_and_print(simulate2, copy.deepcopy(sample))
    util.call_and_print(simulate2, copy.deepcopy(input))


