import csv
from datetime import datetime
import json
import math
import heapq

def read_csv(str):
  file = open(str)
  csvreader = csv.reader(file)
  header = []
  header = next(csvreader)
  rows = []
  for row in csvreader:
    rows.append(row)
  file.close()
  return header, rows

def print_csv(header, rows):
  print(header)
  print('----------------------------------------------')
  for row  in rows:
    print(row)

def getNodes():
  f = open('./data/node_data.json')
  data = json.load(f)
  f.close()
  return data

def findDist(point1, point2):
  '''
  returns estimate of distance between two points

  Input
  point1 as (lat1, long1), point2 as (lat2, long2)
  '''
  lat1, long1 = point1
  lat2, long2 = point2
  return math.sqrt((float(lat1)-float(lat2))**2 + (float(long1)-float(long2))**2)


def findClosestNode(point):
  '''
  Input:
  point as (lat, long)

  Output:
  returns a node ID
  '''

  minDist = float('Inf')
  closestNode = None
  for node in nodes:
    nodeLong = nodes[node]['lon']
    nodeLat = nodes[node]['lat']
    dist = findDist((point), (nodeLat, nodeLong))
    if dist < minDist:
      minDist = dist
      closestNode = node
  
  return closestNode



def Dijkstra(graph, source, dest): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  source as (lat, long)
  dest as (lat, long)

  Output:
  returns time it takes to get from source to destination
  '''
  sourceNode = findClosestNode(source)
  destNode = findClosestNode(dest)

  # Initialize distances dictionary with infinity for all vertices except the source
  timeTillPoint = {vertex: float('infinity') for vertex in graph}
  timeTillPoint[sourceNode] = 0
  i = 0

  priority_queue = [(0, source)]

  while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # If the current distance is greater than the known distance, skip
        if current_distance > timeTillPoint[current_vertex]:
            continue
        
        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            
            # If a shorter path is found, update the distance
            if distance < timeTillPoint[neighbor]:
                timeTillPoint[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
        
        i += 1
    
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to dest param
  
  #return sourceNode, destNode
  

def t1(passengers, drivers):
  '''
  input is passengers array and drivers array
  '''
  # Sort passengers by time
  passengers.sort(key=lambda passenger: datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S"))
  # Sort drivers by time
  drivers.sort(key=lambda driver: datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S"))
  # combine into one list and iterate over list
  waitingPassengerQueue = []
  waitingDriverQueue = []
  while True:
    passengerDate = datetime.strptime(passengers[0][0], "%m/%d/%Y %H:%M:%S")
    driverDate = datetime.strptime(drivers[0][0], "%m/%d/%Y %H:%M:%S")
    if passengerDate < driverDate: #if passenger is from previous day, remove from passengers
      passenger = passengers.pop(0)
      waitingPassengerQueue.append(passenger) #add passenger to queue
      if(len(passengers) == 0):
        print('Ran Out of Passengers')
        break
    else:
      driver = drivers.pop(0) 
      waitingDriverQueue.append(driver)
      if(len(drivers) == 0):
        print('Ran Out of Drivers')
        break
    
    if len(waitingDriverQueue) > 0 and len(waitingPassengerQueue) > 0:
      #match passenger to driver
      passenger = waitingPassengerQueue.pop(0)
      driver = waitingDriverQueue.pop(0)
      #timeFromDriverToPassenger = Djikstra((driver[1], driver[2]), (passenger[1], passenger[2]))
      #timeFromPassengerToDest = Djikstra((passenger[1], passenger[2]), (passenger[3], passenger[4]))
      #print(timeFromDriverToPassenger + timeFromPassengerToDest)

      #   totalTime = timeFromDriverToPassenger + timeFromPassengerToDest
      #   print(f'Total time: {totalTime}')
        
      print(Dijkstra((driver[1], passenger[1]), (driver[2], passenger[2]))) #changed driver and passenger pairings


def createAdjacencyList(type, hour):
  '''
  Input:
  type can either be 'weekday' or 'weekend'
  hour is integer from [0,23]

  Output: 
  adjacency list
  '''
  adjacencyList = []

  if(type == 'weekday'):
    speedIndex = 3+hour #look at column 3+i for weights
  elif(type == 'weekend'):
    speedIndex = 27+hour #look at column 27+i for weights
  else:
    raise TypeError
  
  for edge in edges:
      speed = float(edge[speedIndex])
      length = float(edge[2])
      weight = length/speed
      if len(adjacencyList) == 0 or adjacencyList[-1][0] != edge[0]:
        adjacencyList.append([edge[0],(edge[1], weight)]) # [sourceNode, (destNode, weight)]
      else:
        adjacencyList[-1].append((edge[1], weight)) # (destNode, weight)

  return adjacencyList
  



# READ IN DATA

driversHeader, drivers = read_csv('./data/drivers.csv')
passengersHeader, passengers = read_csv('./data/passengers.csv')
edgesHeader, edges = read_csv('./data/edges.csv')
edges.sort(key=lambda edge: edge[0])

#GLOBAL ELEMENTS

nodes = getNodes()
# each element in below is for hours from 0-23
adjacencyListsWeekdays = [0]*24 
adjacencyListsWeekends = [0]*24 
for edge in edges:
  print(edge)
# for i in range(0,23):
#   adjacencyListsWeekdays[i] = createAdjacencyList('weekday', i)
#  adjacencyListsWeekends[i] = createAdjacencyList('weekend', i)

for i in range(0,23):
  adjacencyListsWeekdays[i] = createAdjacencyList('weekday', i)
  adjacencyListsWeekends[i] = createAdjacencyList('weekend', i)

# RUN CODE
#ret = t1(drivers, passengers)
#print(ret)
