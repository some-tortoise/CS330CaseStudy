import math
import random
import statistics
import time
from datetime import datetime

import global_data
from classes import Passenger, Driver, KdNode


def createAdjacencyLists():
  for i in range(0,24):
    global_data.adjacencyListsWeekdays[i] = createAdjacencyListAsDict('weekday', i)
    global_data.adjacencyListsWeekends[i] = createAdjacencyListAsDict('weekend', i)

def createAdjacencyListAsDict(type, hour):
  '''
  Input:
  type can either be 'weekday' or 'weekend'
  hour is integer from [0,23]

  Output: 
  adjacency list
  '''
  adjacencyList = {}

  if(type == 'weekday'):
    speedIndex = 3+hour #look at column 3+i for weights
  elif(type == 'weekend'):
    speedIndex = 27+hour #look at column 27+i for weights
  else:
    raise TypeError
  
  for edge in global_data.edges:
      speed = float(edge[speedIndex])
      length = float(edge[2])
      weight = (length/speed)*60 # in minutes

      if adjacencyList.get(edge[0]) is not None:
        temp = adjacencyList.get(edge[0])
        temp.append((edge[1], weight))
        adjacencyList.update({edge[0] : temp})
      else:
        adjacencyList.update({edge[0] : [(edge[1], weight)]})

  return adjacencyList

# def createAdjacencyListAsLinkedList(type, hour):
  
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

def getAdjacencyList(dateStr):
  '''
  Input:
  dateString
  Output:
  correct adjacencyList
  '''
  hour = int(dateStr.split()[1][0:2])
  adjacencyList = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    adjacencyList = global_data.adjacencyListsWeekdays[hour]
  else:
    adjacencyList = global_data.adjacencyListsWeekends[hour]
  
  return adjacencyList

def getPassengersWithShortDate(date):
  l = []
  passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
  while(passengerDate == date and len(global_data.passengers)):
    passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
    passenger = global_data.passengers.pop(0)
    l.append(passenger)
  return l  

def getDriversWithShortDate(date):
  l = []
  driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
  while(driverDate == date  and len(global_data.drivers)):
    driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
    driver = global_data.drivers.pop(0)
    l.append(driver)
  return l 

def updateDriverDetails(driver, ride, latestDate):
  driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
  totalTimeInMin = ride.pickupToDropoffTime + ride.driverToPassengerTime

  driver.passengersCarried += 1
  driver.driverProfit += ride.pickupToDropoffTime - ride.driverToPassengerTime

  #update timeOnJob and date in code below
  dateInMin = 0

  if latestDate == driver.datetime:
    driver.timeOnJob += totalTimeInMin
    dateInMin = driverDate.timestamp() / 60 + totalTimeInMin
  else:
    passengerDate = datetime.strptime(latestDate, "%m/%d/%Y %H:%M:%S")
    driver.timeOnJob += (passengerDate-driverDate).total_seconds() / 60 + totalTimeInMin 
    dateInMin = passengerDate.timestamp() / 60 + totalTimeInMin
  
  #date conversion stuff
  driver.datetime = datetime.fromtimestamp(dateInMin*60, tz = None)
  format_string = '%Y-%m-%d %H:%M:%S'
  date_string = driver.datetime.strftime(format_string)
  year,month,dayandrest = date_string.split('-')
  day, rest = dayandrest.split(' ')

  reformatted_date = f'{month}/{day}/{year} {rest}'
  driver.datetime = reformatted_date

  return driver

def getManhattanDist(point1, point2):
  lat1, lon1 = point1
  lat2, lon2 = point2
  dist1 = abs(float(lat1)-float(lat2))*69.09
  dist2 = abs(float(lon1)-float(lon2))*51.34

  return dist1+dist2

def getHaversineDist(point1, point2):
  '''
  returns estimate of distance between two points in miles

  Input
  point1 as (lat1, long1), point2 as (lat2, long2)

  '''
  lat1, lon1 = point1
  lat2, lon2 = point2
  
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
  
  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
  c = 2 * math.asin(math.sqrt(a)) 
  r = 3959
  return c * r

def getApproxHaversineDist(point1, point2):
  '''
  returns estimate of distance between two points in miles

  Input
  point1 as (lat1, long1), point2 as (lat2, long2)

  '''
  
  # convert decimal degrees to radians 
  lat1, lon1, lat2, lon2 = map(math.radians, [point1[0], point1[1], point2[0], point2[1]])

  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 

  # using taylor series approximation to 3 terms
  a = ((dlat/2)-((dlat/2)**3)/6 + ((dlat/2)**5)/120)**2 + (1-(lat1**2)/2 + (lat1**4)/24) * (1-(lat2**2)/2 + (lat2**4)/24) * (((dlon/2)-((dlon/2)**3)/6 + ((dlon/2)**5)/120)**2) 
  x = math.sqrt(a)
  # using taylor series approximation to 2 terms
  cTimesR = 7918 * x+ 1319.666 * (x**3)
  return cTimesR

def findClosestNode(point):
  '''
  Input:
  point as (lat, long)

  Output:
  returns a node ID
  '''

  point = (float(point[0]), float(point[1]))

  minDist = float('Inf')
  closestNode = None
  for node in global_data.nodes:
    nodeStuff = global_data.nodes[node]
    dist = getApproxHaversineDist(point, (float(nodeStuff['lat']), float(nodeStuff['lon'])))
    if dist < minDist:
      minDist = dist
      closestNode = node

  return closestNode

def grabOrCreateNode(point):
  '''
  Input (lat, long)
  Output: node created or closest node if new one not needed
  '''

  if point in global_data.reversedNodes:
    return global_data.reversedNodes[point]
  
  node = str(findClosestNode(point))
  nodeLat = global_data.nodes[node]['lat']
  nodeLong = global_data.nodes[node]['lon']
  dist = getHaversineDist((nodeLat, nodeLong), point)
  
  if dist > global_data.minDistToBecomeNewNode:
    #create new node
    nodeId = str(random.getrandbits(32))
    global_data.nodes[nodeId] = {'lon': point[1], 'lat' : point[0]}
    global_data.reversedNodes[(point[0], point[1])] = nodeId

    for i in range(0, 24):
      temp = global_data.adjacencyListsWeekdays[i].get(node)
      temp.append((nodeId, 60*(dist/20)))
      global_data.adjacencyListsWeekdays[i].update({node : temp})
      global_data.adjacencyListsWeekdays[i][nodeId] = [(node, (dist/20)*60)]

      temp = global_data.adjacencyListsWeekends[i].get(node)
      temp.append((nodeId, 60*(dist/20)))
      global_data.adjacencyListsWeekends[i].update({node : temp})
      global_data.adjacencyListsWeekends[i][nodeId] = [(node, (dist/20)*60)]
    
    return nodeId
  
  return node

def grabOrCreateSexyNode(point):
  '''
  Input (lat, long)
  Output: node created or closest node if new one not needed
  '''

  if point in global_data.reversedNodes:
    return global_data.reversedNodes[point]
  
  node = str(findClosestInKD(global_data.kdroot, (float(point[0]), float(point[1])), global_data.kdroot).value[0])
  nodeLat = global_data.nodes[node]['lat']
  nodeLong = global_data.nodes[node]['lon']
  dist = getHaversineDist((nodeLat, nodeLong), point)
  
  if dist > global_data.minDistToBecomeNewNode:
    #create new node
    nodeId = str(random.getrandbits(32))
    global_data.nodes[nodeId] = {'lon': point[1], 'lat' : point[0]}
    global_data.reversedNodes[(point[0], point[1])] = nodeId

    for i in range(0, 24):
      temp = global_data.adjacencyListsWeekdays[i].get(node)
      temp.append((nodeId, 60*(dist/20)))
      global_data.adjacencyListsWeekdays[i].update({node : temp})
      global_data.adjacencyListsWeekdays[i][nodeId] = [(node, (dist/20)*60)]

      temp = global_data.adjacencyListsWeekends[i].get(node)
      temp.append((nodeId, 60*(dist/20)))
      global_data.adjacencyListsWeekends[i].update({node : temp})
      global_data.adjacencyListsWeekends[i][nodeId] = [(node, (dist/20)*60)]
    
    return nodeId
  
  return node

def buildKD(list, dim=2, splitter=0):
    if len(list) == 0:
      return
    if splitter == 0:
      list.sort(key=lambda w: float(w[1]))
    elif splitter == 1:
      list.sort(key=lambda w: float(w[2]))
    median = len(list) // 2
    rightNode = buildKD(list[median + 1:], dim, (splitter + 1) % dim)
    leftNode = buildKD(list[:median], dim, (splitter + 1) % dim)
    return KdNode(list[median], leftNode, rightNode, splitter)

def findClosestInKD(root, query_point, current_closest, splitter=0):
  if root is None:
    return current_closest
  
  pLat, pLon = query_point
  pLat = float(pLat)
  pLon = float(pLon)
  
  if splitter == 0: # USE LAT
    if pLat < root.value[1]:
      nextNode = root.leftNode
    else:
      nextNode = root.rightNode
  else: # USE LON
    if pLon < root.value[2]:
      nextNode = root.leftNode
    else:
      nextNode = root.rightNode

  current_closest = findClosestInKD(nextNode, query_point, current_closest, splitter=(splitter+1)%2)

  #check nodes
  rootPoint = (float(root.value[1]), float(root.value[2]))
  distToRoot = getApproxHaversineDist(query_point, rootPoint)
  currentClosestDist = getApproxHaversineDist(query_point, (float(current_closest.value[1]), float(current_closest.value[2])))
  if distToRoot < currentClosestDist:
    current_closest = root

  #check other subtrees if need be
  if abs(float(query_point[splitter]) - rootPoint[splitter]) < currentClosestDist:
    nextNode = root.rightNode if nextNode == root.leftNode else root.leftNode
    current_closest = findClosestInKD(nextNode, query_point, current_closest, splitter=(splitter+1)%2)
  
  return current_closest