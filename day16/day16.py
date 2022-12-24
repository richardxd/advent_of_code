"""
Day 16
https://adventofcode.com/2022/day/16
1st time: 
2nd time: 


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
from functools import lru_cache

from util import log


class Vertex:
    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors = set() # this keeps track of all the neighbors of a vertex
        
        # key is name of the vertex, value is the weight of the shortest path
        self.dist = {} # this is a map to a map of edges, i.e., adj_dict[b] = edge weight of (a,b) 
        # if that edge exists. If no matching key exists, then it is assumed that the shortest path is infinity
        


def floyd_warshall(vertices_map):
    '''
    Given an undirected weighted graph (vertices_map = {name of the vertex:vertex struct}) 
    compute the shortest path between all pairs of vertices
    '''
    for u_name, u in vertices_map.items():
        for v_name, v in vertices_map.items():
            # if u_name == v_name:
                # u.dist[v_name] = 0
            # elif v_name in u.neighbors:
                # already taken care of
                # u.dist[v_name] = dist[u][v] hypothestically if there is u,v
            if u_name != v_name and v_name not in u.neighbors:
                u.dist[v_name] = float('inf')
            
            

    for k_name, k in vertices_map.items():
        for u_name, u in vertices_map.items():
            for v_name, v in vertices_map.items():
                # now we make sure u, v, k are unique. 
                # we compute if u, v, k can be made shorter
                u.dist[v_name] = min(u.dist[v_name], u.dist[k_name] + k.dist[v_name])
    return


def remove_zero_flow(neighbors_map, vertices, vertex):
    '''
    Given a vertex struct, remove it from the neighbors_map if this vertex has zero flow
    '''
    if vertex.name not in vertices and vertex.name not in neighbors_map:
        # duplicate removal, want to avoid as much as we can
        print("duplicate removal encountered")
        return 
    if vertex.flow_rate != 0 or vertex.name == 'AA':
        # current vertex is good to go
        return 
    
    zero_flow_vertices = set() # buffer
    neighbors = deque(neighbors_map[vertex.name])
    # otherwise we need to remove the current vertex
    # enumerate all neighboring vertices. If one of them happen to be zero_flow as well, keep them in a buffer
    # recursively remove these buffered vertices once the current vertex has been processed
    while neighbors:
        # original vertex is the vertex that we try to remove from the graph
        # current vertex is the vertex that is one of the neighbors of the original vertex
        current_name = neighbors.pop()
        
        # drop  the original vertex from the neighbors map
        # if vertex.name in neighbors_map[current_name]:
        neighbors_map[current_name].remove(vertex.name) 
        current_vertex = vertices[current_name]
        del current_vertex.dist[vertex.name]
        
        # if current_vertex.flow_rate == 0 and current_vertex.name != 'AA':
        #     # add to the buffer and continue the loop
        #     zero_flow_vertices.add(current_vertex)
        #     continue
        

        # otherwise, we know that we need to keep this vertex. Add an edge between this vertex 
        # and all the remaining neighbors of the original vertex
        for neighbor_name in neighbors:

            neighbor_vertex = vertices[neighbor_name]
            
            # if neighbor_vertex.flow_rate == 0 and neighbor_vertex.name != 'AA':
            #     zero_flow_vertices.add(neighbor_vertex)
            #     continue
            # otherwise, we know that we need to keep this vertex. Add an edge between neighbor vertex and the current vertex
            neighbors_map[current_name].add(neighbor_name)
            neighbors_map[neighbor_name].add(current_name)

            # update the distance, think of a simple C3
            current_vertex.dist[neighbor_name] = vertex.dist[neighbor_name] + vertex.dist[current_name]
            neighbor_vertex.dist[current_name] = vertex.dist[neighbor_name] + vertex.dist[current_name]

    # once finished, we can drop the original vertex entry both in vertices and in vertex
    del neighbors_map[vertex.name]
    del vertices[vertex.name]
    


    # now we want to remove the zero flows vertices we have found along the iteration! 
    # for ele in zero_flow_vertices:
    #     remove_zero_flow(neighbors_map, vertices, ele)
    return
    

def parse_graph(raw_input):
    '''
    Convert the raw input into graph represented using adjacency matrix
    '''  
    neighbors_map = {} # key: name of the vertex, value: the name of the neighbors of that vertex
    vertices = {} # key: name of the vertex, value: a ptr to the Vertex struct


    for line in raw_input:
        vertex_name, flow_rate, neighbors = parse.parse("Valve {} has flow rate={:d}; tunnels lead to valves {}", line) 
        # map vertex name to different values
        neighbors = neighbors.split(", ")
        vertex = Vertex(vertex_name, flow_rate) 
        vertices[vertex_name] = vertex
        
        neighbors_map[vertex_name] = set(neighbors)
        for v in neighbors:
            vertex.dist[v] = 1
        vertex.dist[vertex_name] = 0
    # print_graphs(vertices)
    # print("something is off the chart...")
    # print_graphs(vertices, spec='HH')
    # print(neighbors_map['HH'])
    # print("finished printing")
    # deal with zero flow rate   
    # we want to remove all vertex with zero flow rate
    # for vertex in vertices.values():
        # remove_zero_flow(neighbors_map, vertices, vertex)
    
    keys = list(vertices.keys())
    for key in keys:
        if key in vertices:
            # print("removing:", key)
            # print(neighbors_map['HH'])
            # print(neighbors_map['EE'])
            remove_zero_flow(neighbors_map, vertices, vertices[key])

    # done parsing. Now we can store the result in the Vertex 
    for name, vertex in vertices.items():
        vertex.neighbors = neighbors_map[name]
        


    # now run Floyd-Warshall to find the shortest distance for all pairs of vertices
    floyd_warshall(vertices)    
    return vertices


def bit_map(graph):
    '''
    given the graph, map each vertex's name to a number that represents its position at the bitmap
    '''
    return {name:i for i, name in zip(range(len(graph.keys())), graph.keys())}

def is_kth_bit_set(n,k):
    '''
    return True if kth bit is set otherwise false
    '''
    return True if n & (1 << k) else False

def set_kth_bit(n, k):
    '''
    given an number, set its kth bit to 1 and return a new copy of that
    '''
    return (1 << k) | n

def simulate(graph):
    '''
    Given the processed graph, find the desired valves to oepn at different time
    '''
    # create a tuple of the valves
    vertex_bit_map = bit_map(graph)
    begin = vertex_bit_map['AA']
    n = 0
    n = set_kth_bit(n, begin)

    @lru_cache(maxsize=None)
    def dfs(current, remain_time, valves):
        '''
        Given the current vertex, the remaining time, and the valves(in bitmap) that are on
        compute the most pressure you can release
        '''
        vertex = graph[current]
        max_gain = 0
        for dest_name, distance in vertex.dist.items():
            k = vertex_bit_map[dest_name]
            if is_kth_bit_set(valves, k):
                continue
            dest_vertex = graph[dest_name]
            flow_rate = dest_vertex.flow_rate
            time_valve_on = remain_time - distance - 1
            time_valve_on = max(time_valve_on, 0) # make sure this is not negative    
            
            # add the destination to the bit map
            updated_valves = set_kth_bit(valves, k)
            gain = time_valve_on * flow_rate + dfs(dest_name, time_valve_on, updated_valves)
            max_gain = max(gain, max_gain)
        return max_gain
    return dfs('AA', 30, n)


def print_graphs(graph, spec=None):
    for vertex in graph.values():
        if spec:
            if spec != vertex.name:
                continue
        print("vertex:", vertex.name)
        print(" vertex neighbors:", vertex.neighbors)
        print(" vertex.dist:", vertex.dist.items())
        print(" vertex.flowrate", vertex.flow_rate)

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample.in", sep="\n")
    input = util.read_strs("input/16.in", sep="\n")
    
    sample_graph = parse_graph(sample)
    input_graph = parse_graph(input)
    # print_graphs(sample_graph)

    print(sample_graph.keys())
    
    print("TASK 1")
    util.call_and_print(simulate, sample_graph)
    util.call_and_print(simulate, input_graph)
    

    # print("\nTASK 2")
    # util.call_and_print(part2, copy.deepcopy(sample_map), 20)
    # util.call_and_print(part2, copy.deepcopy(input_map), 4000000)


