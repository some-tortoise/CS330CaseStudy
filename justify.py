import json
import csv
import heapq
import math
from datetime import datetime
import random
import statistics
import time
import timeit ### USES EXTERNAL PACKAGE. THIS IS NOT FOR THE ALGORITHM BUT JUST FOR PROFILING ###

import global_data
from classes import Passenger, Driver, KdNode, Cluster, Clusters
from in_out import * #input output
from algs import * #algorithms
from util import * #utility functions


global_data.edges = read_csv('./data/edges.csv')
global_data.nodes = getNodes() # dict of nodes

passengerCSVarr = read_csv('./data/passengers.csv')
global_data.passengers = [Passenger(*d, 0) for d in passengerCSVarr]

driverCSVarr = read_csv('./data/drivers.csv')
global_data.drivers = [Driver(*d, 0, 0, 0) for d in driverCSVarr]


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



# show findClosestInKDT5 is accurate
def test1():
    errorSum = 0
    maxError = 0
    for p in global_data.passengers:
        queryPoint = (float(p.sourceLat), float(p.sourceLong))
        nodeID = findClosestInKDT5(global_data.kdroot, queryPoint, global_data.kdroot).value[0]

        nodeID2 = findClosestNode(queryPoint)
        
        if nodeID != nodeID2:
            node1 = global_data.nodes[nodeID]
            node2 = global_data.nodes[nodeID]
            error = getHaversineDist((node1['lat'], node1['lon']), (node2['lat'], node2['lon']))
            errorSum += error
            if error > maxError:
                maxError = error

    print(f'average error: {errorSum / len(global_data.passengers)}')
    print(f'max error: {maxError}')

# show findClosestInKDT5 is faster
def test2():
    def findClosest1():
        for p in global_data.passengers:
            queryPoint = (float(p.sourceLat), float(p.sourceLong))
            nodeID = findClosestNode(queryPoint)

    def findClosest2():
        for p in global_data.passengers:
            queryPoint = (float(p.sourceLat), float(p.sourceLong))
            nodeID = findClosestInKDT5(global_data.kdroot, queryPoint, global_data.kdroot).value[0]
        
    time_taken = timeit.timeit(findClosest1, number=1)
    time_taken2 = timeit.timeit(findClosest2, number=1)
    print(f'time taken on findClosestNode: {time_taken}')
    print(f'time taken on findClosestInKDT5: {time_taken2}')
    print(f'findClosestInKDT5 is {time_taken/time_taken2} times faster than findClosestNode')



# Show A* is accurate compared to Dijkstra
def test3():
    errorSum = 0
    maxError = 0
    for p in global_data.passengers:
        sourcePoint = (float(p.sourceLat), float(p.sourceLong))
        destPoint = (float(p.sourceLat), float(p.sourceLong))
        sourceNode = findClosestInKDT5(global_data.kdroot, sourcePoint, global_data.kdroot).value[0]
        destNode = findClosestInKDT5(global_data.kdroot, destPoint, global_data.kdroot).value[0]
        
        graph = getAdjacencyList(p.datetime)

        dist1 = Dijkstra(graph, sourceNode, destNode)
        dist2 = Astar(graph, sourceNode, destNode, p.datetime)
        
        error = abs(dist1 - dist2)
        errorSum += error
        if error > maxError:
            maxError = error

    print(f'average error: {errorSum / len(global_data.passengers)}')
    print(f'max error: {maxError}')

# Show A* is faster than Dijkstra
def test4():
    sourceNodes = []
    destNodes = []
    datetimes = []
    for p in global_data.passengers:
        sourcePoint = (float(p.sourceLat), float(p.sourceLong))
        destPoint = (float(p.sourceLat), float(p.sourceLong))
        sourceNode = findClosestInKDT5(global_data.kdroot, sourcePoint, global_data.kdroot).value[0]
        destNode = findClosestInKDT5(global_data.kdroot, destPoint, global_data.kdroot).value[0]
        sourceNodes.append(sourceNode)
        destNodes.append(destNode)
        datetimes.append(p.datetime)

    def dist1():
        for i in range(len(sourceNode)):
            graph = getAdjacencyList(datetimes[i])
            dist = Dijkstra(graph, sourceNodes[i], destNodes[i])
        
    def dist2():
        for i in range(len(sourceNode)):
            graph = getAdjacencyList(datetimes[i])
            dist = Astar(graph, sourceNodes[i], destNodes[i], datetimes[i])
            
    time_taken = timeit.timeit(dist1, number=1)
    time_taken2 = timeit.timeit(dist2, number=1)
    print(f'time taken on Dijkstra: {time_taken}')
    print(f'time taken on Astar: {time_taken2}')
    print(f'Astar is {time_taken/time_taken2} times faster than Dijkstra')



#Show getApproxHaversine is accurate compared to getHaversine
def test5():
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
    print(f'Average Error: {avgError} miles')
    print(f'Maximum Error: {maxError} miles')

# Show getApproxHaversineDist is faster than getHaversineDist
def test6():
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

    print(f'ApproxHaversine is {time_taken/time_taken2} times faster than Haversine')
