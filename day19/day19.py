"""
Day 19
https://adventofcode.com/2022/day/19
1st time: 01:00:00
2nd time: 00:30:00
I did not believe that the brute-force dfs solves this problem. Then my computer shuts down when I tried the same for the second part
I was only able to get it when I thought more about the pruning techniques involved.
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


class Blueprint:
    def __init__(self, id, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, 
                obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        self.id = id
        self.ore_ore_cost = ore_ore_cost
        self.clay_ore_cost = clay_ore_cost
        self.obsidian_ore_cost = obsidian_ore_cost
        self.obsidian_clay_cost = obsidian_clay_cost
        self.geode_ore_cost = geode_ore_cost
        self.geode_obsidian_cost = geode_obsidian_cost

def task1(raw_input, time, initial_ore_robot):
    '''
    Given the raw unprocessed text, extract necessary informations for the blueprint
    '''
    score = 0

    # @lru_cache(maxsize=None)
    def dfs(bp, time_remain, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, memo={}, maximum=0):
        '''
        DFS with pruning
        '''
        # print("CALLING DFS")
        # print((time_remain, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot))
        args = (bp, time_remain, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot)
        if args in memo:
            return memo[args]

        if time_remain == 0:
            # we have reached the end of the execution, return the number of geode that we have mined
            return geode

        if geode + (2 * geode_robot + time_remain) * time_remain / 2 < maximum:
            return 0

        maximum_geode = geode
        # get the new raw materials from the working robots
        ore_gain = ore_robot
        clay_gain = clay_robot
        obsidian_gain = obsidian_robot
        geode_gain = geode_robot

        if ore >= bp.geode_ore_cost and obsidian >= bp.geode_obsidian_cost:
            # print("more than one ore and obsidian")
            score = dfs(bp, 
                        time_remain - 1, 
                        ore + ore_gain - geode_ore_cost, 
                        clay + clay_gain, 
                        obsidian + obsidian_gain - geode_obsidian_cost, 
                        geode + geode_gain, 
                        ore_robot,
                        clay_robot, 
                        obsidian_robot,
                        geode_robot + 1,
                        memo) 
            maximum_geode = max(maximum_geode, score)  
        else:
            # otherwise, we determine which robots we can make
            if ore_robot < bp.clay_ore_cost or ore_robot < bp.obsidian_ore_cost or ore_robot < bp.geode_ore_cost:
                if ore >= bp.ore_ore_cost:
                    # print("more than one ore")
                    score = dfs(bp,
                                time_remain - 1, 
                                ore + ore_gain - ore_ore_cost, 
                                clay + clay_gain, 
                                obsidian + obsidian_gain, 
                                geode + geode_gain, 
                                ore_robot + 1, 
                                clay_robot, 
                                obsidian_robot, 
                                geode_robot,
                                memo) 
                    maximum_geode = max(maximum_geode, score)    
            if clay_robot < bp.obsidian_clay_cost:
                if ore >= bp.clay_ore_cost:
                    # print("more than one clay")
                    score = dfs(bp,
                                time_remain - 1, 
                                ore + ore_gain - clay_ore_cost, 
                                clay + clay_gain, 
                                obsidian + obsidian_gain,   
                                geode + geode_gain,  
                                ore_robot, 
                                clay_robot + 1,  
                                obsidian_robot, 
                                geode_robot,
                                memo)
                    maximum_geode = max(maximum_geode, score)

            if obsidian_robot < bp.geode_obsidian_cost:
                if ore >= bp.obsidian_ore_cost and clay >= bp.obsidian_clay_cost:
                    # print("more than one ore and one clay")
                    score = dfs(bp, 
                                time_remain - 1, 
                                ore + ore_gain - obsidian_ore_cost, 
                                clay + clay_gain - obsidian_clay_cost, 
                                obsidian + obsidian_gain, 
                                geode + geode_gain, 
                                ore_robot, 
                                clay_robot, 
                                obsidian_robot + 1, 
                                geode_robot,
                                memo) 
                    maximum_geode = max(maximum_geode, score)    
            # we make no robots
            score = dfs(bp, 
                        time_remain - 1, 
                        ore + ore_gain, 
                        clay + clay_gain, 
                        obsidian + obsidian_gain, 
                        geode + geode_gain, 
                        ore_robot,
                        clay_robot, 
                        obsidian_robot,
                        geode_robot,
                        memo)         
            maximum_geode = max(maximum_geode, score)
        
        memo[args] = maximum_geode
        return maximum_geode
    largest_geodes = 1
    for blueprint in raw_input:
        bp_id = parse.parse("Blueprint {:d}:", blueprint[0])[0]
        ore_ore_cost = parse.parse("  Each ore robot costs {:d} ore.", blueprint[1])[0]
        clay_ore_cost = parse.parse("  Each clay robot costs {:d} ore.", blueprint[2])[0]
        obsidian_ore_cost, obsidian_clay_cost = parse.parse("  Each obsidian robot costs {:d} ore and {:d} clay.", blueprint[3])
        geode_ore_cost, geode_obsidian_cost = parse.parse("  Each geode robot costs {:d} ore and {:d} obsidian.", blueprint[4])
        bp = Blueprint(bp_id, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost)
        largest_geode = dfs(bp, time, 0, 0, 0, 0, initial_ore_robot, 0, 0, 0)
        print(bp_id, largest_geode)
        score += (bp_id * largest_geode)
        largest_geodes *= largest_geode
    return score, largest_geodes

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/19.in", sep="\n\n", sep2="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1")
    # util.call_and_print(task1, sample, 24, 1)
    # util.call_and_print(task1, input, 24, 1)
    
    print("\nTASK 2")
    input = input[0:3]
    # sample = sample[0:3]
    # util.call_and_print(task1, sample, 32, 1)
    util.call_and_print(task1, input, 32, 1)


