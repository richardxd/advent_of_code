"""
Day 20
https://adventofcode.com/2022/day/20
1st time: 
2nd time: 

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


class CircularQueue:
    def __init__(self, k: int):
        self.array = [None] * k
        self.head = 0
        self.tail = 0
        self.k = k
        self.length = 0
        


    def enQueue(self, value: int) -> bool:
        if self.length == self.k:
            return False
        # otherwise, add to the end of the queue
        # if self.tail >= self.k:
        idx = self.tail % self.k
        if self.array[idx]:
            print(self.array)
            raise Exception("calculation incorrect")

        self.array[idx] = value
        self.tail += 1
        self.tail %= self.k
        self.length += 1
        return True

    def deQueue(self) -> bool:
        if self.length == 0:
            return False
        # remove, update the head
        self.array[self.head] = None
        self.head += 1
        self.head %= self.k
        self.length -= 1
        return True
        

    def Front(self) -> int:
        if self.length == 0:
            return -1
        return self.array[self.head]

    def Rear(self) -> int:
        if self.length == 0:
            return -1
        return self.array[self.tail - 1]

    def isEmpty(self) -> bool:
        if self.length == 0:
            return True
        return False
        

    def isFull(self) -> bool:
        if self.length == self.k:
            return True
        return False

    def move(self, value, index):
        '''
        move an element equal to the value from the circular buffer to another index
        '''
        self.array.remove(value)
        self.array.insert(index, value)
        

    def find_index(self, value):
        '''
        Given a value, find the index of the value
        '''
        return self.array.index(value)

    def position(self, start_index, position):
        '''
        Given the starting index of the circular buffer, find the element 
        corresponding to the position step forward
        '''
        final_idx = (start_index + (position % self.k)) % self.k 
        return self.array[final_idx]

    
def part1(raw_input):
    queue = CircularQueue(len(raw_input))
    for element in raw_input
        queue.enQueue(element)
    
    for element in raw_input:
        idx = queue.find_index(element)
        position = (idx + element) % queue.k
        queue.move(idx, position)
    return sum(queue.position(0, 1000), queue.position(0, 2000), queue.position(0, 3000))

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample.in", sep="\n")
    input = util.read_ints("input/20.in", sep="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)
    
    # print("\nTASK 2")
    # util.call_and_print(task1, sample, 32, 1)
    # util.call_and_print(task1, input, 32, 1)


