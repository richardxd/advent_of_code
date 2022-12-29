"""
Day 21
https://adventofcode.com/2022/day/21
1st time: 00:29:00
2nd time: 03:08:00
The first half of the question is very straightforward and easy, by just applying basic binary operation tree
The second half is extremely edge-case oriented. It took me very long time to invert the tree correctly.

Note that:
For a binary opeartion tree with the following set up, the inverted version is, respectively:
1) 
root
-- *
---- 2
---- humn
-- y

/
-- y
-- 2

2)
root
-- *
---- humn
---- 2
-- y

/
-- y
-- 2

3)
root
-- /
---- 2
---- humn
-- y

*
--2
--y 
(or vice versa since * is associative)

4)
root
-- /
---- humn
---- 2
-- y

/
--2
--y
Sketching them out helps a lot. In addition, the inversion could be very easily implemented using recursion
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



class Node:
    def __init__(self, op, op_name=None, left_child=None, right_child=None, parent=None):
        self.op = op
        self.op_name = op_name
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent

    def calculate(self):
        '''
        traverse the binary operator tree
        '''
        if not self.left_child and not self.right_child:
            # this is a leaf
            return self.op
        # otherwise
        left_result = self.left_child.calculate()
        right_result = self.right_child.calculate()
        return self.op(left_result, right_result)    


def parse_operator(op, name, name_map):
    '''
    Given the opoerator, i.e., "a + b"
    Generate an instance of the node
    '''
    if "+" in op:
        sep = " + "
        func = lambda x, y: x + y
    elif "-" in op:
        sep = " - "
        func = lambda x, y: x - y
    elif "*" in op:
        sep = " * "
        func = lambda x, y: x * y 
    elif "/" in op: 
        sep = " / "
        func = lambda x, y: x / y 
    else:
        print(op)
        raise Exception("buggy input")

    name1, name2 = op.split(sep)
    if name1 in name_map:
        left_child = name_map[name1]
    else: 
        left_child = Node(None)
        name_map[name1] = left_child
    if name2 in name_map:
        right_child = name_map[name2]
    else:
        right_child = Node(None)    
        name_map[name2] = right_child
    if name in name_map:
        name_map[name].op = func
        name_map[name].op_name = sep
        name_map[name].left_child = left_child
        name_map[name].right_child = right_child
        left_child.parent = name_map[name]
        right_child.parent = name_map[name]
        return name_map[name]
    node = Node(func, op_name=sep, left_child=left_child, right_child=right_child)
    left_child.parent = node
    right_child.parent = node
    return node
    

def parse_input(raw_input):
    '''
    Given the raw input, generate a name-map(key: name, value:node). 
    Then feed this to the execution of the binary operator tree
    '''
    name_map = {} # used to store the corresponding operators
    for line in raw_input:
        name, op = parse.parse("{}: {}", line)
        if op.isnumeric():
            if name in name_map:
                name_map[name].op = int(op)
                name_map[name].op_name = "number"
            else:
                name_map[name] = Node(int(op), op_name="number")
        else:
            name_map[name] = parse_operator(op, name, name_map)
    # print(print_binary_tree(name_map['root']))
    # print("FINISHED PRINTING")
    part1 = name_map["root"].calculate()
    part2 = reconstruct_binary_tree(name_map['root'], name_map['humn'])
    return part1, part2

def reconstruct_binary_tree(root, humn):
    '''
    invert the operation for the binary tree and compute the result for humn
    '''
    # notice the observation that when root's op is = and we need to solve for humn
    # every node along the traversal from root to humn is inverted, while the others are kept the same (the other nodes that do not get involved stay the same) 

    root_new = humn.parent
    current = humn.parent
    parent = humn
    prev = None
    cnt = 0
    second = False

    # essentially, a recursive version of this is wayyyy easier
    while current.parent:
        current_op_0 = current.op_name
        if parent == current.right_child:
            second = True 
        invert_operation(current, second)

        # deal with the root node
        # define y to be the other half of the binary tree (the half not containing humn)
        y = None
        if not current.parent.parent:
            # this means that current.parent is the root node
            # swallo the root node and replace it with the right/left
            if current == current.parent.left_child:
                y = current.parent.right_child
            elif current == current.parent.right_child:
                y = current.parent.left_child
            else:
                raise Exception("buggying ")

        if current_op_0 in [" + ", " * "]:
            if second:
                current.right_child = current.left_child
                current.left_child = current.parent if not y else y
            else:
                # right child does not need to change
                current.left_child = current.parent if not y else y
        elif current_op_0 in [" - ", " / "]:
            if second:
                # left child does not change
                current.right_child = current.parent if not y else y 
            else:
                # right child does not need to change
                current.left_child = current.parent if not y else y
        else:
            raise Exception("BUGGY behavior")
             
        parent = current
        current = current.parent
        second = False
        

    
    # if parent == current.left_child:
    #     # y is on the right child of the root node
    #     y = current.right_child    
    # elif parent == current.right_child:
    #     # vice versa
    #     y = current.left_child
    
    # in other words, this is the base case of the recursion
    
    return root_new.calculate()
        
def invert_operation(root_new, second=False):
    '''
    Given the original node, invert its operation
    '''
    if root_new.op_name == " + ":
        root_new.op_name = " - "
        root_new.op = lambda x, y : x - y
    elif root_new.op_name == " - ":
        if second:
            return
        root_new.op_name = " + "
        root_new.op = lambda x, y: x + y
    elif root_new.op_name == " * ":
        root_new.op_name = " / "
        root_new.op = lambda x, y : x / y

    elif root_new.op_name == " / ":
        if second:
            return
        root_new.op_name = " * "
        root_new.op = lambda x,y : x * y
    elif root_new.op_name == "number":
        return
    else:
        raise Exception("incorrect input")
    return 


def print_binary_tree(root, sep=""):
    if root.op_name == "number":
        print("printing 1")
        print(sep + str(root.op))
    else:
        print("printing 2")
        print(sep + root.op_name)
    if root.parent:
        if root.parent.op_name == "number":
            print("printing 3")
            print("".join(["*"] * len(sep)) + str(root.parent.op))
        else:  
            print("printing 4")
            print("".join(["*"] *len(sep)))
            print(root.parent.op_name)
    if root.op_name == "number":
        return
    print("printing 5")
    print_binary_tree(root.left_child, sep + "--")
    print("printing 6")
    print_binary_tree(root.right_child, sep + "--")    

            
if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/21.in", sep="\n")
    
 
    # note: to not blow up your computer, make sure to only execute one of the following at a time.
    print("TASK 1 & 2")
    util.call_and_print(parse_input, sample)
    util.call_and_print(parse_input, input)
    



