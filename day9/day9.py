"""
Day 9
https://adventofcode.com/2022/day/9
1st time: about 30mins
2nd time: about 30mins

A very tiring problem involving doubly linked list. I'm too tired of it now.
I have an ad-hoc solution for the first-half, so it took me great effort to 
refactor that for the second-half (¯\_(ツ)_/¯)
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


# essentially a class of doubly linked list with values being x,y coordinates
class Knots:
    def __init__(self, x, y, prev=None, next=None):
        self.val = (x,y)
        self.prev = prev
        self.next = next

    
    def update_knot(self, x0, y0, visited):
        """
        update the current node to x0, y0
        in case that this node happens to be the tail of the linked list, update the visited set
        if there is a true update -- the pair of coordinates has indeed chagned -- update the children as well
        """
        if self.next == None:
            visited.add((x0, y0))
        self.val = (x0, y0)
        if not self.next:
            return 
        x1, y1 = check_update_adjacency(x0, y0, self.next.val[0], self.next.val[1])
        if (x1, y1) != self.next.val:
            self.next.update_knot(x1,y1, visited)
        return 
    
def knots_init(size):
    '''
    Given the size of the linked list, make a linked list of size 9
    return the head of the knots
    '''
    dummy = Knots(0,0)
    curr = dummy
    for i in range(size):
        curr.next = Knots(0,0, prev=curr)
        curr = curr.next
    return dummy.next

def check_update_adjacency(x0, y0, x1, y1):
    '''
    Given two pairs of x-y coordinates, check if the Head and the Tail are 8-directionally adjacent
    if not, update the tail coordinate accordingly
    '''
    if abs(x1 - x0) <= 1 and abs(y1 - y0) <= 1:
        return x1, y1
    
    if x0 == x1:
        # same column
        y1 += 1 if y0 > y1 else -1
        return x1, y1
    elif y0 == y1:
        x1 += 1 if x0 > x1 else -1 
        return x1, y1
    
    x1 += 1 if x0 > x1 else -1
    y1 += 1 if y0 > y1 else -1

    return x1, y1

def simulate_dir(head, direction, n, visited):
    '''
    Simulate one sequence of instructions of the head
    given the direction to move and the steps to move
    keep an array of visited grid for the tail
    '''
    x0, y0 = head.val
    while n > 0:
        # update head_coordinate now
        if direction == "L":
            y0 -= 1
        elif direction == "R":
            y0 += 1
        elif direction == "U":
            x0 += 1
        elif direction == "D":
            x0 -= 1
        else:
            raise Exception("Buggy inputs")
        head.update_knot(x0, y0, visited)
        n -= 1

def simulate(moves, size):
    '''
    run the entire simulations and return the number of grid visited at least once by the tail
    '''
    start_x = 0
    start_y = 0

    head = knots_init(size)
    visited = set()
    visited.add(head.val)
    for move in moves: 
        direction, n = move
        simulate_dir(head, direction, int(n), visited)
    return len(visited)

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=" ")
    input = util.read_strs("input/09.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(simulate, copy.deepcopy(sample), 2)
    util.call_and_print(simulate, copy.deepcopy(input), 2)
    
    sample2 = util.read_strs("input/sample2.in", sep="\n", sep2=" ")

    print("\nTASK 2")
    util.call_and_print(simulate, copy.deepcopy(sample2), 10)
    util.call_and_print(simulate, copy.deepcopy(input), 10)


