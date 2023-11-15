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
from tasks import t1 #utility functions
from classes import Driver, Passenger #classes for driver, passenger
import global_data


time1 = time.time()

###READ IN DATA###

drivers = read_csv('./data/drivers.csv')
passengers = read_csv('./data/passengers.csv')
edges = read_csv('./data/edges.csv')
global_data.nodes = getNodes() # list of nodes

edges.sort(key=lambda edge: edge[0])


time2 = time.time()
print(f'time to read data: {time2 - time1} seconds')

###WE ASSUME passengers AND drivers ARE SORTED. NOT GUARANTEED. RUN CODE BELOW TO SORT###
#passengers.sort(key=lambda passenger: datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S"))
#drivers.sort(key=lambda driver: datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S"))


### PREPROCESSING ###
# each element in below is for hours from 0-23

for i in range(0,23):
  global_data.adjacencyListsWeekdays[i] = createAdjacencyListAsDict('weekday', i, edges)
  global_data.adjacencyListsWeekends[i] = createAdjacencyListAsDict('weekend', i, edges)

time3 = time.time()
print(f'time for preprocessing: {time3 - time2} seconds')

### RUN TASK ###

t1(passengers, drivers)

time4 = time.time()
print(f'time to complete task: {time4 - time3} seconds')