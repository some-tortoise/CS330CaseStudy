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
from tasks import t1, t2, t3, t4, t5, t5Clusters, b1, b2, b4 #task functions
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

#ONLY FOR T4 and T5
global_data.kdroot = buildKD(list=initialNodeList, dim=2, splitter=0)

#ONLY FOR T5
global_data.clusters = initializeClusters()

time3 = time.time()
print(f'Time for preprocessing: {time3 - time2} seconds')


### RUN TASK ###

#t1()
#t2()
#t3()
#t4()
#t5()
#t5Clusters()

### RUN BONUS ###

#b1()
#b2()
b4()

time4 = time.time()
print(f'Time for task: {time4 - time3} seconds')
