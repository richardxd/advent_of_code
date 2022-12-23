"""
Day 12
https://adventofcode.com/2022/day/12
1st time: 00:15:00
2nd time: 00:16:00
I spent a ton of time trying to get parser to work only realize that I could have 
simply invokved the function eval to evaluate python expression.... Good lesson for a python newbie
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
from collections import Counter
import bisect

from functools import cmp_to_key

from util import log






def comparator(array1, array2):
    '''
    Given two arrays (datatype deque), compare and decide if they are in the right order
    return:
        -1: array1 < array2(right order)
        0: array1 = array2
        1: array1 > array2(wrong order)
    '''
    array1 = deque(array1)
    array2 = deque(array2)
    while array1 and array2:
        left = array1.popleft()
        right = array2.popleft()
        if type(left) is list and type(right) is list:
            
            ret = comparator(left, right)
            if ret != 0:
                return ret

        elif type(left) is list:
            # elevate right to list
            right_lst = [right]
            ret = comparator(left, right_lst)
            if ret != 0:
                return ret
        elif type(right) is list:
            # left_lst = [left for _ in range(len(right))]
            left_lst = [left]
            ret = comparator(left_lst, right)
            if ret != 0:
                return ret
        elif left > right: 
            return 1
        elif left < right:
            return -1

    if not array1 and not array2:
        return 0
    if array1:
        return 1
    
    return -1        
    



        

def part1(arrays):
    '''
    compute the sum of the indices of the array pairs in right order
    '''
    output = []
    for i in range(len(arrays)):
        array1 = arrays[i][0]
        array2 = arrays[i][1]
        
        if comparator(array1, array2) == -1:
            output.append(i+1)
    return sum(output)

def part2(arrays, divider):
    '''
    sort the arrays + divider and locate the dividers
    '''
    merged = arrays + divider
    cmp = cmp_to_key(comparator)
    sorted_array = sorted(merged, key=cmp)
    div1, div2 = divider
    # idx1 = bisect.bisect_left(div1, sorted_array)
    # idx2 = bisect.bisect_left(div2, sorted_array)
    # for i in range(len(sorted_array)):
    #     curr = sorted_array[i]
    #     if comparator(div1, curr) == 0:
    #         idx1 = i + 1
    #     if comparator(div2, curr) == 0:
    #         idx2 = i + 1
    # print(sorted_array)
    idx1 = sorted_array.index(div1) + 1
    idx2 = sorted_array.index(div2) + 1
    return idx1 * idx2
    

def process_io(arrays):
    '''
    process the io for part1
    '''
    output = []
    for left, right in arrays:
        
        left_ret = eval(left)
        right_ret = eval(right)
        output.append([left_ret, right_ret])
    # print(output)
    return output
        
def process_io_2(arrays):
    '''
    process the io for part2
    '''
    output = []
    for left, right in arrays:
        
        left_ret = eval(left)
        right_ret = eval(right)
        output.append(left_ret)
        output.append(right_ret)

    return output

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/13.in", sep="\n\n", sep2="\n")
    
    sample_processed = process_io(sample)
    input_processed = process_io(input)

    print("TASK 1")
    util.call_and_print(part1, copy.deepcopy(sample_processed))
    util.call_and_print(part1, copy.deepcopy(input_processed))
    
    sample_processed = process_io_2(sample)
    input_processed = process_io_2(input)

    divider = [[[2]], [[6]]]

    print("\nTASK 2")
    util.call_and_print(part2, copy.deepcopy(sample_processed), divider)
    util.call_and_print(part2, copy.deepcopy(input_processed), divider)


