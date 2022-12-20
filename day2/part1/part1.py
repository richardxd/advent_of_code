"""
Day 2
https://adventofcode.com/2022/day/2
1st star: 00:02:56
2nd star: 00:04:23
I don't know
"""
import sys
sys.path.append("../../")

import util
import math
import sys
import re

from utils import log


def sum_top_n(groups, n=1):
    """
    Given a list of groups (where each group is a list of integers),
    find the sum of the values in each group, and then add up the top N
    groups.
    """
    print(groups)
    sums = []
    for group in groups:
        sums.append(sum(group))

    top_n = sorted(sums, reverse=True)[:n]

    return sum(top_n)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/01.in", sep="\n\n", sep2="\n")
    # input = util.read_ints("input/01.in", sep="\n\n", sep2="\n")

    print("TASK 1")
    util.call_and_print(sum_top_n, sample)
    # util.call_and_print(sum_top_n, input)

    print("\nTASK 2")
    util.call_and_print(sum_top_n, sample, 3)
    # util.call_and_print(sum_top_n, input, 3)