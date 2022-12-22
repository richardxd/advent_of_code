"""
Day 11
https://adventofcode.com/2022/day/11
1st time: 01:17:08
2nd time: 02:21:05
It took me this long because I try to explain this problem to my roommate lol
This problem is so fun! It turns out I have learned a lot from this problem
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

import inspect

def lcm(x,y):
    '''
    simply compute the lcm of two given integers
    '''
    return abs(x * y) // math.gcd(x, y)

def compute_lcm(divisibles):
    '''
    given an array of the number used to check for monkey's divisibles  
    '''
    if len(divisibles) == 2:
        x,y = divisibles
        return lcm(x,y)
    x, y, *rest = divisibles

    return lcm(lcm(x,y), compute_lcm(rest))

class Monkey:
    global monkey_map
    monkey_map = {}
    def __init__(self, id, recipient_1, recipient_0, operation, divisible, items):
        self.id = id
        self.queue = items    # a queue(FIFO) that tells you how 
        self.recipient_1 = recipient_1 # if divisible 
        self.recipient_0 = recipient_0 # if not divisible
        self.operation = operation # a lambda function to feed
        self.divisible = divisible
        self.inspect = 0
    
    @classmethod
    def from_str(cls, string):
        '''
        Credit to Borja Sotomayor: https://github.com/borjasotomayor/advent-of-code/blob/main/2022/day11.py
        '''
        id = parse.parse("Monkey {:d}:", string[0])[0]
        operator, op2 = parse.parse("  Operation: new = old {} {}", string[2])
        divisible = parse.parse("  Test: divisible by {:d}", string[3])[0]
        recipient_1 = parse.parse("    If true: throw to monkey {:d}", string[4])[0]
        recipient_0 = parse.parse("    If false: throw to monkey {:d}", string[5])[0]
        
        raw_items = parse.parse("  Starting items: {}", string[1])[0]

        items = deque([int(item) for item in raw_items.split(", ")])
        op = {
            '+': lambda y : lambda x: x + y,
            '*': lambda y : lambda x: x * y
        }
        if op2 == "old":
            operation = lambda x: x**2
        else:
            operation = op[operator](int(op2)) 

        return cls(id, recipient_1, recipient_0, operation, divisible, items)

    @classmethod
    def purge(cls):
        '''
        purge the map
        '''
        monkey_map.clear()   

    def perform_operations(self, div_true, lcm):
        '''
        throw away all of the itemsi in the queue until none is left 
        '''
        while self.queue:
            item = self.queue.popleft()
            self.operate(item, div_true, lcm)
            self.inspect += 1
        return
    
    def operate(self, item, div_true, lcm):
        '''
        Perform the operation for one item
        '''
        # inspect.getsource(self.operation)
        if div_true:
            result = self.operation(item)
            item = result // 3 # double check if this actually rounds down to the nearest integer
        else:
            item = item % lcm
            item = self.operation(item) % lcm
        if item % self.divisible == 0:
            recipient_idx = self.recipient_1
        else:
            recipient_idx = self.recipient_0
        monkey_map[recipient_idx].queue.append(item)
        return 



def simulate(monkies, rounds, div_true):
    '''
    simulate the slinging monkeys behavior by parsing the inputs and 
    recording the monkeys items after each round
    '''
    Monkey.purge()
    for monky in monkies:
        mk = Monkey.from_str(monky)
        if mk.id not in monkey_map:
            monkey_map[mk.id] = mk
    
    lcm = compute_lcm([monkey.divisible for _, monkey in monkey_map.items()])
    for _ in range(rounds):
        for idx, monkey in monkey_map.items():
            monkey.perform_operations(div_true, lcm)

    lst = sorted([monkey.inspect for _, monkey in monkey_map.items()], key = lambda x: -x)
    highest, second = lst[0:2]
    return highest * second

    
    


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/11.in", sep="\n\n", sep2="\n")

    print("TASK 1")
    util.call_and_print(simulate, copy.deepcopy(sample), 20, True)
    util.call_and_print(simulate, copy.deepcopy(input), 20, True)
    

    print("\nTASK 2")
    util.call_and_print(simulate, copy.deepcopy(sample), 10000, False)
    util.call_and_print(simulate, copy.deepcopy(input), 10000, False)


