import math
import random
from datetime import datetime

import global_data
from classes import Passenger, Driver


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
  node = findClosestNode(point)
  nodeLong = global_data.nodes[node]['lon']
  nodeLat = global_data.nodes[node]['lat']
  dist = getHaversineDist((nodeLat, nodeLong), point)
  if dist > global_data.minDistToBecomeNewNode:
    #create new node
    nodeId = random.getrandbits(32)
    global_data.nodes.update({nodeId:{'lon': point[0], 'lat' : point[1]}})
    #global_data.edges.append(node, nodeId, dist, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
    for i in range(0, 24):
      temp = global_data.adjacencyListsWeekdays[i].get(str(node))
      temp.append((str(nodeId), dist/10))
      global_data.adjacencyListsWeekdays[i].update({str(node) : temp})
      global_data.adjacencyListsWeekdays[i].update({str(nodeId) : [(str(node), dist/10)]})
    
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
      weight = length/speed

      if adjacencyList.get(edge[0]) is not None:
        temp = adjacencyList.get(edge[0])
        temp.append((edge[1], weight))
        adjacencyList.update({edge[0] : temp})
      else:
        adjacencyList.update({edge[0] : [(edge[1], weight)]})

  return adjacencyList

def getPassengersWithShortDate(date):
  l = []
  passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
  while(passengerDate == date):
    passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
    passenger = global_data.passengers.pop(0)
    p = Passenger(*passenger, 0)
    l.append(p)
  return l  

def getDriversWithShortDate(date):
  l = []
  driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")
  while(driverDate == date):
    driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")
    driver = global_data.drivers.pop(0)
    d = Driver(*driver, 0, 0, 0)
    l.append(d)
  return l 

def updateDriverDetails(driver, ride, latestDate):
  driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
  totalTimeInMin = ride.pickupToDropoffTime + ride.driverToPassengerTime

  driver.passengersCarried += 1
  driver.driverProfit += ride.pickupToDropoffTime - ride.driverToPassengerTime
  if latestDate == driver.datetime:
    driver.timeOnJob += totalTimeInMin
    driver.datetime = driverDate.timestamp() / 60 + totalTimeInMin
  else:
    passengerDate = datetime.strptime(latestDate, "%m/%d/%Y %H:%M:%S")
    driver.timeOnJob += (passengerDate-driverDate).total_seconds() / 60 + totalTimeInMin 
    driver.datetime = passengerDate.timestamp() / 60 + totalTimeInMin
  
  driver.datetime = datetime.fromtimestamp(driver.datetime*60, tz = None)
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

def findClosestNodeButCoolerAndFasterAndSexier(point):
  '''
  Input:
  point as (lat, long)

  Output:
  returns a node ID
  '''

  minDist = float('Inf')
  lat, long = point
  closestNode = None
  latLowBound = lat - 0.03
  latHighBound = lat + 0.03
  indexLat, valLat = BinarySearchRange([item[1] for item in global_data.nodesSortedByLat], latLowBound, latHighBound)

  arrayOfNodesWithGoodLat = []
  i = indexLat
  while global_data.nodesSortedByLat[i][1]>=latLowBound and global_data.nodesSortedByLat[i][1]<=latHighBound:
    arrayOfNodesWithGoodLat.append(global_data.nodesSortedByLat[i][0])
    i+=1
  i = indexLat-1
  while global_data.nodesSortedByLat[i][1]>=latLowBound and global_data.nodesSortedByLat[i][1]<=latHighBound:
    arrayOfNodesWithGoodLat.append(global_data.nodesSortedByLat[i][0])
    i-=1


  longLowBound = long - 0.03
  longHighBound = long + 0.03
  indexLong, valLong = BinarySearchRange([item[2] for item in global_data.nodesSortedByLong], longLowBound, longHighBound)

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

  return closestNode


def BinarySearchRange(list, a, b):
    '''
    Input:
    list and lower bound a and upper bound b
    '''

    n = len(list)
    if(n == 1):
        if float(list[0]) >= a and float(list[0]) <= b:
            return list[0]
        else:
            return None
    
    m = math.floor(n/2)
    mid = list[m]
    if float(mid)>b:
        return BinarySearchRange(list[:m],a,b)
    elif float(mid)<a:
        return BinarySearchRange(list[m:],a,b)
    
    return m,mid