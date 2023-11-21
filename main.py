import csv
from datetime import datetime
import json
import math
import heapq
import time
import statistics
import cProfile   #REMOVE BEFORE SUBMISSION
import pstats #REMOVE BEFORE SUBMISSION



###self defined files###
from in_out import * #input output
from algs import * #algorithms
from util import * #utility functions
from tasks import t1, t2, t3, t4, t5, t5Clean #utility functions
from classes import Driver, Passenger #classes for driver, passenger
import global_data



time1 = time.time()

###READ IN DATA###

global_data.edges = read_csv('./data/edges.csv')
global_data.nodes = getNodes() # dict of nodes

passengerCSVarr = read_csv('./data/passengers.csv')
global_data.passengers = [Passenger(*d, 0) for d in passengerCSVarr]

driverCSVarr = read_csv('./data/drivers.csv')
global_data.drivers = [Driver(*d, 0, 0, 0) for d in driverCSVarr]

time2 = time.time()
print(f'Time to read data: {time2 - time1} seconds')



### PREPROCESSING ###

global_data.avgSpeedList = [0]*48

for edge in global_data.edges:
    for i in range(0, 48):
        global_data.avgSpeedList[i] += float(edge[i+3])
for i in range(0,48):
    global_data.avgSpeedList[i] /= len(global_data.edges)

createAdjacencyLists()

initialNodeList = []
global_data.reversedNodes = {}
for key, val in global_data.nodes.items():
    global_data.reversedNodes[(global_data.nodes[key]['lat'], global_data.nodes[key]['lon'])] = key
    initialNodeList.append([key, global_data.nodes[key]['lat'], global_data.nodes[key]['lon']])

global_data.kdroot = buildKD(list=initialNodeList, dim=2, splitter=0)

time3 = time.time()
print(f'Time for preprocessing: {time3 - time2} seconds')



### RUN TASK ###

# Run the profiler (REMOVE BEFORE SUBMISSION)
#cProfile.run('t4()', sort='cumulative')

def profiler(command, filename="profile.stats", n_stats=10):
    """Profiler for a python program

    Runs cProfile and outputs ordered statistics that describe
    how often and for how long various parts of the program are executed.

    Stats can be visualized with `!snakeviz profile.stats`.

    Parameters
    ----------
    command: str
        Command string to be executed.
    filename: str
        Name under which to store the stats.
    n_stats: int or None
        Number of top stats to show.
    """
    import cProfile
    import pstats

    cProfile.run(command, filename)
    stats = pstats.Stats(filename).strip_dirs().sort_stats("time")
    return stats.print_stats(n_stats or {})

profiler('t5Clean()', filename='profile.stats', n_stats=30)

time4 = time.time()
print(f'Time for task: {time4 - time3} seconds')

