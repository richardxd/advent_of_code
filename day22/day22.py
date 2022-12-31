"""
Day 22
https://adventofcode.com/2022/day/22
1st time: 01:00:00
2nd time: 


Part I is very basic by just following the instruction with some tweaks (the only difference is now going off bound is allowed.)
And it is really painful.... I do not want to do part II no more 

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

def pad(grid):
    max_len = max(len(s) for s in grid)
    for i,s in enumerate(grid):
        grid[i] = s.ljust(max_len, " ")
    return grid
    

def parse_input(filename):
    '''
    parse the input into the grid and the instructions
    then follow the instruction
    '''
    def update(x, y, dx, dy, facing):
        '''
        Given the original coordinates (x, y), update them by dx and dy respectively
        then return the resulting coordinates
        '''
        
        # check what the updated coordinate looks like:
        updated_col = (x + dx) % len(grid)
        updated_row = (y + dy) % len(grid[0])
        # check if there is an out of bound
        if grid[updated_col][updated_row] == ".":
            return updated_col, updated_row
        elif grid[updated_col][updated_row] == "#":
            return x, y
        elif grid[updated_col][updated_row] == " ":
            # if this is the space, we need to check for the corresponding bound
            bounded_x, bounded_y = x, y 
            if facing == 0:
                # this means we are at the left bound
                bounded_y = left_bound[x]
                print_bound = "left_bound"
            elif facing == 1:
                # at the up bound
                bounded_x = up_bound[y]
                print_bound = "up_bound"

            elif facing == 2:
                # at the right bound
                bounded_y = right_bound[x]
                print_bound = "right_bound"
            elif facing == 3:
                # at the bottom bound
                bounded_x = low_bound[y]
                print_bound = "low_bound"
            else:
                raise Exception("incorrect facing")
            # now we have the bounds, check again
            if grid[bounded_x][bounded_y] == ".":
                return bounded_x, bounded_y
            elif grid[bounded_x][bounded_y] == "#":
                return x, y
            elif grid[bounded_x][bounded_y] == " ":
                raise Exception(print_bound, "computed incorrectly. Abort")
            else: 
                raise Exception("dirty input")
        else:
            raise Exception("dirty input")
        

    def execute(x, y, facing, steps, turn):
        '''
        Given the current position in the grid (x, y) and the direction facing, 
        move forward steps and turn the direction
        return the resulting coordinate and the direction facing(0: ">", 1:"v", 2:"<", 3:"^")
        '''
        i, j = x, y
        while steps > 0:
            # store the coordinate before updates
            tmp_row, tmp_col = i, j
            dx, dy = 0, 0
            # find the value currently being updated by the direction facing
            if facing == 0: 
                # update j by one 
                dy = 1 
            elif facing == 1:
                # update i by one
                dx = 1
            elif facing == 2:
                # update j by minus one
                dy = -1
            elif facing == 3:
                # update i by minus one
                dx = -1
            else:
                raise Exception("the facing value is incorrect")
            i, j = update(i, j, dx, dy, facing)
            steps -= 1
            # if the update yields the same coordinates, stops the while loop (since we are stuck here)
            if (i, j) == (tmp_row, tmp_col):
                break

        # finish moving steps. Now update the direction facing
        if turn == "L":
            facing -= 1
            facing %= 4 
        elif turn == "R":
            facing += 1
            facing %= 4
        
        return i, j, facing


    # start of the function
    with open(filename) as f:
        txt = f.read()
    grid, inst = txt.split(sep="\n\n")
    grid_lines = grid.split("\n")
    # print(grid, "\n")

    grid = pad(grid_lines)
    
    # print("padded grid is: \n", grid, "\n")




    for j in range(len(grid[0])):
        if grid[0][j] != " ":
            start_row = 0
            start_col = j
            break

    
    # parse the grid by finding the locations of the bounds of the 4 directions 
    left_bound = [] # left bound of each row 
    right_bound = [] # right bound of each row 
    up_bound = []   # upper bound of each column
    low_bound = []  # lower bound of each column
    i, j = 0, 0
    for i in range(len(grid)):
    # update the left bound and the right bound of each row
        j = 0
        bound_updated = left_bound
        terminating_cond = [".", "#"]
        broken = False
        if grid[i][j] in terminating_cond:
            bound_updated.append(j)
            bound_updated = right_bound
            terminating_cond = [" "]
        while j < len(grid[0]) and grid[i][j] not in terminating_cond:
            j += 1
            if j < len(grid[0]) and grid[i][j] in terminating_cond:
                if terminating_cond == [".", "#"]:
                    terminating_cond = [" "]
                    bound_updated.append(j)
                    bound_updated = right_bound
                else: 
                    bound_updated.append(j-1)
                    broken = True
                    break
        if not broken:
            # then this means that the right bound is at the very right
            right_bound.append(len(grid[0])-1)            

    i, j = 0, 0
    for j in range(len(grid[0])):
     # update the left bound and the right bound of each row
        i = 0
        bound_updated = up_bound
        terminating_cond = [".", "#"]
        broken = False
        if grid[i][j] in terminating_cond:
            bound_updated.append(i)
            bound_updated = low_bound
            terminating_cond = [" "]
        while i < len(grid) and grid[i][j] not in terminating_cond:
            i += 1
            if i < len(grid) and grid[i][j] in terminating_cond:
                if terminating_cond == [".", "#"]:
                    terminating_cond = [" "]
                    bound_updated.append(i)
                    bound_updated = low_bound
                else: 
                    bound_updated.append(i-1)
                    broken = True
                    break
        if not broken:
            # then this means that the low bound is at the very bottom
            low_bound.append(len(grid)-1)   


    assert len(left_bound) == len(grid)
    assert len(right_bound) == len(grid)
    assert len(up_bound) == len(grid[0])
    assert len(low_bound) == len(grid[0])
    # print("left bound:", left_bound)
    # print("right bound:", right_bound)
    # print("up bound:", up_bound)
    # print("down bound:", low_bound)




    inst = deque(inst)
    # parse the instruction
    instructions = deque()
    buffer = ""
    while inst and inst[0].isnumeric():
        buffer += inst.popleft()
        if not inst:
            instructions.append((int(buffer), None))
            break
        if not inst[0].isnumeric():
            instructions.append((int(buffer), inst.popleft()))
            buffer = ""



    # execute the instructions
    current_row = start_row
    current_col = start_col 
    facing = 0
    for steps, turn in instructions:
        current_row, current_col, facing = execute(current_row, current_col, facing, steps, turn)        
    return 1000 * (current_row+1) + 4 * (current_col+1) + facing # add one since our grid is 0-indexed but the grid in the question is 1-indexed


if __name__ == "__main__":
    util.set_debug(False)

    # sample = util.read_strs("input/sample.in", sep="\n\n", sep2="\n")
    # input = util.read_strs("input/22.in", sep="\n\n", sep2="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(parse_input, "input/sample.in")
    util.call_and_print(parse_input, "input/22.in")

    



