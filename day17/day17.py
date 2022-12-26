"""
Day 17
https://adventofcode.com/2022/day/17
1st time: a day or so
2nd time: N/A
This problem killed me because I made some silly bug. I do not like simulation type of problems. It seems to me that the second problem is related to string matching problem -- I will study them once I have more time...
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


class Tetris:

    PIECE1 = [["#", "#", "#", "#"]]

    PIECE2 = [[".", "#", "."],
              ["#", "#", "#"],
              [".", "#", "."]]

    PIECE3 = [[".", ".", "#"],
              [".", ".", "#"],
              ["#", "#", "#"]]

    PIECE4 = [["#"],
              ["#"],
              ["#"],
              ["#"]]

    PIECE5 = [["#", "#"],
              ["#", "#"]]
    PIECES=[PIECE1, PIECE2, PIECE3, PIECE4, PIECE5]

    def __init__(self, x, y, type):
        # self.piece = piece
        # the x,y coordinate is the lower left corner of the pieces except piece 2
        self.x = x
        self.y = y
        self.type = type




class Grid:
    def __init__(self, width):
        self.rock = set()
        self.highests = [0 for _ in range(width)]
        self.width = width
        self.highest = 0
        self.number = 0
    
        

    def render(self):
        '''
        render the current grid with all rocks
        '''
        output = [["." for _ in range(self.width)] for _ in range(self.highest + 1)]
        # print("--------------------")
        # print(self.highest)
        # print(self.width)
        # print(output)
        for x,y in self.rock:
            # print(x,y)
            # print(self.rock)
            output[y][x] = '#'
        final = "".join(["".join(string) + "\n" for string in reversed(output)])
        return final

    def validate(self, tetris):
        '''
        Given a tetris's position, determine if the tetris touches a rested rock
        '''
        y = tetris.y 
        current = set()
        leftmost = tetris.x
        rightmost = 0
        if tetris.type == 1:
            # check for boundary:
            rightmost = tetris.x + 3               
            for x in range(leftmost, leftmost + 4):
                current.add((x,y))
        elif tetris.type == 2:
            leftmost = tetris.x - 1
            rightmost = tetris.x + 1
            y1 = y + 1
            y2 = y + 2
            x1 = tetris.x
            x0 = x1 - 1
            x2 = x1 + 1
            
            # lower
            current.add((x1, y))
            # middle 
            current.add((x0, y1))
            current.add((x1, y1))
            current.add((x2,y1))
            # upper
            current.add((x1, y2))

        elif tetris.type == 3:
            rightmost = tetris.x + 2
            x0 = tetris.x
            # ---
            for x in range(x0, x0 + 3):
                current.add((x, y))
            # |
            # |
            # |
            for y0 in range(y, y + 3):
                current.add((x0 + 2, y0))
        
        elif tetris.type == 4:
            rightmost = tetris.x
            x = tetris.x
            for y0 in range(y, y + 4):
                current.add((x,y0))

        elif tetris.type == 5:
            rightmost = tetris.x + 1
            x = tetris.x
            current.add((x, y))
            current.add((x + 1, y))
            current.add((x, y + 1))
            current.add((x+1, y+1))
        
        # check for left, right boundary
        if leftmost < 0 or rightmost >= self.width:
            return False
        # check for intersection
        intersection = current & self.rock
        return True if len(intersection) == 0 else False


    def add_rock(self, tetris):
        '''
        add the current coordiantes to the rock
        '''
        y = tetris.y 
        current = set()
        if tetris.type == 1:
            # check for a horizontal line
            leftmost = tetris.x 
            for x in range(leftmost, leftmost + 4):
                current.add((x,y))
        elif tetris.type == 2:
            y1 = y + 1
            y2 = y + 2
            x1 = tetris.x
            x0 = x1 - 1
            x2 = x1 + 1
            
            # lower
            current.add((x1, y))
            # middle 
            current.add((x0, y1))
            current.add((x1, y1))
            current.add((x2,y1))
            # upper
            current.add((x1, y2))

        elif tetris.type == 3:
            x0 = tetris.x
            # ---
            for x in range(x0, x0 + 3):
                current.add((x, y))
            # |
            # |
            # |
            for y0 in range(y, y + 3):
                current.add((x0 + 2, y0))
        
        elif tetris.type == 4:
            x = tetris.x
            for y0 in range(y, y + 4):
                current.add((x,y0))

        elif tetris.type == 5:
            x = tetris.x
            current.add((x, y))
            current.add((x + 1, y))
            current.add((x, y + 1))
            current.add((x+1, y+1))
        # after adding, update the highests array
        self.update_hightest(tetris)
        self.rock = current | self.rock
        self.number += 1


    def fall(self, tetris):
        '''
        return True if the fall is successful
        otherwise return False 
        '''
        if tetris.y == 0:
            # cannot fall anymore, add to the rock
            self.add_rock(tetris)
            return False
        tetris.y -= 1
        if self.validate(tetris):
            return True
        else:
            tetris.y += 1
            self.add_rock(tetris)
        return False 
         

    def push_left(self, tetris):
        if tetris.type == 2:
            if tetris.x - 1 == 0:
                return
        else:
            if tetris.x == 0:
                # ignore 
                return
        tetris.x -= 1
        if self.validate(tetris):
            return 
        else:
            tetris.x += 1
            return

    def push_right(self, tetris):
        if tetris.type == 1:
            rightmost = tetris.x + 3
        elif tetris.type == 2:
            rightmost = tetris.x + 1
        elif tetris.type == 3:
            rightmost = tetris.x + 2
        elif tetris.type == 4:
            rightmost = tetris.x
        elif tetris.type == 5:
            rightmost = tetris.x + 1
        else:
            raise Exception("buggy")
            
        if rightmost  == self.width - 1:
            # ignore

            return
        tetris.x += 1
        if self.validate(tetris):
            return
        else:
            tetris.x -= 1
            return

    def update_hightest(self, tetris):
        '''
        update the highest points of the grid with a resting tetris block 
        '''
        
        # depending on the type of the pieces, add the highest x / highest y to the tetris block 
        
        if tetris.type == 1:
            
            for x in range(tetris.x, tetris.x + 4):
                self.highests[x] = max(self.highests[x], tetris.y)
        elif tetris.type == 2:
            x0 = tetris.x - 1
            x1 = tetris.x 
            x2 = tetris.x + 1 
            y0 = tetris.y + 1
            y1 = tetris.y + 2
            y2 = tetris.y + 1
            self.highests[x0] = max(self.highests[x0], y0)
            self.highests[x1] = max(self.highests[x1], y1)
            self.highests[x2] = max(self.highests[x2], y2)
        elif tetris.type == 3:
            x0 = tetris.x 
            x1 = tetris.x + 1
            x2 = tetris.x + 2
            y0 = tetris.y
            y1 = tetris.y
            y2 = tetris.y + 2
            self.highests[x0] = max(self.highests[x0], y0)
            self.highests[x1] = max(self.highests[x1], y1)
            self.highests[x2] = max(self.highests[x2], y2)
        elif tetris.type == 4:
            self.highests[tetris.x] = max(self.highests[tetris.x], tetris.y + 3)
        elif tetris.type == 5:
            x0 = tetris.x
            x1 = tetris.x + 1
            y0 = tetris.y + 1
            y1 = tetris.y + 1
            self.highests[x0] = max(self.highests[x0], y0)
            self.highests[x1] = max(self.highests[x1], y1)

        self.highest = max(self.highests) + 1
        return 

    def initialize_tetris(self, tetris_type):
        '''
        Given the type of the tetris (1-5)
        return a tetris object given the highest point and 
        '''
        if tetris_type == 2:
            tetris = Tetris(3, self.highest + 3, tetris_type)
        else:
            tetris = Tetris(2, self.highest + 3, tetris_type)
        return tetris

def simulate(raw_input, width, end):
    grid = Grid(width)
    pattern = deque(raw_input)
    i = 0
    tetris_type = 0
    tetris = None
    while grid.number <= end:
        if i == 0:
            # initialize a new rock
            # if grid.number == end - 1:
            if grid.number == end:
                # print("\n\n")
                print(grid.render())
                print(grid.highests)
                print(grid.highest)
                break
                # print(len(pattern))
            tetris = grid.initialize_tetris(tetris_type + 1)
            tetris_type += 1
            tetris_type %= 5 
            i += 1
            continue
        if i % 2 == 0:
            # case of vertical falls
            if not grid.fall(tetris):
                # the tetris fall was unsuccessful, update the tetris
                i = 0
            else:
                i += 1
            continue
        # otherwise, push by the jet
        char = pattern.popleft()
        # if grid.number == end - 1 or grid.number == end:
        #     print(char)
        if char == '<':
            grid.push_left(tetris)
            i += 1
        elif char == '>':
            grid.push_right(tetris)
            i += 1
        if not pattern:
            # print("no pattern, refill")
            pattern = deque(raw_input)
    return grid.highest
        


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in")
    input = util.read_strs("input/17.in")
    

    sample = sample[0]
    input = input[0]
    print("TASK 1")
    util.call_and_print(simulate, sample, 7, 2022)
    util.call_and_print(simulate, input, 7, 2022)
    

    # print("\nTASK 2")
    # util.call_and_print(simulate, sample_graph, False)
    # util.call_and_print(simulate, input_graph, False)


