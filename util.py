import math
import random
import statistics
import time
from datetime import datetime

import global_data
from classes import Passenger, Driver, KdNode, Cluster, Clusters
from algs import AstarToAll

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
  passengerDate = global_data.passengers[0].datetimeAsDatetime()
  while(passengerDate == date and len(global_data.passengers)):
    passengerDate = global_data.passengers[0].datetimeAsDatetime()
    passenger = global_data.passengers.pop(0)
    l.append(passenger)
  return l  

def getDriversWithShortDate(date):
  l = []
  driverDate = global_data.drivers[0].datetimeAsDatetime()
  while(driverDate == date  and len(global_data.drivers)):
    driverDate = global_data.drivers[0].datetimeAsDatetime()
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
  # for small distances we can pretend the Earth is flat (still keep high precision

  # length of meridian is approx 12450 miles
  # dividing by 180 for rad calcs gives the 69.17166249
  kx = math.cos(((point1[0]+point2[0])/2) * (math.pi / 180)) * 69.17166249
  dx = (point1[1] - point2[1]) * kx
  # equator length is approx 24861 miles 
  # dividing by 360 for rad calcs gives 69.05857293
  dy = (point1[0] - point2[0]) * 69.05857293
  return math.sqrt((dx * dx) + (dy * dy))

def getApproxHaversineDistSquared(point1, point2):
  '''
  returns estimate of distance between two points in miles

  Input
  point1 as (lat1, long1), point2 as (lat2, long2)

  '''

  # like approx haversine dist but we pre-estimate the cosine for the new york area. 
  # leads to a max error of 0.1 miles on passenger data set
  dx = (point1[1] - point2[1])
  dy = (point1[0] - point2[0])
  return (2731 * (dx * dx) + 4769.0864 * (dy * dy))

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
    dist = getHaversineDist(point, (nodeStuff['lat'], nodeStuff['lon']))
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
  nodeLat = float(global_data.nodes[node]['lat'])
  nodeLong = float(global_data.nodes[node]['lon'])
  dist = getHaversineDist((nodeLat, nodeLong), (point[0], point[1]))
  
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
  nodeLat = float(global_data.nodes[node]['lat'])
  nodeLong = float(global_data.nodes[node]['lon'])
  dist = getHaversineDist((nodeLat, nodeLong), (point[0], point[1]))
  
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
  rootPoint = (root.value[1], root.value[2])
  distToRoot = getHaversineDist(query_point, rootPoint)
  currentClosestDist = getHaversineDist(query_point, (current_closest.value[1], current_closest.value[2]))
  if distToRoot < currentClosestDist:
    current_closest = root

  #check other subtrees if need be
  if abs(float(query_point[splitter]) - float(rootPoint[splitter])) < currentClosestDist:
    nextNode = root.rightNode if nextNode == root.leftNode else root.leftNode
    current_closest = findClosestInKD(nextNode, query_point, current_closest, splitter=(splitter+1)%2)
  
  return current_closest

def grabOrCreateSexyNodeT5(point):
  '''
  Input (lat, long)
  Output: node created or closest node if new one not needed
  '''

  if point in global_data.reversedNodes:
    return global_data.reversedNodes[point]
  
  node = str(findClosestInKDT5(global_data.kdroot, (float(point[0]), float(point[1])), global_data.kdroot).value[0])
  nodeLat = float(global_data.nodes[node]['lat'])
  nodeLong = float(global_data.nodes[node]['lon'])
  dist = getApproxHaversineDist((nodeLat, nodeLong), (float(point[0]), float(point[1])))
  
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

def findClosestInKDT5(root, query_point, current_closest, splitter=0):
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

  current_closest = findClosestInKDT5(nextNode, query_point, current_closest, splitter=(splitter+1)%2)

  #check nodes
  rootPoint = (float(root.value[1]), float(root.value[2]))
  distToRoot = getApproxHaversineDistSquared(query_point, rootPoint)
  currentClosestDist = getApproxHaversineDistSquared(query_point, (float(current_closest.value[1]), float(current_closest.value[2])))
  if distToRoot < currentClosestDist:
    current_closest = root

  #check other subtrees if need be
  if abs(float(query_point[splitter]) - rootPoint[splitter]) < currentClosestDist:
    nextNode = root.rightNode if nextNode == root.leftNode else root.leftNode
    current_closest = findClosestInKDT5(nextNode, query_point, current_closest, splitter=(splitter+1)%2)
  
  return current_closest

def passengerInRange(p):
  point1 = (float(p.sourceLat), float(p.sourceLong))
  if getApproxHaversineDist(point1,global_data.center) > global_data.clusterRange:
    return False
  
  point2 = (float(p.destLat), float(p.destLong))
  if getHaversineDist(point2,global_data.center) > global_data.clusterRange:
    return False
  
  return True

def addNextInPassengersAndOrDriversT5Clusters():
  
  if global_data.passengers and global_data.drivers:
      firstPassenger = global_data.passengers[0]
      firstDriver = global_data.drivers[0]
      if firstPassenger.datetimeAsDatetime() == firstDriver.datetimeAsDatetime():
        pArr = getPassengersWithShortDate(firstPassenger.datetimeAsDatetime())
        for p in pArr:
          if passengerInRange(p):
            clust = global_data.clusters.findClusterForPoint((p.sourceLat, p.sourceLong))
            clust.passengerList.append(p)
        dArr = getDriversWithShortDate(firstDriver.datetimeAsDatetime())
        for d in dArr:
          clust = global_data.clusters.findClusterForPoint((d.lat, d.long))
          clust.driverList.append(d)
      elif firstPassenger.datetimeAsDatetime() < firstDriver.datetimeAsDatetime():
        pArr = getPassengersWithShortDate(firstPassenger.datetimeAsDatetime())
        for p in pArr:
          if passengerInRange(p):
            clust = global_data.clusters.findClusterForPoint((p.sourceLat, p.sourceLong))
            clust.passengerList.append(p)
      else:
        dArr = getDriversWithShortDate(firstDriver.datetimeAsDatetime())
        for d in dArr:
          clust = global_data.clusters.findClusterForPoint((d.lat, d.long))
          clust.driverList.append(d)
  elif global_data.passengers and not global_data.drivers:
      firstPassenger = global_data.passengers[0]
      passengerDate = global_data.passengers[0].datetimeAsDatetime()
      pArr = getPassengersWithShortDate(firstPassenger.datetimeAsDatetime())
      for p in pArr:
        if passengerInRange(p):
          clust = global_data.clusters.findClusterForPoint((p.sourceLat, p.sourceLong))
          clust.passengerList.append(p)
  elif not global_data.passengers and global_data.drivers:
      firstDriver = global_data.drivers[0]
      driverDate = global_data.drivers[0].datetimeAsDatetime()
      dArr = getDriversWithShortDate(firstDriver.datetimeAsDatetime())
      for d in dArr:
        clust = global_data.clusters.findClusterForPoint((d.lat, d.long))
        clust.driverList.append(d)

def matchPassengersAndDriversT5Cluster(waitingPassengerList, waitingDriverList, finishedDrivers):
  #match passenger to driver
  passenger = None
  driver = 0
  minPairwiseDist = float('inf')
  passengerNodeIDs = []


  lastPassengerDate = waitingPassengerList[-1].datetimeAsDatetime()
  lastDriverDate = waitingDriverList[-1].datetimeAsDatetime()
  latestDateTemp = waitingDriverList[-1].datetime if lastPassengerDate < lastDriverDate else waitingPassengerList[-1].datetime
  
  for p in waitingPassengerList:
    passengerNodeIDs.append(grabOrCreateSexyNodeT5((p.sourceLat, p.sourceLong)))
  
  removeList = []

  
  for d in waitingDriverList:
    
    if ((datetime.strptime(latestDateTemp, "%m/%d/%Y %H:%M:%S")-d.datetimeAsDatetime()).total_seconds() / 60 + d.timeOnJob) > 240:
      d.timeOnJob = 240
      removeList.append(d)
      finishedDrivers.append(d)
      if len(waitingDriverList) == 0:
        for d in removeList:
          waitingDriverList.remove(d)
        return passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers
    else:
      driverNode = grabOrCreateSexyNodeT5((d.lat, d.long))
      adjacencyList = getAdjacencyList(latestDateTemp)
      dist, pID = AstarToAll(adjacencyList, driverNode, passengerNodeIDs, latestDateTemp)
      if(dist < minPairwiseDist):
        passenger = pID
        driver = d
        minPairwiseDist = dist
  
  for d in removeList:
    waitingDriverList.remove(d)
  if len(waitingDriverList) == 0:
    return passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers

  i = passengerNodeIDs.index(pID)
  passenger = waitingPassengerList[i]

  del waitingPassengerList[i]
  waitingDriverList.remove(driver)
  
  return passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers

def initializeClusters():
  clusters = Clusters([])
  for cP in global_data.clusterPoints:
    cluster = Cluster([], [], cP)
    clusters.clusterList.append(cluster)
  return clusters
