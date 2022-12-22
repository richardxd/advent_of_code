"""
Day 8
https://adventofcode.com/2022/day/8
1st time: 00:22:45
2nd time: 01:24:38

I have certainly done this before but I'm too lazy, 
and for the second problem it took me too long to realize that I did not correctly understand the problem itself
Also I am glad that I can implement the monotonic stack right off of my head when I truly understand the second half
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


def reverse_matrix(matrix):
    '''
    Given a matrix, rotate it
    '''
    for row in matrix:
        row.reverse()
    matrix.reverse()

def update_monotonic_stack(array, stack, i, j, compute_i):
    '''
    Given the original array, a monotonically decreasing stack of the corresponding indices
    (not strictly), and the current index, 
    depending on if we are computing i or not,
    update the monotonic decreasing stack and compute the proper distance of i or j
    '''
    while stack and array[stack[-1][0]][stack[-1][1]] < array[i][j]:
        stack.pop()
    if compute_i:
        
        ret = i - stack[-1][0] if stack else i
    else: 
        ret = j - stack[-1][1] if stack else j
    stack.append([i,j])
    return stack, ret

def iterate(array, visited):
    '''
    Given the original array along with visited matrix
    iterate through the array from upper left corner to lower right corner
    compute the score along the row and column from the left and above respectively
    return the number of trees that can be seen from either direction(left or above, and
    discounting duplicates from visited array)
    '''
    up = [0] * len(array[0])
    up_idx = [deque() for i in range(len(array[0]))]
    score = [[[0,0] for _ in range(len(array[0]))] for _ in range(len(array))]
    cnt = 0
    # first pass iterate right and down
    for i in range(len(array)):
        left = 0
        left_idx = deque()
        for j in range(len(array[0])):
            if i == 0 or i == len(array) - 1 or j == 0 or j == len(array) - 1:
                if not visited[i][j]:
                    cnt += 1    
                    visited[i][j] = 1
            curr = array[i][j]
            if (curr > left or curr > up[j]) and not visited[i][j]:
                cnt += 1
                visited[i][j] = 1
            left_idx, vertical = update_monotonic_stack(array, left_idx, i, j, False)
            up_idx[j], horizontal = update_monotonic_stack(array, up_idx[j], i, j, True)
            score[i][j][0] = horizontal
            score[i][j][1] = vertical

            if left < curr:
                left = curr
            if up[j] < curr:
                up[j] = curr
    return score, cnt



def visible(array):
    """
    Given the original array, 
    compute the number of trees visible from outside
    and compute the highest score
    """
    # two pass solution
    visited = [[0] * len(array[0]) for _ in range(len(array))]
    # first pass iterate right and down
    score_first, cnt_first = iterate(array, visited)
    reverse_matrix(array)
    reverse_matrix(visited)

    score_second, cnt_second = iterate(array, visited)
    # visited = reverse_matrix(visited)
    reverse_matrix(score_second)
    
    score_highest = 0
    score = [[0] * len(array[0]) for _ in range(len(array))]
    for i in range(len(array)):
        for j in range(len(array[0])):
            a, b = score_first[i][j]
            c, d = score_second[i][j]
            score[i][j] = a * b * c * d
            score_highest = max(score_highest, a*b*c*d)
    return cnt_first + cnt_second, score_highest


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/08.in", sep="\n")
    sample = [list(map(lambda x:int(x), list(string))) for string in sample]
    input = [list(map(lambda x:int(x), list(string))) for string in input]

    print(sample)
    print("TASK 1 and TASK2")
    util.call_and_print(visible, copy.deepcopy(sample))
    util.call_and_print(visible, copy.deepcopy(input))


