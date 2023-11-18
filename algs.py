import heapq
import math

from util import *

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

  priority_queue = [(sourceNode, 0)]
  seen = set()

  while priority_queue:
        current_vertex, current_distance = heapq.heappop(priority_queue)

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
                heapq.heappush(priority_queue, (neighbor, new_dist))
    
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode
  
  #return sourceNode, destNode
