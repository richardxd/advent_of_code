"""
Day 23
https://adventofcode.com/2022/day/23
1st time: 01:00:00
2nd time: 00:02:00

Again part I is the simulation type of question. I was in hunger, so my brain wasn't functionally capable of being fast
Part II is so simple that i makes mewonder if this is truly a AoC question..
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


def render(elves):
    print(elves)
    y_coordinates = [j for i, j in elves]
    x_coordinates = [i for i, j in elves]
    min_y = min(y_coordinates)
    max_y = max(y_coordinates)
    min_x = min(x_coordinates)
    max_x = max(x_coordinates)
    print(min_y, min_x, max_y, max_x)
    if min_y < 0 and min_x < 0:
        updated_coordinates = {(i + min_x, j + min_y) for i,j in elves}
    elif min_y < 0:
        updated_coordinates = {(i, j + min_y) for i, j in elves}
    elif min_x < 0:
        updated_coordinates = {(i + min_x, j) for i, j in elves}
    else:
        updated_coordinates = elves

    if min_y < 0 and min_x < 0:
        grid = [['.'] * (1 + max_y - min_y) for _ in range(1 + max_x - min_x)]
    elif min_y < 0:
        grid = [['.'] * (1 + max_y) for _ in range(1 + max_x - min_x)]
    elif min_x < 0:
        grid = [['.'] * (1 + max_y - min_y) for _ in range(1 + max_x)]
    else:
        grid = [['.'] * (1 + 5) for _ in range(1 + 6)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i,j) in updated_coordinates:
                grid[i][j] = "#"
    joined = ["".join(string) for string in grid]

    return "\n".join(joined)
    



def smallest_rectangle(elves):
    '''
    Given the coordinates of the elves, compute the number of empty grounds of the bounding box
    '''
    y_coordinates = [j for i, j in elves]
    x_coordinates = [i for i, j in elves]
    min_y = min(y_coordinates)
    max_y = max(y_coordinates)
    min_x = min(x_coordinates)
    max_x = max(x_coordinates)
    ret = (1 + max_x - min_x) * (1 + max_y - min_y) - len(elves)
    return ret

    


def one_round(elves, priority):
    '''
    Given the elves' coordinates (as a set), compute the elves next moving coordinates
    '''
    DIRECTION = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1),(-1,-1)]
    current = {}
    desired = {}
    cnt_stay = 0
    for i, j in elves:
        # determine whether to move or not:
        stay = True
        for di, dj in DIRECTION:
            if (i + di, j + dj) in elves: 
                stay = False
                break
        if stay:
            cnt_stay += 1
            desired[(i,j)] = (i,j)
            current[(i,j)] = 1
            continue 

        # determine the locations to move
        for direction in priority:
            coordinates = []
            dx, dy = 0, 0
            if direction == "N":
                coordinates.append((i-1, j-1))
                coordinates.append((i-1, j))
                coordinates.append((i-1, j+1))
                dx = -1
            elif direction == "S":
                coordinates.append((i+1, j-1))
                coordinates.append((i+1, j))
                coordinates.append((i+1, j+1))
                dx = 1
            elif direction == "W":
                coordinates.append((i-1, j - 1))
                coordinates.append((i, j - 1))
                coordinates.append((i+1, j - 1))
                dy = -1
            elif direction == "E":
                coordinates.append((i-1, j+1))
                coordinates.append((i, j+1))
                coordinates.append((i+1, j+1))
                dy = 1
            else:
                raise Exception("incorrect priority")
            continue_var = False
            for x, y in coordinates:
                if (x,y) in elves:
                    dx, dy = 0, 0
                    continue_var = True
            if continue_var:
                continue
            else:
                break
            # otherwise, move to the corresponding location
        if (i+dx, j +dy) not in current: 
            current[(i+dx, j +dy)] = 0
        current[(i+dx, j+dy)] += 1
        desired[(i,j)] = (i+dx, j + dy)
        if (i, j) not in desired:
            desired[(i,j)] = (i,j)

    ret = True if cnt_stay == len(elves) else False

    output = set()    
    # iterate again to make sure no one is moving to the same grid
    for i, j in elves:
        x, y = desired[(i, j)]
        if current[(x,y)] > 1:
            output.add((i, j))
        else:
            output.add((x,y))
    return output, ret


def simulate(grid):
    '''
    Given a grid, compute the samllest rectangle that contains all the elves after 10 rounds
    '''
    elves = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                elves.add((i,j))
    
    priority = deque(["N", "S", "W", "E"])
    i = 0
    while True:
        elves, stay = one_round(elves, priority)
        if stay:
            break 
        priority.append(priority.popleft())
        i += 1
    return smallest_rectangle(elves), i+1



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/23.in", sep="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(simulate,  sample)
    util.call_and_print(simulate, input)

    



