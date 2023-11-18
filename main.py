import csv
from datetime import datetime
import json
import math
import heapq
import time
import statistics

###self defined files###
from in_out import * #input output
from algs import * #algorithms
from util import * #utility functions
from tasks import t1, t2, t3, t4 #utility functions
from classes import Driver, Passenger #classes for driver, passenger
import global_data


time1 = time.time()

###READ IN DATA###

global_data.passengers = read_csv('./data/passengers.csv')
global_data.edges = read_csv('./data/edges.csv')
global_data.nodes = getNodes() # list of nodes

passengerCSVarr = read_csv('./data/passengers.csv')
global_data.passengers = [Passenger(*d, 0) for d in passengerCSVarr]

driverCSVarr = read_csv('./data/drivers.csv')
global_data.drivers = [Driver(*d, 0, 0, 0) for d in driverCSVarr]

time2 = time.time()
print(f'time to read data: {time2 - time1} seconds')


### PREPROCESSING ###

createAdjacencyLists()

initialNodeList = []
global_data.reversedNodes = {}
for key, val in global_data.nodes.items():
    global_data.reversedNodes[(global_data.nodes[key]['lat'], global_data.nodes[key]['lon'])] = key
    initialNodeList.append([key, global_data.nodes[key]['lat'], global_data.nodes[key]['lon']])

global_data.nodesSortedByLat = sorted(initialNodeList, key=lambda x: x[1])
global_data.nodesSortedByLong = sorted(initialNodeList, key=lambda x: x[2])

time3 = time.time()
print(f'time for preprocessing: {time3 - time2} seconds')
### RUN TASK ###

t1()

time4 = time.time()
