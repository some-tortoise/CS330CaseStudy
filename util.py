import math
import random
from datetime import datetime

from util import *
import global_data

#I BELIEVE IT IS GETTING THE DISTANCE IN MILES??? NOT SURE
def getHaversineDist(point1, point2):
  '''
  returns estimate of distance between two points

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

def addNodeToGraphIfNeeded(point):
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
    nodeId = random.getrandbits(64)
    global_data.nodes.append({nodeId:{'lon': point[0], 'lat' : point[1]}})
    global_data.edges.append(node, nodeId, dist, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
    for i in range(0, len(global_data.adjacencyListsWeekdays)):
      temp = global_data.adjacencyListsWeekdays[i][node]
      temp.append((nodeId, dist/10))
      global_data.adjacencyListsWeekdays[i].update({node : temp})
      global_data.adjacencyListsWeekdays[i].update({nodeId : [node, dist/10]})
    
    return nodeId
  
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
  