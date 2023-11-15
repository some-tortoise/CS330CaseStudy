import csv
from datetime import datetime
import json
import math
import heapq
import time
import statistics

###self defined files###
import inOut #input output
import algs #algorithms
import util #utility functions
 

def t1(passengers, drivers):
  '''
  input is passengers array and drivers array
  '''
  startTimeForT1 = time.time()

  # combine into one list and iterate over list
  waitingPassengerQueue = []
  waitingDriverQueue = []
  driveToPassengersTime = []
  driveToDestTime = []
  while True:
    passengerDate = datetime.strptime(passengers[0][0], "%m/%d/%Y %H:%M:%S")
    driverDate = datetime.strptime(drivers[0][0], "%m/%d/%Y %H:%M:%S")
    if passengerDate < driverDate: #if passenger is from previous day, remove from passengers
      passenger = passengers.pop(0)
      waitingPassengerQueue.append(passenger) #add passenger to queue
      if(len(passengers) == 0):
        #print('Ran Out of Passengers')
        break
    else:
      driver = drivers.pop(0) 
      waitingDriverQueue.append(driver)
      if(len(drivers) == 0):
        #print('Ran Out of Drivers')
        break
    
    if len(waitingDriverQueue) > 0 and len(waitingPassengerQueue) > 0:
      #match passenger to driver
      passenger = waitingPassengerQueue.pop(0)
      driver = waitingDriverQueue.pop(0)

      passengerDate = datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S")

      #First we want to calculate the hour it is and whether it is a weekday or the weekend
      #we want to look at the time of the later of the two (driver or passenger) bc that is when the driving will occur
      #we assume that any trip stays within the same hour segment (even though this is def not true). It makes the adjacency list calculations A GOOD BIT easier
      #also the average speed from one hour to the next should be relatively similar so our answer should be relatively close

      latestDate = 0
      if passengerDate < driverDate:
        latestDate = driver[0]
      else:
        latestDate = passenger[0]
      
      adjacencyList = getAdjacencyList(latestDate)


      timeFromDriverToPassenger = Dijkstra(adjacencyList, (driver[1], driver[2]), (passenger[1], passenger[2]))
      timeFromPassengerToDest = Dijkstra(adjacencyList, (passenger[1], passenger[2]), (passenger[3], passenger[4]))
      totalTime = timeFromDriverToPassenger + timeFromPassengerToDest
      driveToPassengersTime.append(timeFromDriverToPassenger)
      driveToDestTime.append(timeFromPassengerToDest)
      print(totalTime)

  #get diagnostics info at the end of the test
  endTimeForT1 = time.time()
  
  timeForTest = (startTimeForT1 - endTimeForT1)

  sumOfToPassengersTime = 0
  sumOfToDestTime = 0
  sumOfdriverProfit = 0
  for t in range(0,driveToPassengersTime):
    sumOfToPassengersTime += driveToPassengersTime[t]
    sumOfToDestTime += driveToDestTime[t]
    sumOfdriverProfit += driveToDestTime[t] - driveToPassengersTime[t]
  avgOfToPassengersTime = sumOfToPassengersTime / len(driveToPassengersTime)
  avgOfToDestTime = sumOfToDestTime / len(driveToPassengersTime)
  avgOfDriverProfit = sumOfdriverProfit / len(driveToPassengersTime)

  #print diagnostics info at the end of the test
  print('------------INFO------------')
  print(f'Average time to reach a passenger: {statistics.mean(driveToPassengersTime)}')
  print(f'Standard deviation of time to reach passenger: {statistics.stdev(driveToPassengersTime)}')
  print(f'Average time from pickup to dropoff: {statistics.mean(driveToDestTime)}')
  print(f'Average unmatched till dest (time to reach passenger + time to dropoff): {statistics.mean(driveToPassengersTime) + statistics.mean(driveToDestTime)}')
  print(f'Average driver profit: {avgOfDriverProfit}')
  print(f'Time for entire test: {timeForTest}')


# READ IN DATA

# driversHeader, drivers = read_csv('./data/drivers.csv')
# passengersHeader, passengers = read_csv('./data/passengers.csv')

# edgesHeader, edges = read_csv('./data/edges.csv')
# edges.sort(key=lambda edge: edge[0])

# #GLOBAL ELEMENTS

nodes = getNodes()
# Sort passengers by time
passengers.sort(key=lambda passenger: datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S"))
  
# Sort drivers by time
drivers.sort(key=lambda driver: datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S"))
# # each element in below is for hours from 0-23
# adjacencyListsWeekdays = [0]*24 
# adjacencyListsWeekends = [0]*24 

# for i in range(0,23):
#   adjacencyListsWeekdays[i] = createAdjacencyListAsDict('weekday', i)
#   adjacencyListsWeekends[i] = createAdjacencyListAsDict('weekend', i)

# # RUN CODE
# ret = t1(passengers, drivers)
# print(ret)