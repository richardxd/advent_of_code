"""
Day 15
https://adventofcode.com/2022/day/15
1st time: 00:32:00
2nd time: 02:00:00 (brute force only takes another 5 mins...)
Part1: Merged interval baby!
Part2: i give up on finding faster solution. I will just iterate all possible distress beacon coordinates
also I'm glad I bought a fancy desktop just to get the brute-force solution lol
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


def compute_distance(x0, y0, x1, y1):
    '''
    Compute the manhattan distance between two coordinates
    '''
    manhattan = abs(x0 - x1) + abs(y0 - y1)
    return manhattan

def process_io(raw_input):
    '''
    Given the raw sensor/beacon inputs, create a hash map that maps sensors to beacons
    return the hash map
    '''
    sb_map = {}
    for sb in raw_input:
        x0,y0,x1,y1 = parse.parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", sb)[0:4]
        sb_map[(x0, y0)] = (x1, y1)
    return sb_map


def positions_unobtainable(sb_map, y):
    '''
    Given the sensor beacon map and the row's coordinate y, 
    find the number of positions already covered by all sb pairs
    '''
    intervals = []
    for (x0, y0), (x1, y1) in sb_map.items():
        dist = compute_distance(x0, y0, x1, y1)
        epsilon = dist - abs(y - y0)
        if epsilon < 0:
            continue 
        left = x0 - epsilon
        right = x0 + epsilon
        intervals.append([left, right])
    merged_interval = merge_interval(intervals)
    return count_positions(merged_interval), merged_interval
    
def merge_interval(intervals):
    '''
    Given an array of intervals, merge the interval such that there exists no overlapping intervals
    '''
    sorted_intervals = deque(sorted(intervals, key=lambda x:(x[0], x[1])))
    output = []
    output.append(sorted_intervals.popleft())
    while sorted_intervals:
        x1, y1 = sorted_intervals.popleft()
        x0, y0 = output[-1]
        if y1 <= y0:
            '''
            x0 --- y0
              x1-y1
            '''
            continue
        if x1 <= y0:
            '''
            x0 --- y0
              x1 ---- y1
            '''
            output[-1][1] = y1
            continue
        '''
        otherwise:
        x0 --- y0
                 x1 --- y1
        '''
        output.append([x1, y1])
    return output




def count_positions(intervals):
    '''
    Given sorted, non duplicate intervals, count the number of points covered by intervals in the form [x, y]
    '''
    cnt = 0
    for x, y in intervals:
        cnt += (y - x)
    return cnt 




def part2(sb_map, limit):
    '''
    iterate through all the possible locations for y and find that distress beacon
    '''
    for y in range(limit+1):
        _, intervals = positions_unobtainable(sb_map, y)
        intervals = deque(intervals)
        while intervals:
            curr = intervals.popleft()
            if curr[1] < 0:
                continue
            if curr[1] > 4000000:
                break
            if intervals:
                # if there are still remaining intervals, 
                # that means we have found the gap between two intervals
                # by uniqueness and the check we performed, this is the distress beacon
                return (curr[1] + 1) * 4000000 + y
    return -1


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/15.in", sep="\n")
    
    sample_map = process_io(sample)
    input_map = process_io(input)

    print("TASK 1")
    util.call_and_print(positions_unobtainable, copy.deepcopy(sample_map), 10)
    util.call_and_print(positions_unobtainable, copy.deepcopy(input_map), 2000000)
    

    print("\nTASK 2")
    util.call_and_print(part2, copy.deepcopy(sample_map), 20)
    util.call_and_print(part2, copy.deepcopy(input_map), 4000000)


