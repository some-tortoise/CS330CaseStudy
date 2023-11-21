import heapq
import math
from datetime import datetime

import global_data

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
        if (list[mid].datetime <= a and mid == high) or (list[mid].datetime <= a and list[mid+1].datetime >= a):
            return mid + 1
        elif list[mid].datetime < a:
            low = mid + 1
        elif list[mid].datetime > a:
            high = mid - 1
        else:
            return TypeError
        
    return mid

def Dijkstra(graph, sourceNode, destNode): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  # Initialize distances dictionary with 0 for the source

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
  
  return timeTillPoint[destNode] #returns estimated time from given source param to destNode

def DijkstraToAll(graph, sourceNode, destNodesList): #added adj list parameter, deleted time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as list of node

  Output:
  returns time it takes to get from source to closest destination
  '''

  # Initialize distances dictionary with 0 for the source

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
  
  return timeTillPoint[current_vertex], current_vertex #returns estimated time from given source param to destNode and that destNode

def Astar(graph, sourceNode, destNode, dateStr): #added time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  # Initialize distances dictionary with 0 for the source

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  hour = int(dateStr.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  const1 = (69.09 * 60)/(avgSpeed * 1.5) # (69.09 (miles per degree of latitude) / 1.5*avgSpeed in miles per hour) * 60 (hours to minutes)
  const2 = (51.34 * 60)/(avgSpeed * 1.5) # (51.34 (miles per degree of longitude) / 1.5*avgSpeed in miles per hour) * 60 (hours to minutes)

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
  return timeTillPoint[destNode] #returns estimated time from given source param to destNode

def AstarToAll(graph, sourceNode, destNodes, dateStr): #added time variable from parameters
  '''
  Input:
  graph (adjacency list)
  source as node
  dest as node

  Output:
  returns time it takes to get from source to destination
  '''

  # Initialize distances dictionary with 0 for the source

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  hour = int(dateStr.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  const1 = (69.09 * 60)/(avgSpeed * 1.5) # (69.09 (miles per degree of latitude) / 1.5*avgSpeed in miles per hour) * 60 (hours to minutes)
  const2 = (51.34 * 60)/(avgSpeed * 1.5) # (51.34 (miles per degree of longitude) / 1.5*avgSpeed in miles per hour) * 60 (hours to minutes)

  s = global_data.nodes[sourceNode]
  lat1 = float(s['lat'])
  lon1 = float(s['lon'])
  minH = float('inf')
  for destNode in destNodes:
    d = global_data.nodes[destNode]
    lat2 = float(d['lat'])
    lon2 = float(d['lon'])
    dist1 = abs(lat1-lat2)*const1
    dist2 = abs(lon1-lon2)*const2
    if dist1+dist2 < minH:
        minH = dist1+dist2


  priority_queue = [(minH, sourceNode)] # (f, node) 
  seen = set()

  while priority_queue:
        f, current_vertex  = heapq.heappop(priority_queue)
        current_distance = timeTillPoint[current_vertex]

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex in destNodes:
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
                # does not inclue new_dist

                lat1 = float(temp['lat'])
                lon1 = float(temp['lon'])
                minH = float('inf')
                for destNode in destNodes:
                    d = global_data.nodes[destNode]
                    lat2 = float(d['lat'])
                    lon2 = float(d['lon'])
                    dist1 = abs(lat1-lat2)*const1
                    dist2 = abs(lon1-lon2)*const2
                    if dist1+dist2 < minH:
                        minH = dist1+dist2
                heapq.heappush(priority_queue, (minH, neighbor))
  
  # Return the time to the destination
  return timeTillPoint[current_vertex], current_vertex #returns estimated time from given source param to destNode
