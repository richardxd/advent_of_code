"""
Day 16
https://adventofcode.com/2022/day/16
1st time: 00:10:00
2nd time: 04:00:00
This is the question that got me stuck forever. I really enjoyed the thinking behind it and coming up
with the dp solution is such a good feeling!
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
import bisect

from functools import cmp_to_key
from functools import lru_cache

from util import log



def simulate(raw_input):
    points = set()
    side = 0
    for x,y,z in raw_input:
        if (x,y,z) in points:
            raise Exception("duplicate points?")
        uncovered = 6
        if ((x+1), y, z) in points:
            uncovered -= 1
            side -= 1 # 1 side of an existing cube is connected to the new cube
        if ((x-1), y, z) in points:
            uncovered -= 1
            side -= 1
        if (x, (y-1), z) in points:
            uncovered -= 1
            side -= 1
        if (x, y+1, z) in points:
            uncovered -= 1
            side -= 1
        if (x, y, z-1) in points:
            uncovered -= 1
            side -= 1
        if (x, y, z+1) in points:
            uncovered -= 1
            side -=1 
        side += uncovered
        points.add((x,y,z))
    return side




if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample.in", sep="\n", sep2=",")
    input = util.read_ints("input/18.in", sep="\n", sep2=",")
    

    
    print("TASK 1 and 2")
    util.call_and_print(simulate, sample)
    util.call_and_print(simulate, input)
    

    # print("\nTASK 2")
    # util.call_and_print(simulate, sample_graph, False)
    # util.call_and_print(simulate, input_graph, False)


