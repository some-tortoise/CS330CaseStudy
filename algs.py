import heapq
import math
from datetime import datetime

from util import *
import global_data

def Dijkstra(graph, sourceNode, destNode): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  # Initialize distances dictionary with infinity for all vertices except the source

  #timeTillPoint = {vertex: float('infinity') for vertex in graph}
  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  priority_queue = [(0, sourceNode)]
  seen = set()

  while priority_queue:
        current_distance, current_vertex  = heapq.heappop(priority_queue)

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex == destNode:
            break

        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            new_dist = current_distance + weight
            # If a shorter path is found, update the distance
            if neighbor not in timeTillPoint or timeTillPoint[neighbor] > new_dist:
                timeTillPoint[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))
    
  # Return the time to the destination
  
  return timeTillPoint[destNode] #this would return distance from given source param to destNode
 

def BinarySearchOnDrivers(list, a):
    '''
    Input:
    list and value of a we want to find

    Output: 
    index
    '''
    low = 0
    high = len(list) - 1
    mid = 0
    while low <= high:
        mid = math.floor((low+high)/2)
        # print('---')
        # print(mid)
        # print(list[mid])
        # print(a)
        # print('---')
        if (list[mid].datetime <= a and mid == high) or (list[mid].datetime <= a and list[mid+1].datetime >= a):
            return mid + 1
        elif list[mid].datetime < a:
            low = mid + 1
        elif list[mid].datetime > a:
            high = mid - 1
        else:
            return TypeError
        
    return mid


def Astar(graph, sourceNode, destNode, dateStr): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  hour = int(dateStr.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  const1 = (69.09 * 60)/(avgSpeed * 1.5) # 69.09 * 40 /avgSpeed
  const2 = (51.34 * 60)/(avgSpeed * 1.5) # 51.34 * 40 / avgSpeed

  s = global_data.nodes[sourceNode]
  d = global_data.nodes[destNode]
  lat1 = float(s['lat'])
  lon1 = float(s['lon'])
  lat2 = float(d['lat'])
  lon2 = float(d['lon'])
  dist1 = abs(lat1-lat2)*const1
  dist2 = abs(lon1-lon2)*const2
  h = dist1+dist2

  priority_queue = [(h, sourceNode)] # (f, node) 
  seen = set()

  
  while priority_queue:
        f, current_vertex  = heapq.heappop(priority_queue)
        current_distance = timeTillPoint[current_vertex]

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex == destNode:
            break
        
        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            new_dist = current_distance + weight
            # If a shorter path is found, update the distance
            if neighbor not in timeTillPoint or timeTillPoint[neighbor] > new_dist:
                timeTillPoint[neighbor] = new_dist
                
                temp = global_data.nodes[neighbor]
                f = new_dist + abs(float(temp['lat'])-lat2)*const1+abs(float(temp['lon'])-lon2)*const2

                heapq.heappush(priority_queue, (f, neighbor))
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode



def Astar_V2(graph, sourceNode, destNode, dateStr): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  hour = int(dateStr.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  const1 = (69.09 * 60)/(avgSpeed * 1.5) # 69.09 * 40 /avgSpeed
  const2 = (51.34 * 60)/(avgSpeed * 1.5) # 51.34 * 40 / avgSpeed

  s = global_data.nodes[sourceNode]
  d = global_data.nodes[destNode]
  lat1 = float(s['lat'])
  lon1 = float(s['lon'])
  lat2 = float(d['lat'])
  lon2 = float(d['lon'])
  dist1 = abs(lat1-lat2)*const1
  dist2 = abs(lon1-lon2)*const2
  h = dist1+dist2

  priority_queue = [(h, sourceNode)] # (f, node) 
  seen = set()

  
  while priority_queue:
        f, current_vertex  = heapq.heappop(priority_queue)
        current_distance = timeTillPoint[current_vertex]

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex == destNode:
            break
        
        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            new_dist = current_distance + weight
            # If a shorter path is found, update the distance
            if neighbor not in timeTillPoint or timeTillPoint[neighbor] > new_dist:
                timeTillPoint[neighbor] = new_dist
                
                temp = global_data.nodes[neighbor]
                f = abs(float(temp['lat'])-lat2)*const1+abs(float(temp['lon'])-lon2)*const2

                heapq.heappush(priority_queue, (f, neighbor))
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode


def DijkstraToAll(graph, sourceNode, destNodesList): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as list of node

  Output:
  returns time it takes to get from source to closest destination
  '''

  # Initialize distances dictionary with infinity for all vertices except the source

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  priority_queue = [(0, sourceNode)]
  seen = set()

  current_vertex = ''

  while priority_queue:
        current_distance, current_vertex  = heapq.heappop(priority_queue)

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex in destNodesList:
            break

        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            new_dist = current_distance + weight
            # If a shorter path is found, update the distance
            if neighbor not in timeTillPoint or timeTillPoint[neighbor] > new_dist:
                timeTillPoint[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))
    
  # Return the time to the destination
  
  return timeTillPoint[current_vertex], current_vertex #this would return distance from given source param to destNode
 