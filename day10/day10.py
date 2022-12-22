"""
Day 10
https://adventofcode.com/2022/day/10
1st time: 00:22:35
2nd time: 01:19:08

It took me this long because I got distracted by Zhihu and also some wechat messages.
Also I hate this type of questions....
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

def render_image(input, wide):
    output = []
    buffer = []
    i = 0
    while input:
        buffer.append(input.popleft())
        i += 1
        if i != wide:
            continue
        output.append(buffer)
        buffer = []
        i = 0
    string_list = ["".join(lst + ['\n']) for lst in output]
    return "".join(string_list)

def check_lit(X, cycle_rendered, gap):
    rendered = set()
    rendered.add(X-1)
    rendered.add(X)
    rendered.add(X+1)
    if cycle_rendered % gap in rendered:
        return True
    return False

def simulate(instructions, start, end, gap):
    cycle = 0
    X = 1
    output = []
    result = 0
    buffer = None
    for ins in instructions:
        if cycle > end:
            break

        if cycle % gap == start:
            result += (cycle * X)
        if buffer:
            X += buffer
            buffer = None
        if ins[0] == "noop":
            cycle += 1
        elif ins[0] == "addx":
            # first cycle
            cycle += 1
            # first cycle completes
            if check_lit(X, cycle-1, gap):
                output.append("#")
            else:
                output.append(".")

            if cycle % gap == start:
                result += (cycle * X)
            # second cycle
            cycle += 1
            buffer = int(ins[1])
            # second cycle complete
        if check_lit(X, cycle-1, gap):
            output.append("#")
        else:
            output.append(".")
    image = render_image(deque(output), gap)
    print(image)
    return result    

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=" ")
    input = util.read_strs("input/10.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(simulate, copy.deepcopy(sample), 20, 220, 40)
    util.call_and_print(simulate, copy.deepcopy(input), 20, 220, 40)
    

    print("\nTASK 2")
    util.call_and_print(simulate, copy.deepcopy(sample), 20, 240, 40)
    util.call_and_print(simulate, copy.deepcopy(input), 20, 240, 40)


