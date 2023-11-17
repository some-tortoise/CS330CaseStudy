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

        seen.add(current_vertex)

        if current_vertex == destNode:
            return timeTillPoint[destNode]

        # Iterate over neighbors of the current vertex
        for neighbor, weight in graph[current_vertex]:
            if neighbor in seen:
                continue

            if neighbor not in timeTillPoint:
                timeTillPoint[neighbor] = float('infinity')

            # If a shorter path is found, update the distance
            if timeTillPoint[neighbor] > timeTillPoint[current_vertex] + weight:
                timeTillPoint[neighbor] = timeTillPoint[current_vertex] + weight
                heapq.heappush(priority_queue, (neighbor, timeTillPoint[neighbor]))
    
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode
  
  #return sourceNode, destNode
