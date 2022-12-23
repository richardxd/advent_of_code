"""
Day 12
https://adventofcode.com/2022/day/12
1st time: 00:15:00
2nd time: 00:16:00
Very standard BFS problem. I wanted to go to sleep at first but realizing this is just BFS wakes me up
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

from util import log




def find_start_end(grid, part1):
    '''
    Given a 2d matrix of alphabets, find S and E
    return the coordinates for corresponding points
    '''
    start = []
    end = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if part1:
                if grid[i][j] == 'S':
                    start.append([i,j])
            else:
                if grid[i][j] == 'S' or grid[i][j] == 'a':
                    start.append([i,j])
                
            if grid[i][j] == 'E':
                end = (i,j)
    return start, end            


def reachable(grid, x0, y0, x1, y1):
    '''
    Given x0,y0, check if I can reach to x1, y1]
    return True if reachable
    otherwise False
    '''
    current = grid[x0][y0] if grid[x0][y0] != 'S' else 'a'
    end = grid[x1][y1] if grid[x1][y1] != 'E' else 'z'
    if ord(end) <= ord(current) + 1:
        return True
    return False
    

def bfs(grid, start, end):
    '''
    Given start, end of a given grid, run bfs to find the shortest path to the end
    if no path available, return none
    '''
    # queue = deque(start)
    start = [coordinate + [0] for coordinate in start]
    queue = deque(start)
    visited = set()
    directions = [(-1,0), (0,-1), (1,0), (0,1)]
    
    while queue:
        x0, y0, step = queue.popleft()
        if (x0, y0) == end:
            return step
        for dx, dy in directions:
            x1, y1 = x0 + dx, y0 + dy
            if x1 < 0 or x1 >= len(grid) or y1 < 0 or y1 >= len(grid[0]):
                continue
            if (x1,y1) in visited or not reachable(grid, x0, y0, x1, y1):
                continue

            queue.append((x1, y1, step + 1))
            visited.add((x1, y1))
    return -1
        

def part1(grid):
    '''
    Given raw string input for part1, find the shortest path
    '''
    grid = [list(string) for string in grid]
    start, end = find_start_end(grid, True)
    return bfs(grid, start, end)

def part2(grid):
    '''
    Given raw string input for part2, find the shortest path
    '''
    grid = [list(string) for string in grid]
    start, end = find_start_end(grid, False)
    return bfs(grid, start, end)

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/12.in", sep="\n")

    print("TASK 1")
    util.call_and_print(part1, copy.deepcopy(sample))
    util.call_and_print(part1, copy.deepcopy(input))
    

    print("\nTASK 2")
    util.call_and_print(part2, copy.deepcopy(sample))
    util.call_and_print(part2, copy.deepcopy(input))


