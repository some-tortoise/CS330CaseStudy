import concurrent.futures
import time
import math

def parallel_function(item):
    # Define the function that will be executed in parallel
    # This is where you put the code you want to parallelize
    result = 0
    for i in range(0, 50):
        result += item * item + item * item + math.sqrt(item)
    return result

def main():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]*10000  # Your iterable data

    # Number of worker processes in the process pool
    num_workers = 1

    t1 = time.time()
    # Create a ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use the map function to apply the parallel_function to each item in data
        results = list(executor.map(parallel_function, data))

    # Print the results
    #print(results)

    print(time.time() - t1)

if __name__ == "__main__":
    main()



# def findParallelClosestNode(point):
#   '''
#   Input:
#   point as (lat, long)

#   Output:
#   returns a node ID
#   '''
#   with concurrent.futures.ThreadPoolExecutor() as executor:
#     distances = list(executor.map(lambda item: (item[0], getApproxHaversineDist(point, (float(item['lat']), float(item['lon'])))), global_data.nodes.items()))
#   print(di)
#   # point = (float(point[0]), float(point[1]))

#   # closestNode = None
#   # with concurrent.futures.ThreadPoolExecutor() as executor:
#   #     # Use executor.map to parallelize the computation
#   #     distances = list(executor.map(lambda item: (item[0], getApproxHaversineDist(point, (float(item['lat']), float(item['lon'])))), global_data.nodes.items()))

#   # minDist = min(distances)  # Find the minimum distance

#   # for node in global_data.nodes:
#   #   nodeStuff = global_data.nodes[node]
#   #   dist = getHaversineDist(point, (float(nodeStuff['lat']), float(nodeStuff['lon'])))
#   #   if dist < minDist:
#   #     minDist = dist
#   #     closestNode = node

#   return closestNode