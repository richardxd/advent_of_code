"""
Day 7
https://adventofcode.com/2022/day/7
1st time: 30mins
2nd time: 30mins
Now we are simulating a subset of the operting systems! 
It seems weird that everyone enjoys this question. Maybe I'm not a system type person
Edit: implementing the 1st part is actually quite interesting and I loved it
Edit2: Lol there are a ton of bugs in my second part. I should aim to better formulate the problem next

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


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class Directory:
    def __init__(self, name, root=None, parent=None):
        self.name = name # name of the current directory
        self.root = root # a ptr to the root
        self.parent = parent
        self.sub = {} # maps to ptr to all the remaining directories
        self.files = {} # collects all the files inside the current directory
        self.size = 0
        
    def calculate_size(self):
        '''
        Calculate the total size of the directory
        '''
        size = 0
        for key,file in self.files.items():
            size += file.size
        for _, sub in self.sub.items():
            size += sub.calculate_size()
        return size
    
    def add_file(self, file_name, file_size):
        '''
        add a file and update the file sizes for all direcotries
        '''
        if file_name in self.files and self.files[file_name].size != 0:
            return

        self.files[file_name] = File(file_name, file_size)
        self.update_size(file_size)
        return
    
    def update_size(self, file_size):
        '''
        update sizes for all relevant directories
        '''

        self.size += file_size
        if self.parent:
            self.parent.update_size(file_size)
        

    def add_folder(self, folder_name):
        '''
        add a folder to the current folder
        '''
        if folder_name in self.sub:
            return
        self.sub[folder_name] = Directory(folder_name, self.root, self)
        return 
    
    def find_dir(self, size, greater):
        '''
        find the directory that satisifies a specific size restriected by whether it is 
        greater than that size or less than that size
        '''
        output = []
        dfs = []
        for name, directory in self.sub.items():
            if not greater and directory.size <= size:
                output.append(directory)
            elif directory.size >= size:
                output.append(directory)
            dfs.append(directory)
        for ele in dfs:
            output += ele.find_dir(size, greater)
        return output
    
    
    

def parse_results(cmd, buffer, curr_dir):
    '''
    Given a command starting with $ and the terminal result stored at buffer,
    and the current directory of the operations
    parse the result and add the necessary to the file systems
    '''
    ins = cmd[1]
    if ins == "cd":
        param = cmd[2]
        if param == "/":
            return curr_dir.root
        elif param == "..":
            if not curr_dir.parent:
                raise Exception("Error")
            return curr_dir.parent
        else:
            curr_dir.add_folder(param)
            return curr_dir.sub[param]
    elif ins == "ls":
        while buffer:
            details = buffer.popleft()
            if details[0] == "dir":
                dir_name = details[1]
                curr_dir.add_folder(dir_name)
            else:
                size = details[0]
                name = details[1]
                curr_dir.add_file(name, int(size))
    else:
        raise Exception("unspecified command")
    return curr_dir
        
def execute_command(terminals, size):
    """
    Given a list of terminal outputs, filter out the command executed
    and record the result of each command
    """
    i = 0
    cmd = None
    buffer = deque()
    root = Directory("/")
    root.root = root
    curr_dir = root
    while i < len(terminals):
        current = terminals[i]
        i += 1
        if current[0] == '$':
            if not cmd:
                cmd = current
                continue
            curr_dir = parse_results(cmd, buffer, curr_dir)
            buffer = deque()
            cmd = current
            continue
        buffer.append(current)
    # traverse(root)
    if buffer:
        curr_dir = parse_results(cmd, buffer, curr_dir)
        buffer = deque()
        cmd = current
        lst = root.find_dir(size, False) 
    sum = 0
    for directory in lst:
        sum += directory.size
    return sum, root

def delete_directories(terminals, size, target):
    '''
    Given the terminal inputs, the total size of the disk, and the 
    target amount of size needed, find the directory/file to delete
    in order to free enough space to reach the target
    '''
    _, root = execute_command(terminals, size)
    remaining = size - root.size
    root_size = 0

    to_delete = target - remaining
    lst = [root] + root.find_dir(to_delete, True)
    lst.sort(key = lambda x : x.size)
    return lst[0].size 
            
def traverse(curr_dir, tabs=""):
    '''
    traverse the filesystems and print out all the directory
    for debugging only
    '''
    queue = []
    queue.append((tabs, curr_dir))
    while queue:
        tab, curr = queue.pop()
        print(tab + curr.name)
        tab += "--"
        for name, directory in reversed(curr.sub.items()):
            queue.append((tab, directory))
    return
        
    
        



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n", sep2=" ")
    input = util.read_strs("input/07.in", sep="\n", sep2=" ")


    print("TASK 1")
    util.call_and_print(execute_command, copy.deepcopy(sample), 100000)
    util.call_and_print(execute_command, copy.deepcopy(input), 100000)

    print("\nTASK 2")
    util.call_and_print(delete_directories, sample, 70000000, 30000000)
    util.call_and_print(delete_directories, input, 70000000, 30000000)
