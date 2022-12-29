"""
Day 20
https://adventofcode.com/2022/day/20
1st time: 02:00:00
2nd time: 00:10:00
My original solution did not take into account of the fact that the given list could contain duplicate elements, and I spent a lot of time trying to debug edges cases
I finally realized that i need to perform % (len - 1) instead of % len

I spent 10 mins figuring out the second half and desparetely trying to debug only to realize I accidently changed one value in the input file....
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
    # the circurlar queue is not fully utilized because the problem is not particularly suited to my original implementattion of circular buffer/queue
    def __init__(self, raw_input = None, k=None):
        if raw_input:
            self.array = copy.deepcopy(raw_input)
        else:
            self.array = [None] * k
        self.head = 0
        self.tail = 0
        if not k: 
            self.k = len(raw_input)
        else:
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
        final_idx = (start_index + position) % (self.k)
        print("FINAL_INDEX:", final_idx)
        print("SELF.K:", self.k)
        return self.array[final_idx]

    
def simulate(raw_input, mixing_number=1, multiplier=1):
    '''
    Compute the sum of the elements at 1000th, 2000th, and 3000th position
    '''

    # we first zip together the values along with their index to make sure that each value is unique
    # i.e., if the original list is [4, 21, 1], the result is [(4,0), (21, 1), (1,2)]
    zero_original = raw_input.index(0)
    zero_tuple = (0, zero_original)
    raw_input = [multiplier * number for number in raw_input]
    input_tuple = list(zip(raw_input,range(len(raw_input))))
    queue = CircularQueue(input_tuple)

    for _ in range(mixing_number):
        for element in input_tuple:
            idx = queue.find_index(element)
            # for each element, we perform the mixing encryption
            # i.e., move the element to the number of steps equal to its value right in the circular queue        
            position = (idx + element[0]) % (queue.k - 1) # NOTE: we do % (queue.k - 1) because we remove the element first, and then add it back. Adding is done when the array has (len - 1) number of elements remaining. Hence the minus 1.
            
            queue.move(element, position)

    idx_0 = queue.find_index(zero_tuple) # find the zero index
    # compute the sum
    print(queue.position(idx_0, 1000), queue.position(idx_0, 2000), queue.position(idx_0, 3000))
    return sum([queue.position(idx_0, 1000)[0], queue.position(idx_0, 2000)[0], queue.position(idx_0, 3000)[0]])

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample.in", sep="\n")
    input = util.read_ints("input/20.in", sep="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    util.call_and_print(simulate, sample)
    util.call_and_print(simulate, input)
    
    print("\nTASK 2")
    util.call_and_print(simulate, sample, 10, 811589153)
    util.call_and_print(simulate, input, 10, 811589153)


