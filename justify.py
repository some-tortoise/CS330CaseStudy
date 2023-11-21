import json
import csv
import heapq
import math
from datetime import datetime
import random
import statistics
import time
import timeit

import global_data
from classes import Passenger, Driver, KdNode, Cluster, Clusters
from in_out import * #input output
from algs import * #algorithms
from util import * #utility functions



# global_data.edges = read_csv('./data/edges.csv')
# global_data.nodes = getNodes() # dict of nodes

passengerCSVarr = read_csv('./data/passengers.csv')
global_data.passengers = [Passenger(*d, 0) for d in passengerCSVarr]

# driverCSVarr = read_csv('./data/drivers.csv')
# global_data.drivers = [Driver(*d, 0, 0, 0) for d in driverCSVarr]


# global_data.avgSpeedList = [0]*48

# for edge in global_data.edges:
#     for i in range(0, 48):
#         global_data.avgSpeedList[i] += float(edge[i+3])
# for i in range(0,48):
#     global_data.avgSpeedList[i] /= len(global_data.edges)

# createAdjacencyLists()

# initialNodeList = []
# global_data.reversedNodes = {}
# for key, val in global_data.nodes.items():
#     global_data.reversedNodes[(global_data.nodes[key]['lat'], global_data.nodes[key]['lon'])] = key
#     initialNodeList.append([key, global_data.nodes[key]['lat'], global_data.nodes[key]['lon']])

# global_data.kdroot = buildKD(list=initialNodeList, dim=2, splitter=0)



#Show A* and A* To All are more efficient and still accurate enough compared to Dijkstra and Dijkstra To All
#Specifically measure how often A* overshoots





#Show getApproxHaversine is more efficient and still accurate enough compared to getHaversine

avgError = 0
maxError = 0
for p in global_data.passengers:
    distHav = getHaversineDist((p.sourceLat, p.sourceLong), (p.destLat, p.destLong))
    distApprox = getApproxHaversineDist((float(p.sourceLat), float(p.sourceLong)),(float(p.destLat), float(p.destLong)))
    err = abs(distHav - distApprox)
    if err > maxError:
        maxError = err
    avgError += err
avgError /= len(global_data.passengers)

def func1():
    distance1 =  0
    for p in global_data.passengers:
        distance1 += getHaversineDist((float(p.sourceLat), float(p.sourceLong)), (float(p.destLat), float(p.destLong)))

def func2():
    distance2 = 0
    for p in global_data.passengers:
        distance2 += getApproxHaversineDist((float(p.sourceLat), float(p.sourceLong)),(float(p.destLat), float(p.destLong)))

time_taken = timeit.timeit(func1, number=1000)
print(f'time taken on Haversine: {time_taken}')
time_taken2 = timeit.timeit(func2, number=1000)
print(f'time taken on Approx Haversine: {time_taken2}')
print(f'Average Error: {avgError} miles')
print(f'Maximum Error: {maxError} miles')
print(f'ApproxHaversine is {time_taken/time_taken2} times faster than Haversine')
