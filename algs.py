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
  timeTillPoint = {vertex: float('infinity') for vertex in graph}
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
            distance = current_distance + weight
            
            # If a shorter path is found, update the distance
            if distance < timeTillPoint[neighbor]:
                timeTillPoint[neighbor] = distance
                if neighbor not in seen:
                    heapq.heappush(priority_queue, (neighbor, distance))
    
  # Return the time to the destination
  return timeTillPoint[destNode] #this would return distance from given source param to destNode
  
  #return sourceNode, destNode

'''ATTEMPT at floydWarshall'''
def floydWarshall(graph):
    """ dist[][] will be the output 
       matrix that will finally
        have the shortest distances 
        between every pair of vertices """
    """ initializing the solution matrix 
    same as input graph matrix
    OR we can say that the initial 
    values of shortest distances
    are based on shortest paths considering no 
    intermediate vertices """
 
    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
 
    """ Add all vertices one by one 
    to the set of intermediate
     vertices.
     ---> Before start of an iteration, 
     we have shortest distances
     between all pairs of vertices 
     such that the shortest
     distances consider only the 
     vertices in the set 
    {0, 1, 2, .. k-1} as intermediate vertices.
      ----> After the end of a 
      iteration, vertex no. k is
     added to the set of intermediate 
     vertices and the 
    set becomes {0, 1, 2, .. k}
    """
    for k in range(V):
 
        # pick all vertices as source one by one
        for i in range(V):
 
            # Pick all vertices as destination for the
            # above picked source
            for j in range(V):
 
                # If vertex k is on the shortest path from
                # i to j, then update the value of dist[i][j]
                dist[i][j] = min(dist[i][j],
                                 dist[i][k] + dist[k][j]
                                 )
    printSolution(dist)
 
 