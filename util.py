import math
import random
import statistics
import time
from datetime import datetime

import global_data
from classes import Passenger, Driver


def getManhattanDist(point1, point2):
  lat1, lon1 = point1
  lat2, lon2 = point2
  dist1 = getHaversineDist(point1, (lat1, lon2))
  dist2 = getHaversineDist(point2, (lat2, lon1))
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

def findClosestNode(point):
  '''
  Input:
  point as (lat, long)

  Output:
  returns a node ID
  '''

  minDist = float('Inf')
  closestNode = None
  for node in global_data.nodes:
    nodeLong = global_data.nodes[node]['lon']
    nodeLat = global_data.nodes[node]['lat']
    dist = getHaversineDist(point, (nodeLat, nodeLong))
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
  node = findClosestNode(point)
  nodeLat = global_data.nodes[node]['lat']
  nodeLong = global_data.nodes[node]['lon']
  dist = getHaversineDist((nodeLat, nodeLong), point)
  
  if dist > global_data.minDistToBecomeNewNode:
    #create new node
    nodeId = random.getrandbits(32)
    global_data.nodes[str(nodeId)] = {'lon': point[1], 'lat' : point[0]}
    #global_data.edges.append(node, nodeId, dist, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
    for i in range(0, 24):
      temp = global_data.adjacencyListsWeekdays[i].get(str(node))
      temp.append((str(nodeId), 60*(dist/20)))
      global_data.adjacencyListsWeekdays[i].update({str(node) : temp})
      global_data.adjacencyListsWeekdays[i][str(nodeId)] = [(str(node), (dist/20)*60)]

      temp = global_data.adjacencyListsWeekends[i].get(str(node))
      temp.append((str(nodeId), 60*(dist/20)))
      global_data.adjacencyListsWeekends[i].update({str(node) : temp})
      global_data.adjacencyListsWeekends[i][str(nodeId)] = [(str(node), (dist/20)*60)]
    
    return str(nodeId)
  
  return node

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
      weight = (length/speed)*60

      if adjacencyList.get(edge[0]) is not None:
        temp = adjacencyList.get(edge[0])
        temp.append((edge[1], weight))
        adjacencyList.update({edge[0] : temp})
      else:
        adjacencyList.update({edge[0] : [(edge[1], weight)]})

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

def createAdjacencyLists():
  for i in range(0,24):
    global_data.adjacencyListsWeekdays[i] = createAdjacencyListAsDict('weekday', i)
    global_data.adjacencyListsWeekends[i] = createAdjacencyListAsDict('weekend', i)

def findClosestNodeButCoolerAndFasterAndSexier(point, distToCheck):
  '''
  Input:
  point as (lat, long)

  Output:
  returns a node ID
  '''

  minDist = float('Inf')
  lat, long = point
  closestNode = None
  latLowBound = float(lat) - distToCheck
  latHighBound = float(lat) + distToCheck
  indexLat = BinarySearchRangeForSexyNode(global_data.nodesSortedByLat, latLowBound, latHighBound, 1)

  arrayOfNodesWithGoodLat = []
  i = indexLat
  while global_data.nodesSortedByLat[i][1]>=latLowBound and global_data.nodesSortedByLat[i][1]<=latHighBound:
    arrayOfNodesWithGoodLat.append(global_data.nodesSortedByLat[i][0])
    i+=1
  i = indexLat-1
  while global_data.nodesSortedByLat[i][1]>=latLowBound and global_data.nodesSortedByLat[i][1]<=latHighBound:
    arrayOfNodesWithGoodLat.append(global_data.nodesSortedByLat[i][0])
    i-=1
  
  longLowBound = float(long) - distToCheck
  longHighBound = float(long) + distToCheck
  indexLong = BinarySearchRangeForSexyNode(global_data.nodesSortedByLong, longLowBound, longHighBound, 2)

  arrayOfNodesWithGoodLong = []
  i = indexLong
  while global_data.nodesSortedByLong[i][2]>=longLowBound and global_data.nodesSortedByLong[i][2]<=longHighBound:
    arrayOfNodesWithGoodLong.append(global_data.nodesSortedByLong[i][0])
    i+=1
  i = indexLong-1
  while global_data.nodesSortedByLong[i][2]>=longLowBound and global_data.nodesSortedByLong[i][2]<=longHighBound:
    arrayOfNodesWithGoodLong.append(global_data.nodesSortedByLong[i][0])
    i-=1
  
  #get intersection
  possibleNodes = []
  for a  in arrayOfNodesWithGoodLat:
    if a in arrayOfNodesWithGoodLong:
      possibleNodes.append(a)
  
  #loop through
  minDist = float('Inf')
  closestNode = None
  for node in possibleNodes:
    nodeLong = global_data.nodes[node]['lon']
    nodeLat = global_data.nodes[node]['lat']
    dist = getHaversineDist(point, (nodeLat, nodeLong))
    if dist < minDist:
      minDist = dist
      closestNode = node
  return str(closestNode)


def BinarySearchRangeForSexyNode(list, a, b, k):
    '''
    Output: 
    index
    '''
    low = 0
    high = len(list) - 1
    mid = 0
    while low <= high:
        mid = int(math.floor((low+high)/2))
        if list[mid][k] >= a and list[mid][k] <= b:
            return mid
        elif list[mid][k] < a:
            low = mid + 1
        elif list[mid][k] > b:
            high = mid - 1
        else:
            return TypeError
        
    return mid


def grabOrCreateSexyNode(point):
  '''
  Input (lat, long)
  Output: node created or closest node if new one not needed
  '''

  if point in global_data.reversedNodes:
    return global_data.reversedNodes[point]
  
  node = None
  distToCheck = 0.00002
  t = time.time()
  while node == None:
    node = findClosestNodeButCoolerAndFasterAndSexier(point, distToCheck)
    distToCheck *= 2
  node = findClosestNode(point)
  nodeLat = global_data.nodes[node]['lat']
  nodeLong = global_data.nodes[node]['lon']
  dist = getHaversineDist((nodeLat, nodeLong), point)
  
  if dist > global_data.minDistToBecomeNewNode:
    #create new node
    nodeId = random.getrandbits(32)
    global_data.nodes[str(nodeId)] = {'lon': point[1], 'lat' : point[0]}
    #global_data.edges.append(node, nodeId, dist, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
    for i in range(0, 24):
      temp = global_data.adjacencyListsWeekdays[i].get(str(node))
      temp.append((str(nodeId), 60*(dist/20)))
      global_data.adjacencyListsWeekdays[i].update({str(node) : temp})
      global_data.adjacencyListsWeekdays[i][str(nodeId)] = [(str(node), (dist/20)*60)]

      temp = global_data.adjacencyListsWeekends[i].get(str(node))
      temp.append((str(nodeId), 60*(dist/20)))
      global_data.adjacencyListsWeekends[i].update({str(node) : temp})
      global_data.adjacencyListsWeekends[i][str(nodeId)] = [(str(node), (dist/20)*60)]
    
    return str(nodeId)
  
  return node