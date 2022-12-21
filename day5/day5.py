"""
Day 5
https://adventofcode.com/2022/day/5
1st star: 15 min
2nd star: less than 5 min
I hate this question because I need to parse the inputs
I am borrowing Professor Borja's input reading function, lol.
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


def read_input(filename):
    """
    Credit to: https://github.com/borjasotomayor/advent-of-code/blob/main/2022/day05.py
    Custom function for reading the input, since the read_* 
    functions in my util module strip whitespace, which
    is significant in this problem.
    This function also does the legwork of parsing the stacks, etc.
    """
    with open(filename) as f:
        txt = f.read()
        stacks_str, moves_str = txt.split(sep="\n\n")  
        stacks_lines = stacks_str.split("\n")
        moves_lines = moves_str.split("\n")

    # Remove the last line of the stacks portion
    indices_line = stacks_lines.pop()

    # The last number in that line conveniently gives
    # us the number of stacks
    num_stacks = int(indices_line.split()[-1])
    
    # Parse the stacks lists
    stacks = [[] for _ in range(num_stacks)]
    for line in stacks_lines:
        # Read the character corresponding to each stack
        # If it is not blank, insert it into the corresponding
        # stack list
        for s in range(num_stacks):
            c = line[1 + s*4]
            if c != " ":
                stacks[s].insert(0, c)

    # Parse the moves
    moves = []
    for n, sfrom, sto in util.iter_parse(moves_lines, "move {:d} from {:d} to {:d}"):        
        moves.append((n, sfrom-1, sto-1))

    return stacks, moves
def get_top(stacks):
    result = []
    for stack in stacks:
        result.append(stack[-1])
    return "".join(result)

def crane_segment(stacks, moves):
    stacks = copy.deepcopy(stacks)
    moves = copy.deepcopy(moves)
    for move in moves:
        n, sfrom, sto = move
        curr = deque()
        while n > 0:
            ele = stacks[sfrom].pop()
            curr.appendleft(ele)
            n -= 1
        stacks[sto].extend(curr)
    return get_top(stacks)

def crane(stacks, moves):
    stacks = copy.deepcopy(stacks)
    moves = copy.deepcopy(moves)
    for move in moves:
        n, sfrom, sto = move
        while n > 0:
            curr = stacks[sfrom].pop()
            stacks[sto].append(curr)
            n -= 1
    return get_top(stacks)

if __name__ == "__main__":
    util.set_debug(False)

    sample_stacks, sample_moves = read_input("input/sample.in")
    input_stacks, input_moves =  read_input("input/05.in")

    print("TASK 1")
    util.call_and_print(crane, sample_stacks[:], sample_moves[:])
    util.call_and_print(crane, input_stacks[:], input_moves[:])

    print("\nTASK 2")
    util.call_and_print(crane_segment, deque(sample_stacks), sample_moves)
    util.call_and_print(crane_segment, deque(input_stacks), input_moves)