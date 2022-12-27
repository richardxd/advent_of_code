"""
Day 16
https://adventofcode.com/2022/day/16
1st time: 00:10:00
2nd time: 04:00:00
I figured out the first half of the question fairly easily. 
Only to realize that the second half is way more complicated than the first half.
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

DIRECTION = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,-1], [0,0,1]]

def find_connected_components(cubes):
    '''
    we pad the current coordinates, and find the connected component for each coordinate and group them in a set
    '''
    x_sub = [x for x,y,z in cubes]
    y_sub = [y for x,y,z in cubes]
    z_sub = [z for x,y,z in cubes]
    
    # beginning 
    min_x = min(x_sub) - 1
    min_y = min(y_sub) - 1
    min_z = min(z_sub) - 1
    max_x = max(x_sub) + 1
    max_y = max(y_sub) + 1
    max_z = max(z_sub) + 1
    
    
    visited = set()
    components = [] # keep track of the connected components of the graph
    for a in range(min_x, max_x + 1):
        for b in range(min_y, max_y + 1):
            for c in range(min_z, max_z + 1):
                is_cube = copy.deepcopy((a, b, c) in cubes)
                queue = deque()
                queue.append((a, b, c, is_cube))
                component = []  # store the 
                # traverse the graph using BFS
                while queue:
                    x, y, z, is_cube = queue.popleft()

                    if not (min_x <= x <= max_x) or not (min_y <= y <= max_y) or not (min_z <= z <= max_z):
                        # if the current coordinate is out of bound
                        continue 
                    
                    if (x,y,z) in cubes and not is_cube:                  
                        continue
                    
                    if (x,y,z) not in cubes and is_cube:
                        continue
                    
                    # now we check if the coordinate is valid             
                    if (x,y,z) in visited:
                        continue
                    component.append((x,y,z))
                    visited.add((x,y,z))
                    # everything checks out. we add its 6-directionally connected neighbors to the queue
                    for dx, dy, dz in DIRECTION:
                        queue.append((x + dx, y + dy, z + dz, is_cube))
                if not component:
                    continue
                component.append(is_cube)
                components.append(component)
    
    components.pop(0) # the first component is the padding and those "airs" that is not surrounded by the lava 
    return components

def count_exterior(components):
    '''
    Given connected components of the graph, calculate the connected components' exterior surface area
    '''
    surface = 0
    interior = 0
    for component in components:
        is_cube = component.pop()
        if not is_cube:
            result = simulate(component)
            interior += result
            continue
        result = simulate(component)
        surface += result         
    return surface - interior
    
     
        
                



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample.in", sep="\n", sep2=",")
    input = util.read_ints("input/18.in", sep="\n", sep2=",")
    
    sample = {(x,y,z) for x,y,z in sample}
    input = {(x,y,z) for x,y,z in input}
    
    print("TASK 1")
    util.call_and_print(simulate, sample)
    util.call_and_print(simulate, input)
    print("\nTASK 2")
    sample_components = find_connected_components(sample)
    input_components = find_connected_components(input)

    util.call_and_print(count_exterior, sample_components)
    util.call_and_print(count_exterior, input_components)


