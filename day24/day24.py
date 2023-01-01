"""
Day 24
https://adventofcode.com/2022/day/24
1st time: 03:00:00
2nd time: 00:15:00

My implementation for the first half is quite inefficient and dirty -- there are plenty of edge cases and conditionals that I failed to consider. 

I also spent a fair amount of time trying to optimize my existing code since my blizzard bfs took very long to execute -- the problem that I faced was that
I did not create the visited set to remove any duplicate visits, since I thought that we may be sitting at the same pair of coordinates in differnt round. But what we may also encounter 
is the same pair of coordinates in the same round. In other words, this is a 3d BFS instead of a 2d BFS. 

Realizing this speeds up the BFS. 

The other trick is that the blizzard map is unique only up to lcm(mx, my) (mx, my are the length of the available grids excluding the walls). 
I did not come to this until I read Borja's solution.
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

def render(grid, row=None, col=None):
    final = [["." for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]['#'] == 1:
                final[i][j] = '#'
                continue
            if grid[i][j]['.'] == 1:
                final[i][j] = '.'
                continue
            cnt = 0
            for key in '><^v':
                cnt += grid[i][j][key]
            if cnt > 1:
                final[i][j] = str(cnt)
            elif cnt == 1:
                if grid[i][j]['>'] == 1:
                    final[i][j] = '>'
                elif grid[i][j]['^'] == 1:
                    final[i][j] = '^'
                elif grid[i][j]['v'] == 1:
                    final[i][j] = 'v'
                elif grid[i][j]['<'] == 1:
                    final[i][j] = '<'
                else:
                    raise Exception("must be buggy")
            # else:
                # print("rendering ", i, j, grid[i][j])
                # raise Exception("buggy")
    if row and col:
        final[row][col] = 'E'

    print("\n".join(["".join(string) for string in final]))
    print("\n")


def simulate(grid):
    '''
    Simulate the expedition's movements along with the blizzard's movements
    '''
    render(grid)

    grid_map = {}
    
    queue = deque()
    queue.append((0, 1, 0))
    visited = set()
    visited.add((0,1,0))
    mx, my = len(grid) - 2, len(grid[0]) - 2
    lcm = abs(mx * my) // math.gcd(mx, my)

    def blizzard_bfs(queue, dest_x, dest_y):
        DIRECTION = [(1,0), (0,1), (0,0), (-1,0), (0,-1)]
        # for this we need to simulate using BFS
        while queue:
            '''
            Given the current coordiante, move 4-directionally to the neighbors to traverse to the extraction point.
            '''
            i, j, round_num = queue.popleft()
            if round_num % lcm not in grid_map:
                if round_num == 0:
                    grid_map[round_num] = grid
                else:
                    grid_map[round_num % lcm] = blizzard(grid_map[round_num-1])


            current_grid = grid_map[round_num % lcm]
            

            if (i, j) == (dest_x, dest_y):
                return  round_num
            # need to make sure the current location is available
            
            # if the current grid is covered by blizzard... oops
            # if current_grid[i][j]['>'] > 0 or current_grid[i][j]['^'] > 0 or current_grid[i][j]['v'] > 0 or current_grid[i][j]['<'] > 0 or current_grid[i][j]['#'] > 0:
            #     continue
            

            # render(grid_map[round_num], i, j)


            for di, dj in DIRECTION:
                if not (0 <= i+di < len(current_grid)) or not (0 <= j + dj < len(current_grid[0])):
                    continue
                # print("try adding", i+di, j+dj)
                if current_grid[i+di][j+dj]['#'] == 1 or current_grid[i+di][j+dj]['.'] != 1:
                    # print("failure")
                    # print(current_grid[i+di][j+dj])
                    continue
                # otherwise, we have a place to move
                if (i+di, j+dj, round_num+1) in visited:
                    continue
                # we explore the possiblities of moving to that place
                queue.append((i+di, j+dj, round_num+1))
                visited.add((i+di, j+dj, round_num+1))
            # we also explore the possiblities of not moving anywhere
            # queue.append((i, j, round_num + 1))
        return None        
    round_num = blizzard_bfs(queue, len(grid) - 1, len(grid[0]) - 2)
    queue = deque()
    queue.append((len(grid) - 1, len(grid[0]) - 2, round_num))
    
    round_num = blizzard_bfs(queue, 0, 1)
    queue = deque()
    queue.append((0, 1, round_num))
    round_num = blizzard_bfs(queue, len(grid) - 1, len(grid[0]) - 2)
    return round_num - 1
    
    

def blizzard(grid):
    '''
    Simulate one round of the blizzard movement
    return the updated blizzard
    '''
    
    # each grid is a hashmap, which records the number of ".", "#", ">", "<", "^", "v" 
    updated_grid = [[defaultdict(int) for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            map0 = grid[i][j]
            map1 = updated_grid[i][j]
            if map0['#'] == 1:
                map1['#'] = 1
                continue
            if map0['.'] == 1:
                continue_var = False
                for key in "><^v":
                    if map1[key] != 0:
                        continue_var = True
                if continue_var:
                    continue
                # otehrwise, update map1 as well
                map1['.'] = 1
                continue
            for key in "><^v":
                while map0[key] > 0:
                    if key == '>':
                        col = j + 1
                        if grid[i][col]['#'] == 1:
                            # update column is 1 instead of j + 1
                            col = 1
                        updated_grid[i][col]['>'] += 1
                        if grid[i][col]['.'] == 1:
                            updated_grid[i][col]['.'] = 0
                    elif key == '<':
                        col = j - 1
                        if grid[i][col]['#'] == 1:
                            # update column is -2 instead of j + 1
                            col = -2
                        updated_grid[i][col]['<'] += 1
                        if grid[i][col]['.'] == 1:
                            updated_grid[i][col]['.'] = 0
                    elif key == '^':
                        row = i - 1
                        if grid[row][j]['#'] == 1:
                            # update row is -2 instead of i - 1
                            row = -2
                        updated_grid[row][j]['^'] += 1
                        if grid[row][j]['.'] == 1:
                            updated_grid[row][j]['.'] = 0
                    elif key == 'v':
                        row = i + 1
                        if grid[row][j]['#'] == 1:
                            # update row is -2 instead of i - 1
                            row = 1
                        updated_grid[row][j]['v'] += 1
                        if grid[row][j]['.'] == 1:
                            updated_grid[row][j]['.'] = 0
                    else:
                        raise Exception("incorrect key")
                    map0[key] -= 1

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            map1 = updated_grid[i][j]
            if map1['#'] == 1:
                continue
            cont_var = False
            for key in "><^v":
                if map1[key] > 0:
                    cont_var = True
                    break
            if cont_var:
                continue
            if map1['.'] == 1:
                continue
            #otehrwise, we need to assign it to be an empty tile
            map1['.'] = 1
            
    
    return updated_grid
                    


def parse_input(raw_input):
    '''
    Convert the grid from character-based into hashmaps, where keys are  ".", "#", ">", "<", "^", "v" 
    and values are the frequency of each character. 
    '''
    raw_input = [list(string) for string in raw_input]
    grid = [[defaultdict(int) for _ in range(len(raw_input[0]))] for _ in range(len(raw_input))]
    for i in range(len(raw_input)):
        for j in range(len(raw_input[0])):
            current = raw_input[i][j]
            hash_map = grid[i][j]
            if current == "#":
                hash_map[current] = 1
                continue
            elif current == ".":
                hash_map[current] = 1
                continue
            elif current in ">^<v":
                hash_map[current] = 1
                continue
    return grid
            

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/24.in", sep="\n")
    
    sample = parse_input(sample)
    input = parse_input(input)
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(simulate,  sample)
    util.call_and_print(simulate, input)

    



