"""
Day 2
https://adventofcode.com/2022/day/2
1st star: a bit long setting up everything
2nd star: long enough to hardcode a hashmap
I don't know what to put here. the compute score function is indeed messy
"""
import sys
sys.path.append("../")

import util
import math
import sys
import re

from util import log

def part2(x,y):
    """
    x represents the choice of the opponent
    y represents the desired outcome of the game
    return the total score obtained 
    """
    
    # hardcode a hashmap since I have no better ways
    score = {'X':0, 'Y':3, 'Z':6}
    game = {
        'A': #rock
        {
            'X': 3, #lose, scissor
            'Y': 1, #draw, rock
            'Z': 2, #win, paper
        }, 
        'B': #paper  
        {
            'X': 1, #lose, rock
            'Y': 2, #draw, paper
            'Z': 3, #win, scissor
        }, 
        'C': #scissor
        {
            'X': 2, #lose, paper
            'Y': 3, #draw, scissor
            'Z': 1, #win, rock
        }, 
    }
    return game[x][y] + score[y]

def part1(x,y):
    """
    given two string reprensetning the choice of two players, return true 
    if the player who chooses y wins else false
    """
    score = 0
    if x == 'A':
        if y == 'X':
            score = 3
        elif y == 'Y':
            score = 6
        elif y == 'Z':
            score = 0
        else:
            raise Exception("incorrect input")
    elif x == 'B':
        if y == 'X':
            score = 0
        elif y == 'Y':
            score = 3
        elif y == 'Z':
            score = 6
        else:
            raise Exception("incorrect input")
    elif x == 'C':
        if y == 'X':
            score = 6
        elif y == 'Y':
            score = 0
        elif y == 'Z':
            score = 3
        else:
            raise Exception("incorrect input")
    else:
        raise Exception("incorrect input")
    if y == 'X':
        score += 1
    elif y == 'Y':
        score += 2
    elif y == 'Z':
        score += 3
    else:
        raise Exception("incorrect input")
    return score


def compute_score(strat, part):
    """
    compute the total score obtained by two players depending on the type of input
    """
    x, y = strat
    score = 0
    if part == 1:
        score = part1(x,y)
    elif part == 2:
        score = part2(x,y)
    else:
        raise Exception("incorrect input part")
    return score



def total_score(strategies, part):
    """
    Given a list of strategies, 
    compute the total score of all games included
    """
    score = 0
    for strat in strategies:
        score += compute_score(strat, part)
    return score


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=" ")
    input = util.read_strs("input/01.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(total_score, sample, 1)
    util.call_and_print(total_score, input, 1)

    print("\nTASK 2")
    util.call_and_print(total_score, sample, 2)
    util.call_and_print(total_score, input, 2)