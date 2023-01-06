"""
Day 17
https://adventofcode.com/2022/day/17
1st time: a day or so
2nd time: too many days
This problem killed me because I made some silly bug. I do not like simulation type of problems. It seems to me that the second problem is related to string matching problem 
-- I will study them once I have more time...

Okay. This involves studying plenty of pattern matching algorithms, and the LPS array is the one that stood out. 
I thought LCP is the LPS only to realize they are completely different.....
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
                # print(grid.render())
                # print(grid.highests)
                # print(grid.highest)
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
        

    # Using counting sort to sort the elements in the basis of significant places
def countingSort_int(array, place):
    size = len(array)
    output = [0] * size
    count = [0] * 10

    # Calculate count of elements
    for i in range(0, size):
        index = array[i] // place
        count[index % 10] += 1

    # Calculate cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Place the elements in sorted order
    i = size - 1
    while i >= 0:
        index = array[i] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(0, size):
        array[i] = output[i]

def countingSort_tuple(array, place):
    '''
    Given the index, or place, of the tuples in the array,
    apply countingSort to the array of tuples
    Note: the array elemeent should be tuples with each element in the range of 0 - 9 
    '''
    size = len(array)
    output = [0] * size
    count = [0] * 10
    idx = place - 1

    # calculate count of elements 
    for i in range(0, size):
        index = array[i][idx]
        count[index] += 1
    
    i = size - 1
    while i >= 0:
        index = array[i][idx]
        output[count[index] - 1] = array[i]
        count[index] -= 1
        i -= 1
    for i in range(0, size):
        array[i] = output[i]


# Main function to implement radix sort to both array of integers and array of tuples
def radixSort(array):
    # Get maximum element
    max_element = max(array)

    # Apply counting sort to sort elements based on place value.
    place = 1
    if type(array[0]) == int:
        while max_element // place > 0:
            if type(array[0]) == int:
                countingSort_int(array, place)
                place += 1

    elif type(array[0]) == tuple:
        while place < len(max_element):
            countingSort_tuple(array, place)
            place += 1


# Python3 program for building suffix
# array of a given text

# Class to store information of a suffix
class suffix:
	
	def __init__(self):
		
		self.index = 0
		self.rank = [0, 0]

# This is the main function that takes a
# string 'txt' of size n as an argument,
# builds and return the suffix array for
# the given string
def buildSuffixArray(txt, n, start_ord="a"):
    
    # A structure to store suffixes
    # and their indexes
    suffixes = [suffix() for _ in range(n)]

    # Store suffixes and their indexes in
    # an array of structures. The structure
    # is needed to sort the suffixes alphabetically
    # and maintain their old indexes while sorting
    for i in range(n):
        suffixes[i].index = i
        suffixes[i].rank[0] = (ord(txt[i]) -
                            ord(start_ord))
        suffixes[i].rank[1] = (ord(txt[i + 1]) -
                        ord(start_ord)) if ((i + 1) < n) else -1
    
    # Sort the suffixes according to the rank
    # and next rank
    suffixes = sorted(
        suffixes, key = lambda x: (
            x.rank[0], x.rank[1]))
    # suffixes = radixSort(suffixes)

    # At this point, all suffixes are sorted
    # according to first 2 characters. Let
    # us sort suffixes according to first 4
    # characters, then first 8 and so on
    ind = [0] * n # This array is needed to get the
                # index in suffixes[] from original
                # index.This mapping is needed to get
                # next suffix.
    k = 4
    while (k < 2 * n):
        
        # Assigning rank and index
        # values to first suffix
        rank = 0
        prev_rank = suffixes[0].rank[0]
        suffixes[0].rank[0] = rank
        ind[suffixes[0].index] = 0

        # Assigning rank to suffixes
        for i in range(1, n):
            
            # If first rank and next ranks are
            # same as that of previous suffix in
            # array, assign the same new rank to
            # this suffix
            if (suffixes[i].rank[0] == prev_rank and
                suffixes[i].rank[1] == suffixes[i - 1].rank[1]):
                prev_rank = suffixes[i].rank[0]
                suffixes[i].rank[0] = rank
                
            # Otherwise increment rank and assign
            else:
                prev_rank = suffixes[i].rank[0]
                rank += 1
                suffixes[i].rank[0] = rank
            ind[suffixes[i].index] = i

        # Assign next rank to every suffix
        for i in range(n):
            nextindex = suffixes[i].index + k // 2
            suffixes[i].rank[1] = suffixes[ind[nextindex]].rank[0] \
                if (nextindex < n) else -1

        # Sort the suffixes according to
        # first k characters
        suffixes = sorted(
            suffixes, key = lambda x: (
                x.rank[0], x.rank[1]))

        k *= 2

    # Store indexes of all sorted
    # suffixes in the suffix array
    suffixArr = [0] * n
    
    for i in range(n):
        suffixArr[i] = suffixes[i].index

    # Return the suffix array
    return suffixArr

# A utility function to print an array
# of given size
def printArr(arr, n):
    
    for i in range(n):
        print(arr[i], end = " ")
        
    print()

def buildLCP(s, pos):
    '''
    Given a string s and its suffix array pos, compute the LCP array
    '''
    lcp = [0] * len(pos)
    rank = [0] * len(pos)
    for i in range(len(pos)):
        rank[pos[i]] = i
    n = len(pos)
    k = 0

    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = pos[rank[i] + 1]
        while (i + k < n and j + k < n and s[i + k] == s[j + k]):
            k += 1
        lcp[rank[i]] = k 
        if k > 0:
            k -= 1
    return lcp



def part2(string):
    '''
    We are under the assumption that there is a repeating substructure and we try to justify that substructure by applying KMP
    '''
    # This attempt tries to find the repeated substring in the string such taht the string can be divided into a + s + s .... + s FOR k such s's
    # it failed ;-;
    # divide the string into multiple segments such that 
    # the string is in the format of a + s + s + s + ... + s FOR k such s's 
    # return the answer by simulating a plus k times simulating s
    
    # runs in O(n^2)
    
    for i in range(len(string)):
        preceding = string[:i]
        remaining = string[i:]
        result = repeatedSubstringPattern(remaining)
        if result:
            # we have found our pattern
            # do the simulation for the preceding part 
            # and do one simulation for the next part
            break

    grid = Grid(7)
    pattern = deque(preceding)
    i = 0
    tetris_type = 0
    tetris = None
    output = []
    first = True
    while pattern:
        if i == 0:
            # initialize a new rock
            # if grid.number == end - 1:
            # if grid.number == end:
            #     # print("\n\n")
            #     # print(grid.render())
            #     # print(grid.highests)
            #     # print(grid.highest)
            #     break
            #     # print(len(pattern))
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
        if not pattern and first:
            # print("no pattern, refill")
            pattern = deque(result)
            output.append(grid.highest)
            first = False
    output.append(grid.highest)
    print(output)
    period = output[1] - output[0]
    print(preceding)
    print(remaining)
    return output[0] + len(remaining) // len(result) * period

def LSP(pattern):
        # longest suffix prefix problem
        # return an array where arr[i] represents the longest length of the suffix prefix match
        A = [0] * len(pattern)

        i, prev = 1, 0
        while i < len(pattern):
            if pattern[i] == pattern[prev]:
                A[i] = prev + 1
                i += 1
                prev += 1
            elif prev == 0:
                A[i] = 0
                i += 1
            else:
                prev = A[prev - 1]
        return A

def find_pattern(heights):
    '''
    Given the increase in heights, find the cyclic pattern
    if no pattern is found, return None
    '''
    
    # compute the suffix array, and compute the lcp array of the reversed height increase array
    reverse_string = "".join(list(reversed(heights)))
    # print("string:", heights)
    # suffixes = buildSuffixArray(reverse_string, len(heights), "0")
    # lcp = buildLCP(reverse_string, suffixes)
    # print("reversed string:", reverse_string)

    # print("suffix array:", suffixes)
    # print("lcp array:", lcp)
    maximum = 0
    cycle_length = None
    lps = LSP(reverse_string)
    # print("lps array:", lps)
    for i in range(len(lps)):
        j = (i+1) // 2
        if (i + 1) % 2 == 0 and lps[i] == j and lps[i] > maximum:
            # print(reverse_string[0:i+1])
            # print(reverse_string[0:(i-j)+1])
            maximum = i
            cycle_length = i - j + 1
            # print("maximum lps:", lps[maximum])
            # print("length of the entire:", len(reverse_string[0:i + 1]))
            # print("length of the first half:", len(reverse_string[0:(i - j) + 1]))
    if cycle_length not in range(0, 20):
        return cycle_length
    else: 
        return None
    


def part2_updated(string):
    grid = Grid(7)
    pattern = deque(string)
    i = 0
    tetris_type = 0
    tetris = None
    heights = []
    heights_increase = []
    while pattern:
        if i == 0:
            # initialize a new rock
            # if grid.number == end - 1:
            # if grid.number == end:
            #     # print("\n\n")
            #     # print(grid.render())
            #     # print(grid.highests)
            #     # print(grid.highest)
            #     break
            #     # print(len(pattern))
            result = None
            if tetris and not heights_increase:
                heights_increase.append(str(grid.highest))
                heights.append(grid.highest)
            elif tetris and heights_increase:
                heights_increase.append(str(grid.highest - heights[-1]))
                heights.append(grid.highest)

                result = find_pattern(heights_increase) 
            
            if result:
                cycle_length = result
                # print("cycle length:", cycle_length)
                # print("heights increase:", heights_increase)
                    # increase in heights will be: 
                heights_increase_ints = [int(string) for string in heights_increase]
                diff =  1_000_000_000_000 - grid.number
                groups =  diff // cycle_length
                remainder = diff % cycle_length
                cycle_increase = sum((heights_increase_ints)[-cycle_length:])
                cycle_increase_remainder = sum(heights_increase_ints[-cycle_length:-(cycle_length-remainder)])
                print(cycle_length)
                print(cycle_increase)
                print(cycle_increase_remainder)
                grid.highest += (groups * cycle_increase)
                grid.highest += cycle_increase_remainder
                break                    
                    
                # we simulate until our block reach to 
                # repeat the same cycle until we reach to block number
            tetris = grid.initialize_tetris(tetris_type + 1)
            tetris_type += 1
            tetris_type %= 5
            i += 1
            continue
        if i % 2 == 0:
            # case of vertical falls
            if not grid.fall(tetris):
                # the tetris fall was unsuccessful, meaning that our height has changed
                # update the tetris
                i = 0
            else:
                i += 1
            continue
        # otherwise, push by the jet
        char = pattern.popleft()
        # if grid.number == end - 1 or grid.number == end:
        if char == '<':
            grid.push_left(tetris)
            i += 1
        elif char == '>':
            grid.push_right(tetris)
            i += 1
        if not pattern:
            pattern = deque(string)
    
    return grid.highest
            
    
    
    

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in")
    input = util.read_strs("input/17.in")
    

    sample = sample[0]
    input = input[0]
    print("TASK 1")
    # util.call_and_print(simulate, sample, 7, 2022)
    # util.call_and_print(simulate, input, 7, 2022)
    



    print("\nTASK 2")
    util.call_and_print(part2_updated, sample)
    util.call_and_print(part2_updated, input)


