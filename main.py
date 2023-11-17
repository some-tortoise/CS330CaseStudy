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

global_data.drivers = read_csv('./data/drivers.csv')
global_data.passengers = read_csv('./data/passengers.csv')
global_data.edges = read_csv('./data/edges.csv')
global_data.nodes = getNodes() # list of nodes

#global_data.edges.sort(key=lambda edge: edge[0])


time2 = time.time()
print(f'time to read data: {time2 - time1} seconds')

###WE ASSUME passengers AND drivers ARE SORTED. NOT GUARANTEED. RUN CODE BELOW TO SORT###
#passengers.sort(key=lambda passenger: datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S"))
#drivers.sort(key=lambda driver: datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S"))


### PREPROCESSING ###
# each element in below is for hours from 0-23

createAdjacencyLists()

initialNodeList = []
for key, val in global_data.nodes.items():
    initialNodeList.append([key, global_data.nodes[key]['lat'], global_data.nodes[key]['lon']])

global_data.nodesSortedByLat = sorted(initialNodeList, key=lambda x: x[1])
global_data.nodesSortedByLong = sorted(initialNodeList, key=lambda x: x[2])


time3 = time.time()
print(f'time for preprocessing: {time3 - time2} seconds')
### RUN TASK ###

t1()

time4 = time.time()
print(f'time to complete task: {time4 - time3} seconds')