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
            return current_distance

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
  


# '''ATTEMPT at floydWarshall'''
# def floydWarshall(graph):
#     """ dist[][] will be the output 
#        matrix that will finally
#         have the shortest distances 
#         between every pair of vertices """
#     """ initializing the solution matrix 
#     same as input graph matrix
#     OR we can say that the initial 
#     values of shortest distances
#     are based on shortest paths considering no 
#     intermediate vertices """
 
#     dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
 
#     """ Add all vertices one by one 
#     to the set of intermediate
#      vertices.
#      ---> Before start of an iteration, 
#      we have shortest distances
#      between all pairs of vertices 
#      such that the shortest
#      distances consider only the 
#      vertices in the set 
#     {0, 1, 2, .. k-1} as intermediate vertices.
#       ----> After the end of a 
#       iteration, vertex no. k is
#      added to the set of intermediate 
#      vertices and the 
#     set becomes {0, 1, 2, .. k}
#     """
#     for k in range(V):
 
#         # pick all vertices as source one by one
#         for i in range(V):
 
#             # Pick all vertices as destination for the
#             # above picked source
#             for j in range(V):
 
#                 # If vertex k is on the shortest path from
#                 # i to j, then update the value of dist[i][j]
#                 dist[i][j] = min(dist[i][j],
#                                  dist[i][k] + dist[k][j]
#                                  )
#     printSolution(dist)
 
 

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

  '''
  hour = int(time.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(time, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  '''


  # Initialize distances dictionary with infinity for all vertices except the source

  timeTillPoint = {}
  timeTillPoint[sourceNode] = 0

  hour = int(dateStr.split()[1][0:2])
  avgSpeed = 0
  date = datetime.strptime(dateStr, "%m/%d/%Y %H:%M:%S")
  if date.weekday() < 5:
    avgSpeed = global_data.avgSpeedList[hour]
  else:
    avgSpeed = global_data.avgSpeedList[hour + 24]

  sourcePoint = (global_data.nodes[sourceNode]['lat'], global_data.nodes[sourceNode]['lon'])
  destPoint = (global_data.nodes[destNode]['lat'], global_data.nodes[destNode]['lon'])
  h = (getManhattanDist(sourcePoint, destPoint)/avgSpeed)*60
  # h = getHaversineDist(sourcePoint, destPoint)*2
  priority_queue = [(h, sourceNode)] # (f, node) 
  seen = set()

  while priority_queue:
        f, current_vertex  = heapq.heappop(priority_queue)
        current_distance = timeTillPoint[current_vertex]

        if current_vertex in seen: 
            continue
        seen.add(current_vertex)

        if current_vertex == destNode:
            return current_distance
        
        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            new_dist = current_distance + weight
            # If a shorter path is found, update the distance
            if neighbor not in timeTillPoint or timeTillPoint[neighbor] > new_dist:
                timeTillPoint[neighbor] = new_dist

                srcPoint = (global_data.nodes[neighbor]['lat'], global_data.nodes[neighbor]['lon'])

                h = (getManhattanDist(srcPoint, destPoint)/avgSpeed)*60

                print('---')
                print(h)
                print(Dijkstra(graph, neighbor, destNode))
                if h-Dijkstra(graph, neighbor, destNode) > 0:
                    print(f'overshot by {h-Dijkstra(graph, neighbor, destNode)}')
                print(h-Dijkstra(graph, neighbor, destNode))
                print('---')

                heapq.heappush(priority_queue, (new_dist + h, neighbor))
    
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode